#!/usr/bin/env python3
"""Render/replay actual Python states; visual layout is not emergent geometry."""
from __future__ import annotations
import argparse
import copy
import itertools
import json
import math
import textwrap
from pathlib import Path
import numpy as np
from simulation import ROOT, Trace, build_demo, save_trace

PAIRS=list(itertools.combinations(range(8),2))


def export_view(trace: Trace) -> dict:
    starts={}; frames=[]
    for i,f in enumerate(trace.frames):
        starts.setdefault(f.phase,i)
        frames.append({'phase':f.phase,'label':f.label,'message':f.message,'record':f.record,
                       'ordinal':f.ordinal,'event_number':f.event_number,'algebra_level':f.algebra_level,
                       'extent':None if f.extent is None else round(f.extent,8),
                       'probabilities':[round(float(v.real),9) for v in np.diag(f.rho)],
                       'coherence':[round(float(abs(f.rho[a,b])),9) for a,b in PAIRS]})
    return {'frames':frames,'phase_starts':starts,'summary':trace.summary()}


def make_bundle(scenario: dict,cadence: int=20) -> dict:
    branches={}
    for k in range(8):
        s=copy.deepcopy(scenario); s['actual_records']=[int(c) for c in f'{k:03b}']
        branches[f'{k:03b}']=export_view(build_demo(s,cadence))
    return {'version':'v15.12','initial_branch':''.join(map(str,scenario['actual_records'])),
            'display_samples_per_second':cadence,'branches':branches,'pairs':PAIRS,
            'notice':'Python-computed replay. Animation cadence, camera motion and cube coordinates are display conventions only.'}


def write_html(bundle: dict,path: Path) -> None:
    template=(ROOT/'viewer_template.html').read_text()
    payload=json.dumps(bundle,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(template.replace('__DEMO_DATA__',payload),encoding='utf-8')


def render_movie(trace: Trace,path: Path,fps: int=20,poster: Path | None=None) -> None:
    if type(fps) is not int or fps<=0: raise ValueError('video fps must be a positive integer; it is not a physical clock')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter
    from matplotlib import animation
    from mpl_toolkits.mplot3d import proj3d
    if not animation.writers.is_available('ffmpeg'): raise RuntimeError('FFmpeg is needed to render MP4; the HTML replay does not need it')
    # One chart/axes. Typography and annotations are figure text, not subplots.
    fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    ax=fig.add_axes([.025,.21,.60,.63],projection='3d')
    coords=np.array([[1 if c=='1' else -1 for c in f'{k:03b}'] for k in range(8)],dtype=float)
    ax.set_axis_off(); ax.set_box_aspect((1,1,1)); ax.set(xlim=(-1.5,1.5),ylim=(-1.5,1.5),zlim=(-1.5,1.5))
    # Matplotlib default colors; no decorative physics-colored fields.
    ax.scatter(*coords.T,s=90,facecolors='none',alpha=.25,depthshade=False)
    edges=[]
    for a,b in PAIRS:
        edges.append(ax.plot(*coords[[a,b]].T,linewidth=.8,alpha=.3)[0])
    nodes=ax.scatter(*coords.T,s=np.full(8,450),depthshade=False)
    texts=[fig.text(0,0,f'{k:03b}',ha='center',va='center',fontsize=10) for k in range(8)]
    fig.text(.045,.955,'UQCF–GEM  /  v15.12  /  INTEGRATED CONDITIONAL MODEL',fontsize=10,weight='bold')
    fig.text(.045,.897,'From reversible motion to retained history',fontsize=25,weight='bold')
    title=fig.text(.64,.77,'',fontsize=14,weight='bold',va='top')
    description=fig.text(.64,.69,'',fontsize=12,va='top',linespacing=1.4)
    fig.text(.64,.51,'ACTUAL RECORD',fontsize=9,weight='bold')
    record_text=fig.text(.64,.46,'',fontsize=28,family='monospace')
    ordinal=fig.text(.64,.393,'',fontsize=12)
    detail=fig.text(.64,.34,'',fontsize=11,va='top',linespacing=1.5)
    fig.text(.045,.245,'Node area: basis probability  ·  Link width/opacity: coherence magnitude',fontsize=10)
    fig.text(.045,.217,'The eight-node layout is illustrative, not space or a derived metric.',fontsize=10)
    history=fig.text(.045,.142,'',fontsize=20,family='monospace',weight='bold')
    fig.text(.045,.09,'RAS = supplied retained algebra  ·  RCR = supplied actual record  ·  No automatic choice',fontsize=10)
    fig.text(.045,.045,'Playback is not physical time. Event order is conditional; duration, entropy production and gravity are not derived.',fontsize=10)
    sample_label=fig.text(.955,.955,'',fontsize=9,ha='right')
    branches=''.join(map(str,trace.records))
    def draw(idx):
        f=trace.frames[idx]; probs=np.maximum(np.real(np.diag(f.rho)),0)
        nodes.set_sizes(4600*probs)
        for line,(a,b) in zip(edges,PAIRS):
            magnitude=float(abs(f.rho[a,b]))
            line.set_alpha(min(1.,4*magnitude)); line.set_linewidth(.5+14*magnitude)
        ax.view_init(elev=18+4*math.sin(idx/len(trace.frames)*math.pi),azim=-58+idx/len(trace.frames)*68)
        for k,text in enumerate(texts):
            text.set_text(f'{k:03b}\n{probs[k]*100:4.1f}%')
            text.set_alpha(1 if f'{k:03b}'.startswith(f.record) else .25)
            xp,yp,_=proj3d.proj_transform(*coords[k],ax.get_proj())
            xf,yf=fig.transFigure.inverted().transform(ax.transData.transform((xp,yp)))
            dx=(.027+.018*math.sqrt(probs[k]))*(1 if xf>.325 else -1)
            dy=(.024+.022*math.sqrt(probs[k]))*(1 if yf>.525 else -1)
            text.set_position((xf+dx,yf+dy))
        ax.view_init(elev=18+4*math.sin(idx/len(trace.frames)*math.pi),azim=-58+idx/len(trace.frames)*68)
        title.set_text(f.label.replace('  /  ','\n'))
        description.set_text('\n'.join(textwrap.wrap(f.message,41)))
        record_text.set_text(f.record+'_'*(3-len(f.record)))
        ordinal.set_text(f'Ordinal records committed: {f.ordinal}   |   Sector rank: {2**(3-len(f.record))}')
        if f.phase.startswith('pretime'):
            detail.set_text(f'Finite transformation extent: {f.extent:.3f}\nNo elapsed-time interpretation\nFull-cycle inverse error: {trace.checks["pretime_reversal_error"]:.2e}')
        elif f.event_number:
            e=trace.events[f.event_number-1]
            if f.phase.startswith('ras'):
                detail.set_text(f'Input distinguishability: {e["witness_before"]:.3f}\nAfter RAS: {e["witness_after_ras"]:.3f}\nShown before supplying this record')
            else:
                detail.set_text(f'Declared record: {e["chosen_record"]}\nIts conditional weight: {e["chosen_conditional_weight"]:.2%}\nWeight did not select actuality')
        else:
            detail.set_text('Earlier record remains exactly retained\nReversible motion adds no new event\nNo calibrated clock has been inserted')
        chain=['ROOT']+[branches[:j]+'_'*(3-j) for j in range(1,f.ordinal+1)]
        history.set_text('  →  '.join(chain))
        sample_label.set_text(f'DISPLAY SAMPLE {idx+1}/{len(trace.frames)}')
    path.parent.mkdir(parents=True,exist_ok=True)
    if poster is not None:
        index=next(i for i,f in enumerate(trace.frames) if f.phase=='rcr_1')
        draw(index); fig.savefig(poster,dpi=130)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=2600,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    with writer.saving(fig,str(path),dpi=100):
        for idx in range(len(trace.frames)):
            draw(idx); writer.grab_frame()
    plt.close(fig)


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario',type=Path,default=ROOT/'scenario.json')
    parser.add_argument('--out',type=Path,default=ROOT/'outputs')
    parser.add_argument('--cadence',type=int,default=20)
    parser.add_argument('--video',action='store_true')
    args=parser.parse_args(); scenario=json.loads(args.scenario.read_text())
    trace=build_demo(scenario,args.cadence); save_trace(trace,args.out)
    bundle=make_bundle(scenario,args.cadence)
    write_html(bundle,args.out/'interactive_demo.html')
    (args.out/'all_branches_summary.json').write_text(json.dumps({k:b['summary'] for k,b in bundle['branches'].items()},indent=2,allow_nan=False)+'\n')
    if args.video: render_movie(trace,args.out/'pretime_to_history.mp4',args.cadence,args.out/'poster.png')
    print(f'Generated {len(trace.frames)} display samples and 8 supplied branch replays in {args.out}')

if __name__=='__main__': main()
