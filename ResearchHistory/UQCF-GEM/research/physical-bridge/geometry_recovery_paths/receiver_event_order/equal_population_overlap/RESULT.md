# What two triples recover from 7,260 indistinguishable pairs

In the original equal-population 121-chart atlas, the work on every pair fixes each chart's 200-leaf count. Within the 484 original allowed supports, exactly 25 different multiplicity assignments have this work. All 25 can preserve the complete, named records of the same 11 charts simultaneously. Two measurements on triples containing two of these fixed charts distinguish all 25 assignments. The measurement is the root grade returned by the original positive P1 gluing code. The named charts, support dictionary, two measurements and call are supplied. The result concerns joint comparison in a prepared finite model.

## Exact classification

Use the 968 addressed leaves, common Pin of grade 1, leaf grade 2, chart numbering x+11y and eight oriented translation layers of orbit_exchange/probe.py. A column is a 25-chart set. Four distinct translation orbits of 121 columns occur, each column initially with multiplicity 2. Order the four by the signs (--),(-+),(+-),(++) applied without swapping coordinates. The footprint is invariant under swapping axes, so the remaining four layers duplicate this dictionary. Throughout the classification, names of charts remain fixed and permutations of leaf names are identified.

Let H be pair work divided by four, d_i the number of leaves at chart i, and G_ij the shared count. Since every leaf has population 25, summing H_ij over j gives 25·968+(121−2·25)d_i. Equality to the archived table therefore forces d_i=200 and G_ij=(400−H_ij)/2, including G_ii=200. Conversely G fixes the work. Write K_(ij),T=1 if both i and j lie in support T, with i≤j. For multiplicity vector n these data are Kn.

The sum of K columns over a translation orbit is the number of translates containing i and j, the autocorrelation of its footprint at j−i. Inverting the footprint negates the displacement and autocorrelation is even. The two pairwise differences between inversion-related orbit sums vanish. They give two independent kernel vectors. The [certificate](rank_minor.json) gives a 482-by-482 minor of K with determinant 52 modulo 101. The row indices enumerate all 7,381 lexicographically ordered pairs with replacement starting at zero; the columns use the original four blocks in their original translation order. Two separately implemented eliminations verify the nonzero residue. Over the rationals and reals K has rank exactly 482. Thus every integer solution differs from the baseline by a constant on each orbit and has the four multiplicities

    (2+a, 2+b, 2−b, 2−a),   a,b in {−2,−1,0,1,2}.

The directions have disjoint supports and unit entries, making integrality exact. Each solution uses 968 leaves. This counts support multiplicities for fixed chart addresses. Arbitrary 25-subsets and equivalence under chart automorphisms are outside the count.

## Which exterior records fix the assignment?

Given a fixed set E of charts with their original addressed records, a candidate multiplicity vector can be assigned to the named leaf slots precisely when its histogram of T intersect E matches the baseline. Necessity follows by checking each address. For sufficiency match the columns to baseline slots separately in each identical restriction class. The Pin and grades follow from these addressed holdings.

For E equal to the anti-diagonal x+y=0, all 25 pass. Matching and original work are verified for every explicit assignment. For E outside any of the tested native squares {(u+v,u−v) : 0≤u,v<r}, r=1 through 10, exactly (a,b)=(0,0) survives. This is uniqueness of multiplicities within the dictionary. Named slots can still be permuted when their restrictions agree. The earlier 9-by-9 and 10-by-10 count examples used a different 25/96-holder preparation.

## A pair of states and an inherited joint readout

Reflect just the 121 named columns in the original (++) layer by (x,y)→(−y,−x). Its new translated footprints belong to the (--) orbit. The other 847 named columns stay in place. Relative to the original (a,b)=(0,0), this gives (1,0). Exactly the 11 fixed-line charts keep their entire named row. Every leaf still has 25 holders and every chart has 200 leaves. The original has 484 support types used twice each. The new state uses 121 types once, 242 twice and 121 three times. A permutation of leaves or even of charts and leaves together cannot change this histogram.

| Charts 0, 5 and 41 | Original | Reflected layer |
| --- | ---: | ---: |
| Pair intersections for (0,5), (0,41), (5,41) | 32, 48, 48 | 32, 48, 48 |
| Held by all three | 16 | 12 |
| Distinct leaves held across the three | 488 | 484 |
| P1 root on the union | 961 | 969 |

Charts 0 and 41 have identical full addressed priors in the two preparations. All 7,260 work entries match. Across every unordered triple, 99,462 of 287,980 triple intersections change. Of 6,050 triples containing exactly two fixed-line charts, 1,650 change. An unmatched substitution changes 904 pair entries. A plain exchange of two leaf names preserves the entire multiset of supports, hence all intersection counts. The fixed counts on singletons and pairs also fix every pair-union root, so that scalar cannot distinguish the states.

On a star with honest marginals from the same fine record, the positive P1 glue returns the marginal on the union. Each retained leaf appears with grade 2, and inclusion-exclusion on the common root gives its grade as 1+2(968−|union|). For a triple the union contains 600 minus the sum of its three pair intersections plus the triple intersection. replay.py calls the pinned v16.23 push and glue_many from the original engine, checks the whole union record against the direct fine push, and checks its pushback to every contributing chart. For the displayed witness it tests all six orders in both states. The two same-prior charts recover exactly their original records on pushback. The function returns a union and has no write into any chart. The witness changes a third input. It supplies neither an event causing that change nor delivery of the joint value to a chart. No claim about all possible callers is required.

## How much can these readouts recover?

This follow-up analysis was added after the initial triple census. Keep the same two fixed charts 0 and 41, and compare their triple first with chart 5 and then with chart 1. The two intersections are respectively 16−4a+4b and 24−4b. Integer counts of translated footprints give these coefficients independently in verify.py. Since the two coefficient rows are independent, their outputs determine the entire support-multiplicity vector. The scalar P1 root on each triple is an invertible affine function of that intersection with its known pair counts. Direct calls to the original engine produced 25 different ordered pairs of root grades on 25 preparations with the full fixed-line records. Across all 287,980 triples, a single triple root can take at most 13 distinct values over this family. Thus two triple-root values suffice and one cannot suffice for all 25. This minimum concerns this specific scalar interface. It does not specify who selects the triples or who can read their union.

## Reproduce

Use Python 3.11 with numpy and sympy. From the study directory run the commands below, setting ORBIT to the sibling orbit_exchange/probe.py and ENGINE to the v16.23-overlap-descent/engine.py from historical commit e61d5b0e827f7b412824ad46021e2ad6cc6f7875. replay.py checks both Git blob identities before running them.

```bash
python replay.py "$ORBIT" "$ENGINE" /tmp/uqcf-rank-minor.json > /tmp/uqcf-equal-results.json
cmp /tmp/uqcf-rank-minor.json rank_minor.json
cmp /tmp/uqcf-equal-results.json results.json
python verify.py | cmp - verification.json
```

The second program uses an explicit independent coordinate table and exact integer arithmetic. The work table, all classification constraints, the minor, exterior constraints, complete triple census and two-root formulas are checked separately. No ensemble, entropy, physical identification or receiver update is assumed.
