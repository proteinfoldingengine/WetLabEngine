#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,pathlib
from functools import lru_cache
import numpy as np
import target_origin as m
ROOT=pathlib.Path(__file__).resolve().parent
STORY=('FACTOR_NO_GO','MICRO_FAIL','HODGE_CONDITIONAL','ZERO_EXTRA','TOPOLOGY_FAMILY','FINAL_STOP')

@lru_cache(None)
def payload():
    a=m.audit();c=m.base.base.torus_complex(7);q,_=m.base.base.incidence_defect(c,(0,0),'bottom',1.0);R=m.base.response_operator(c)
    family=[]
    for alpha in (-1.,0.,1.):
        j=m.topological_current(c,q,alpha);t=m.topological_target(c,q,alpha)
        family.append({'alpha':alpha,'current':j.tolist(),'target_norm':float(np.linalg.norm(t)),'current_norm':float(np.linalg.norm(j)),'source_error':float(np.linalg.norm(c.B1@j+q))})
    candidates=[
      {'key':'FACTOR_NO_GO','name':'Inherit Rj from q','status':'NO-GO','detail':'R is nonzero on all 50 cycle directions, so Rj does not factor through q=B1j.'},
      {'key':'MICRO_FAIL','name':'Microscopic defect inheritance','status':'FAILS QUOTIENT','detail':'Adding a closed face leaves q unchanged but moves the inherited target by 4.4721.'},
      {'key':'HODGE_CONDITIONAL','name':'Hodge / minimum action','status':'CONDITIONAL','detail':'It selects a section only after an edge inner product is supplied.'},
      {'key':'ZERO_EXTRA','name':'Zero target','status':'EXTRA CONDITION','detail':'Mathematically lawful, but not implied by compatibility or topology.'},
      {'key':'TOPOLOGY_FAMILY','name':'Topology + covariance','status':'NONUNIQUE','detail':'A q-only, linear, relabeling-covariant one-parameter family survives.'},
    ]
    return {'version':'v15.27','audit':a,'candidates':candidates,'topology_family':family,'views':{x:True for x in STORY},'notice':'Origin audit only. No candidate is selected using holonomy, gravity fitting, pruning, entropy or physical time.'}

def write_html(data,path):
    path.parent.mkdir(parents=True,exist_ok=True);s=json.dumps(data,separators=(',',':'),allow_nan=False).replace('<','\\u003c');path.write_text((ROOT/'viewer.html').read_text().replace('__DATA__',s),encoding='utf-8')

def movie(path,fps=10):
    if type(fps) is not int or fps<=0:raise ValueError('positive fps required')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter,writers
    if not writers.is_available('ffmpeg'):raise RuntimeError('FFmpeg required')
    d=payload();fam={x['alpha']:x for x in d['topology_family']};fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    ax=fig.add_axes([.07,.31,.53,.40]);x=np.arange(98);line,=ax.plot(x,np.zeros(98),linewidth=1.5);ax.axhline(0,linewidth=.8);ax.set_xlim(0,97);ax.set_ylim(-1.2,1.2);ax.set_xlabel('edge label — display only');ax.set_ylabel('current coefficient')
    fig.text(.05,.95,'UQCF–GEM / v15.27 / PRE-TIME CYCLE-TARGET ORIGIN AUDIT',fontsize=10,weight='bold');fig.text(.05,.875,'The target law is not in the frozen ontology.',fontsize=25,weight='bold');title=fig.text(.64,.70,'',fontsize=17,weight='bold',va='top');detail=fig.text(.64,.60,'',fontsize=12,linespacing=1.65,va='top')
    fig.text(.05,.19,'R does not factor through q · microscopic inheritance is not quotient-covariant · covariance leaves a family',fontsize=11);fig.text(.05,.13,'No gravity signal certified. The next step requires an explicit new pre-time coupling law or newly derived structure.',fontsize=10);fig.text(.05,.08,'No minimum norm · no holonomy optimization · no Newton/GR fit',fontsize=10);fig.text(.05,.035,'No physical time · no pruning · no entropy · no actual outcome',fontsize=10)
    notes={
      'FACTOR_NO_GO':('FACTOR THROUGH q: IMPOSSIBLE','Same q can differ by any cycle z.\nRz is nonzero on 50 cycle directions.'),
      'MICRO_FAIL':('MICROSCOPIC INHERITANCE FAILS','Closed-face changes of the microscopic representative\nleave q fixed but change the target.'),
      'HODGE_CONDITIONAL':('HODGE IS CONDITIONAL','Changing the positive edge inner product\nchanges both current and response target.'),
      'ZERO_EXTRA':('ZERO IS AN EXTRA CONDITION','A valid section, but topology does not demand it.'),
      'TOPOLOGY_FAMILY':('COVARIANCE LEAVES FREEDOM','alpha = -1, 0, +1 are all source-linear,\nq-only and relabeling-covariant.'),
      'FINAL_STOP':('FROZEN ONTOLOGY: STOP','No audited candidate derives a unique target.\nA new independently motivated pre-time coupling is required.')}
    def draw(key):
        if key=='TOPOLOGY_FAMILY':r=fam[1.0]
        elif key=='ZERO_EXTRA':r=fam[0.0]
        elif key=='FINAL_STOP':r=fam[-1.0]
        else:r=fam[0.0]
        line.set_ydata(r['current']);title.set_text(notes[key][0]);detail.set_text(notes[key][1]+f"\n\nCurrent norm: {r['current_norm']:.6f}\nTarget norm: {r['target_norm']:.6f}")
    path.parent.mkdir(parents=True,exist_ok=True);draw('FINAL_STOP');fig.savefig(path.with_suffix('.png'),dpi=120)
    writer=FFMpegWriter(fps=fps,codec='libx264',bitrate=1800,extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    with writer.saving(fig,str(path),dpi=100):
        for key in STORY:
            draw(key)
            for _ in range(4*fps):writer.grab_frame()
    plt.close(fig)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=pathlib.Path,default=ROOT/'outputs');p.add_argument('--video',action='store_true');a=p.parse_args();d=payload();a.out.mkdir(parents=True,exist_ok=True);write_html(d,a.out/'target_origin.html');(a.out/'replay_data.json').write_text(json.dumps(d,separators=(',',':'),allow_nan=False)+'\n');(a.out/'verification.json').write_text(json.dumps(d['audit'],indent=2,allow_nan=False)+'\n');
    if a.video:movie(a.out/'target_origin.mp4')
    print('Five origin candidates audited. No gravity signal certified.')
if __name__=='__main__':main()
