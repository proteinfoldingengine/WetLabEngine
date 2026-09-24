"""Stage C2 exact representation-family controls."""
def factorizations(n,min_factor=2):
 out=[]
 def rec(rem,start,prefix):
  out.append(tuple(prefix+[rem]))
  for f in range(start,int(rem**0.5)+1):
   if rem%f==0 and f>=min_factor:
    rec(rem//f,f,prefix+[f])
 rec(n,min_factor,[])
 return tuple(sorted(set(out),key=lambda x:(len(x),x)))
def neutral_factorization_selector(d):
 return None
def node_site_dictionary(node_count,site_count,cross_domain_relations):
 if node_count!=site_count or not cross_domain_relations:return None
 return tuple(range(node_count))
def same_carrier_type(a,b):
 return int(a)==int(b)
