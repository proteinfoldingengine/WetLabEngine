# C3 first obstruction gate: three singleton anchors

Date: 2026-10-07.
Status: PROSPECTIVE ANALYTICAL SCOPE; C3 remains open.

Parent accepted C2 closeout: COUPLED_C2_CLOSEOUT.md at 787467cc6a1bfc9f09f586809948ebfe16d32742.
Parent coupled C1-C6 program: COUPLED_AUXILIARY_SCOPE.md at f95cdfef30b452e1688172b978ee2e25fb1924d8.

## Objective

Before searching for a four-root coupled endpoint-only deadlock, test a structural no-go in the tempting three-singleton-anchor carrier.

Four labelled nonempty roots with original positive floors. Source:
    r1={a}, r2={b}, r3={c}, r4=S,
where a,b,c are distinct and S is nonempty. The exact target changes r4 to T (T nonempty, |T|>=f4), and may independently change the other three roots. Assume f1=f2=f3=1 and f4<=min(|S|,|T|). All native events are single-incidence toggles. The protected band is 3<=tau<=4.

Required claims:
1. With r1,r2,r3 frozen at their source singleton supports, every intermediate nonempty r4 support has tau in {3,4}, irrespective of overlaps.
2. If S!=T, an endpoint-only all-additions-then-deletions schedule changing only r4 is floor-legal and protected.
3. Consequently, no such carrier can exhibit a source state with ZERO legal endpoint-only first moves while r4 has an endpoint difference. This does NOT prove that a full endpoint-only path exists to arbitrary targets for r1-r3.
4. Apply the result to the C2 carrier and distinguish safe first move from a complete safe schedule.
5. State the falsification boundary: if no three disjoint singleton anchors remain, or if r4 floor is incompatible with an endpoint, the lemma does not apply.

If proved, redirect C3 candidate search away from three singleton roots plus an active fourth root. Seek overlapping supports whose lower protection is not guaranteed by a frozen triple of singleton anchors.

No numerical campaign, physical claim, or independent acceptance is authorized.
