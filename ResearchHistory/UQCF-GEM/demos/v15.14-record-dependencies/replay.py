#!/usr/bin/env python3
"""Offline computed replay and movie of a declared record-read dependency."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import adaptive as m
ROOT=Path(__file__).resolve().parent


def write_html(data: dict,path: Path) -> None:
    text=(ROOT/'viewer.html').read_text()
    payload=json.dumps(data,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text.replace('__DATA__',payload),encoding='utf-8')


def movie_story(records: str='1001') -> list[dict]:
    m.base.validate_records(records)
    f=m.start(); story=[{'snapshot':f,'blocked_attempt':None,'heading':'Two events are ready',
                       'message':'A1 and B1 may be computed in either order.\nNo actual record has been selected by the model.'}]
    for e in ('B1','A1','B2','A2'):
        f=m.advance(f,e,int(records[m.EVENTS.index(e)]))
        story.append({'snapshot':f,'blocked_attempt':None,
                      'heading':f'{e}: supplied record committed',
                      'message': 'A1 is now available to the B2 controller.\nA2 and B2 can still be interleaved.' if e=='A1' else
                                 (f'The controller reads the realized A1={dict(f.records)["A1"]}.\nIt does not look ahead into the outcome script.' if e=='B2' else
                                  ('Same retained result across five valid schedules.\nNo unique global execution order is imposed.' if e=='A2' else
                                   'B1 is recorded. B2 still needs the A1 record.\nIts local predecessor alone is not sufficient.'))})
        if e=='B1':
            try: m.advance(f,'B2',int(records[3]))
            except m.MissingRecord: pass
            else: raise AssertionError('premature event should be blocked')
            story.append({'snapshot':f,'blocked_attempt':'B2','heading':'B2 is blocked — A1 is missing',
                          'message':'The attempted event leaves the quantum state unchanged.\nThe simulator neither guesses A1 nor reads its future value.'})
    return story


def movie(path: Path,fps: int=10) -> None:
    if type(fps) is not int or fps<=0: raise ValueError('positive playback fps required')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter,writers
    if not writers.is_available('ffmpeg'): raise RuntimeError('FFmpeg needed for MP4, not HTML')
    fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    ax=fig.add_axes([.055,.30,.44,.44]); ax.axis('off'); ax.set(xlim=(-.4,1.4),ylim=(-.5,1.5))
    coords={'A1':(0,1),'A2':(0,0),'B1':(1,1),'B2':(1,0)}
    for a,b in m.edges():
        extra=(a,b)==('A1','B2')
        ax.annotate('',coords[b],coords[a],arrowprops=dict(arrowstyle='->',shrinkA=32,shrinkB=32,lw=2,linestyle='--' if extra else '-',alpha=1 if extra else .4))
    ax.text(.55,.60,'reads A1',fontsize=12,ha='center',rotation=-27)
    markers={e:ax.scatter([x],[y],s=1500,facecolors='none',linewidths=3) for e,(x,y) in coords.items()}
    statuses={}
    for e,(x,y) in coords.items():
        ax.text(x,y,e,ha='center',va='center',fontsize=16,weight='bold')
        statuses[e]=ax.text(x,y-.27,'',ha='center',fontsize=12)
    fig.text(.05,.95,'UQCF–GEM / v15.14 / COMPUTED RECORD-DEPENDENT DEMONSTRATOR',fontsize=10,weight='bold')
    fig.text(.05,.877,'Records constrain order. Not a global clock.',fontsize=26,weight='bold')
    fig.text(.05,.819,'Added illustrative rule: B2 reads the realized A1 record.',fontsize=13)
    heading=fig.text(.55,.725,'',fontsize=17,weight='bold')
    info=fig.text(.55,.653,'',fontsize=12,linespacing=1.65,va='top')
    fig.text(.55,.485,'REALIZED RECORD STORE',fontsize=10,weight='bold')
    record=fig.text(.55,.432,'',fontsize=29,family='monospace')
    value=fig.text(.55,.37,'',fontsize=12,linespacing=1.8,va='top')
    history=fig.text(.05,.21,'',fontsize=20,family='monospace',weight='bold')
    fig.text(.05,.137,'80 valid runs: matching records, matching quantum states and joint weights.',fontsize=12)
    fig.text(.05,.087,'The record wire, controller, carrier, RAS and actual outcomes are supplied illustrative inputs.',fontsize=10)
    fig.text(.05,.043,'Playback is not physical time. No fundamental causality, entropy-production, duration or collapse law is derived.',fontsize=10)
    story=movie_story(); path.parent.mkdir(parents=True,exist_ok=True)
    def draw(row,index):
        f=row['snapshot']; rec=dict(f.records)
        for e,marker in markers.items():
            marker.set_alpha(1 if e in f.done else .7 if e in m.enabled(f) else .25)
            statuses[e].set_text('record '+str(rec[e]) if e in rec else 'ready' if e in m.enabled(f) else 'blocked')
        heading.set_text(row['heading']); info.set_text(row['message'])
        record.set_text('A '+''.join(str(rec.get(e,'_')) for e in ('A1','A2'))+'  |  B '+''.join(str(rec.get(e,'_')) for e in ('B1','B2')))
        value.set_text('Ready: '+(', '.join(m.enabled(f)) or 'complete')+f'\nJoint branch weight: {f.mass:.6f}')
        path_done=['B1','A1','B2','A2'][:len(f.done)]
        history.set_text('ROOT'+('  →  '+'  →  '.join(path_done) if path_done else ''))
    draw(story[2],2); fig.savefig(path.with_suffix('.png'),dpi=120)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=1800,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    with writer.saving(fig,str(path),dpi=100):
        for i,row in enumerate(story):
            draw(row,i)
            for _ in range(4*fps): writer.grab_frame()
    plt.close(fig)


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--out',type=Path,default=ROOT/'outputs');p.add_argument('--video',action='store_true')
    a=p.parse_args(); data=m.payload();a.out.mkdir(parents=True,exist_ok=True)
    write_html(data,a.out/'record_dependencies.html')
    (a.out/'verification.json').write_text(json.dumps(data['audit'],indent=2,allow_nan=False)+'\n')
    (a.out/'replay_data.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
    if a.video: movie(a.out/'record_dependencies.mp4')
    print('Computed and exported 80 valid record-dependent runs; no physical clock supplied.')

if __name__=='__main__':main()
