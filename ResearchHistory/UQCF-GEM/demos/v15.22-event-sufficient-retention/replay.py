#!/usr/bin/env python3
"""Computed next-event comparison; inspection parameters are not clocks."""
from __future__ import annotations
import argparse
from functools import lru_cache
import json
from pathlib import Path
import numpy as np
import event_sufficiency as m
ROOT=Path(__file__).resolve().parent


@lru_cache(None)
def payload() -> dict:
    result=m.audit();f=m.prior.start();v,labels,_=m.joint_basis(f)
    x=v[:,labels.index((0,0))];y=v[:,labels.index((1,0))]
    a=(x+y)/np.sqrt(2);b=(x-y)/np.sqrt(2)
    rho=np.outer(a,a.conj());other=np.outer(b,b.conj())
    pa=m.effects(f,'A1');ka=m.kraus(f,'A1');kb=m.kraus(f,'B1');points=[]
    for weight in np.linspace(0,1,41):
        sigma=(1-weight)*rho+weight*m.retain(rho,pa)
        partner=(1-weight)*other+weight*m.retain(other,pa)
        exact=max(float(np.linalg.norm(k@sigma@k.conj().T-k@rho@k.conj().T)) for k in ka)
        pe=max(float(abs(np.trace(k@sigma@k.conj().T)-np.trace(k@rho@k.conj().T))) for k in kb)
        left=kb[0]@rho@kb[0].conj().T;right=kb[0]@sigma@kb[0].conj().T
        pair=kb[0]@partner@kb[0].conj().T
        batch=max(float(np.linalg.norm(k2@k1@(sigma-rho)@k1.conj().T@k2.conj().T)) for k1 in ka for k2 in kb)
        points.append({'mixture_weight':float(weight),'matching_event_error':exact,'other_event_probability_error':pe,
            'other_event_state_distance':m.prior.base.distance(left/np.trace(left),right/np.trace(right)),
            'pair_distance':m.prior.base.distance(right,pair),'two_event_batch_error':batch})
    return {'version':'v15.22','audit':result,'cases':result['cases'],'comparison':points,
        'notice':'Mixtures compare alternative CPTP preprocessors before a supplied next event. The weight is not physical time or a law selecting an event; no actual record selected.'}


def write_html(data: dict,path: Path) -> None:
    value=json.dumps(data,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text((ROOT/'viewer.html').read_text().replace('__DATA__',value),encoding='utf-8')


def movie(path: Path,fps: int=10) -> None:
    if type(fps) is not int or fps<=0:raise ValueError('positive playback fps required')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter,writers
    if not writers.is_available('ffmpeg'):raise RuntimeError('FFmpeg required for MP4 only')
    data=payload();points=data['comparison'];x=[r['mixture_weight'] for r in points]
    fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    ax=fig.add_axes([.075,.295,.49,.43]);ax.set(xlim=(0,1),ylim=(-.05,1.1))
    ax.set_xlabel('Alternative preprocessing mixture — not time',fontsize=10)
    ax.set_ylabel('Quantum-state distinguishability',fontsize=10)
    ax.plot(x,[r['matching_event_error'] for r in points],linewidth=2,label='Matching A1 branch: unchanged')
    ax.plot(x,[r['other_event_state_distance'] for r in points],linewidth=2,label='B1 post-event state error')
    ax.plot(x,[r['pair_distance'] for r in points],linestyle='--',linewidth=2,label='Distinction left in B1 output')
    ax.legend(loc='upper center',fontsize=8)
    cursor=ax.axvline(0,linestyle=':',alpha=.6)
    fig.text(.05,.95,'UQCF–GEM / v15.22 / EVENT-SUFFICIENT RETENTION',fontsize=10,weight='bold')
    fig.text(.05,.875,'What may be lost depends on what comes next.',fontsize=24,weight='bold')
    fig.text(.05,.809,'Same instruments. Exact branch outputs, not just outcome probabilities.',fontsize=13)
    heading=fig.text(.61,.715,'',fontsize=17,weight='bold',va='top')
    detail=fig.text(.61,.615,'',fontsize=12,linespacing=1.65,va='top')
    fig.text(.05,.195,'80 supplied histories · 320 branch steps · no readout gain needed for the specified next event',fontsize=12)
    fig.text(.05,.133,'If both ready events must remain exact alternatives, the common preprocessing is identity on the current sector.',fontsize=10)
    fig.text(.05,.08,'A1-specific retention is a factorization of its supplied instrument, not an additional actual pruning event.',fontsize=10)
    fig.text(.05,.035,'No actual record selected. Playback is not physical time. No physical collapse or entropy-production law is derived.',fontsize=10)
    story=[(0,'NO PREPROCESSING','Both event alternatives remain intact.\nNo distinction has been removed.'),
        (10,'SPECIFY THE NEXT EVENT','A1-specific pinching preserves A1 branches.\nBoth probabilities and quantum outputs match.'),
        (20,'PROBABILITIES ARE NOT ENOUGH','B1 probabilities still match here.\nBut its remaining quantum state changes.'),
        (40,'FULL EVENT-SPECIFIC PINCHING','A1 branch error: approximately zero.\nB1 post-event state distance: 0.5.\nThe B1 witness distinction is lost.'),
        (40,'BATCH IS A DIFFERENT CONTRACT','After actually executing BOTH events,\nall final branches again match.\nThat does not preserve an open choice\nof which complete instrument occurs next.'),
        (0,'OPEN ALTERNATIVES','At all seven two-ready contexts,\nexact preservation of both instruments\nforces a common CPTP preprocessor\nto be identity on the current sector.')]
    def draw(row):
        i,title,text=row;cursor.set_xdata([points[i]['mixture_weight']]*2)
        heading.set_text(title);detail.set_text(text)
    path.parent.mkdir(parents=True,exist_ok=True);draw(story[3]);fig.savefig(path.with_suffix('.png'),dpi=110)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=1800,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    with writer.saving(fig,str(path),dpi=100):
        for row in story:
            draw(row)
            for _ in range(4*fps):writer.grab_frame()
    plt.close(fig)


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs');p.add_argument('--video',action='store_true')
    a=p.parse_args();data=payload();a.out.mkdir(parents=True,exist_ok=True)
    write_html(data,a.out/'event_sufficiency.html')
    (a.out/'replay_data.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
    (a.out/'verification.json').write_text(json.dumps(data['audit'],indent=2,allow_nan=False)+'\n')
    if a.video:movie(a.out/'event_sufficiency.mp4')
    print('29 nonterminal contexts, 80 supplied histories, exact next-event branch preservation. No actual outcome selected.')

if __name__=='__main__':main()
