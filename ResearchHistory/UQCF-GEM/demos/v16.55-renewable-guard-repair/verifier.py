"""Independent verifier: frozensets and direct cardinality-ordered enumeration.

No producer model, universe, mechanism, witness counter or hitting routine is imported.
Every cache key is the complete ordered support tuple and palette size.
"""
from collections import Counter
from functools import lru_cache
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import comb
import json
from independent_inputs import reconstruct_cases

def canonical(x):return json.dumps(x,sort_keys=True,separators=(",",":"),allow_nan=False)
def sets(vertex):return tuple(frozenset(row) for row in vertex)

@lru_cache(maxsize=10000)
def minimum_cover(k,vertex):
    roots=tuple(frozenset(row) for row in vertex)
    for size in range(k+1):
        for candidate in combinations(range(k),size):
            chosen=frozenset(candidate)
            if all(chosen&root for root in roots):return candidate
    raise ValueError("empty root has no cover")

def cover(k,vertex):return minimum_cover(k,tuple(tuple(row) for row in vertex))
def legal(k,floors,vertex):
    if not isinstance(vertex,list) or len(vertex)!=len(floors):return False
    return all(isinstance(row,list) and row==sorted(set(row)) and all(type(x) is int and 0<=x<k for x in row) and len(row)>=floor for row,floor in zip(vertex,floors))
def witnesses(k,vertex,indices):
    roots=sets(vertex)
    return all(any(not roots[i].intersection(pair) for i in indices) for pair in combinations(range(k),2))

def conditional(k,source,L,p,D):
    if not set(D)<=set(L) or len(D)!=len(set(D)) or len(D)>p:return None
    ell=len(L);s=len(D);denominator=comb(ell-s,p-s) if 0<=p-s<=ell-s else 0
    if not denominator:return None
    roots=sets(source);remaining=set(L)-set(D);value=Fraction()
    for pair in combinations(range(k),2):
        w=sum(not roots[i].intersection(pair) for i in remaining)
        n=ell-s-w;j=p-s-w
        numerator=comb(n,j) if 0<=j<=n else 0
        value+=Fraction(numerator,denominator)
    return value

def expected_status(case):
    k=case["k"];floors=case["floors"]
    if not legal(k,floors,case["A"]) or not legal(k,floors,case["C"]):return "INVALID_INPUT_FLOOR"
    if len(cover(k,case["A"]))!=4 or len(cover(k,case["C"]))!=4:return "NONEXACT_INPUT"
    method=case.get("parent_method",case["method"])
    if method=="X33":
        total=0
        for h in sorted(set(floors)):
            n=floors.count(h);total+=n*(k-h)//(n//2+1)
        if total>=k:return "SUFFICIENT_BOUND_NOT_MET"
    if method=="X32":
        L=case["L"];F=case["F"];U=case["U"]
        if set(L)&set(F) or set(L)|set(F)!=set(range(len(floors))):return "INVALID_GUARD_INPUT"
        if len({floors[i] for i in L})!=1 or not set(U)<=set(L):return "INVALID_GUARD_INPUT"
        if not witnesses(k,case["A"],L) or not witnesses(k,case["C"],F+U):return "INVALID_GUARD_INPUT"
        if conditional(k,case["A"],L,len(U),[])>=1:return "SUFFICIENT_BOUND_NOT_MET"
    return "PATH"

def verify_universe(expected,actual):
    return [] if Counter(map(canonical,expected))==Counter(map(canonical,actual)) else ["identity set/multiplicity mismatch"]
def verify_provenance(actual,expected):
    return ["provenance mismatch: "+key for key,value in expected.items() if actual.get(key)!=value]
def verify_manifest(files,manifest):
    errors=[]
    if set(files)!=set(manifest):errors.append("manifest inventory mismatch")
    errors += ["digest mismatch: "+p for p,data in files.items() if sha256(data).hexdigest()!=manifest.get(p)]
    return errors
def verify_diagnostics(counts,required):return ["missing category: "+name for name in required if type(counts.get(name)) is not int or counts[name]<=0]

def concatenate(*paths):
    result=[]
    for path in paths:
        if not path:return []
        if result and result[-1]!=path[0]:raise ValueError("false actual metadata join")
        result.extend(path if not result else path[1:])
    return result

def independent_conversion(case,vertices):
    """Separate set-model reconstruction of deterministic maximum-layer removal."""
    current=vertices;layers=[];k=case["k"]
    if len(cover(k,current[0]))!=4 or len(cover(k,current[-1]))!=4:raise ValueError("inexact A entry")
    while True:
        peak=max(len(cover(k,state)) for state in current)
        if peak<=4:return current,layers
        replacements=[]
        for state in current:
            roots=sets(state)
            if len(cover(k,state))==peak:
                x,y=cover(k,state)[:2]
                roots=tuple(root|{x} if y in root else root for root in roots)
            replacements.append(roots)
        result=[[sorted(row) for row in replacements[0]]]
        now=list(replacements[0])
        for target in replacements[1:]:
            for adding in (True,False):
                for i in range(len(now)):
                    changed=sorted(target[i]-now[i] if adding else now[i]-target[i])
                    for x in changed:
                        now[i]=now[i]|{x} if adding else now[i]-{x}
                        result.append([sorted(row) for row in now])
                        if len(result)>1000000:raise ValueError("conversion resource bound")
        after=max(len(cover(k,state)) for state in result)
        if after>=peak:raise ValueError("nondecreasing maximum layer")
        layers.append(dict(before=peak,after=after,vertices_before=len(current),vertices_after=len(result)))
        current=result

def verify_path(case,vertices,lower,upper):
    errors=[];k=case["k"];floors=case["floors"]
    if not vertices:return ["empty path"]
    prior=None
    for n,vertex in enumerate(vertices):
        if not legal(k,floors,vertex):
            errors.append(f"illegal vertex {n}");prior=None;continue
        tau=len(cover(k,vertex))
        if tau<lower or upper is not None and tau>upper:errors.append(f"hitting bound at {n}: {tau}")
        current=sets(vertex)
        if prior is not None and sum(len(a^b) for a,b in zip(prior,current))!=1:errors.append(f"nonprimitive edge {n-1}")
        prior=current
    return errors

def verify_record(case,record):
    try:return _verify_record(case,record)
    except (KeyError,IndexError,TypeError,ValueError,StopIteration) as error:return ["malformed or inconsistent certificate: "+repr(error)]

def _verify_record(case,record):
    errors=[]
    if record.get("identity")!=case["identity"]:errors.append("wrong identity")
    expected=expected_status(case)
    if record.get("status")!=expected:errors.append("wrong status: expected "+expected)
    if expected!="PATH":
        if record.get("preliminary") or record.get("final"):errors.append("refusal carries path")
        return errors
    k=case["k"];floors=case["floors"];r=len(floors)
    preliminary=record.get("preliminary",[]);final=record.get("final",[]);meta=record.get("meta",{})
    errors+=verify_path(case,preliminary,3,None)+verify_path(case,final,3,4)
    for name,path in (("preliminary",preliminary),("final",final)):
        if path and (path[0]!=case["A"] or path[-1]!=case["C"]):errors.append(name+" original endpoint mismatch")
    if "cover" in meta:
        H=meta["cover"]
        if H!=list(cover(k,case["A"])):errors.append("false minimum cover")
    for item in meta.get("covers",[]):
        if item["H"]!=list(cover(k,item["vertex"])):errors.append("false supplied exact cover")
    for event in meta.get("progress",[]):
        if not event["after"]<event["before"]:errors.append("nondecreasing macro progress")
    for vertex in meta.get("upper_entry",[]):
        if not legal(k,floors,vertex) or len(cover(k,vertex))!=4:errors.append("inexact upper/permutation entry")
    if "assignment" in meta:
        assignment=meta["assignment"]
        if sorted(assignment)!=list(range(r)):errors.append("incomplete token assignment")
        elif any(floors[slot]!=floors[token] or len(case["C"][token])<floors[slot] for slot,token in enumerate(assignment)):errors.append("incompatible token assignment")
    for item in meta.get("pair_witnesses",[]):
        vertex=item.get("vertex",case["A"]);i=item["index"];pair=item["pair"]
        if not 0<=i<r or sets(vertex)[i].intersection(pair):errors.append("false pair witness")
    if "placement" in meta:
        placement=meta["placement"];L=placement["L"];p=placement["p"];steps=placement["steps"];old=[];oldphi=conditional(k,case["A"],L,p,[])
        for step in steps:
            D=step["D"];phi=conditional(k,case["A"],L,p,D)
            if phi is None or Fraction(step["phi"])!=phi:errors.append("false conditional count")
            if D:
                if len(D)!=len(old)+1 or D[:-1]!=old or phi is None or oldphi is None or phi>oldphi:errors.append("invalid conditional selection")
                else:
                    eligible=[i for i in L if i not in old and conditional(k,case["A"],L,p,old+[i])<=oldphi]
                    if not eligible or D[-1]!=eligible[0]:errors.append("nonlex conditional move")
            old=D;oldphi=phi
        if len(old)!=p or oldphi!=0:errors.append("unfinished witness placement")
    # Family-specific metadata ties witness/progress certificates to actual paths.
    method=case.get("parent_method",case["method"])
    if method=="X15N":
        errors+=verify_level_cycles(case,preliminary,meta)
        if not all(key in meta for key in ("cover","upper_entry","leveling","cycle_path","cycles","conversion","progress")):errors.append("missing mandatory incidence certificate")
        else:
            expected=concatenate(meta["leveling"]["source"]["vertices"],meta["cycle_path"],list(reversed(meta["leveling"]["destination"]["vertices"])))
            if preliminary!=expected:errors.append("unattached incidence metadata")
            converted,layers=independent_conversion(case,expected)
            if final!=converted or meta["conversion"]!=layers:errors.append("incorrect full-path A reconstruction")
            if meta["upper_entry"]!=[case["A"],case["C"]]:errors.append("missing actual exact incidence entries")
    if method in ("X32","X33"):
        errors+=verify_handover(case,meta)
        mandatory=("cover","upper_entry","assignment","handover","permutation","preparation","conversion")+( ("placement",) if method=="X32" else ("covers",))
        if not all(key in meta for key in mandatory):errors.append("missing mandatory handover certificate")
        else:
            prep=meta["preparation"];middle=meta["handover"]["vertices"];reverseM=list(reversed(meta["permutation"]["vertices"]));reverseC=list(reversed(prep["destination"]))
            expected=concatenate(prep["source"],middle,reverseM,reverseC)
            converted,layers=independent_conversion(case,middle)
            expectedFinal=concatenate(prep["source"],converted,reverseM,reverseC)
            if preliminary!=expected or final!=expectedFinal or meta["conversion"]!=layers:errors.append("unattached handover/A/M reconstruction")
            cert=meta["handover"]
            if meta["upper_entry"]!=[case["A"],case["C"],cert["source"],cert["destination"],cert["placed"]]:errors.append("missing actual exact handover entries")
            if method=="X33" and meta["covers"]!=[dict(vertex=case["A"],H=list(cover(k,case["A"]))),dict(vertex=case["C"],H=list(cover(k,case["C"])) )]:errors.append("missing actual endpoint compaction covers")
    if case["method"]=="NATIVE":
        errors+=verify_nested(case,record.get("nested",{}))
        if record.get("nested")!=independent_lift(case,final):errors.append("native path differs from prescribed parent/clearance lift")
    return errors

def independent_cycle(current,destination):
    edges=sorted((x,y,i) for i,(a,b) in enumerate(zip(current,destination)) for x,y in zip(sorted(a-b),sorted(b-a)))
    def completions(start,tail,used,sequence):
        for edge in edges:
            x,y,i=edge
            if x!=tail:continue
            if y==start:yield sequence+[list(edge)]
            elif y not in used:yield from completions(start,y,used|{y},sequence+[list(edge)])
    for start in sorted({edge[0] for edge in edges}):
        candidate=next(completions(start,start,{start},[]),None)
        if candidate:return candidate
    return None

def verify_level_cycles(case,path,meta):
    errors=[];k=case["k"];r=len(case["floors"])
    for endpoint in ("source","destination"):
        leg=meta.get("leveling",{}).get(endpoint)
        if leg is None:errors.append("missing leveling leg");continue
        errors+=verify_path(case,leg["vertices"],3,None)
        start=case["A"] if endpoint=="source" else case["C"]
        if leg["vertices"][0]!=start:errors.append("wrong leveling origin")
        boundary=0
        for event in leg["events"]:
            a=sets(leg["vertices"][event["start"]]);b=sets(leg["vertices"][event["end"]]);x,y,i=event["x"],event["y"],event["i"]
            da=[sum(v in row for row in a) for v in range(k)];db=[sum(v in row for row in b) for v in range(k)]
            if da[x]<=3 or da[y]>=3 or x not in a[i] or y in a[i] or b[i]!=(a[i]-{x})|{y}:errors.append("ineligible leveling move")
            eligiblex=next((v for v,d in enumerate(da) if d>3),None);eligibley=next((v for v,d in enumerate(da) if d<3),None)
            eligiblei=next((j for j,row in enumerate(a) if x in row and y not in row),None)
            if (x,y,i)!=(eligiblex,eligibley,eligiblei):errors.append("nonlex leveling move")
            if event["start"]!=boundary or event["end"]!=boundary+2:errors.append("incomplete leveling event coverage")
            middle=[sorted(row|{y}) if j==i else sorted(row) for j,row in enumerate(a)]
            if leg["vertices"][event["start"]+1]!=middle:errors.append("wrong leveling primitive order")
            boundary=event["end"]
            if sum(max(d-3,0) for d in db)!=sum(max(d-3,0) for d in da)-1:errors.append("false leveling progress")
            if event["before"]!=sum(max(d-3,0) for d in da) or event["after"]!=sum(max(d-3,0) for d in db):errors.append("fabricated leveling potential")
        if boundary!=len(leg["vertices"])-1:errors.append("unaccounted leveling primitives")
        if any(sum(x in row for row in sets(leg["vertices"][-1]))!=3 for x in range(k)):errors.append("unfinished saturated leveling")
    cyclepath=meta.get("cycle_path",[])
    if not cyclepath:errors.append("missing common degree connection");return errors
    errors+=verify_path(case,cyclepath,3,None)
    boundary=0
    for event in meta.get("cycles",[]):
        start,end=event["start"],event["end"];edges=event["edges"]
        before=sets(cyclepath[start]);after=sets(cyclepath[end]);destination=sets(meta["leveling"]["destination"]["vertices"][-1])
        if edges!=independent_cycle(before,destination):errors.append("nonlex/ unavailable pending cycle")
        if len({edge[0] for edge in edges})!=len(edges) or any(edge[1]!=edges[(i+1)%len(edges)][0] for i,edge in enumerate(edges)):errors.append("invalid cycle")
        if any(x not in before[row] or x in destination[row] or y in before[row] or y not in destination[row] for x,y,row in edges):errors.append("ineligible pending edge")
        pre=sum(len(a-b) for a,b in zip(before,destination));post=sum(len(a-b) for a,b in zip(after,destination))
        if post!=pre-len(edges):errors.append("false cycle progress")
        if event["before"]!=pre or event["after"]!=post:errors.append("fabricated cycle potential")
        if start!=boundary or end!=start+2*len(edges):errors.append("incomplete cycle event coverage")
        current=list(before);expected=[cyclepath[start]]
        for x,y,i in [edges[0]]+list(reversed(edges[1:])):
            current[i]=current[i]|{y};expected.append([sorted(row) for row in current])
            current[i]=current[i]-{x};expected.append([sorted(row) for row in current])
        if cyclepath[start:end+1]!=expected:errors.append("wrong saturated primitive schedule")
        boundary=end
        for vertex in cyclepath[start:end+1]:
            roots=sets(vertex);degrees=[sum(x in row for row in roots) for x in range(k)]
            if max(degrees)>4 or sum(deg==4 for deg in degrees)>1:errors.append("cycle temporary capacity exceeded")
        if any(sum(x in row for row in after)!=3 for x in range(k)) or any(len(row)!=floor for row,floor in zip(after,case["floors"])):errors.append("unrestored cycle boundary")
    if boundary!=len(cyclepath)-1:errors.append("unaccounted cycle primitives")
    if cyclepath[0]!=meta["leveling"]["source"]["vertices"][-1] or cyclepath[-1]!=meta["leveling"]["destination"]["vertices"][-1]:errors.append("wrong degree endpoints")
    return errors

def verify_handover(case,meta):
    errors=[];k=case["k"];floors=case["floors"]
    cert=meta.get("handover")
    if cert is None:return ["missing full handover certificate"]
    A=cert["source"];C=cert["destination"];placed=cert["placed"];J=cert["J"]
    assignment=meta.get("assignment",[])
    if sorted(assignment)==list(range(len(floors))) and placed!=[C[i] for i in assignment]:errors.append("false placed full destination")
    method=case.get("parent_method",case["method"])
    preparation=meta.get("preparation",{})
    for name,original in (("source",case["A"]),("destination",case["C"])):
        leg=preparation.get(name,[])
        errors+=verify_path(case,leg,4,4)
        if not leg or leg[0]!=original or leg[-1]!=cert[name]:errors.append("wrong exact preparation")
        if method=="X33" and leg:
            H=frozenset(cover(k,original))
            expected=[]
            for root,floor in zip(original,floors):
                expected.append(list(next(subset for subset in combinations(root,floor) if H.intersection(subset))))
            if leg[-1]!=expected:errors.append("nonlex cover-retaining compaction")
            sequence=[original];now=list(sets(original))
            for slot,root in enumerate(expected):
                for label in sorted(now[slot]-frozenset(root)):
                    now[slot]=now[slot]-{label};sequence.append([sorted(row) for row in now])
            if leg!=sequence:errors.append("noncanonical exact preparation primitives")
    permutation=meta.get("permutation",{});mvertices=permutation.get("vertices",[])
    errors+=verify_path(case,mvertices,3,4)
    if not mvertices or mvertices[0]!=C or mvertices[-1]!=placed:errors.append("wrong full permutation endpoints")
    for swap in permutation.get("swaps",[]):
        i,j=swap["i"],swap["j"];start,end=swap["start"],swap["end"]
        if floors[i]!=floors[j]:errors.append("cross-grade swap")
        a=mvertices[start];b=mvertices[end]
        if len(cover(k,a))!=4 or len(cover(k,b))!=4:errors.append("inexact completed permutation")
        expected=[row[:] for row in a];expected[i],expected[j]=expected[j],expected[i]
        if expected!=b:errors.append("unrestored permutation token")
    if method=="X33":
        for endpoint in ("source","destination"):
            vertex=cert[endpoint];x=cert[endpoint+"_label"];indices=cert[endpoint+"_guard"]
            eligible=[]
            for label in range(k):
                if all(sum(label not in vertex[i] for i,h0 in enumerate(floors) if h0==h)<=floors.count(h)//2 for h in set(floors)):eligible.append(label)
            if not eligible or x!=eligible[0] or indices!=[i for i,row in enumerate(vertex) if x not in row]:errors.append("false simultaneous grade guard")
            if not witnesses(k,vertex,indices):errors.append("unguarded exact endpoint")
        I=cert["source_guard"];U=cert["destination_guard"]
        if set(I)&set(J) or not witnesses(k,placed,J):errors.append("invalid disjoint handover")
        requiredJ=[]
        for h in sorted(set(floors)):
            slots=[i for i,v in enumerate(floors) if v==h];count=sum(i in U for i in slots)
            requiredJ+= [i for i in slots if i not in I][:count]
        if sorted(J)!=sorted(requiredJ):errors.append("wrong grade placement")
        sourceindices=I;destindices=J
        expected_phases=[(sorted(J),sorted(I)),(sorted(set(range(len(floors)))-set(J)),sorted(J))]
    else:
        L=case["L"];F=case["F"]
        if not witnesses(k,A,sorted(set(L)-set(J))) or not witnesses(k,placed,F+J):errors.append("invalid patch witnesses")
        sourceindices=sorted(set(L)-set(J));destindices=F+J
        expected_phases=[(sorted(F),sorted(L)),(sorted(J),sorted(set(L)-set(J))),(sorted(set(L)-set(J)),sorted(F+J))]
        placement=meta.get("placement")
        if placement is None or placement["L"]!=L or placement["p"]!=len(case["U"]) or sorted(placement["steps"][-1]["D"])!=sorted(J):errors.append("unbound actual patch placement")
    # Reconstruct every token, including tokens outside the guards.
    expectedAssignment=list(range(len(floors)))
    if method=="X33":
        groups=[[i for i,value in enumerate(floors) if value==h] for h in sorted(set(floors))]
        guardTokens=cert["destination_guard"]
    else:groups=[case["L"]];guardTokens=case["U"]
    for group in groups:
        tokens=[i for i in guardTokens if i in group];slots=[i for i in J if i in group]
        for slot,token in zip(slots,tokens):expectedAssignment[slot]=token
        for slot,token in zip([i for i in group if i not in slots],[i for i in group if i not in tokens]):expectedAssignment[slot]=token
    if assignment!=expectedAssignment:errors.append("nonlex/incomplete full token assignment")
    # Full token permutation M, including zero-incidence swaps of equal tokens.
    permutationStates=[C];permutationEvents=[];tokens=list(range(len(floors)));now=list(sets(C))
    for slot,token in enumerate(expectedAssignment):
        if tokens[slot]==token:continue
        other=tokens.index(token);start=len(permutationStates)-1;a,b=now[slot],now[other]
        for i,target in ((slot,a|b),(other,a|b),(slot,b),(other,a)):
            for adding in (True,False):
                changed=sorted(target-now[i] if adding else now[i]-target)
                for x in changed:
                    now[i]=now[i]|{x} if adding else now[i]-{x};permutationStates.append([sorted(row) for row in now])
        tokens[slot],tokens[other]=tokens[other],tokens[slot]
        permutationEvents.append(dict(i=slot,j=other,start=start,end=len(permutationStates)-1))
    if mvertices!=permutationStates or permutation.get("swaps")!=permutationEvents:errors.append("unaccounted/noncanonical saved permutation macros")
    phasepath=cert["vertices"]
    errors+=verify_path(case,phasepath,3,None)
    if phasepath[0]!=A or phasepath[-1]!=placed:errors.append("wrong handover endpoint")
    if [(p["allowed"],p["fixed"]) for p in cert["phases"]]!=expected_phases:errors.append("wrong phase schedule")
    if cert["phases"] and (cert["phases"][0]["start"]!=0 or cert["phases"][-1]["end"]!=len(phasepath)-1 or any(a["end"]!=b["start"] for a,b in zip(cert["phases"],cert["phases"][1:]))):errors.append("incomplete phase coverage")
    for phase in cert["phases"]:
        fixed=phase["fixed"];allowed=phase["allowed"]
        start,end=phase["start"],phase["end"]
        actual=list(sets(phasepath[start]));expected=[phasepath[start]]
        for slot in sorted(allowed):
            desired=frozenset(placed[slot])
            for adding in (True,False):
                changed=sorted(desired-actual[slot] if adding else actual[slot]-desired)
                for label in changed:
                    actual[slot]=actual[slot]|{label} if adding else actual[slot]-{label}
                    expected.append([sorted(row) for row in actual])
        if phasepath[start:end+1]!=expected:errors.append("phase does not supply lexicographic next primitive")
        for n in range(start,end+1):
            vertex=phasepath[n]
            if not witnesses(k,vertex,fixed):errors.append("phase loses actual pair guard")
            if any(vertex[i]!=phasepath[start][i] for i in fixed):errors.append("held guard was edited")
            if n>start:
                old=sets(phasepath[n-1]);new=sets(vertex)
                if any(old[i]!=new[i] for i in range(len(floors)) if i not in allowed):errors.append("phase edits wrong slot")
                if sum(len(a^b) for a,b in zip(new,sets(placed)))!=sum(len(a^b) for a,b in zip(old,sets(placed)))-1:errors.append("no next primitive progress")
        # Explicit first actual witness for every pair at every phase vertex.
        supplied=phase["pair_witnesses"]
        if len(supplied)!=end-start+1:errors.append("incomplete phase witness vertices");continue
        for n,indices in zip(range(start,end+1),supplied):
            roots=sets(phasepath[n]);pairs=list(combinations(range(k),2))
            expected=[next((i for i in sorted(fixed) if not roots[i].intersection(pair)),None) for pair in pairs]
            if indices!=expected or None in expected:errors.append("false/incomplete phase witnesses")
    return errors

def verify_nested(case,record):
    vertices=record.get("vertices",[]);errors=[]
    if not vertices:return ["missing native vertices"]
    initial=[[ [x] for x in row[:floor]] for row,floor in zip(case["A"],case["floors"])]
    if vertices[0].get("parent")!=case["A"] or vertices[0].get("leaves")!=initial:errors.append("wrong initial tree")
    if vertices[-1].get("parent")!=case["C"]:errors.append("wrong final parent")
    previous=None
    for n,vertex in enumerate(vertices):
        parent=vertex["parent"];leaves=vertex["leaves"]
        if not legal(case["k"],case["floors"],parent) or len(leaves)!=len(parent):errors.append("illegal nested carrier");continue
        flat=sets(parent);defect=abs(len(cover(case["k"],parent))-case.get("target",4));allsets=list(flat)
        for i,children in enumerate(leaves):
            if len(children)!=case["floors"][i] or not legal(case["k"],[1]*len(children),children):errors.append("illegal child")
            if any(not frozenset(child)<=flat[i] for child in children):errors.append("nesting violation")
            defect+=abs(len(cover(case["k"],children))-case["floors"][i]);allsets.extend(sets(children))
        if defect>1:errors.append("second global defect unit")
        if previous is not None and sum(len(a^b) for a,b in zip(previous,allsets))!=1:errors.append("nonprimitive nested edge")
        previous=allsets
    return errors

def independent_lift(case,parent_path):
    current=sets(case["A"]);children=[[frozenset((x,)) for x in root[:floor]] for root,floor in zip(case["A"],case["floors"])]
    vertices=[];clearances=[]
    def save():vertices.append(dict(parent=[sorted(row) for row in current],leaves=[[sorted(leaf) for leaf in group] for group in children]))
    save()
    for target in parent_path[1:]:
        target=sets(target)
        edits=[(i,x) for i,(a,b) in enumerate(zip(current,target)) for x in sorted(a^b)]
        if len(edits)!=1:raise ValueError("invalid parent projection")
        i,x=edits[0]
        if x not in target[i]:
            union=frozenset().union(*children[i])
            if x in union:
                y=min(current[i]-union);j=next(j for j,leaf in enumerate(children[i]) if x in leaf);start=len(vertices)-1
                children[i][j]=children[i][j]|{y};save();children[i][j]=children[i][j]-{x};save()
                clearances.append(dict(root=i,child=j,x=x,y=y,start=start,end=len(vertices)-1))
        current=target;save()
    return dict(vertices=vertices,clearances=clearances)

def smoke_cases():
    wanted=[("R1",{"d":1},{"a":1,"b":1,"v":1}), ("R2",{},{"a":1,"b":1,"v":1}), ("R3",{"m":4,"d":15},{"a":1,"v":1,"bL":1,"bF":1})]
    for case in reconstruct_cases():
        ident=case["identity"]
        if ident[0]=="R4" or ident[0]=="R5" or ident[3]=="NONE" and any(ident[:3]==list(x) for x in wanted):yield case
