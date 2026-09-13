#!/usr/bin/env python3
"""Offline inspection of alternative partial reductions of one fixed encoding."""
from __future__ import annotations
import argparse
from functools import lru_cache
import itertools
import json
from pathlib import Path
import numpy as np
import recoverability as m
ROOT=Path(__file__).resolve().parent
STORY=('0000','1000','0001','1100','1110','1111')


@lru_cache(None)
def visual_payload() -> dict:
    a=m.audit();f=m.basis();rho=m.fixture();cases=[]
    for mask in m.masks():
        row=m.details(mask);witnesses=[]
        for i,j in itertools.combinations(range(16),2):
            values=[]
            for phase in (1,1j):
                x,y=m.phase_pair(i,j,phase)
                values.append(m.distance(m.reduce_input(x,mask),m.reduce_input(y,mask)))
            witnesses.append({'i':i,'j':j,'output_distances':values})
        row['witnesses']=witnesses
        row['record_probabilities']=np.diag(f@m.reduce_input(rho,mask)@f.conj().T).real.tolist()
        cases.append(row)
    return {'version':'v15.16','cases':cases,'audit':a,'records':list(m.old.EVENTS),
            'story':list(STORY),'notice':'Alternative reductions of the same completed encoding; no actual record selected.'}


def write_html(data: dict,path: Path) -> None:
    payload=json.dumps(data,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    text=(ROOT/'viewer.html').read_text().replace('__DATA__',payload)
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')


def movie(path: Path,fps: int=10) -> None:
    if type(fps) is not int or fps<=0:raise ValueError('positive playback fps required; not a physical clock')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter,writers
    if not writers.is_available('ffmpeg'):raise RuntimeError('FFmpeg required only for MP4')
    data=visual_payload();rows={c['mask']:c for c in data['cases']}
    fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    ax=fig.add_axes([.07,.25,.43,.50]);im=ax.imshow(rows['0000']['keep_matrix'],vmin=0,vmax=1,interpolation='nearest')
    ax.set_xticks([0,7,15],['0000','0111','1111']);ax.set_yticks([0,7,15],['0000','0111','1111'])
    ax.tick_params(length=0,labelsize=9)
    fig.text(.05,.95,'UQCF–GEM / v15.16 / PARTIAL-PRUNING OBSERVABLE MAP',fontsize=10,weight='bold')
    fig.text(.05,.874,'What survives a partial pruning?',fontsize=28,weight='bold')
    fig.text(.05,.815,'Same completed quantum encoding. Different declared record reductions.',fontsize=14)
    label=fig.text(.55,.72,'',fontsize=17,weight='bold')
    counts=fig.text(.55,.665,'',fontsize=15,linespacing=1.7,va='top')
    witness=fig.text(.55,.49,'',fontsize=14,weight='bold',linespacing=1.6,va='top')
    detail=fig.text(.55,.335,'',fontsize=12,linespacing=1.6,va='top')
    fig.text(.065,.195,'Matrix entry 1: observable direction survives. Entry 0: erased between those label sectors.',fontsize=11)
    fig.text(.05,.12,'Dimension counts include the identity. They are not entropy, duration or numbers of physical qubits.',fontsize=10)
    fig.text(.05,.075,'No actual record selected. The dynamics, carrier and retained-description choices remain supplied.',fontsize=10)
    fig.text(.05,.031,'Playback is not physical time. Each view is recomputed from the same encoding; backward replay is not recovery.',fontsize=10)
    def draw(mask):
        row=rows[mask];im.set_data(row['keep_matrix']);k=mask.count('1')
        label.set_text('PINCHED RECORDS: '+(', '.join(row['pinched_records']) or 'none'))
        counts.set_text(f"Surviving observable directions: {row['hermitian_dimension']} / 256\nQuantum blocks: {2**k} × M{2**(4-k)}\nSurviving phase pairs: {row['surviving_unordered_pairs']} / 120")
        w=next(w for w in row['witnesses'] if w['i']==0 and w['j']==8)
        witness.set_text('Witness: 0000 ± 1000\nInput distinguishability: 1\nAfter reduction: '+f"{w['output_distances'][0]:.6f}")
        detail.set_text('The witness lies in the derived input basis.\nSame-size masks can erase different distinctions.\nFull outcome probabilities remain unchanged.')
    path.parent.mkdir(parents=True,exist_ok=True);draw('1000');fig.savefig(path.with_suffix('.png'),dpi=120)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=1800,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    with writer.saving(fig,str(path),dpi=100):
        for mask in STORY:
            draw(mask)
            for _ in range(4*fps):writer.grab_frame()
    plt.close(fig)


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs');p.add_argument('--video',action='store_true')
    a=p.parse_args();data=visual_payload();a.out.mkdir(parents=True,exist_ok=True)
    write_html(data,a.out/'partial_pruning.html')
    (a.out/'visual_data.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
    if a.video:movie(a.out/'partial_pruning.mp4')
    print('Exported 16 supplied masks and 3,840 measured phase-witness controls; no physical clock or actual outcome.')

if __name__=='__main__':main()
