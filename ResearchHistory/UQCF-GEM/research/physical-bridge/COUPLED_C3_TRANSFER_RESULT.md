# Global pair miss counts recover the exact outside admission record

Status: frozen analytical argument; independent verification/reviews pending.

## Objects and source connection
Use the exact admission result at8441eb84ffd7123080cdaf057dbd77c67689a72a and the inherited dynamic residual definition M_R(H)=number of roots in R missing H. Here declare R to be ALL roots, rather than assuming a separately initialized outside-root record.

At the initial slice, A occupies selected nonhost roots W and is absent from host h. E occurs only at h. All other pool-role conditions and fixed pool-disjoint hidden Q are inherited. F consists of the nonhost roots outside W. Stable K of size<=2 covers F. The source is promised to have hitting number3 or4. The prior theorem implies F is nonempty and its hitting number is1 or2; admission is equivalent to empty full-support intersection of F.

M(H) is a CORRECTLY initialized GLOBAL miss-count record over a known finite complete palette L. This availability is conditional. No hidden support, host spectator list, new probe, acknowledgment or new coupling is supplied to the decoder. Existing core/template access and the source-band promise are still assumed.

## Exact transfer identity
For any x in L, the roots missing both A and x comprise the F roots missing x, plus h if h misses x. Thus

M({A,x})=M_F({x})+1[x notin S_h].

Because E occurs at exactly h, the global counts satisfy

M({x})-M({E,x})=1[x notin S_h].

Subtracting yields the exact decoder

M_F({x})=M({A,x})-M({x})+M({E,x}).

Repeated labels are sets, so for x=A or x=E the formula uses singleton coordinates where appropriate. Empty F would also satisfy the identity; its nonemptiness is needed only for the admission equivalence and follows here from the initial protected source. Labels absent from every root cause no problem. Hidden sharing and arbitrary original valid floors do not affect this count identity.

Consequently admission holds iff the decoded value is positive for every x in L. This uses only global singleton/pair coordinates. It does not require a global degree3 or4 field, or host-support access, or a separate initial count field on F. The global field must still itself be initialized correctly. The proof removes an extra restricted-record input; it does not remove the global-record availability assumption. A correctly certified bit remains sufficient for the ensuing single handoff, during which F is fixed.

## Global singleton counts alone do not suffice
Use common palette0..6, common floors(1,1,1,1,1,2), W={0,1,2}, A=0, E=4, D=3, K={1,2}. Compare

X=({0,6},{0,6},{0},{1},{2},{3,4})
Y=({0},{0},{0},{1,6},{2,6},{3,4}).

Cores, static parameters, palette, floors and root count agree. Each label has the same incidence count in X,Y: label0 occurs three times,1/2/3/4 once each,5 never,6 twice. Therefore ALL global singleton miss coordinates agree. Both sources satisfy the protected-band promise: X has tau4 (roots2,3,4 force0,1,2, plus3 or4 for host); Y has tau3 (root0 forces0, host3 or4, and6 covers roots3,4; no two-cover exists because these three requirements have disjoint labels).

For X, F=({1},{2}) has empty intersection, so admitted. For Y, F=({1,6},{2,6}) has common6, so rejected. Global pair records distinguish them: M_X({0,6})=3 whereas M_Y({0,6})=1. Decoder at x=6 gives2 versus0. Thus order2 is sufficient and order1 insufficient in the hierarchy of full GLOBAL truncated miss-count records augmented by the same core/static data and band promise. This is NOT minimal bit complexity, a statement about all possible channels, or a contradiction of first-order sufficiency on F itself. Exact tau is not part of the compared input; supplying it changes the interface.

## What is and is not advanced
This establishes a typed connection from the previously defined global retained field to the newly identified admission predicate. The unique existing host label E removes the host's unknown contribution algebraically. No external alignment or hidden read is introduced by the decoder. Correctness is exact, not statistical.

It does not derive native production, initialization, retention or observer access to global moments. Earlier dynamic-residual updates still require their stated current active-support information; earlier event or probe results retain their own response premises. The singleton counterexample is a specific interface lower bound, not a universal observer impossibility. Broad C3 origin, actual resolution/progress and general C4 remain OPEN. No force, fundamental time, geometry, dark-matter variable or GR derivation follows.
