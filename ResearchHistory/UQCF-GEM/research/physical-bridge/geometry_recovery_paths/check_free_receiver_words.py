"""Enumerate the complete local histories by walking the archived v16.26 deletion graph."""
from functools import lru_cache
from itertools import product
from pathlib import Path
import sys
from free_receiver_io import ATOM, module, write_xz


def produce(root, out):
    atom = module(root, ATOM, "free_atom", "c10ac57f988a439144e21898bd2b33ece0838a9b")
    output = []
    for n in range(1, 5):
        for tail in product(*(range(v) for v in range(1, n))):
            p = (-1,) + tail
            views = atom.legal(p)
            encode = {v:sum(1 << t for t in v) for v in views}
            decode = {m:v for v,m in encode.items()}
            for k in (2, 3):
                @lru_cache(None)
                def steps(state):
                    rows = tuple(decode[m] for m in state)
                    edges = []
                    for j, view in enumerate(rows):
                        for v in view:
                            try:
                                after = atom.atomic(p, rows, j, v)["after"]
                            except ValueError:
                                continue
                            edges.append((j, v, tuple(encode[tuple(y)] for y in after)))
                    return edges

                @lru_cache(None)
                def seen(state, coalition):
                    edges = steps(state)
                    if not edges:
                        return {""}
                    words = set()
                    for j, v, nxt in edges:
                        symbol = chr(65 + n * j + v) if coalition >> j & 1 else ""
                        words.update(symbol + word for word in seen(nxt, coalition))
                    return words

                for state in product(sorted(decode), repeat=k):
                    if set.union(*(set(decode[m]) for m in state)) != set(range(n)):
                        continue
                    for coalition in range(1, 2**k-1):
                        words = sorted(seen(state, coalition))
                        output.append([p, state, coalition, words])
                seen.cache_clear()
                steps.cache_clear()
    out.mkdir(exist_ok=True,parents=True)
    write_xz(out/"free_receiver_words.json.xz", output)
    print("Projection families",len(output),"distinct words summed over families",sum(len(x[3]) for x in output))


if __name__ == "__main__":
    produce(Path(sys.argv[1]), Path(sys.argv[2]))
