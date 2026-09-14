#!/usr/bin/env python3
"""Computed algebra-completion inspector. No state recovery is performed."""
from __future__ import annotations
import argparse
from functools import lru_cache
import json
from pathlib import Path
import numpy as np
import completion as m
ROOT=Path(__file__).resolve().parent
STORY=(('B1','1111'),('A1','1111'),('pretime','1111'),('B1','1100'),('all_six','1000'),('all_six','1111'))

@lru_cache(None)
def payload() -> dict:
    result=m.audit();rows=[]
    for c in result['cases']:
        row=dict(c);row['initial_matrix']=m.keep(c['initial_blocks']).astype(int).tolist()
        row['completed_matrix']=m.keep(c['final_blocks']).astype(int).tolist();rows.append(row)
    return {'version':'v15.18','cases':rows,'summary':result['classification_by_family'],
            'audit':result,'physical_pruning_law_derived':False,
            'notice':'Required information before pruning; not recovered information. All coordinates and view order are display conventions.'}


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
    data=payload();cases={(c['family'],c['mask']):c for c in data['cases']}
    fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    ax=fig.add_axes([.07,.31,.86,.38])
    image=ax.imshow(np.zeros((16,35)),vmin=0,vmax=1,interpolation='nearest')
    ax.set_xticks([0,7,15,19,26,34],['0000','0111','1111','0000','0111','1111'])
    ax.set_yticks([0,7,15],['0000','0111','1111']);ax.tick_params(length=0,labelsize=9)
    for spine in ax.spines.values():spine.set_visible(False)
    fig.text(.05,.949,'UQCF–GEM / v15.18 / MINIMAL INVARIANT OBSERVABLE ALGEBRA',fontsize=10,weight='bold')
    fig.text(.05,.875,'What must have been kept?',fontsize=29,weight='bold')
    case_title=fig.text(.05,.807,'',fontsize=14)
    fig.text(.30,.731,'ORIGINAL RETAINED ALGEBRA',ha='center',fontsize=12,weight='bold')
    fig.text(.71,.731,'MINIMUM INVARIANT ENLARGEMENT',ha='center',fontsize=12,weight='bold')
    counts=fig.text(.05,.236,'',fontsize=19,weight='bold')
    detail=fig.text(.05,.182,'',fontsize=12)
    fig.text(.05,.128,'Algebra completion requires multiplication. A smaller linear prediction space is a different question.',fontsize=10)
    fig.text(.05,.080,'This is information required BEFORE pruning—not recovered information, and not a new retention law.',fontsize=10)
    fig.text(.05,.035,'Playback is not physical time. No actual record selected. Duration, physical entropy and gravity remain unproved.',fontsize=10)
    def draw(key):
        c=cases[key];matrix=np.concatenate((c['initial_matrix'],np.full((16,3),np.nan),c['completed_matrix']),axis=1)
        image.set_data(matrix);case_title.set_text('Supplied motion family: '+c['family']+'   |   Original pinched mask: '+c['mask'])
        counts.set_text(f"{c['initial_dimension']} → {c['final_dimension']} Hermitian observable directions")
        detail.set_text('Result: '+c['status'].replace('_',' ').lower()+'.  Final blocks: '+ ' + '.join('M'+str(len(g)) for g in c['final_blocks']))
    path.parent.mkdir(parents=True,exist_ok=True);draw(STORY[0]);fig.savefig(path.with_suffix('.png'),dpi=120)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=1800,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    with writer.saving(fig,str(path),dpi=100):
        for key in STORY:
            draw(key)
            for _ in range(4*fps):writer.grab_frame()
    plt.close(fig)


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs');p.add_argument('--video',action='store_true')
    args=p.parse_args();data=payload();args.out.mkdir(parents=True,exist_ok=True)
    write_html(data,args.out/'algebra_completion.html')
    (args.out/'replay_data.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
    (args.out/'verification.json').write_text(json.dumps(data['audit'],indent=2,allow_nan=False)+'\n')
    if args.video:movie(args.out/'algebra_completion.mp4')
    print('Generated 112 algebra-completion cases; original dynamics unchanged.')

if __name__=='__main__':main()
