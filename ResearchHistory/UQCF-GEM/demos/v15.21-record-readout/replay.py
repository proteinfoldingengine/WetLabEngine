#!/usr/bin/env python3
"""Offline readout inspector and movie generated from the frozen quantum model."""
import argparse
import json
from pathlib import Path
import numpy as np
import record_readout as m
ROOT=Path(__file__).resolve().parent
STORY=(('fixture',0),('fixture',4),('basis_0000',0),('basis_1010',2),('maximally_mixed',0),('basis_1111',4))


def write_html(data,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    value=json.dumps(data,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    path.write_text((ROOT/'viewer.html').read_text().replace('__DATA__',value),encoding='utf-8')


def movie(path,fps=10):
    if type(fps) is not int or fps<=0:raise ValueError('positive playback fps required')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter,writers
    if not writers.is_available('ffmpeg'):raise RuntimeError('FFmpeg is needed for MP4 only')
    data=m.payload();cases={(c['input'],c['schedule_index']):c for c in data['cases']}
    fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    ax=fig.add_axes([.08,.29,.54,.43]);ax.set(xlim=(-.5,15.5),ylim=(-.05,1.12))
    ax.set_xticks([0,5,10,15],['0000','0101','1010','1111']);ax.set_ylabel('Complete-history probability')
    ideal,=ax.plot(range(16),np.zeros(16),marker='o',linewidth=2,label='Original')
    raw,=ax.plot(range(16),np.zeros(16),marker='x',linestyle='--',label='Encoded: actual measurement')
    corrected,=ax.plot(range(16),np.zeros(16),marker='s',fillstyle='none',linestyle=':',label='Signed ensemble readout')
    ax.legend(fontsize=8,loc='upper right')
    fig.text(.05,.95,'UQCF–GEM / v15.21 / RECORD READOUT VERSUS RECORD EVENTS',fontsize=10,weight='bold')
    fig.text(.05,.87,'Exact prediction is not an exact record event.',fontsize=25,weight='bold')
    heading=fig.text(.05,.795,'',fontsize=13)
    fig.text(.67,.70,'FULL-HISTORY READOUT',fontsize=12,weight='bold')
    fig.text(.67,.64,'q = p/2 + 1/32\np = 2q − 1/16',fontsize=19,linespacing=1.4,va='top')
    fig.text(.67,.49,'Signed correction is not a\nphysical measurement effect.\n\nFirst binary event: best\nsingle-copy worst-case error = 1/4.',fontsize=12,linespacing=1.6,va='top')
    fig.text(.05,.195,'Decode joint masses before forming conditional probabilities—not each conditional independently.',fontsize=12)
    fig.text(.05,.13,'Same four-qubit encoding and adaptive instruments. No new motion or physical pruning law.',fontsize=11)
    fig.text(.05,.075,'No actual record selected. Distributions are enumerated; no random outcome is sampled.',fontsize=11)
    fig.text(.05,.032,'Playback is not physical time. Cases compare supplied inputs, not successive physical histories.',fontsize=10)
    def draw(key):
        c=cases[key];ideal.set_ydata(c['ideal']);raw.set_ydata(c['raw']);corrected.set_ydata(c['decoded'])
        heading.set_text('Supplied input: '+c['input']+'    |    '+ ' → '.join(c['schedule']))
    path.parent.mkdir(parents=True,exist_ok=True);draw(STORY[2]);fig.savefig(path.with_suffix('.png'),dpi=110)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=1800,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    with writer.saving(fig,str(path),dpi=100):
        for key in STORY:
            draw(key)
            for _ in range(4*fps):writer.grab_frame()
    plt.close(fig)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs');p.add_argument('--video',action='store_true')
    a=p.parse_args();data=m.payload();a.out.mkdir(parents=True,exist_ok=True)
    write_html(data,a.out/'record_readout.html')
    (a.out/'verification.json').write_text(json.dumps(data['audit'],indent=2,allow_nan=False)+'\n')
    (a.out/'replay_data.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
    if a.video:movie(a.out/'record_readout.mp4')
    print('Exported 90 input/schedule comparisons. No physical record channel or actuality derived.')

if __name__=='__main__':main()
