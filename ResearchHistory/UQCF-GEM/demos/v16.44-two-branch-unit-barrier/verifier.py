"""Independent two-branch identities, quotient coverage and path certificates."""
import graph_verifier as graph
require=graph.require
DOMAIN=((2,2,2),(2,2,3),(2,2,4),(2,3,2),(2,3,3),(2,3,4),(3,2,2),(3,2,3),(3,2,4),(3,3,2),(3,3,3),(3,3,4))
def canonical(a,b,k,r,s):
 n=a+b+1;supports=[set(range(k))]+[set() for _ in range(n-1)]
 palette=list(range(s)) if r<a else list(range(a-1,a-1+s))
 supports[1]=set(palette)
 for j in range(b):supports[2+j]={palette[j] if j<s else palette[0]}
 sideq=r if r<a else a-1
 for j in range(a-1):supports[b+2+j]={j if j<sideq else 0}
 return tuple(sum(1<<v for v in range(n) if j in supports[v]) for j in range(k))
def outcome(nonunit,construction):
 if nonunit:return 'NONUNIT_WITNESS'
 return 'CONSTRUCTION_REFUTED' if construction else 'TWO_BRANCH_THEOREM_VALIDATED'
def path_valid(path,x,y,g,q):
 states=g['states']
 if not isinstance(path,list) or not path or path[0]!=x or path[-1]!=y:return False
 if any(type(i)is not int or not 0<=i<len(states) for i in path):return False
 if any(sum(abs(a-b) for a,b in zip(g['attained_profiles'][g['profile_ids'][i]],q))>1 for i in path):return False
 return all(sum((a^b).bit_count() for a,b in zip(states[i],states[j]))==1 for i,j in zip(path,path[1:]))
def verify(doc,domain=DOMAIN):
 require(set(doc)=={'schema','domain','entries'} and doc['schema']==1,'document membership')
 require(doc['domain']==[list(x) for x in domain] and [(e['a'],e['b'],e['k']) for e in doc['entries']]==list(domain),'complete canonical two-branch domain')
 rows=[];pathfail=[]
 for e,(a,b,k) in zip(doc['entries'],domain):
  require(set(e)=={'a','b','k','graph','normalizations'},'entry membership');g=e['graph']
  require(g['parents']==[-1,0]+[1]*b+[0]*(a-1) and g['code']=='(('+('()'*b)+')'+('()'*(a-1))+')','two-branch identity')
  row=graph.verify_graph(g,k)
  identities=[(c[0],r['q']) for r in g['profiles'] for c in r['zero_components']]
  require([(r['state'],r['q']) for r in e['normalizations']]==identities,'complete canonical component-representative identities')
  index={tuple(s):i for i,s in enumerate(g['states'])}
  for rec in e['normalizations']:
   require(set(rec)=={'state','q','path'},'normalization membership');i=rec['state'];q=rec['q']
   y=index.get(canonical(a,b,k,q[0],q[1]));require(y is not None and g['attained_profiles'][g['profile_ids'][y]]==q,'canonical endpoint admitted and exact')
   if not path_valid(rec['path'],i,y,g,q):pathfail.append({'a':a,'b':b,'k':k,'state':i,'q':q})
  rows.append(dict(row,a=a,b=b,k=k,normalizations=len(identities)))
 nonunit=sum(r['nonunit_pairs'] for r in rows)
 return {'status':'VERIFIED','outcome':outcome(nonunit,pathfail),'per_graph':rows,'construction_failures':pathfail,'nonunit_pairs':nonunit,'normalizations':sum(r['normalizations'] for r in rows),'profiles':sum(r['profiles'] for r in rows),'general_claim':'All admitted no-unary rooted trees with exactly two internal vertices and k>=2; barriers1 between distinct exact components','universal_unit_barrier':'REFUTED' if nonunit else 'UNRESOLVED','three_or_more_internal_vertices':'UNRESOLVED'}
