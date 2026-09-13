#!/usr/bin/env python3
"""Computed partial-order replay. No display quantity is a physical clock."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import event_model as m
ROOT=Path(__file__).resolve().parent


def comparison(a: m.Snapshot,b: m.Snapshot) -> dict:
    same=a.done==b.done
    return {'comparable':same,'state_distance':m.distance(a.rho,b.rho) if same else None,
            'joint_mass_difference':abs(a.mass-b.mass) if same else None}


def write_html(payload: dict,path: Path) -> None:
    text=(ROOT/'viewer.html').read_text()
    data=json.dumps(payload,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text.replace('__DATA__',data),encoding='utf-8')


def movie(path: Path,fps: int=10) -> None:
    if type(fps) is not int or fps<=0: raise ValueError('positive playback fps required')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter, writers
    if not writers.is_available('ffmpeg'): raise RuntimeError('FFmpeg required for MP4, not HTML')
    records='1001'; schedules=m.schedules(); trajectories=[m.run(s,records) for s in schedules]
    result=m.audit(); fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    ax=fig.add_axes([.06,.22,.52,.55]); ax.set(xlim=(-.55,2.55),ylim=(-.5,2.5))
    ax.set_xticks([0,1,2],['A: __','A: 1_','A: 10'])
    ax.set_yticks([0,1,2],['B: __','B: 0_','B: 01'])
    ax.tick_params(length=0,labelsize=12); [sp.set_visible(False) for sp in ax.spines.values()]
    for i in range(3):
        for j in range(3):
            if i<2: ax.annotate('',(i+1,j),(i,j),arrowprops=dict(arrowstyle='->',alpha=.2))
            if j<2: ax.annotate('',(i,j+1),(i,j),arrowprops=dict(arrowstyle='->',alpha=.2))
    dots=ax.scatter([i for i in range(3) for j in range(3)],[j for i in range(3) for j in range(3)],s=260,alpha=.2)
    for i in range(3):
        for j in range(3): ax.text(i,j-.15,f'rank {16//2**(i+j)}',ha='center',va='top',fontsize=9)
    line,=ax.plot([],[],linewidth=4,marker='o',markersize=14)
    fig.text(.055,.94,'UQCF–GEM / v15.13 / INDEPENDENT-EVENT SIMULATION',fontsize=10,weight='bold')
    fig.text(.055,.866,'One record structure. Six valid execution orders.',fontsize=24,weight='bold')
    fig.text(.055,.80,'A1 precedes A2. B1 precedes B2. No cross-stream ordering is supplied.',fontsize=12)
    schedule_label=fig.text(.65,.70,'',fontsize=15,weight='bold')
    context=fig.text(.65,.61,'',fontsize=17,family='monospace')
    detail=fig.text(.65,.48,'',fontsize=12,linespacing=1.6)
    fig.text(.65,.285,f'96 supplied runs checked\nShared-set distance: {result["max_state_error"]:.2e}\nJoint-weight error: {result["max_mass_error"]:.2e}',fontsize=12,linespacing=1.6)
    fig.text(.055,.13,'Each node is a completed record set, not a point in space or a clock reading.',fontsize=12)
    fig.text(.055,.085,'Independent operations can have correlated outcomes. Conditional weights are not universal event properties.',fontsize=10)
    fig.text(.055,.045,'Playback is not physical time. Carrier, motion, RAS and actual records are supplied; no collapse law is derived.',fontsize=10)
    def draw(si,step):
        fs=trajectories[si]; points=[(sum(e[0]=='A' for e in f.done),sum(e[0]=='B' for e in f.done)) for f in fs[:step+1]]
        line.set_data([x for x,y in points],[y for x,y in points])
        f=fs[step]; a=''.join(records[m.EVENTS.index(e)] for e in ('A1','A2') if e in f.done)
        b=''.join(records[m.EVENTS.index(e)] for e in ('B1','B2') if e in f.done)
        schedule_label.set_text(f'EXECUTION ORDER {si+1}/6\n'+ ' → '.join(schedules[si]))
        context.set_text('A: '+a.ljust(2,'_')+'    B: '+b.ljust(2,'_'))
        detail.set_text(f'Completed events: {len(f.done)}\nJoint branch weight: {f.mass:.6f}\n'+(f'Last conditional weight: {f.conditional_weight:.6f}' if step else 'No actual records supplied yet')+'\n'+('Same final record and joint weight.' if step==4 else 'Compare states only at matching nodes.'))
    path.parent.mkdir(parents=True,exist_ok=True)
    draw(2,2); fig.savefig(path.with_suffix('.png'),dpi=110)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=1800,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    hold=max(1,round(.7*fps))
    with writer.saving(fig,str(path),dpi=100):
        for si in range(6):
            for step in range(5):
                draw(si,step)
                for _ in range(hold): writer.grab_frame()
    plt.close(fig)


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--out',type=Path,default=ROOT/'outputs'); p.add_argument('--video',action='store_true')
    args=p.parse_args(); payload=m.build_payload(); args.out.mkdir(parents=True,exist_ok=True)
    write_html(payload,args.out/'independent_events.html')
    (args.out/'verification.json').write_text(json.dumps(payload['audit'],indent=2,allow_nan=False)+'\n')
    (args.out/'replay_data.json').write_text(json.dumps(payload,separators=(',',':'),allow_nan=False)+'\n')
    if args.video: movie(args.out/'independent_events.mp4')
    print('Generated computed replay for 16 supplied records x 6 schedules.')
if __name__=='__main__': main()
