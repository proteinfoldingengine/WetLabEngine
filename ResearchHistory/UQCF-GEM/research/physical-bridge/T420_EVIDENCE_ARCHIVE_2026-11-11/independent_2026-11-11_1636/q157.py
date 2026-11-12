from fractions import Fraction as F
xp={'o':F(1,5),'p':F(1,5),'u':F(2,5),'v':F(1,5)}; xm={'o':F(1,5),'p':F(1,5),'u':F(1,5),'v':F(2,5)}
fib=('p','u')
def fixed(x,m={'p':1,'u':1}):
    tot=x['p']+x['u']; M=m['p']+m['u']
    return all(x[a]==tot*m[a]/M for a in fib)   # canonical lift = trace-weighted redistribution
print("uniform trace: fixed(x+)=",fixed(xp)," fixed(x-)=",fixed(xm))
for m in ({'p':1,'u':2},{'p':2,'u':1}):
    print("weights",m,": fixed(x+)=",fixed(xp,m)," fixed(x-)=",fixed(xm,m))
# post-event retained grades
post=lambda x:(x['o'],x['p']+x['u'],x['v'])
print("post x+",post(xp),"post x-",post(xm))
