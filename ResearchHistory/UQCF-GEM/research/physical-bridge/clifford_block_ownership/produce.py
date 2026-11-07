"""Exact phase/word producer; no matrix checker imports."""
import hashlib,itertools,json
from pathlib import Path
BASE=Path(__file__).resolve().parent
G=['XIII','YIII','ZXII','ZYII','ZZXI','ZZYI','ZZZX','ZZZY','ZZZZ']
CYCLE={('X','Y'):'Z',('Y','Z'):'X',('Z','X'):'Y'}
def mul(a,b):
 p=(a[0]+b[0])%4; w=''
 for x,y in zip(a[1],b[1]):
  if x=='I': w+=y
  elif y=='I': w+=x
  elif x==y: w+='I'
  elif (x,y) in CYCLE: p=(p+1)%4;w+=CYCLE[x,y]
  else: p=(p+3)%4;w+=CYCLE[y,x]
 return p,w
def product(xs):
 r=(0,'IIII')
 for x in xs:r=mul(r,x)
 return r
g=[(0,w) for w in G];local=[];omega=[]
for v in range(3):
 a,b,c=g[3*v:3*v+3]
 local.append([(0,'IIII')]+[mul((3,'IIII'),mul(x,y)) for x,y in ((b,c),(c,a),(a,b))])
 omega.append(mul((3,'IIII'),product((a,b,c))))
records=[]
def add(key,value):records.append(dict(id=key,phase=value[0],word=value[1]))
for i,x in enumerate(g):add(f'G/{i}',x)
for v in range(3):
 for k in range(1,4):add(f'L/{v}/{k}',local[v][k])
 add(f'O/{v}',omega[v])
for a,b,c in itertools.product(range(4),repeat=3):add(f'B/{a}/{b}/{c}',product((local[0][a],local[1][b],local[2][c])))
records.sort(key=lambda x:x['id'])
result=dict(schema=1,source_sha256=hashlib.sha256((BASE/'SOURCE_ARGUMENT.md').read_bytes()).hexdigest(),count=len(records),records=records)
print(json.dumps(result,indent=2,sort_keys=True))
