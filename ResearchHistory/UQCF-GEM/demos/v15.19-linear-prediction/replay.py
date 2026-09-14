#!/usr/bin/env python3
"""Offline replay of computed prediction-coordinate tests, not physical time."""
from __future__ import annotations
import argparse
from functools import lru_cache
import json
from pathlib import Path
import numpy as np
import linear_module as m
ROOT=Path(__file__).resolve().parent
STORY=(('B1','1111'),('A1','1111'),('pretime','1111'),('all_six','1111'),('pretime','0001'),('all_six','1000'))


def trajectory(family,mask):
    row,q=m.case(family,mask);units=m.old.label_motions(family)
    f=m.old.old.old.basis();rho=f@m.old.old.old.fixture()@f.conj().T
    z=m.state_features(rho,q);transfers=[q.T@m.adjoint_action(u)@q for u in units]
    output=q[0,:];frames=[]
    names=list(m.old.old.frozen_motions()) if family=='all_six' else [family]
    for k in range(13):
        frames.append({'checkpoint':k,'direct_probability':float(rho[0,0].real),
                       'linear_probability':float(output@z),
                       'feature_error':float(np.linalg.norm(z-m.state_features(rho,q))),
                       'last_operation':None if k==0 else names[(k-1)%len(units)]+(' inverse' if (k-1)%3==0 else '')})
        i=k%len(units);inverse=k%3==0
        u=units[i].conj().T if inverse else units[i]
        t=transfers[i].T if inverse else transfers[i]
        z=t.T@z;rho=u@rho@u.conj().T
    return frames


@lru_cache(None)
def payload():
    result=m.audit();cases=[]
    for row in result['cases']:
        c=dict(row);c['trajectory']=trajectory(row['family'],row['mask']);cases.append(c)
    return {'version':'v15.19','cases':cases,'audit':result,
            'notice':'Computed finite-word expectation predictions. Initial features must be available before pruning; no lost information is restored.'}


def write_html(data,path):
    value=json.dumps(data,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text((ROOT/'viewer.html').read_text().replace('__DATA__',value),encoding='utf-8')


def movie(path,fps=10):
    if type(fps) is not int or fps<=0:raise ValueError('positive display fps required')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter,writers
    if not writers.is_available('ffmpeg'):raise RuntimeError('FFmpeg needed only for MP4')
    data=payload();rows={(c['family'],c['mask']):c for c in data['cases']}
    fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    ax=fig.add_axes([.08,.29,.47,.43]);ax.set_xlim(-.3,12.3)
    ax.set_xlabel('Finite word length — not elapsed time',fontsize=10)
    ax.set_ylabel('Probability of the original label 0000',fontsize=10)
    direct,=ax.plot([],[],linewidth=2,label='Full density-matrix route')
    pred,=ax.plot([],[],linestyle='none',marker='o',markersize=5,fillstyle='none',label='Linear prediction coordinates')
    cursor=ax.axvline(0,linestyle=':',alpha=.6)
    ax.legend(loc='upper left',fontsize=8)
    fig.text(.05,.949,'UQCF–GEM / v15.19 / LINEAR PREDICTION VERSUS ALGEBRA',fontsize=10,weight='bold')
    fig.text(.05,.875,'How much must be kept to predict?',fontsize=27,weight='bold')
    title=fig.text(.05,.81,'',fontsize=14)
    dims=fig.text(.61,.68,'',fontsize=21,weight='bold',linespacing=1.8,va='top')
    evidence=fig.text(.61,.44,'',fontsize=12,linespacing=1.75,va='top')
    fig.text(.05,.177,'Single-motion savings can be large. The full motion family leaves only one hidden parity direction.',fontsize=11)
    fig.text(.05,.119,'Linear expectation coordinates are not a density matrix or a physical pruning channel.',fontsize=11,weight='bold')
    fig.text(.05,.073,'No actual record selected. No new motion, entropy objective, clock or collapse law is introduced.',fontsize=10)
    fig.text(.05,.032,'Playback is not physical time. Original dynamics and target observables remain supplied and unchanged.',fontsize=10)
    def draw(key,k):
        c=rows[key];ts=c['trajectory'];xs=list(range(13));ys=[r['direct_probability'] for r in ts]
        direct.set_data(xs,ys);pred.set_data(xs,[r['linear_probability'] for r in ts]);cursor.set_xdata([k,k])
        lo,hi=min(ys),max(ys);pad=max(.025,(hi-lo)*.3);ax.set_ylim(max(-.01,lo-pad),min(1.05,hi+pad))
        title.set_text('Supplied motion family: '+c['family']+'   |   Original mask: '+c['mask'])
        dims.set_text(f"Initial observables: {c['initial_dimension']}\nLinear module: {c['linear_dimension']}\nInvariant algebra: {c['algebra_dimension']}")
        evidence.set_text(f"Saved versus algebra: {c['saved_vs_algebra']} directions\nPrediction error: {abs(ts[k]['direct_probability']-ts[k]['linear_probability']):.2e}\n112 supplied cases verified")
    path.parent.mkdir(parents=True,exist_ok=True);draw(('pretime','1111'),6);fig.savefig(path.with_suffix('.png'),dpi=120)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=2000,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    with writer.saving(fig,str(path),dpi=100):
        for key in STORY:
            for frame in range(4*fps):
                draw(key,min(12,int(frame*13/(4*fps))));writer.grab_frame()
    plt.close(fig)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs');p.add_argument('--video',action='store_true');a=p.parse_args()
    data=payload();a.out.mkdir(parents=True,exist_ok=True)
    write_html(data,a.out/'linear_prediction.html')
    (a.out/'replay_data.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
    (a.out/'verification.json').write_text(json.dumps(data['audit'],indent=2,allow_nan=False)+'\n')
    np.savez_compressed(a.out/'example_modules.npz',pretime=m.case('pretime','1111')[1],all_six=m.case('all_six','1111')[1],input_basis=m.old.old.old.basis())
    if a.video:movie(a.out/'linear_prediction.mp4')
    print('Computed 112 modules and 1,456 replay checkpoints. No physical time or actual outcome selected.')

if __name__=='__main__':main()
