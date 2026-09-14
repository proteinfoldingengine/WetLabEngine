#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,pathlib
from functools import lru_cache
import numpy as np
import selector_rank as m
ROOT=pathlib.Path(__file__).resolve().parent
STORY=('HODGE_TARGET','MICROSCOPIC_TARGET','CYCLE_SHIFT_TARGET','HODGE_TARGET','MICROSCOPIC_TARGET','CYCLE_SHIFT_TARGET')

@lru_cache(None)
def payload():
    a=m.audit();c=m.base.torus_complex(7);q,d=m.base.incidence_defect(c,(0,0),'bottom',1.0);R=m.response_operator(c);far=m.base.farthest_face(c,(0,0))
    jh=m.base.compatibility_response(c.B1,q).current;jl=-d;js=jh+0.25*c.B2[:,c.face_index[far]]
    def item(name,j):
        target=R@j
        return {'name':name,'target_norm':float(np.linalg.norm(target)),'current_norm':float(np.linalg.norm(j)),'support_fraction':float(np.mean(np.abs(j)>1e-10)),'remote_holonomy':m.base.holonomy_defect(m.base.face_holonomy(c,j,far,.2,False)),'face_curl_norm':float(np.linalg.norm(c.B2.T@j)),'periods':(m.period_rows(c)@j).tolist(),'current':j.tolist(),'target':target.tolist()}
    return {'version':'v15.26','audit':a,'targets':{'HODGE_TARGET':item('HODGE_TARGET',jh),'MICROSCOPIC_TARGET':item('MICROSCOPIC_TARGET',jl),'CYCLE_SHIFT_TARGET':item('CYCLE_SHIFT_TARGET',js)},'notice':'Three exact currents for the same source q. The rank gate reconstructs whichever cycle-response target is supplied; it does not choose the target law.'}

def write_html(data,path):
    text=json.dumps(data,separators=(',',':'),allow_nan=False).replace('<','\\u003c');path.parent.mkdir(parents=True,exist_ok=True);path.write_text((ROOT/'viewer.html').read_text().replace('__DATA__',text),encoding='utf-8')

def movie(path,fps=10):
    if type(fps) is not int or fps<=0:raise ValueError('positive playback rate required')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter,writers
    if not writers.is_available('ffmpeg'):raise RuntimeError('FFmpeg required')
    d=payload();fig=plt.figure(figsize=(12.8,7.2),dpi=100);ax=fig.add_axes([.07,.30,.55,.42]);x=np.arange(98);line,=ax.plot(x,np.zeros(98),linewidth=1.5);ax.axhline(0,linewidth=.8);ax.set_xlim(0,97);ax.set_ylim(-1.05,1.05);ax.set_xlabel('edge label — display only');ax.set_ylabel('current coefficient')
    fig.text(.05,.95,'UQCF–GEM / v15.26 / PRE-TIME RESPONSE SELECTOR RANK GATE',fontsize=10,weight='bold');fig.text(.05,.875,'Full rank is not a selector.',fontsize=27,weight='bold');title=fig.text(.66,.70,'',fontsize=18,weight='bold',va='top');detail=fig.text(.66,.60,'',fontsize=12,linespacing=1.65,va='top')
    fig.text(.05,.19,'cycle dim 50  ·  face response rank 48  ·  +2 homology periods ⇒ rank 50',fontsize=13);fig.text(.05,.13,'Same source q. Different cycle-response targets. Different currents.',fontsize=11);fig.text(.05,.08,'No gravity signal certified. The missing object is a pre-time source→cycle-response target law.',fontsize=10);fig.text(.05,.035,'No physical time · no pruning · no entropy · no Newton/GR fit',fontsize=10)
    notes={'HODGE_TARGET':'Global diagnostic representative.\nRemote holonomy is nonzero.\nIts target was supplied by the Hodge representative.','MICROSCOPIC_TARGET':'Exact one-edge cancellation.\nRemote holonomy is zero.\nMicroscopic source inheritance picks this target.','CYCLE_SHIFT_TARGET':'Same q plus a lawful closed cycle.\nCompatibility still closes.\nRemote holonomy changes.'}
    def draw(key):
        r=d['targets'][key];line.set_ydata(r['current']);title.set_text(key.replace('_',' '));detail.set_text(notes[key]+f"\n\nTarget norm: {r['target_norm']:.6f}\nRemote holonomy: {r['remote_holonomy']:.6e}")
    path.parent.mkdir(parents=True,exist_ok=True);draw('HODGE_TARGET');fig.savefig(path.with_suffix('.png'),dpi=120)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=1800,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    with writer.saving(fig,str(path),dpi=100):
        for key in STORY:
            draw(key)
            for _ in range(4*fps):writer.grab_frame()
    plt.close(fig)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=pathlib.Path,default=ROOT/'outputs');p.add_argument('--video',action='store_true');a=p.parse_args();d=payload();a.out.mkdir(parents=True,exist_ok=True);write_html(d,a.out/'selector_rank.html');(a.out/'replay_data.json').write_text(json.dumps(d,separators=(',',':'),allow_nan=False)+'\n');(a.out/'verification.json').write_text(json.dumps(d['audit'],indent=2,allow_nan=False)+'\n');
    if a.video:movie(a.out/'selector_rank.mp4')
    print('Three exact same-q response targets exported. No gravity signal certified.')
if __name__=='__main__':main()
