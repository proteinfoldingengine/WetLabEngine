#!/usr/bin/env python3
"""Replay computed distinctions; parameters and playback are not physical time."""
from functools import lru_cache
import argparse
import json
from pathlib import Path
import numpy as np
import retained_motion as m
ROOT=Path(__file__).resolve().parent

@lru_cache(None)
def payload():
    mask='1000';a,b=m.old.phase_pair(0,8);e=lambda r:m.old.reduce_input(r,mask)
    h=m.label_operator('YIII');ps=m.old.projectors(mask);frames=[]
    for angle in np.linspace(0,np.pi/2,65):
        u=m.exp_unitary(h,angle);ad=lambda r:u@r@u.conj().T
        moved_ps=[ad(p) for p in ps]
        transported=lambda r:sum(p@r@p for p in moved_ps)
        frames.append({'extent':float(angle),'status':m.classify(u,mask)['status'],
          'unpruned_retained_distance':m.distance(e(ad(a)),e(ad(b))),
          'actually_pruned_distance':m.distance(e(ad(e(a))),e(ad(e(b)))),
          'transported_distance':m.distance(transported(ad(a)),transported(ad(b))),
          'initial_retained_distance':m.distance(e(a),e(b))})
    return {'version':'v15.17','frames':frames,'audit':m.audit(),
       'notice':'Unpruned route is a counterfactual comparison, not recovery of discarded information. Fixed and transported algebras are different declared descriptions.'}

def write_html(data,path):
    data=json.dumps(data,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text((ROOT/'viewer.html').read_text().replace('__DATA__',data),encoding='utf-8')

def movie(path,fps=10):
    if type(fps) is not int or fps<=0:raise ValueError('positive playback fps required')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter,writers
    if not writers.is_available('ffmpeg'):raise RuntimeError('FFmpeg required for MP4')
    data=payload();frames=data['frames'];fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    ax=fig.add_axes([.08,.30,.48,.43]);ax.set(xlim=(0,np.pi/2),ylim=(-.05,1.1))
    ax.set_xticks([0,np.pi/4,np.pi/2],['0','π/4','π/2'])
    ax.set_xlabel('Finite transformation extent — not elapsed time',fontsize=10)
    ax.set_ylabel('Retained distinguishability',fontsize=11)
    x=[f['extent'] for f in frames]
    ax.plot(x,[f['unpruned_retained_distance'] for f in frames],linewidth=2,label='No initial pruning: counterfactual')
    ax.plot(x,[f['actually_pruned_distance'] for f in frames],linewidth=2,label='Actually pruned first')
    ax.plot(x,[f['transported_distance'] for f in frames],linestyle='--',linewidth=2,label='Transported retained algebra')
    ax.legend(loc='upper left',fontsize=8)
    cursor=ax.axvline(0,linestyle=':',alpha=.7)
    fig.text(.05,.95,'UQCF–GEM / v15.17 / RETAINED-MOTION COMPARISON',fontsize=10,weight='bold')
    fig.text(.05,.875,'Can motion descend to what remains?',fontsize=26,weight='bold')
    fig.text(.05,.812,'Two inputs share the same retained state. Keep the operation order explicit.',fontsize=13)
    heading=fig.text(.61,.70,'',fontsize=16,weight='bold',va='top')
    text=fig.text(.61,.59,'',fontsize=12,linespacing=1.65,va='top')
    fig.text(.05,.185,'Effective continuous motion dimensions: 255 → 126 → 60 → 24 → 0',fontsize=15,weight='bold')
    fig.text(.05,.133,'Fixed record identities; central phases removed. These are not entropy or duration.',fontsize=11)
    fig.text(.05,.080,'No actual record selected. Existing motions are tested, not replaced by a fitted post-pruning law.',fontsize=10)
    fig.text(.05,.035,'Playback is not physical time. Nonclosure does not resurrect lost information or make a quantum operation invalid.',fontsize=10)
    story=[(0,'NO ROTATION','The retained inputs are identical.\nAll three displayed distances are zero.'),
      (16,'INTERMEDIATE MOTION','Omitting initial pruning exposes a difference.\nActually pruned inputs stay identical.'),
      (32,'MAXIMAL CONTRAST','Unpruned-first route: distance 1.\nActually pruned-first route: distance 0.\nTransported algebra: distance 0.'),
      (48,'FIXED VS TRANSPORTED','A moving retained algebra has exact closure.\nA fixed algebra need not.\nThese are different descriptions.'),
      (64,'REVERSIBLE RECORD SWAP','The endpoint permutes record sectors.\nIt closes the algebra but changes fixed labels.\nIntermediate rotations were not closed.'),
      (32,'NO NEW MOTION LAW','96 old-motion/mask combinations tested.\n17 closed on the fixed algebra; 79 not.\nAll admit covariant algebra transport.')]
    def draw(item):
        idx,title,detail=item;f=frames[idx];cursor.set_xdata([f['extent']]*2)
        heading.set_text(title);text.set_text(detail)
    path.parent.mkdir(parents=True,exist_ok=True);draw(story[2]);fig.savefig(path.with_suffix('.png'),dpi=120)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=1800,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart'])
    with writer.saving(fig,str(path),dpi=100):
        for item in story:
            draw(item)
            for _ in range(4*fps):writer.grab_frame()
    plt.close(fig)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs');p.add_argument('--video',action='store_true')
    a=p.parse_args();data=payload();a.out.mkdir(parents=True,exist_ok=True)
    write_html(data,a.out/'retained_motion.html')
    (a.out/'replay_data.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    (a.out/'verification.json').write_text(json.dumps(data['audit'],indent=2,allow_nan=False)+'\n')
    if a.video:movie(a.out/'retained_motion.mp4')
    print('Computed 96 frozen-motion/mask cases and 65 diagnostic rotation frames.')
if __name__=='__main__':main()
