#!/usr/bin/env python3
"""An offline inspector of alternative sufficient channels, not event history."""
from __future__ import annotations
import argparse
from functools import lru_cache
import json
from pathlib import Path
import numpy as np
import retention_family as m
ROOT=Path(__file__).resolve().parent

@lru_cache(None)
def payload():
    ps=m.old.effects(m.old.prior.start(),'A1');a,b=m.phase_pair(ps);points=[]
    for radius in np.linspace(0,1,9):
        for phase in np.linspace(0,2*np.pi,9):
            c=radius*np.exp(1j*phase);out=m.apply(a,ps,m.binary(c));partner=m.apply(b,ps,m.binary(c))
            points.append({'radius':float(radius),'phase':float(phase),'real':float(c.real),'imag':float(c.imag),
              'distance':m.old.prior.base.distance(out,partner),'reference_distance':m.old.prior.base.distance(out,a),
              'idempotence':float(abs(c*c-c)),'linear_injective':bool(radius>0),'cptp_reversible':bool(radius==1)})
    partitions=[{'matrix':c.astype(int).tolist(),'blocks':int(np.linalg.matrix_rank(c,tol=m.TOL))} for c in m.idempotent_correlations(4)]
    return {'version':'v15.23','points':points,'partitions':partitions,'audit':m.audit(),
      'notice':'Alternative maps preserving the same supplied event. No physical clock or actual outcome is selected.'}

def write_html(data,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    text=json.dumps(data,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    path.write_text((ROOT/'viewer.html').read_text().replace('__DATA__',text),encoding='utf-8')

def movie(path,fps=10):
    if type(fps) is not int or fps<=0:raise ValueError('positive playback fps required')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter,writers
    if not writers.is_available('ffmpeg'):raise RuntimeError('FFmpeg required for MP4 only')
    data=payload();fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    ax=fig.add_axes([.06,.29,.40,.44]);ax.set(xlim=(-1.3,1.3),ylim=(-1.3,1.3),aspect='equal')
    theta=np.linspace(0,2*np.pi,129);ax.plot(np.cos(theta),np.sin(theta),linewidth=1)
    ax.axhline(0,alpha=.2);ax.axvline(0,alpha=.2)
    ax.set_xlabel('Real part of c',fontsize=10);ax.set_ylabel('Imaginary part of c',fontsize=10)
    ax.scatter([p['real'] for p in data['points']],[p['imag'] for p in data['points']],s=8,alpha=.18)
    dot,=ax.plot([1],[0],marker='o',markersize=12)
    fig.text(.05,.95,'UQCF–GEM / v15.23 / EXACT SUFFICIENT-CHANNEL CLASSIFICATION',fontsize=10,weight='bold')
    fig.text(.05,.876,'Same event. A family of retention maps.',fontsize=27,weight='bold')
    fig.text(.05,.807,'Every point in the disk preserves the specified event’s full quantum branch outputs.',fontsize=13)
    heading=fig.text(.52,.70,'',fontsize=19,weight='bold',va='top')
    metrics=fig.text(.52,.61,'',fontsize=15,linespacing=1.65,va='top')
    detail=fig.text(.52,.415,'',fontsize=12,linespacing=1.65,va='top')
    fig.text(.05,.192,'Binary idempotents: identity or full pinching. Four-outcome batch: 15 partition maps.',fontsize=13)
    fig.text(.05,.133,'An invertible coordinate formula is not necessarily a reversible physical quantum channel.',fontsize=11)
    fig.text(.05,.08,'No actual outcome selected. The instrument and tested coefficients remain supplied.',fontsize=11)
    fig.text(.05,.034,'Playback is not physical time. No entropy-production, collapse-selection or gravitational law is derived.',fontsize=10)
    story=[(1,0,'IDENTITY','Nothing is reduced.\nAll event branches remain exact.'),(.5,0,'PARTIAL DEPHASING','Still linearly injective, but no all-input\nCPTP inverse can undo the contraction.'),(1,np.pi/2,'REVERSIBLE PHASE','A nontrivial unitary changes relative phase.\nIt preserves all distinguishability.'),(0,0,'FULL PINCHING','The only nonidentity binary idempotent.\nIt still does not select an actual outcome.'),(.5,np.pi,'NOT ONE REAL MIXTURE','Complex coefficients were not fixed by\nsufficiency. Repetition generally changes the map.'),(1,np.pi,'THE REMAINING CHOICE','Full batch preservation admits 15 idempotents.\nA supplied event or batch does not choose actuality.')]
    def draw(row):
        radius,phase,title,note=row;c=radius*np.exp(1j*phase);dot.set_data([c.real],[c.imag])
        heading.set_text(title);metrics.set_text(f'Phase-pair distinguishability: {radius:.2f}\nIdempotence residual |c² − c|: {abs(c*c-c):.2f}\nSpecified event outputs: unchanged')
        detail.set_text(note)
    path.parent.mkdir(parents=True,exist_ok=True);draw(story[3]);fig.savefig(path.with_suffix('.png'),dpi=120)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=1800,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    with writer.saving(fig,str(path),dpi=100):
        for row in story:
            draw(row)
            for _ in range(4*fps):writer.grab_frame()
    plt.close(fig)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs');p.add_argument('--video',action='store_true')
    args=p.parse_args();data=payload();args.out.mkdir(parents=True,exist_ok=True)
    write_html(data,args.out/'retention_family.html')
    (args.out/'replay_data.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
    (args.out/'verification.json').write_text(json.dumps(data['audit'],indent=2,allow_nan=False)+'\n')
    if args.video:movie(args.out/'retention_family.mp4')
    print('Generated 81 inspected coefficients and 15 batch partition maps. No physical selector added.')
if __name__=='__main__':main()
