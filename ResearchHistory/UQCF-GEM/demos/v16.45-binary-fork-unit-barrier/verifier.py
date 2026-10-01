"""Independent fork identities, quotient coverage, endpoints and full path costs."""
import graph_verifier as graph
require=graph.require
DOMAIN=((2,2,2),(2,2,3),(2,3,2),(2,3,3),(3,3,2),(3,3,3))
def canonical(b,c,k,q):
 r,s,t=q[0],q[1],q[c+2];N=b+c+3;S=[set() for _ in range(N)];S[0]=set(range(k))
 left=list(range(s));right=list(range(t)) if r==1 else list(range(s,s+t))
 S[1]=set(left);S[c+2]=set(right)
 for i in range(c):S[i+2]={left[i] if i<s else left[0]}
 for i in range(b):S[c+3+i]={right[i] if i<t else right[0]}
 return tuple(sum(1<<v for v in range(N) if j in S[v]) for j in range(k))
def outcome(nonunit,construction):
 if nonunit:return 'NONUNIT_WITNESS'
 return 'CONSTRUCTION_REFUTED' if construction else 'BINARY_FORK_THEOREM_VALIDATED'
def path_valid(path,x,y,g,q):
 states=g['states']
 if not isinstance(path,list) or not path or path[0]!=x or path[-1]!=y:return False
 if any(type(i)is not int or not 0<=i<len(states) for i in path):return False
 if any(sum(abs(a-b) for a,b in zip(g['attained_profiles'][g['profile_ids'][i]],q))>1 for i in path):return False
 return all(sum((a^b).bit_count() for a,b in zip(states[i],states[j]))==1 for i,j in zip(path,path[1:]))
def verify(doc,domain=DOMAIN):
 require(set(doc)=={'schema','domain','entries'} and doc['schema']==1,'document membership')
 require(doc['domain']==[list(x) for x in domain] and [(e['b'],e['c'],e['k']) for e in doc['entries']]==list(domain),'complete canonical fork domain')
 rows=[];pathfail=[]
 for e,(b,c,k) in zip(doc['entries'],domain):
  require(set(e)=={'b','c','k','graph','normalizations'},'entry membership');g=e['graph']
  codes=sorted(['('+'()'*b+')','('+'()'*c+')'])
  require(g['code']=='('+''.join(codes)+')' and g['parents']==[-1,0]+[1]*c+[0]+[c+2]*b,'canonical binary-fork identity')
  row=graph.verify_graph(g,k)
  identities=[(comp[0],rec['q']) for rec in g['profiles'] for comp in rec['zero_components']]
  require([(rec['state'],rec['q']) for rec in e['normalizations']]==identities,'complete canonical component-representative identities')
  index={tuple(s):i for i,s in enumerate(g['states'])}
  for rec in e['normalizations']:
   require(set(rec)=={'state','q','path'},'normalization membership');i=rec['state'];q=rec['q']
   y=index.get(canonical(b,c,k,q));require(y is not None and g['attained_profiles'][g['profile_ids'][y]]==q,'canonical endpoint admitted and exact')
   if not path_valid(rec['path'],i,y,g,q):pathfail.append({'b':b,'c':c,'k':k,'state':i,'q':q})
  rows.append(dict(row,b=b,c=c,k=k,normalizations=len(identities),sibling_active_pairs=sum(len(rec['pairs']) for rec in g['profiles'] if rec['q'][1]>=2 and rec['q'][c+2]>=2)))
 nonunit=sum(r['nonunit_pairs'] for r in rows)
 return {'status':'VERIFIED','outcome':outcome(nonunit,pathfail),'per_graph':rows,'construction_failures':pathfail,'nonunit_pairs':nonunit,'normalizations':sum(r['normalizations'] for r in rows),'profiles':sum(r['profiles'] for r in rows),'general_claim':'All admitted binary roots with two star children of arbitrary degrees>=2 and k>=2; barriers1 between distinct exact components','universal_unit_barrier':'REFUTED' if nonunit else 'UNRESOLVED','chains_and_higher_degree_roots':'UNRESOLVED'}
