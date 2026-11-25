"""Direct chart-based layer expansion and independent two-chart cover deficit checks."""
from itertools import combinations


def verify_budget(data,summary):
    def check(ok):
        if not ok:raise ValueError("budget domain, projection or return mismatch")
    def inputs(N,m,n,v):
        full=(1<<(N+m+n))-1
        ms=(1<<N)-1
        receiver=((1<<n)-1)<<(N+m)
        source=(ms|( ((1<<m)-1)<<N))^(1<<(v-1))
        return full,(receiver,source,*(1<<i for i in range(N)))
    def state_key(s,k,length):
        return sum(1<<(i*k+j) for j,c in enumerate(s) for i in range(length) if c & (1<<i))
    def return_at(s,full):
        return any((x|y)==full for x,y in combinations(s,2))
    def witness(s,positions,dest,full):
        k=len(s)
        state=list(s);codes=[];qs=[3]
        for i in positions:
            check(not state[dest] & (1<<i))
            state[dest] |= 1<<i
            codes.append(i*k+dest+1)
            qs.append(2 if return_at(state,full) else 3)
        check(qs==[3]*len(codes)+[2])
        return [codes,qs]
    def enumerate_ball(N,m,n,v,restrict):
        full,origin=inputs(N,m,n,v)
        k=len(origin)
        length=full.bit_length()
        active={origin:0};end={};front={origin}
        collision=1<<(v-1)
        for depth in range(1,4):
            new=set()
            for s in front:
                for j in range(int(restrict),k):
                    for i in range(length):
                        bit=1<<i
                        if j==1 and bit==collision:continue
                        c=s[j]^bit
                        nxt=s[:j]+(c,)+s[j+1:]
                        if nxt in active or nxt in end or nxt in new:continue
                        if s[j]&bit and not any(x&bit for x in nxt):continue
                        if return_at(nxt,full):
                            end[nxt]=depth
                        else:
                            new.add(nxt)
            active.update(dict.fromkeys(new,depth))
            front=new
        def packed(nodes):return sorted([state_key(s,k,length),d] for s,d in nodes.items())
        marked=(1<<N)-1
        projection=[sorted({s[0]&marked for s,dep in end.items() if dep<=b}) for b in range(1,4)]
        return dict(active=packed(active),returned=packed(end),marked_masks=projection)
    expected_keys=[(N,m,n,v) for N in range(2,5) for m in range(1,4)
                   for n in range(1,4) for v in range(1,N+1)]
    check([tuple(row[:4]) for row in data["cases"]]==expected_keys)
    for row in data["cases"]:
        N,m,n,v,d=row[:5];full,s=inputs(N,m,n,v)
        k=N+2;ind=v-1
        misses=[]
        for a,b in combinations(range(k),2):
            mask=full&~(s[a]|s[b])
            misses.append([a,b,[i+1 for i in range(full.bit_length()) if mask&(1<<i)]])
        eligible=[len(rest) for a,b,rest in misses if (a,b)!=(0,1)]
        check(min(eligible)==d==min(n,m+N-1))
        check(row[5]==misses)
        receiver_witness=witness(s,range(N+m,N+m+n),v+1,full)
        source_witness=witness(s,[*range(N,N+m),*(i for i in range(N) if i!=ind)],v+1,full)
        check(row[6:8]==[receiver_witness,source_witness])
        marks={}
        for size in range(1,min(N+1,d)):
            for choice in combinations(range(N),size):
                if ind in choice:
                    mask=sum(1<<i for i in choice)
                    marks[mask]=witness(s,[i for i in choice if i!=ind]+[ind],0,full)
        check(row[8]==[[key,marks[key]] for key in sorted(marks)])
    bkeys=[key for key in expected_keys if key[:3] in ((2,2,2),(3,1,3))]
    check([tuple(b[:4]) for b in data["balls"]]==bkeys)
    projected=[];total=0
    for row in data["balls"]:
        N,m,n,v=row[:4]
        for j,restrict in enumerate((False,True)):
            expected=enumerate_ball(N,m,n,v,restrict)
            check(row[4+j]==expected)
            total+=len(expected["active"])+len(expected["returned"])
            for b in range(1,min(4,n,m+N-1)):
                sets=sorted(t for t in range(1,1<<N) if t&(1<<(v-1)) and t.bit_count()<=b)
                check(expected["marked_masks"][b-1]==([] if restrict else sets))
            depth=min(n,m+N-1)
            check(0 in expected["marked_masks"][depth-1])
        projected.append(dict(source=row[:4],all=row[4]["marked_masks"],untouched_R=row[5]["marked_masks"]))
    check(summary==dict(priors=27,arms=81,balls=10,labeled_vertices=total,projected=projected))
    # The two different source arms have a common two-mark report, even below the
    # bypass distance for three marks. No two-mark report is possible for all three.
    three=[set(b[4]["marked_masks"][1]) for b in data["balls"] if b[0]==3]
    check(all(a&b for a,b in combinations(three,2)) and not set.intersection(*three))
