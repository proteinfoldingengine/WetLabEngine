"""Recover terminal assignments independently from holders, and check the exact archived rows."""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import gzip
import json
import lzma
from pathlib import Path
import sys

C = range(4)
LEAVES = range(1,5)
ARCHIVE = Path("ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/evidence/science/scientific/CERTIFICATE.json.gz")


def check(value, error):
    if not value:
        raise ValueError(error)


def reject(function, error):
    try:
        function()
    except ValueError as e:
        check(str(e)==error, "wrong rejecting control")
    else:
        raise ValueError("accepted defect: "+error)


def pack(row):
    n=0
    for mask in reversed(row):
        n=32*n+mask
    return n


def masks(n):
    out=[]
    for _ in C:
        n,m=divmod(n,32)
        out.append(m)
    check(n==0,"state domain")
    return out


@lru_cache(maxsize=None)
def assignment_sets(key):
    state=masks(key)
    holders=[tuple(j for j in C if state[j] & (1<<v)) for v in LEAVES]
    check(all(holders),"uncovered leaf")
    teams=[set(t) for n in range(1,5) for t in combinations(C,n)
           if all(set(t).intersection(col) for col in holders)]
    q=min(map(len,teams))
    bare,fixed=set(),set()
    for assignment in product(*holders):
        row=[1]*4
        for v,j in zip(LEAVES,assignment):
            row[j]+=1<<v
        result=pack(row)
        bare.add(result)
        if len(set(assignment))==q:
            fixed.add(result)
    return [q, sorted(fixed), sorted(bare)], [t for t in teams if len(t)==q]


def check_rows(loaded, expected):
    check(len(loaded)==len(expected),"preparation count")
    actual={tuple(row[0]):row[1:] for row in loaded}
    check(len(actual)==len(loaded),"duplicate preparation")
    check(actual==expected,"preparation identity")


def check_terminal(given, expected):
    check(given==expected,"false terminal family")


def local_status(teams, j):
    return {j in h for h in teams}


def main(source, directory):
    raw=lzma.decompress((directory/"cover_member_universe.json.xz").read_bytes())
    doc=json.loads(raw)
    cert=json.loads((directory/"cover_member_certificate.json").read_bytes())
    check(cert["universe_sha256"]==sha256(raw).hexdigest(),"universe digest")
    cases,ends,pairs={}, {}, []
    exchange_words=set()
    by_height=Counter()
    for a,c,d in product(range(16), repeat=3):
        if a|c|d != 15:
            continue
        state=[1,1+2*a,1+2*c,1+2*d]
        cols=tuple(sum(1<<j for j,m in enumerate(state) if m&(1<<v)) for v in LEAVES)
        precover,_=assignment_sets(pack(state))
        arms=[]
        for leaf in LEAVES:
            bit=1<<(leaf-1)
            if c & bit and (a|d) & bit:
                post=state.copy()
                post[2]-=2*bit
                key=pack(post)
                arms.append([leaf,key])
                ends[str(key)]=assignment_sets(key)[0]
        cases[cols]=[precover[0],arms]
        for (x,k),(y,l) in combinations(arms,2):
            X,H=assignment_sets(k)
            Y,K=assignment_sets(l)
            forced=[j for j in (0,1,3) if local_status(H,j).isdisjoint(local_status(K,j))]
            check(set(X[2]) & set(Y[2]),"bare diamond")
            pairs.append([list(cols),x,y,forced,[]])
            if forced and X[0]==Y[0]:
                exchange_words.add((cols,x,y))
                by_height[precover[0]]+=1
            # Independent of the particular keeper assigned to a shared leaf.
            for families,teams in ((X,H),(Y,K)):
                check(all({masks(z)[j]!=1 for z in families[1]}==local_status(teams,j) for j in C),
                      "cover-member equivalence")
    check_rows(doc["preparations"],cases)
    check_terminal(doc["post_states"],ends)
    check(sorted(pairs)==doc["pairs"],"pair or receiver identity")
    # Reconstruct the same-height class directly by its mandatory and optional columns.
    predicted=set()
    for extra in (4,6,12,10,14):
        for word in set(permutations((4,6,12,extra))):
            for u in LEAVES:
                for v in range(u+1,5):
                    if {word[u-1],word[v-1]}=={6,12}:
                        predicted.add((word,u,v))
    check(predicted==exchange_words and by_height=={1:84,2:24},"analytic exchange words")

    archive=(source/ARCHIVE).read_bytes()
    check(sha256(archive).hexdigest()==cert["archive_sha256"],"archive identity")
    entry,=(e for e in json.loads(gzip.decompress(archive))["entries"] if (e["m"],e["k"])==(4,4))
    states=entry["graph"]["states"]
    canon={q:pack([1+sum(1<<v for v in LEAVES if (v-1 if v<=q else 0)==i) for i in C])
           for q in (1,2,3)}
    for key,rec in doc["archived_paths"].items():
        start=int(key)
        idx=rec["archive_row"]
        imported=entry["normalizations"][idx]
        check(pack(states[idx])==start and imported["state"]==idx and imported["q"]==rec["q"],
              "archived start")
        seq=[pack(states[i]) for i in imported["path"]]
        check(seq==rec["path"] and seq[-1]==canon[rec["q"]],"archived trajectory")
        prefix=next(i for i,z in enumerate(seq) if z in assignment_sets(start)[0][2])
        check(rec["first_singleton"]==prefix and seq[prefix] in assignment_sets(start)[0][1],
              "cleanup boundary")

    all_ids=set(product(permutations(C),permutations(LEAVES)))
    seen=set()
    requested=set()
    for cm,lm,strict,other in doc["permutations"]:
        marker=tuple(cm),tuple(lm)
        check(marker not in seen,"duplicate permutation")
        seen.add(marker)
        for v,k,expected_nonempty in ((1,strict,False),(2,other,True)):
            # Transform original rows by the inverse label map and the directly transported leaves.
            leaves=((),(1,),tuple(LEAVES),(2,3))
            state=[1+sum(1<<lm[n-1] for n in leaves[cm.index(j)]
                         if not (j==cm[2] and n==v)) for j in C]
            check(pack(state)==k,"permuted event")
            requested.add(str(k))
            rec=doc["archived_paths"][str(k)]
            terminal=masks(rec["path"][rec["first_singleton"]])
            check((terminal[cm[3]]!=1)==expected_nonempty,"transported receiver")
    check(seen==all_ids and requested==set(doc["archived_paths"]),"archive coverage")

    for arm in cert["witness"]:
        vals,covers=assignment_sets(pack(arm["post"]))
        wanted = [1,2] if arm["cut"]==1 else [2,3]
        check(covers==[set(wanted)] and arm["star_record"]["keeper_cover"]==wanted,"chosen cover")
        check(arm["source_height"]==[1,2] and arm["source_delta"]==1 and arm["trigger"],"source scalar")
        rec=doc["archived_paths"][str(pack(arm["post"]))]
        clean=masks(rec["path"][rec["first_singleton"]])
        check(arm["receiver_cleanup"]==clean[3] and clean==arm["star_record"]["cleanup_state"],"receiver owner")
        check(arm["star_record"]["path"]==rec["path"] and arm["receiver_star_final"]==masks(rec["path"][-1])[3],
              "named archive")
        root=lambda mask: 6-mask.bit_count()
        expected=[root(cert["prior"][2]), root(arm["post"][2]), root(cert["prior"][3]), root(clean[3])]
        check(arm["unit_roots_source_before_after_receiver_before_cleanup"]==expected,"root grade")
        for j,b,leaves,t in arm["star_record"]["donor_reads"]:
            row=masks(rec["path"][t])
            check(leaves==[v for v in LEAVES if row[j]&(1<<v)],"donor data")
            for i,v in enumerate(leaves):
                after=masks(rec["path"][t+i+1])
                before=masks(rec["path"][t+i])
                check(after[b]^before[b]==1<<v and after[b]>before[b],"donor copy")
    routes=cert["same_endpoint_routes"]
    check(set(routes)=={"v16.39","v16.53","direct"},"route identity")
    for name,rec in routes.items():
        seq=rec["path"]
        check(seq[0]==[1,19,13,9] and seq[-1]==[15,17,1,1],"same named endpoints")
        costs=[]
        for state in seq:
            ns=[sum(int(bool(mask&(1<<v))) for mask in state) for v in LEAVES]
            costs.append(sum(n*(4-n) for n in ns))
        check(rec["minimum_work"]==min(costs)
              and rec["covers"]==[assignment_sets(pack(row))[0][0] for row in seq],"route geometry")
        check(all(sum((x^y).bit_count() for x,y in zip(a,b))==1 for a,b in zip(seq,seq[1:])),
              "route primitive")
        check(rec["charts_ever_full"]==[any(s[j]==31 for s in seq) for j in C],"route chart history")

    end=pack(cert["bare_common_terminal"])
    for i,path in enumerate(cert["bare_control_paths"]):
        check(path[0]==pack(cert["witness"][i]["post"]) and path[1]==pack(cert["bare_join"])
              and path[-1]==end,"erasing continuation")
        for u,v in zip(path,path[1:]):
            before,after=masks(u),masks(v)
            check(all(b&a==a for b,a in zip(before,after)) and
                  sum((b^a).bit_count() for b,a in zip(before,after))==1,"bare deletion")
            assignment_sets(v)
        check(assignment_sets(end)[0][2]==[end],"absorbing state")
    same_q=sum(1 for cols,x,y,_,_ in pairs
               if ends[str(dict(cases[tuple(cols)][1])[x])][0]==ends[str(dict(cases[tuple(cols)][1])[y])][0])
    n=sum(bool(p[3]) for p in pairs)
    stats=dict(preparations=len(cases),arms=sum(len(row[1]) for row in cases.values()),pairs=len(pairs),
               equal_cover_pairs=same_q,pairs_separating_empty_nonempty=n,
               equal_cover_separating=len(predicted),different_cover_separating=n-len(predicted),
               pair_receiver_incidences=sum(len(p[3]) for p in pairs),bare_forced_pair_receivers=0,
               distinct_base_poststates=len(ends),relabelings=len(seen),archival_poststates=len(requested))
    check(stats==cert["counts"],"reported counts")
    rows=doc["preparations"]
    reject(lambda:check_rows(rows[:-1],cases),"preparation count")
    reject(lambda:check_rows(rows[:-1]+rows[:1],cases),"duplicate preparation")
    reject(lambda:check_rows([[[-1]*4,*rows[0][1:]],*rows[1:]],cases),"preparation identity")
    reject(lambda:assignment_sets(pack([1,3,3,3])),"uncovered leaf")
    false=dict(ends)
    false[str(pack(cert["witness"][0]["post"]))]=[2,[end],[end]]
    reject(lambda:check_terminal(false,ends),"false terminal family")
    reject(lambda:check(cert["witness"][1]["receiver_cleanup"]==cert["witness"][1]["star_record"]["cleanup_state"][0],
                        "incorrect receiver"),"incorrect receiver")
    print(json.dumps(dict(**stats, equal_height_rising=by_height[1],equal_height_flat=by_height[2],
                          controls="passed"),sort_keys=True))


if __name__=="__main__":
    main(Path(sys.argv[1]),Path(sys.argv[2]))
