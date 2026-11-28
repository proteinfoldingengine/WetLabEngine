"""Check the first-child prefix property of the v16.53 canonical endpoint."""
from itertools import product, permutations
import fixed_order_delivery as prior

producer,verifier = prior.producer,prior.verifier


def main():
    count = 0
    for arity in (2,3,4):
        for widths in product(range(1,4),repeat=arity):
            for target in range(1,arity+1):
                minimum = verifier.minimum(widths,target)
                for extra in (0,1):
                    palette = list(reversed(range(minimum+extra)))
                    rows = producer.palettes(palette,widths,target)
                    assert rows[0] == palette[:widths[0]]
                    count += 1
    print("First-child prefix checks, arities 2-4, widths 1-3, all targets, two palette sizes:", count)
    outcomes = {}
    for which,layout in (("previous layout",(0,2,1,3)),("receiver first",(1,0,2,3))):
        order = {**prior.identity,"Q":layout}
        ends = []
        for condition in ("base","reduce"):
            tree,sites,start,q = prior.prepare((),"A",order,condition)
            nodes = producer.layout(tree)
            k = len(start)
            path = producer.normalize(start,tree,k,q)
            end = verifier.model(tree,q,k)[2]
            verifier.path_check(tree,k,q,path,start,end)
            region = producer.vertices(nodes,sites["A"])
            ends.append(tuple(sum(1<<i for i,v in enumerate(region) if row>>v&1) for row in end))
        outcomes[which] = ends
        print(which,"whole receiver endpoint masks",ends)
    a,b = outcomes["previous layout"]
    c,d = outcomes["receiver first"]
    assert a!=b and c==d


if __name__=="__main__":
    main()
