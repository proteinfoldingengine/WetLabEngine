# v16.28 — Typed endpoint classification, proofs D1–D7

Written before adjudication implementation. General finite mathematical arguments, not proof-assistant formalization. No physical geometry is assumed. Provenance is the completed v16.27 publication `134b3d6c3358d91df2e34a9bb57ac82a2f0406ce`; relative references below are under ResearchHistory/UQCF-GEM at that commit.

## Provenance and type ledger

| ID | Construction/type | Assumptions and exact provenance | Status |
|---|---|---|---|
| T1 | X finite common-Genesis rooted lineage, Y=(Y_i), Z=(Z_i), Z_i subset Y_i, equal union U | v16.27 completion/PROOFS.md T1–T3, C1; literal retained identities, root-containing prefix subsets | Inherited admitted category |
| T2 | E={(i,v):v in Y_i minus Z_i}; e precedes f when its node is a strict descendant in the SAME indexed view | v16.27 completion/PROOFS.md T4, C1 | Derived finite poset; no inter-Genesis identification |
| T3 | J(E)={S subset E: all predecessors of each element in S belong to S}; Y^S_i=Y_i minus {v:(i,v) in S} | T1–T2, D1 | Actual intermediate retained covers, not arbitrary Boolean states |
| T4 | F:J(E)->Z, F(S)=h(Y^S); h=max(1,max_v tau_v), tau minimum child-cover cardinality | v16.24 TYPE_AND_PROOF.md C7–C8,H2–H3; v16.27 C2 | Inherited integer invariant; cone interpretation conditional, no source-scalar extension here |
| T5 | m_e(S)=F(S union {e})-F(S), for enabled e | v16.26 P2–P4, v16.27 C2 | Actual transition increment in {0,1} |
| T6 | D(S;e,f)=F(Sef)-F(Se)-F(Sf)+F(S), simultaneously enabled distinct e,f | T3–T5 | Derived symmetric integer difference; not response-space transport |
| T7 | Pred(e) strict predecessor ideal; w_e=F(Pred(e) union {e})-F(Pred(e)) | T2–T5, D4 | Derived candidate coefficients, not a chosen allocation or coupling |
| T8 | Equivalences are parent-preserving lineage bijections and simultaneous indexed-view permutations | v16.27 completion/PROOFS.md T8,C6 | Typed identity transport, not equal-dimension identification |

## D1 — Intermediate states are exactly the order ideals

A legal prefix of a full deletion path has removed every descendant before an ancestor in each view, so its event set S is an ideal. Conversely, delete an ideal S in a topological order. A retained descendant of a deleted node cannot remain: if it is in the final Z_i, prefix closure would retain that node; otherwise it is a predecessor and already deleted. Thus every step removes a current leaf. Each node in U is retained by some final Z_j, so union U never changes. The remaining events can also be topologically ordered, giving a full legal completion. This is the same-domain argument of .27 C1, now applied to prefixes.

An event is enabled at S exactly when it is outside S and all its predecessors are in S. Two distinct enabled events are incomparable. Both orders e,f and f,e reach the SAME actual retained cover Sef. Intersections/unions of ideals are ideals, so they also correspond to earned retained states.

## D2 — Exact adjacent-swap comparison

For a reachable S enabling e and f, compare the two two-step sequences. The increment for e AFTER f minus its increment BEFORE f equals D(S;e,f). The analogous comparison for f is also D when phrased 'after the other minus before'. Between the full paths ef and fe the two event assignments change by opposite amounts. Their total is the same endpoint difference, regardless of D.

Because each actual marginal is 0 or 1, D lies in {-1,0,1}. This is a mixed difference of a scalar state function; the oriented circulation of delta F around the four states is ZERO for all D. There is no nonzero loop transport or curvature claim.

## D3 — A nonzero diamond supplies an admissible full-path counterexample

Order the events of S legally, append e,f, then any legal completion of the remaining events. Swapping only e,f keeps the same prefix, suffix, starting cover, final cover and event set. D1 ensures legality and unchanged union throughout. D2 shows that if D is nonzero, at least those two event attributions differ. Consequently path-independent event attribution implies every diamond is zero.

## D4 — Zero diamonds force unique actual event coefficients

Fix e and an arbitrary ideal S enabling e. S includes Pred(e) but not e. Every element of S minus Pred(e) is incomparable with e: a predecessor would already be in Pred(e), and a successor in an ideal would force e into S. Build S from Pred(e) by adding these remaining elements in a legal topological order. At each addition f, both f and e are enabled. D=0 implies m_e does not change when f is added. Induction gives m_e(S)=m_e(Pred(e))=w_e.

Thus every legal context and full path gives the same actual coefficient w_e. Conversely, if event attribution is constant along every full path, all enabling contexts are prefixes of some full path by D1, so their marginals coincide. Pred(e) is an enabling context; therefore w_e is uniquely determined, not one of many splittings. For the inherited h, each w_e is 0 or 1. Identity and one-path intervals are included; no path multiplicity is presumed.

## D5 — Additive and modular formulations are equivalent

When D4 holds, take any topological ordering of any ideal S and telescope its actual increments. Then

    F(S)=F(empty)+sum_{e in S} w_e.

Conversely that identity makes every enabled marginal exactly w_e, hence gives event independence. Such a sum satisfies

    F(A)+F(B)=F(A union B)+F(A intersection B)

because every event occurs with the same multiplicity on both sides. Conversely apply this modular equation to A=Se and B=Sf to obtain D=0. Combining D3–D5 proves the four-way equivalence for EVERY finite admissible endpoint, without a bound on tree size or number of events.

This is a standard valuation-type criterion applied to the existing retained invariant, not a claim to have invented distributive lattices. The coefficients describe actual deltas only on the specified endpoint interval; they need not agree for a different endpoint interval.

## D6 — Concrete positive and negative boundaries

For the .27 witness Y=({0,1},{0,2},{0,1,2}), Z=({0,1},{0,2},{0}) on (-1,0,0), the four h values are 1,2,2,2. D=-1, and the same two events swap assignments (1,0) and (0,1).

Opposite sign is also admissible in the full category: take Y=({0,1,2},{0,1,2}), Z=({0,2},{0,1}). Either one-event deletion leaves another full view, so the four h values are 1,1,1,2 and D=+1. Repeated INITIAL views are permitted in this control, not silently counted in the distinct-initial-view primary enumeration. No universal sign-definite interaction law follows.

A one-event interval can have w=1. A chain-ordered event interval has a unique legal path and no incomparable enabled pair; the criterion is vacuous there but produces its actual unique coefficients. Constant F gives all w=0. These positive cases prevent equating 'some pruning occurs' with 'attribution fails'.

## D7 — Naturality, computability and limitations

The admitted bijections send E and its predecessor relation bijectively, hence ideals, enabled pairs and diamond states bijectively. They preserve h. Therefore D is preserved, and the coefficient w_e transports with its event where it exists. A chosen topological ordering used to print a counterexample is a computational witness, not a physically preferred order.

Within any refined subinterval, zero diamonds remain zero, so event independence restricts consistently; this statement concerns subintervals of a FIXED endpoint poset, not unrelated carriers. A nonzero diamond provides a four-state certificate even when listing every full path would be expensive. Finding every ideal may still be exponential: no polynomial-complexity claim is made.

The theorem does not derive physical source attainability, response-law selection, an operational quantum bridge or a temporal/geometric law. h remains a worst-case consistency-testing order. Source/response maps earned earlier are not discarded; they are simply not identified with these integers.

Background attribution: G. Pruesse and F. Ruskey, Generating Linear Extensions of Posets by Transpositions, JCT B 54 (1992), 77–101, author publication page https://webhome.cs.uvic.ca/~ruskey/Publications/JCTextension/JCTextension.html . The proofs above are direct and do not assume a Hamilton ordering of all extensions.

**Time is pruning / ordered recoverability update.**
