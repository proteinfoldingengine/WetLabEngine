#!/usr/bin/env python3
"""Computed partition inspector. Shared phases are not sampled actual records."""
from __future__ import annotations
import argparse
from functools import lru_cache
import json
from pathlib import Path
import numpy as np
import composition_gate as m
ROOT=Path(__file__).resolve().parent
STORY=('0000','0011','0110','0120','0001','0123')

@lru_cache(None)
def payload():
    result=m.audit();rows=[]
    for row in result['partitions']:
        item=dict(row)
        item['phase_recipe']=m.phase_recipe(row['matrix']) if row['non_signalling'] else None
        rows.append(item)
    return {'version':'v15.24','partitions':rows,'audit':result,
            'notice':'Independent composition and non-signalling are different tested contracts, not derived physical laws.'}

def write_html(data,path):
    text=json.dumps(data,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text((ROOT/'viewer.html').read_text().replace('__DATA__',text),encoding='utf-8')

def movie(path,fps=10):
    if type(fps) is not int or fps<=0:raise ValueError('positive playback rate required')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter,writers
    if not writers.is_available('ffmpeg'):raise RuntimeError('FFmpeg is required for MP4 only')
    rows={r['partition']:r for r in payload()['partitions']}
    fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    ax=fig.add_axes([.08,.295,.39,.43]);im=ax.imshow(np.eye(4),vmin=0,vmax=1,interpolation='nearest')
    ax.set_xticks(range(4),['00','01','10','11']);ax.set_yticks(range(4),['00','01','10','11'])
    ax.set_xlabel('Joint record label');ax.set_ylabel('Joint record label')
    fig.text(.05,.95,'UQCF–GEM / v15.24 / COMPOSITION AND CROSS-INPUT INFLUENCE',fontsize=10,weight='bold')
    fig.text(.05,.875,'No signalling does not mean independence.',fontsize=26,weight='bold')
    fig.text(.05,.807,'All 15 maps preserve the completed batch. Their local quantum effects differ.',fontsize=13)
    title=fig.text(.53,.70,'',fontsize=18,weight='bold',va='top')
    flags=fig.text(.53,.60,'',fontsize=14,linespacing=1.8,va='top')
    note=fig.text(.53,.415,'',fontsize=12,linespacing=1.65,va='top')
    fig.text(.05,.19,'15 batch-sufficient maps  /  7 non-signalling  /  4 independent products',fontsize=16,weight='bold')
    fig.text(.05,.135,'Preserving either complete next-event instrument is stronger still: only identity remains.',fontsize=11)
    fig.text(.05,.08,'Shared phase mixtures are diagnostic constructions, not sampled outcomes or new physical laws.',fontsize=10)
    fig.text(.05,.035,'No actual outcome selected. Playback is not physical time. No spacetime locality or gravity is derived.',fontsize=10)
    titles={'0000':'IDENTITY','0011':'INDEPENDENT A REDUCTION','0110':'CORRELATED PARITY REDUCTION',
            '0120':'ONE JOINT PHASE SURVIVES','0001':'BATCH-SAFE, BUT SIGNALLING','0123':'INDEPENDENT COMPLETE PINCHING'}
    notes={'0000':'Both local quantum systems are unchanged.',
           '0011':'Pinch A, leave B unchanged.\nNo cross-input influence is introduced.',
           '0110':'Same local outputs as two full pinchings,\nbut different joint retained coherence.\nShared phases suffice; no communication needed.',
           '0120':'Three correlated phase pairs realize this map.\nIt is not a product of independent channels.',
           '0001':'Changing the other input can change a local\nquantum output by trace distance 0.5.\nFinal record probabilities alone miss this.',
           '0123':'This is one of four product choices.\nNo criterion here selects it physically.'}
    def draw(key):
        r=rows[key];im.set_data(r['matrix']);title.set_text(titles[key])
        flags.set_text('Non-signalling: '+('YES' if r['non_signalling'] else 'NO')+'\nIndependent product: '+('YES' if r['product'] else 'NO')+'\nComplete batch preserved: YES')
        note.set_text(notes[key])
    path.parent.mkdir(parents=True,exist_ok=True);draw('0110');fig.savefig(path.with_suffix('.png'),dpi=120)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=1800,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    with writer.saving(fig,str(path),dpi=100):
        for key in STORY:
            draw(key)
            for _ in range(4*fps):writer.grab_frame()
    plt.close(fig)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs');p.add_argument('--video',action='store_true')
    a=p.parse_args();data=payload();a.out.mkdir(parents=True,exist_ok=True)
    write_html(data,a.out/'composition_gate.html')
    (a.out/'replay_data.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
    (a.out/'verification.json').write_text(json.dumps(data['audit'],indent=2,allow_nan=False)+'\n')
    if a.video:movie(a.out/'composition_gate.mp4')
    print('15 partitions, 105 context cases, 1200 completed histories; no outcomes sampled.')
if __name__=='__main__':main()
