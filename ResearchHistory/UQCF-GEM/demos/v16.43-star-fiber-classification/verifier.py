"""Independent star domain, canonical endpoints and normalization path costs."""
from math import factorial
import graph_verifier as graph
require=graph.require
DOMAIN=((2,2),(2,3),(2,4),(3,2),(3,3),(3,4),(4,2),(4,3),(4,4),(5,2),(5,3))
def canonical(m,k,q):
 out=[1]*k
 for i in range(m):out[i if i<q else 0]|=1<<(i+1)
 return tuple(out)
def outcome(nonunit,classification,construction):
 if nonunit:return 'NONUNIT_WITNESS'
 if classification:return 'CLASSIFICATION_REFUTED'
 return 'CONSTRUCTION_REFUTED' if construction else 'STAR_CLASSIFICATION_VALIDATED'
def path_valid(path,x,y,g,q,bound):
 states=g['states']
 if not isinstance(path,list) or not path or path[0]!=x or path[-1]!=y:return False
 if any(type(i)is not int or not 0<=i<len(states) for i in path):return False
 if any(abs(g['attained_profiles'][g['profile_ids'][i]][0]-q)>bound for i in path):return False
 return all(sum((a^b).bit_count() for a,b in zip(states[i],states[j]))==1 for i,j in zip(path,path[1:]))
def verify(doc,domain=DOMAIN):
 require(set(doc)=={'schema','domain','entries'} and doc['schema']==1,'document membership')
 require(doc['domain']==[list(x) for x in domain] and [(e['m'],e['k']) for e in doc['entries']]==list(domain),'complete canonical star domain')
 rows=[];classfail=[];pathfail=[]
 for e,(m,k) in zip(doc['entries'],domain):
  require(set(e)=={'m','k','graph','normalizations'},'entry membership');g=e['graph']
  require(g['parents']==[-1]+[0]*m and g['code']=='('+'()'*m+')','star identity')
  row=graph.verify_graph(g,k)
  require(g['attained_profiles']==[[q]+[0]*m for q in range(1,min(m,k)+1)],'complete feasible q identities')
  for rec in g['profiles']:
   q=rec['q'][0];packed=m==k==q;want=factorial(m) if packed else 1
   if len(rec['zero_components'])!=want or (packed and any(len(c)!=1 for c in rec['zero_components'])):classfail.append({'m':m,'k':k,'q':q})
  states=g['states'];index={tuple(s):i for i,s in enumerate(states)}
  require([r['state'] for r in e['normalizations']]==list(range(len(states))),'complete normalization identities')
  for r in e['normalizations']:
   require(set(r)=={'state','q','path'},'normalization membership');i=r['state'];q=g['attained_profiles'][g['profile_ids'][i]][0]
   require(r['q']==q,'normalization target profile');y=index.get(canonical(m,k,q));require(y is not None,'canonical endpoint admitted')
   if not path_valid(r['path'],i,y,g,q,int(m==k==q)):pathfail.append({'m':m,'k':k,'state':i,'q':q})
  rows.append(dict(row,m=m,k=k,normalizations=len(states)))
 nonunit=sum(r['nonunit_pairs'] for r in rows)
 return {'status':'VERIFIED','outcome':outcome(nonunit,classfail,pathfail),'per_graph':rows,'classification_failures':classfail,'construction_failures':pathfail,'nonunit_pairs':nonunit,'normalizations':sum(r['normalizations'] for r in rows),'profiles':sum(r['profiles'] for r in rows),'general_claim':'All rooted stars with m,k>=2; one exact component except m=k=q','universal_unit_barrier':'REFUTED' if nonunit else 'UNRESOLVED','nested_interactions':'UNRESOLVED'}
