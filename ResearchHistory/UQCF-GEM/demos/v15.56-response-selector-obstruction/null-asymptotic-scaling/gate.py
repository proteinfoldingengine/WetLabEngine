"""v15.65 asymptotic scaling of v15.64 finite mixed-rotation residual."""
import importlib.util,json,pathlib,numpy as np
HERE=pathlib.Path(__file__).resolve().parent;PARENT=HERE.parent
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
V64=load(PARENT/'source-vector-field-null'/'gate.py','v64scale')
TS=[1e-3,5e-4,2.5e-4,1.25e-4,6.25e-5]
def mixed_norm(rho,Y,t):
 ro={};mineig=1.
 for ie in (-1,1):
  sig=rho+ie*V64.ETA*V64.HIDDEN
  for jt in (-1,1):
   z=V64.T(sig,rho,Y,jt*t);mineig=min(mineig,float(np.linalg.eigvalsh(z).min()));ro[(ie,jt)]=V64.rotations(z)
 M=(ro[(1,1)]-ro[(1,-1)]-ro[(-1,1)]+ro[(-1,-1)])/(4*V64.ETA*t)
 return float(np.linalg.norm(M)),mineig
def fit(ts,ys):
 x=np.log(np.asarray(ts));y=np.log(np.asarray(ys));p=np.polyfit(x,y,1);pred=np.polyval(p,x)
 ssr=np.sum((y-pred)**2);sst=np.sum((y-y.mean())**2);return float(p[0]),float(1-ssr/sst if sst else 1.)
def run_measurement():
 states=V64.ASYM.select_states();rows=[];allok=True
 for row in states:
  rho=row['rho'];Y,lift=V64.target_Y(rho);norms=[];mineig=1.
  for t in TS:
   n,m=mixed_norm(rho,Y,t);norms.append(n);mineig=min(mineig,m)
  slope,r2=fit(TS,norms);adj=[float(np.log(norms[i+1]/norms[i])/np.log(TS[i+1]/TS[i])) for i in range(4)]
  ratio=float(norms[-1]/norms[0]);ok=1.7<=slope<=2.3 and ratio<.01 and mineig>=-1e-12 and lift<=1e-10
  allok&=ok;rows.append({'candidate_index':row['candidate_index'],'norms':norms,'slope':slope,'r2':r2,'adjacent_slopes':adj,'small_to_large_ratio':ratio,'min_finite_eigenvalue':mineig,'pass':bool(ok)})
 verdict='NULL_DERIVATIVE_ASYMPTOTICS_CONFIRMED' if allok else 'NULL_DERIVATIVE_ASYMPTOTICS_NOT_CONFIRMED'
 return {'verdict':verdict,'amplitudes':TS,'rows':rows}
if __name__=='__main__':
 r=run_measurement();print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(0)
