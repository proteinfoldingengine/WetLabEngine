# Identical complete exterior records and distinct interior chart counts

In a prepared 9-by-9 square of the 121-chart finite atlas, 16 distinct interior count profiles give exactly the same complete pair-work matrix. Every one of the 40 exterior charts has the same named leaves in all 16 cases. Each named leaf also has the same total number of holders in all 16. In a 10-by-10 square the construction gives 16,930,529,280 interior count profiles with all 21 exterior charts fixed. All profiles use the archived work matrix. The construction supplies the population of each leaf: some have 25 holders, some 96. This matters. Requiring *every* leaf to keep the original population of 25 fixes the count at *every* chart.

These counts are exact in the explicit family below and give lower bounds on the full set of compatible states. Chart identities are fixed. Local counts ignore leaf names. The model's supplied equal grades make its local Pin grade a function of that count, so different counts distinguish local records even if leaves are anonymous. The exterior equality is stronger and preserves named holdings as well as the grade at the Pin. This is an unnumbered mathematical extension of the [reviewed orbit](../orbit_exchange/RESULT.md) and the [earlier fixed-total observation](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-7203809301). The [prospective scope](SCOPE.md) discloses the constructive lead.

## What the work really fixes

Let there be N charts and m indexed leaves. Write b_il for membership of chart i at leaf l, s_l for the number of holders of l, d_i for the number of leaves at i, and H_ij for the Hamming distance of two charts. In this equal-grade model the work is 4 H_ij. Summing over j, including i, gives

    sum_j H_ij = sum_l s_l + sum_l (N - 2 s_l) b_il.

For one leaf, a holder disagrees with N-s_l charts and a nonholder disagrees with s_l. This proves the identity. When all leaf populations equal s and N differs from 2s, the work and the common population therefore determine d_i. The original instance has N=121, m=968, s=25. Each row sum in Hamming units is 25×968 + 71×200 = 38,400. Thus every chart must still hold 200 leaves in ANY endpoint with that work and those populations. This conclusion concerns counts; different addressed states could share those counts.

For fixed populations in {25,96}, the work row instead fixes the difference between the number of 25-holder leaves and 96-holder leaves at a chart. A local count can then change by an even number. The proof below realizes such changes wholly inside the specified square. If starting from the original all-25 state is required, the mixed population first needs to be prepared; the equal-work endpoints below are compared within that shared preparation.

## How to change the interior and keep the exterior fixed

For odd prime p, work on (Z/p)^2. Write S for the supplied 25-point footprint. Keep all eight orientation copies and their translations. Only the p² translations T_t=S+t in one **indexed** orientation are used for the following construction. All other named leaf slots keep their original supports. Let R be a square in the minimum-work graph. Define E as all charts outside R. Partition the p² templates into classes by exact equality of T_t intersected with E.

In each class of size m_g designate k_g=floor(m_g/2) named slots as the long slots. Pick any k_g of the templates in the class. Put their **complements** in the designated long slots, and put the remaining uncomplemented templates in the short slots. Use a fixed ordering within each group for assigning the selected templates to slots. All populations remain fixed at their named addresses across choices. All exterior charts retain identical named rows: every template in a class agrees on E, and its orientation (short or long) is fixed at each address. Each endpoint is a common permutation and sign change of binary columns of the original table, so the Hamming difference of every chart pair is preserved. This includes every pair crossing the boundary.

There are exactly product_g binom(m_g,k_g) choices. They all have distinct chart-count vectors. Before reassignment the variable orientation contributes 25 leaves at every chart. If F is the chosen set of translated templates and K=|F|, its new contribution at x is

    25 + K - 2 sum_{t in F} 1_S(x-t).

To see injectivity, over the field F_p let T_s be translation by s on functions on the chart group and M=sum_{s in S} T_s. Translations commute; the pth power of a sum in characteristic p is the sum of the pth powers. Each translation has pth power I, hence M^p=25 I. For our primes p=11 or p≥19, 25 is invertible, so M is invertible. If two integral count vectors are equal, their choices have the same K and the displayed integer convolution of the difference is zero. Reducing modulo p and applying the inverse forces the two choice indicators to agree modulo p, hence exactly. All count differences must occur inside R. The result does not require an exterior observer to know the initial record or reconstruct an interior state.

Every pair of the constructed endpoints can be joined by bare edits at interior charts alone. At each named leaf, add every required membership before removing obsolete ones. Neither endpoint has an empty support, so coverage survives; all nonroot vertices are leaves and the common Pin is untouched. Constant pair work and fixed leaf totals are **endpoint** requirements. The path need not preserve them at each individual edit. Distinct endpoints cannot preserve every named leaf total at each single-incidence move.

## Finite record

The original work minima are 704 on the four displacements (±1,±1) and the next work level is 1088. In chart coordinates let e=(1,1) and f=(1,-1). They form a basis modulo each odd prime here. The square is R={ue+vf : 0≤u,v<r}. It has r² charts, with 4r graph edges crossing to E when 1≤r<p. Location and the choice of axes are supplied, and the adjacency comes from work.

| Native side | Exterior charts | Nontrivial exterior restriction classes | Distinct chart-count profiles in this family |
| --- | ---: | --- | ---: |
| 1–8 | 120 down to 57 | None | 1 at each side |
| 9 | 40 | Four pairs | 16 |
| 10 | 21 | Eight pairs, six triples, four groups of four, one group of eight | 16,930,529,280 |

For side 9 the same four named leaves have 96 holders and the other 964 have 25. Two extreme choices differ in the counts of 48 interior charts. Their 7,260 work values match the archived geometry exactly. The independent enumeration traverses all 16 possibilities using a separately reconstructed footprint and tests every pair's variable contribution as well as every exterior row. For side 10 the count follows from the class sizes and injectivity; two explicit endpoints differ in 94 interior chart counts. The negative controls include one incorrect complement that preserves work while changing a named leaf total and every outside row, and an outside edit that changes work. The replay also compares the prospective exterior restrictions for all ten sizes. Finite counts treat chart names as fixed; no enumeration of all possible equal-work configurations was attempted.

## Scaling against a boundary defined by the graph

Take the specified signed footprint in [-4,4]², its eight orientations and their translations for odd primes p≥19. The sum of the eight autocorrelations has value 112 on the four diagonal displacements and at most 64 on any other nonzero displacement, as the exact 25×25 offset summation checks. No two offsets in [-8,8]² alias modulo such a p. The work therefore selects the same four diagonal nearest directions throughout this family. This concerns the weighted table and its minimum graph; a separate full carrier implementation for every p is not assumed.

Let r=floor(3p/4), h=floor(p/2). In the native (u,v) coordinates a footprint offset (x,y) is ((x+y)/2,(x-y)/2) modulo p. Even numerators lie between -8 and 8; both native coordinates then lie in [-4,4]. For odd numerators use (p+x±y)/2 to represent them. Both coordinates lie in h+[-4,4]. Thus translating by any native center whose two coordinates lie from 4 through r-1-h-4 places the whole footprint inside R. At least M=max(0,r-h-8)² templates have empty exterior signature. Choosing half the templates of this class gives at least binom(M,floor(M/2)) profiles, using monotonicity of the central binomial coefficient. To keep the **inner boundary ring** fixed as well, group templates by their restriction outside the square inset by one chart on all four sides. Using centers from 5 through r-2-h-4 gives the same conclusion with M=max(0,r-h-10)². The boundary ring and every exterior chart now keep all their addressed holdings.

Since binom(M,floor(M/2))≥2^M/(M+1) and the one-orientation construction has at most 2^(p²) choices, the logarithm in bits grows on the order of p², including with the inner ring fixed. The number of crossing edges is 4r, on the order of p. Therefore no uniform constant times the boundary-edge count upper-bounds this log multiplicity in this prepared family. Both the square and its complement occupy a nonvanishing fraction of the torus. The statement concerns distinct count profiles in a fixed chart frame, unconstrained by a probability law or the spontaneous accessibility of endpoints. The binary logarithm is a combinatorial capacity. The model assigns no physical area, horizon or thermodynamic entropy to this graph boundary.

| p | Square side | Crossing edges | Templates fully inside | Floor of log₂ count from that class alone |
| ---: | ---: | ---: | ---: | ---: |
| 31 | 23 | 92 | 54 | 50 |
| 59 | 44 | 176 | 460 | 455 |
| 127 | 95 | 380 | 3,078 | 3,071 |
| 251 | 188 | 752 | 13,804 | 13,796 |

The finite scaled examples count offsets in the specified coordinate footprint. Only the 11×11 witness was compared against every entry of the original archived work geometry. Run `python replay.py` and `python verify.py` from this directory; reference output is in `results.json` and `verification.json`.
