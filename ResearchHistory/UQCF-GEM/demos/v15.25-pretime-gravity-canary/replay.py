#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from functools import lru_cache
import numpy as np
import pretime_gravity_canary as m
ROOT=Path(__file__).resolve().parent

@lru_cache(None)
def payload():
    c=m.torus_complex(7);q,delta=m.incidence_defect(c,(0,0),'bottom',1.0);r=m.compatibility_response(c.B1,q)
    edges=[]
    for i,(u,v,t) in enumerate(c.edges):
        edges.append({'i':i,'u':list(u),'v':list(v),'kind':t,'current':float(r.current[i]),'source_incidence':bool(abs(delta[i])>0)})
    faces=[]
    for f in c.faces:
        faces.append({'face':list(f),'distance':m.torus_face_distance(c,(0,0),f),
                      'noncommuting':m.holonomy_defect(m.face_holonomy(c,r.current,f,.2,False)),
                      'commuting':m.holonomy_defect(m.face_holonomy(c,r.current,f,.2,True)),
                      'commutator':m.holonomy_defect(m.response_commutator_holonomy(c,r.current,f,.2,False))})
    orientations=[]
    for slot in ('bottom','right','top','left'):
        qs,_=m.incidence_defect(c,(0,0),slot,1.0);rs=m.compatibility_response(c.B1,qs)
        orientations.append({'slot':slot,'response_norm':float(np.linalg.norm(rs.current)),
                             'response_fraction':float(np.mean(np.abs(rs.current)>1e-10)),
                             **m.remote_shell_summary(c,rs.current,(0,0),.2)})
    audit=m.audit()
    story=[
      {'mode':'source','title':'LOCAL INCIDENCE DEFECT','text':'One provenance incidence is changed.\nNo state is measured and no record is selected.'},
      {'mode':'remote','title':'GLOBAL COMPATIBILITY RESPONSE','text':'The diagnostic Hodge representative spreads globally.\nRemote noncommuting loop response is nonzero.\nThis apparent field is not forced by compatibility.'},
      {'mode':'null','title':'CLOSED-FACE NULL CONTROL','text':'Changing a complete closed face keeps boundary-of-boundary zero.\nThe compatibility response vanishes.'},
      {'mode':'nonuniqueness','title':'PHYSICAL SELECTOR STILL OPEN','text':'Exact one-edge cancellation already closes the defect.\nClosed cycles and edge weights add further nonuniqueness.\nThe gravity canary is killed.'}
    ]
    return {'version':'v15.25','audit':audit,'L':c.L,'edges':edges,'faces':faces,'source_q':q.tolist(),'orientations':orientations,'story':story,
            'notice':'No pruning, entropy, physical time, Newton fit, or GR fit. The source law and diagnostic Hodge representative are supplied canary structures.'}

def write_html(data,path):
    text=json.dumps(data,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text((ROOT/'viewer.html').read_text().replace('__DATA__',text),encoding='utf-8')

def movie(path,fps=10):
    if type(fps) is not int or fps<=0:raise ValueError('positive playback fps required')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter,writers
    if not writers.is_available('ffmpeg'):raise RuntimeError('FFmpeg required for MP4 only')
    data=payload();L=data['L'];fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    ax=fig.add_axes([.06,.23,.53,.62]);ax.set_xlim(-.4,L-.6);ax.set_ylim(-.4,L-.6);ax.set_aspect('equal');ax.set_xticks([]);ax.set_yticks([])
    edge_lines=[]
    for e in data['edges']:
        x1,y1=e['u'];x2,y2=e['v']
        if abs(x2-x1)>1 or abs(y2-y1)>1:continue
        ln,=ax.plot([x1,x2],[y1,y2],linewidth=max(0.5,1+14*abs(e['current'])),alpha=.75)
        edge_lines.append((ln,e))
    ax.scatter([0],[0],marker='s',s=80);ax.scatter([1],[0],marker='s',s=80)
    fig.text(.05,.95,'UQCF–GEM / v15.25 / PRE-TIME GLOBAL COMPATIBILITY CANARY',fontsize=10,weight='bold')
    fig.text(.05,.885,'Apparent long-range signal — killed.',fontsize=27,weight='bold')
    title=fig.text(.63,.76,'',fontsize=17,weight='bold',va='top')
    body=fig.text(.63,.66,'',fontsize=12,linespacing=1.6,va='top')
    metric=fig.text(.63,.43,'',fontsize=13,linespacing=1.6,va='top')
    fig.text(.05,.145,'Response equation:  ∂j + q = 0    •    no pruning    •    no physical time',fontsize=12)
    fig.text(.05,.085,'Bare compatibility admits exact local cancellation. The global Hodge field is not forced.',fontsize=10)
    fig.text(.05,.035,'Playback is not physical time. No actual record selected. No Newton/GR fit.',fontsize=10)
    modes=data['story']
    def scene(row):
        title.set_text(row['title']);body.set_text(row['text'])
        if row['mode']=='source':metric.set_text('Localized source support: 2 vertices\nClosed-face control: exactly zero response')
        elif row['mode']=='remote':metric.set_text(f"Diagnostic Hodge edge coverage: {data['audit']['global_response_fraction']:.1%}\nRemote shell holonomy RMS: {data['audit']['remote_shell']['noncommuting_rms']:.3e}\nBut exact one-edge cancellation also exists")
        elif row['mode']=='null':metric.set_text(f"Boundary-of-boundary baseline: {data['audit']['baseline_chain_error']:.1e}\nClosed-face response: {data['audit']['closed_face_control_response']:.1e}")
        else:metric.set_text(f"Cycle-space freedom: {data['audit']['response_nonuniqueness_dimension']} dimensions\nCycle-shift holonomy change: {data['audit']['cycle_shift_holonomy_change']:.3e}\nWeighted-response change: {data['audit']['weighted_response_difference']:.3e}")
    path.parent.mkdir(parents=True,exist_ok=True);scene(modes[1]);fig.savefig(path.with_suffix('.png'),dpi=110)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=1800,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    with writer.saving(fig,str(path),dpi=100):
        for row in modes:
            scene(row)
            for _ in range(6*fps):writer.grab_frame()
    plt.close(fig)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs');p.add_argument('--video',action='store_true')
    a=p.parse_args();data=payload();a.out.mkdir(parents=True,exist_ok=True)
    write_html(data,a.out/'pretime_gravity_canary.html')
    (a.out/'replay_data.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
    (a.out/'verification.json').write_text(json.dumps(data['audit'],indent=2,allow_nan=False)+'\n')
    if a.video:movie(a.out/'pretime_gravity_canary.mp4')
    print('v15.25 canary exported: bare compatibility does not force a global response; gravity canary killed.')
if __name__=='__main__':main()
