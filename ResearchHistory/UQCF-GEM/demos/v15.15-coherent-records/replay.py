#!/usr/bin/env python3
"""Offline visual comparison of computed coherent and pinched record blocks."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import coherent_records as m
ROOT=Path(__file__).resolve().parent


def write_html(data: dict,path: Path) -> None:
    text=(ROOT/'viewer.html').read_text()
    encoded=json.dumps(data,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text.replace('__DATA__',encoded),encoding='utf-8')


def movie(path: Path,fps: int=10) -> None:
    if type(fps) is not int or fps<=0:raise ValueError('positive playback fps required')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter,writers
    if not writers.is_available('ffmpeg'):raise RuntimeError('FFmpeg required for MP4, not the HTML replay')
    data=m.visual_payload();stages=data['branches'][0]['frames'];result=data['audit']
    fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    # One chart with a fixed shared scale; no separate subplot scales or fitted colors.
    ax=fig.add_axes([.06,.305,.88,.42])
    def matrix(f):
        return np.concatenate((np.array(f['coherent_blocks']),np.full((16,3),np.nan),np.array(f['pinched_blocks'])),axis=1)
    max_value=max(np.max(f['coherent_blocks']) for f in stages)
    image=ax.imshow(matrix(stages[0]),vmin=0,vmax=max_value,interpolation='nearest')
    ax.set_xticks([0,7,15,19,26,34],['0000','0111','1111','0000','0111','1111'])
    ax.set_yticks([0,7,15],['0000','0111','1111'])
    ax.tick_params(length=0,labelsize=9)
    for spine in ax.spines.values():spine.set_visible(False)
    fig.text(.05,.95,'UQCF–GEM / v15.15 / COHERENT RECORD COMPARISON',fontsize=10,weight='bold')
    fig.text(.05,.88,'Same outcome map. Different recoverability.',fontsize=26,weight='bold')
    stage_label=fig.text(.05,.811,'',fontsize=14)
    fig.text(.30,.757,'COHERENT ENCODING',fontsize=12,ha='center',weight='bold')
    fig.text(.71,.757,'AFTER DECLARED RECORD PINCHING',fontsize=12,ha='center',weight='bold')
    fig.text(.05,.245,'Cells: norms of record-sector blocks in the joint state — not just the memory marginal.',fontsize=11)
    detail=fig.text(.05,.188,'',fontsize=14,weight='bold')
    secondary=fig.text(.05,.14,'',fontsize=12)
    fig.text(.05,.078,'No actual record selected. Carrier, record registers and pinching are explicitly supplied.',fontsize=11)
    fig.text(.05,.035,'Playback is not physical time. This does not derive objective collapse, entropy production, duration or gravity.',fontsize=10)
    def draw(i):
        f=stages[min(i,4)];image.set_data(matrix(f))
        if i<5:
            stage_label.set_text('Declared circuit prefix: '+(' → '.join(data['branches'][0]['schedule'][:i]) or 'empty'))
            detail.set_text('Identical record probabilities; inter-sector coherence '+('has not yet been encoded.' if i==0 else 'survives only on the left.'))
            secondary.set_text('Joint off-diagonal record-block norm: '+f'{f["joint_offdiagonal_norm"]:.6f}'+'   |   No branch has been made actual.')
        else:
            stage_label.set_text('FULL INVERSE CONTROL — computed separately from playback')
            detail.set_text(f'Coherent inverse error: {result["echo"]["coherent_inverse_error"]:.2e}   |   Pinched inverse distance: {result["echo"]["pinched_inverse_distance"]:.6f}')
            secondary.set_text('Orthogonal input witness: distinguishability 1 survives encoding, but falls to ≈0 after pinching.')
    path.parent.mkdir(parents=True,exist_ok=True)
    draw(4);fig.savefig(path.with_suffix('.png'),dpi=120)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=1800,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    with writer.saving(fig,str(path),dpi=100):
        for i in range(6):
            draw(i)
            for _ in range(4*fps):writer.grab_frame()
    plt.close(fig)


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'outputs')
    parser.add_argument('--video',action='store_true')
    args=parser.parse_args();data=m.visual_payload();args.out.mkdir(parents=True,exist_ok=True)
    write_html(data,args.out/'coherent_records.html')
    (args.out/'replay_data.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
    (args.out/'verification.json').write_text(json.dumps(data['audit'],indent=2,allow_nan=False)+'\n')
    if args.video:movie(args.out/'coherent_records.mp4')
    print('Computed five schedules, 80 final branch maps, and 155 prefix maps. No actual outcome selected.')

if __name__=='__main__':main()
