"""Capacity-bounded complementary-cover reconfiguration in supplied label order."""
def reconfigure(start,target,capacities,order):
    order=list(order);P=set(order);bins=[set(A) for A in start];target=[set(A) for A in target]
    if len(order)!=len(P) or not P or len(bins)!=len(target) or len(bins)!=len(capacities):raise ValueError('cover dimensions')
    if any(type(b)!=int or b<0 for b in capacities) or sum(capacities)<len(P)+1:raise ValueError('cover surplus')
    for cover in (bins,target):
        if set().union(*cover)!=P or any(not A<=P or len(A)>b for A,b in zip(cover,capacities)):raise ValueError('cover admission')
    path=[[set(A) for A in bins]]
    def edit(i,x,add):
        if add:
            if x in bins[i] or len(bins[i])>=capacities[i]:raise ValueError('cover addition')
            bins[i].add(x)
        else:
            if x not in bins[i] or sum(x in A for A in bins)<2:raise ValueError('cover deletion')
            bins[i].remove(x)
        path.append([set(A) for A in bins])
    owners={x:next(i for i,A in enumerate(bins) if x in A) for x in order}
    goals={x:next(i for i,A in enumerate(target) if x in A) for x in order}
    for i,A in enumerate(bins):
        for x in order:
            if x in A and i!=owners[x]:edit(i,x,False)
    def transfer(x,j):
        old=owners[x];edit(j,x,True);edit(old,x,False);owners[x]=j
    while any(owners[x]!=goals[x] for x in order):
        x=next(x for x in order if owners[x]!=goals[x]);j=goals[x]
        if len(bins[j])==capacities[j]:
            y=next(y for y in order if y in bins[j] and goals[y]!=j)
            spare=next(i for i,A in enumerate(bins) if len(A)<capacities[i])
            transfer(y,spare)
        transfer(x,j)
    for i,A in enumerate(target):
        for x in order:
            if x in A and x not in bins[i]:edit(i,x,True)
    return path
