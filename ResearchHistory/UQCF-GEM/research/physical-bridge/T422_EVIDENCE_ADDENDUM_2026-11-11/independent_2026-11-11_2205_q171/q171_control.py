import sys; sys.dont_write_bytecode=True
exec(open('q171.py').read().split('print("(1)')[0])
for kk in (19,20,50):
    par=dict(T); par.update({f'n{i}':'o' for i in range(kk)})
    w=f(par,xp,GPT,1); print('GPT f(I x+) with',kk,'empty root leaves: min component',min(w.values()),'root',w['o'])
par=dict(T); par.update({f'n{i}':'o' for i in range(50)}); w=f(par,xp,{(1,1):1,(2,2):1},1); print('id control min',min(w.values()))
