"""Produce the marked-leaf budget witnesses and exact finite first-return balls."""
from collections import deque
from itertools import combinations


def budget_universe(h,atom):
    model=h["model"]
    def initial(nmarks,m,n):
        # 0 is R, 1 is S, 2..N+1 are distinct helpers.
        return tuple(map(frozenset,[{1,2+i} for i in range(nmarks)]+[{1}]*m+[{0}]*n))
    def put(rows,i,j):
        if j in rows[i]:
            raise ValueError("idle witness")
        s=list(rows)
        s[i]=rows[i]|{j}
        return tuple(s)
    def run(start,indices,dest,k):
        s=start
        seq=[]
        profile=[model.tau(s)]
        for i in indices:
            s=put(s,i,dest)
            seq.append(1+k*i+dest)
            profile.append(model.tau(s))
        return [seq,profile]
    def packed(rows,k):
        return sum(sum(1<<j for j in row)<<(i*k) for i,row in enumerate(rows))
    def ball(start,N,k,marked,freeze):
        queue=deque([(start,0)])
        live={start:0}
        end={}
        while queue:
            s,d=queue.popleft()
            if d==3:
                continue
            for i,row in enumerate(s):
                for j in range(k):
                    if (i==marked and j==1) or (freeze and j==0) or row=={j}:
                        continue
                    y=list(s)
                    y[i]=row^{j}
                    child=tuple(y)
                    if child in live or child in end:
                        continue
                    z=model.tau(child)
                    if z==2:
                        end[child]=d+1
                    else:
                        if z<3:raise ValueError("skipped first return")
                        live[child]=d+1
                        queue.append((child,d+1))
        # All finite keys encode the complete labeled leaf-by-chart array.
        def entries(nodes):return sorted([packed(s,k),d] for s,d in nodes.items())
        projection=[]
        for budget in (1,2,3):
            values={sum(1<<i for i in range(N) if 0 in s[i]) for s,d in end.items() if d<=budget}
            projection.append(sorted(values))
        return dict(active=entries(live),returned=entries(end),marked_masks=projection)
    cases=[]
    balls=[]
    for N in (2,3,4):
        k=N+2
        for m in (1,2,3):
            for n in (1,2,3):
                s=initial(N,m,n)
                for v in range(N):
                    post,trigger=atom(h,s,k,1,v+1)
                    if trigger!=[2,3,True]:raise ValueError("source did not raise cover")
                    d=min(n,m+N-1)
                    deficits=[[a,b,[i+1 for i,row in enumerate(post) if not ({a,b}&row)]]
                              for a,b in combinations(range(k),2)]
                    via_r=run(post,range(N+m,N+m+n),2+v,k)
                    via_s=run(post,[*range(N,N+m),*(i for i in range(N) if i!=v)],2+v,k)
                    local=[]
                    for mask in range(1,1<<N):
                        if mask & (1<<v) and mask.bit_count()<d:
                            seq=[i for i in range(N) if i!=v and mask&(1<<i)]+[v]
                            local.append([mask,run(post,seq,0,k)])
                    cases.append([N,m,n,v+1,d,deficits,via_r,via_s,local])
                    if (N,m,n) in ((2,2,2),(3,1,3)):
                        balls.append([N,m,n,v+1,ball(post,N,k,v,False),ball(post,N,k,v,True)])
    stats=dict(priors=27,arms=len(cases),balls=2*len(balls),
               labeled_vertices=sum(len(g[key]) for b in balls for g in b[4:] for key in ("active","returned")),
               projected=[dict(source=b[:4],all=b[4]["marked_masks"],untouched_R=b[5]["marked_masks"])
                          for b in balls])
    return dict(cases=cases,balls=balls),stats
