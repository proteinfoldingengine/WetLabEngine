#!/usr/bin/env python3
"""Computed CPTP/readout tradeoff inspector. No quantum outcomes are sampled."""
from __future__ import annotations
import argparse
from functools import lru_cache
import json
from pathlib import Path
import numpy as np
import physical_predictor as m
ROOT=Path(__file__).resolve().parent
STORY=((1.,1.),(1.,0.),(.75,.5),(.5,0.),(.25,0.),(.5,0.))


def point(lam: float,t: float) -> dict:
    lam,t=m.parameters(lam,t);q=m.pauli_weights(lam,t);valid=bool(q.min()>=-m.CP_TOL)
    p=m.paulis()[m.labels().index('XIII')];rho=(np.eye(16)+p)/16
    sigma=m.linear_map(rho,lam,t)
    pure=m.linear_map(m.y_product_state(),lam,t)
    return {'lambda':lam,'t':t,'cptp':valid,
            'min_choi_eigenvalue':float(q.min()),
            'min_pure_witness_eigenvalue':float(np.linalg.eigvalsh(pure).min()),
            'input_visible_expectation':1.,'raw_visible_expectation':float(np.trace(p@sigma).real),
            'parity_twin_output_distance':m.distance(*(m.linear_map(r,lam,t) for r in m.parity_twins())),
            'decoded_expectation':m.decode_expectation(p,sigma,lam) if valid and lam>0 else None,
            'readout_gain':1/lam if valid and lam>0 else None,
            'decoded_zero_signal_variance':1/lam**2 if valid and lam>0 else None,
            'status':'CPTP_DIAGNOSTIC_CHANNEL' if valid else 'NONPOSITIVE_DIAGNOSTIC_ONLY'}


@lru_cache(None)
def payload() -> dict:
    return {'version':'v15.20','grid':[point(i/20,j/20) for j in range(21) for i in range(21)],
            'story':list(STORY),'audit':m.audit(),
            'notice':'Diagnostic channel parameters are not physical time or a selected physical pruning law. Ensemble readout is not quantum-state recovery.'}


def write_html(data: dict,path: Path) -> None:
    text=(ROOT/'viewer.html').read_text()
    encoded=json.dumps(data,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text.replace('__DATA__',encoded),encoding='utf-8')


def movie(path: Path,fps: int=10) -> None:
    if type(fps) is not int or fps<=0:raise ValueError('positive integer playback fps required')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter,writers
    if not writers.is_available('ffmpeg'):raise RuntimeError('FFmpeg needed for MP4, not HTML')
    data=payload();fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    ax=fig.add_axes([.075,.32,.42,.39]);x=np.linspace(0,1,100)
    ax.fill_between(x,0,(1+x)/2,alpha=.14,label='CPTP region')
    ax.plot(x,(1+x)/2,linewidth=2,label='Best direct-feature boundary')
    dot=ax.scatter([1],[1],s=150,marker='o')
    ax.set(xlim=(-.04,1.04),ylim=(-.04,1.04),xlabel='Retained parity coefficient t',ylabel='Direct visible-signal gain λ')
    ax.set_xticks([0,.5,1]);ax.set_yticks([0,.5,1]);ax.legend(loc='lower right',fontsize=8)
    fig.text(.05,.95,'UQCF–GEM / v15.20 / PHYSICAL CHANNEL AND PREDICTION READOUT',fontsize=10,weight='bold')
    fig.text(.05,.875,'A valid state. A measurable readout cost.',fontsize=27,weight='bold')
    title=fig.text(.05,.80,'',fontsize=14,weight='bold')
    metrics=fig.text(.56,.715,'',fontsize=15,linespacing=1.7,va='top')
    detail=fig.text(.56,.51,'',fontsize=12,linespacing=1.7,va='top')
    fig.text(.05,.215,'The earlier motions are unchanged. The same four-qubit carrier is retained.',fontsize=13)
    fig.text(.05,.16,'Direct exact preservation forces identity; explicit signed ensemble readout permits a noisy representation.',fontsize=10)
    fig.text(.05,.10,'No actual record selected. No physical collapse, entropy-production or gravitational law is derived.',fontsize=10)
    fig.text(.05,.05,'Playback is not physical time. Readout scaling is not quantum-state recovery; its sampling variance is included.',fontsize=10)
    titles=('IDENTITY: KEEP EVERYTHING','EXACT PARITY DELETION: NOT A VALID CHANNEL',
            'PARTIAL PARITY REDUCTION AT THE CPTP BOUNDARY','ERASE PARITY WITH A VALID QUANTUM CHANNEL',
            'MORE ATTENUATION MEANS HIGHER READOUT VARIANCE','VALID PREDICTOR REPRESENTATION, NOT A PRUNING LAW')
    def draw(k):
        lam,t=STORY[k];row=point(lam,t);dot.set_offsets([[t,lam]]);title.set_text(titles[k])
        metrics.set_text(f'Parity distinguishability: {row["parity_twin_output_distance"]:.2f}\nDirect visible signal: {row["raw_visible_expectation"]:.2f}\n'+('Channel: CPTP' if row['cptp'] else 'Channel: REJECTED'))
        if row['readout_gain'] is not None:
            detail.set_text(f'Readout gain: {row["readout_gain"]:g}\nDecoded expectation: {row["decoded_expectation"]:.2f}\nZero-signal variance: {row["decoded_zero_signal_variance"]:g}\nIdeal zero-signal variance: 1')
        else:
            detail.set_text(f'Pure-state output eigenvalue: {row["min_pure_witness_eigenvalue"]:.4f}\nNormalized Choi minimum: {row["min_choi_eigenvalue"]:.6f}\nNo physical-state readout displayed.')
    path.parent.mkdir(parents=True,exist_ok=True);draw(3);fig.savefig(path.with_suffix('.png'),dpi=120)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=1600,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    with writer.saving(fig,str(path),dpi=100):
        for k in range(len(STORY)):
            draw(k)
            for _ in range(4*fps):writer.grab_frame()
    plt.close(fig)


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs');p.add_argument('--video',action='store_true')
    a=p.parse_args();data=payload();a.out.mkdir(parents=True,exist_ok=True)
    write_html(data,a.out/'physical_predictor.html')
    (a.out/'replay_data.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
    if a.video:movie(a.out/'physical_predictor.mp4')
    print(f'Exported {len(data["grid"])} parameter cases. Quantum channels and diagnostic nonpositive maps are distinguished.')

if __name__=='__main__':main()
