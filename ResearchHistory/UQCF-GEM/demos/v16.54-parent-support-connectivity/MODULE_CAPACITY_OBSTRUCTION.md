# Complete-module normal forms can be unavailable

Status: candidate analytical result for independent review. Parent analytical head 6d9d023d89a59fe8f8902241762b70f200c10d62. No implementation, numerical search, enumeration or scientific execution.

## 1. The question being tested

HYPEREDGE_STAR_RELOCATION.md connects complete uniform hyperedge modules and asks whether arbitrary higher-floor exact endpoints can reach those forms. We now show that a universal route through those forms is impossible with the original root-slot budget. For an explicit infinite family of exact endpoints, no such exact-target module state exists anywhere in the same carrier.

The result is an obstruction to the proposed normal form, not a disconnected pair of exact endpoints and not a native repair barrier. It leaves the module connectivity theorem intact. It means that a universal proof must accommodate additional overlap structures.

All native roots below have floor 3. A complete triple module on S means that every three-element subset of S appears as an actual core root. Distinct modules use disjoint label sets; extra root slots may contain redundant supports as in Theorem Y. We strengthen the candidate normal-form class by allowing labels outside all core modules, as long as extra roots remain redundant with the core. Such labels may be genuinely unused or occur in redundant roots. This relaxation makes the impossibility result stronger than a mere divisibility obstruction for partitions of the entire palette.

## 2. An exact cyclic triple family

For any integer a>=2, partition a palette P into three parts A,B,C of size a. Its size is k=3a. Include each of the following supports exactly once as a root:

1. Every triple contained in one part.
2. Every triple with two labels in A and one in B.
3. Every triple with two labels in B and one in C.
4. Every triple with two labels in C and one in A.

All supports have size 3, so all floors are met exactly. The root types are disjoint and the number of root slots is

    r = 3*binomial(a,3) + 3*a*binomial(a,2)
      = a(a-1)(2a-1).

Here binomial(2,3)=0; the construction includes a=2.

**Lemma Z1.** The independence number of this root family is exactly 3, so its hitting number is q=k-3=3a-3.

Proof. One label from each part gives an independent triple: no root has distribution (1,1,1). Conversely every four-label set contains a root. If at least three labels lie in one part, those three form a root. Otherwise the distribution across parts is (2,2,0) or (2,1,1). In the first case there is one directed arc between the two occupied parts in the cycle A->B->C->A; two labels from its source and one from its destination form a root. In the second case the part with two labels has an occupied successor, again supplying a root. These exhaust the distributions. An independent set of size greater than four would contain an independent four-set, which is impossible. Thus alpha=3. Complementation between hitting and independent sets gives tau=k-alpha=k-3.

This proves exact-q feasibility in the native carrier without numerical search. It therefore has all the stronger exact-endpoint properties derived earlier, including coverage of every (q-1)-subset by complements, at least one uncovered q-subset, and the local redundancy hierarchy. Those properties are not imposed as unsupported assumptions.

## 3. Positive slack does not supply missing root slots

Every label has the same incidence degree

    D = binomial(a-1,2) + a(a-1) + binomial(a,2)
      = (a-1)(2a-1).

The three terms count internal triples, cyclic triples in which its own part contributes two labels, and cyclic triples in which its part contributes one label. In particular 3r=kD, as also follows from all roots having size 3.

Put d=r-q+1 and delta=sum_i(k-a_i)-(q-1)k=dk-3r, with each a_i=3. Then

    delta = k(d-D)
          = 3a[1+(a-1)(a-2)(2a+1)] > 0.

Thus this is a positive-slack family. The root-slot obstruction below persists despite exact admissibility and the derived total-capacity inequality. It is not a failure caused by excluding saturated cases or by a missing label in the input.

## 4. No exact-target complete-module state fits

**Theorem Z (module-capacity obstruction).** On the same k=3a labels, r=a(a-1)(2a-1) root slots and all floors 3, there is no complete-triple-module state of hitting number q=k-3, even if labels outside the modules and redundant extra roots are allowed.

Proof. Suppose such a state has m nonempty core modules, each of size s_j>=3. A complete triple module on s_j labels has hitting number s_j-2. Distinct modules add, and redundant extras do not change that hitting number. If L=sum_j s_j is the number of labels in core modules, exactness requires

    q = L-2m,   L<=k.

Since q=k-3, this gives 2m<=3. Also q>=3, so at least one module is needed. Therefore m=1 and its size must be L=q+2=k-1.

That single module requires every triple on k-1 labels as a distinct core root. It needs at least binomial(k-1,3)=binomial(3a-1,3) slots. But

    binomial(3a-1,3) - r
      = (a-1)^2(5a-2)/2 > 0.

There are strictly too few slots. Duplicate roots, larger redundant supports, and labels outside the core cannot reduce the number of required distinct core triples. A root slot contains one support; it cannot stand for several distinct core roots. This is a contradiction.

The proof rules out the terminal form itself, independent of the chosen path, star-exchange schedule or progress measure. It does not rule out other common endpoint forms.

## 5. A smaller illustrative carrier

An unequal-part version makes the mechanism visible at target 4. Take part sizes (3,2,2) and the same cyclic root rule. It has k=7 labels and

    r = 1 + binomial(3,2)*2 + binomial(2,2)*2
          + binomial(2,2)*3 = 12

distinct triple roots. The independence proof in Section 2 uses only three nonempty parts and the inclusion rule, so alpha=3 and tau=4 here as well.

An exact-4 complete-module core on at most seven labels again has only one module, now of size six, and needs binomial(6,3)=20 distinct core roots. Twelve slots cannot realize it. These arithmetic values illustrate the symbolic obstruction; they are not results from an executed finite campaign, and no minimality claim for the twelve-root construction is made.

## 6. Consequence for the research direction

Theorem Y remains a valid connectivity result for endpoints of its module type. What fails is the proposed universal strategy of sending every higher-floor endpoint to that type at the same target and within the same root-slot budget. This cannot be repaired simply by a better route, by allowing unused labels, or by replacing the balancing potential: in the constructed carriers there is no permitted terminal module state.

Allowing extra root slots or introducing a different kind of constraint would change the native carrier and is not a repair of this proof. Passing temporarily through a different hitting level does not create a missing exact-q terminal form. The result does not rule out a different argument that intentionally uses non-exact intermediate forms and eventually reaches a different exact endpoint class.

The revised global obligation is to connect higher-floor structures without presuming complete-module availability. Candidate mechanisms must preserve the fixed root-slot budget and the required complementary subset covers while handling cyclic overlap. No theorem that the cyclic family is disconnected, no pair with a proved barrier greater than one, and no universal replacement normal form is established here.

Prior conditional native lifting remains unchanged; width-floor method failure is not native necessity. No numerical execution, implementation certification, efficiency bound, novelty claim or physical implication is made. Independent review should verify all four-set distributions, endpoint exactness, incidence/slack identities, the allowance for unused labels, and the exact slot-count contradiction.
