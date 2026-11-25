"""Generate the receiver languages from tip ownership and linear extensions without calling the atom."""
from collections import defaultdict
from itertools import product
from pathlib import Path
import sys
from free_receiver_io import read_xz, require, save


def words_from_endpoints(p, masks, group):
    n, k = len(p),len(masks)
    visible = tuple(j for j in range(k) if group & (1 << j))
    local = {j:{v for v in range(n) if masks[j] & (1<<v)} for j in visible}
    tips = [v for v in range(1,n) if v not in p]
    choices = []
    for v in tips:
        choices.append([j for j in visible if v in local[j]] +
                       ([-1] if any(j not in local and mask & (1<<v) for j,mask in enumerate(masks)) else []))
    output = set()
    for owners in product(*choices):
        target = {j:{0} for j in visible}
        for tip,j in zip(tips,owners):
            if j < 0:
                continue
            v = tip
            while v != -1:
                target[j].add(v)
                v = p[v]
        pending = {(j,v) for j in visible for v in local[j] - target[j]}
        def extend(todo, prefix):
            if not todo:
                output.add(prefix)
            for j,v in todo:
                if all(label != j or p[child] != v for label,child in todo):
                    extend(todo-{(j,v)}, prefix+chr(65+n*j+v))
        extend(pending,"")
    return output


def indexed_covers(p,k):
    # Assign holders to vertices, only from the holders of their parent.
    def visit(supports):
        if len(supports)==len(p):
            yield tuple(sum(1<<v for v, holders in enumerate(supports) if holders & (1<<j)) for j in range(k))
            return
        top = supports[p[len(supports)]]
        subset = top
        while subset:
            yield from visit(supports+[subset])
            subset = (subset-1) & top
    return visit([(1<<k)-1])


def verify(rows):
    actual = {}
    for parents, state, group, words in rows:
        key = (tuple(parents),tuple(state),group)
        require(key not in actual and words == sorted(set(words)), "duplicated record or unsorted words")
        actual[key] = set(words)
    groups = defaultdict(list)
    totals = dict(families=0,complete_visible_words=0,cover_states=0)
    for n in range(1,5):
        for tail in product(*(range(i) for i in range(1,n))):
            p = (-1,*tail)
            for k in (2,3):
                for state in indexed_covers(p,k):
                    totals["cover_states"] += 1
                    for group in range(1,(1<<k)-1):
                        key = (p,state,group)
                        predicted = words_from_endpoints(p,state,group)
                        require(key in actual and actual.pop(key) == predicted, "projected language "+str(key))
                        projected = tuple(m for j,m in enumerate(state) if (1<<j)&group)
                        groups[p,k,group,projected].append(predicted)
                        totals["families"] += 1
                        totals["complete_visible_words"] += len(predicted)
    require(not actual, "unsolicited histories")
    for family in groups.values():
        require(set.intersection(*family), "one complete visible history shared across all outside assignments")
    totals["fixed_visible_preparations"] = len(groups)
    return totals


def controls(rows):
    r = next(row for row in rows if len(row[3]) >= 3)
    def altered(words):
        return [r[:3]+[words],*(x for x in rows if x is not r)]
    for bad in (rows[1:],rows+[rows[0]],altered(r[3][1:]),altered(sorted(r[3]+["Z"])),
                altered([r[3][0]]+r[3]),[[[-1,0],[3,3],1,[""]]]+rows):
        try:
            verify(bad)
        except (KeyError,ValueError):
            continue
        raise ValueError("corrupt free-pruning language accepted")
    # A shared internal stub has to be removed even if no source tells that receiver to act.
    # Root has children x and y; x has leaf t. R holds only the root and x.
    p=(-1,0,0,1)
    pair=((15,3,5),(11,3,5))  # S retains x,t; the other chart holds y.
    expected={chr(65+len(p)+1)}
    require(all(words_from_endpoints(p, views, 2)==expected for views in pair), "forced receiver edit on a dead stub")
    # Last-copy, external-owner availability, and descendant-before-ancestor probes.
    require(words_from_endpoints((-1,0),(3,1),1)=={""}, "last copy")
    require(words_from_endpoints((-1,0),(3,3),1)=={"","B"}, "outside option")
    w=words_from_endpoints((-1,0,1),(7,7),1)
    require("CB" in w and "BC" not in w, "ancestry order")
    return 10


if __name__=="__main__":
    data=Path(sys.argv[1])
    rows=read_xz(data/"free_receiver_words.json.xz")
    result=verify(rows)
    result["controls"]=controls(rows)
    save(data/"free_receiver_language.json",result)
    print(result)
