# What source balance forces before a current is selected

Date: 2026-10-14 UTC. Inspected parent: `fb907fefb60ac55b30f219b0321a819ded5452b9`.

**Disposition: exact conditional source-readout criterion; native realization and access not established.** The inherited relation `BJ=s` is a concrete lead that permits a common consequence without choosing a unique current. This note determines exactly which fixed linear receiver interfaces can distinguish two sources for every current allowed by that relation. It then checks the inherited five-node fixture and locates the supplied premises. This is elementary finite linear algebra applied to the research interface, not a priority claim, numerical campaign, or physical-force derivation.

## 1. Inherited input and the question being tested

The v13.25-v13.26 reports preserve retained source balance and conditional current reconstruction from a response. They distinguish these results from observer calibration and physical stress-energy. Their finite control has five nodes, seven edges and three independent cycle directions. The earlier v15.02 report identifies its source fixture as `Tmp/TOE/ThePhysicsParadox/Physics101/phi lab.py`.

That file declares the graph, the source vector, and several current choices. Its strong response probe is `R_full=Z.T`, where columns of Z form an orthonormal basis of `ker B`. Reconstruction uses the known source through a particular current J0. The code computes `R @ J_true` from a supplied hidden-current construction; it does not implement a native receiver acquiring that quantity. We inspect these statements without importing or running the module.

The present question is different from reconstructing a current when its source is already known:

> For two possible source vectors on the same graph, does a fixed receiver output distinguish them independently of the unresolved cycle current?

This does not require a unique microscopic action. The admissible class below is precisely the signed real current class of the inherited balance calculation, with no metric, energy minimization, stochastic law, or extra cycle restriction imposed.

## 2. Exact criterion for a fixed linear interface

Let G be a finite connected graph with an arbitrary fixed orientation. Let B be its vertex-by-edge incidence matrix, with -1 at an edge's tail and +1 at its head. Currents J are real signed edge vectors. A feasible source s has total sum zero. Write

    C(s) = {J : BJ=s} = J_s + ker B.

Let R be the same fixed real linear readout for both preparations, and let y=RJ. The attainable receiver outputs are

    Y_R(s) = R J_s + R(ker B).

The readout is not permitted to inspect s to choose its rows or a decoder. Nor is an actual channel claimed available merely by writing R.

### Proposition 1: source separation with arbitrary cycle freedom

For feasible s0,s1, put delta_s=s1-s0 and choose any delta_J with B delta_J=delta_s. The following are equivalent:

1. `Y_R(s0)` and `Y_R(s1)` are disjoint.
2. `R delta_J` is not in `R(ker B)`.
3. There exist output coefficients lambda and a vertex potential phi such that

       R^T lambda = B^T phi,
       phi^T delta_s != 0.

For these coefficients, every compatible current gives the forced scalar

    lambda^T y = phi^T B J = phi^T s.

Proof. Both output sets are translates of the same vector subspace D=R(ker B), so they are either identical or disjoint. Their displacement is R delta_J; changing the particular delta_J changes that displacement only by D. A vector lies outside a finite-dimensional subspace exactly when a linear functional annihilates the subspace but not that vector. Thus (2) is equivalent to some lambda with lambda^T R z=0 for every z in ker B and lambda^T R delta_J nonzero. The annihilator of ker B is `im B^T`, so this is exactly (3). The displayed forced value follows by substitution. QED.

This also characterizes every linear scalar output invariant under cycle freedom: its edge coefficient belongs to `row(R) intersect im(B^T)`. If the two attainable output sets coincide, no decoder of y alone can guarantee distinguishing the sources across this entire admissible class. This is not a statement about a narrower family selected by an additional derived law, nor about probability distributions that have not been specified.

## 3. Exact criterion when the receiver reads particular edges

Suppose R selects the signed currents on a fixed edge set F. Form the undirected graph containing all vertices and just the UNOBSERVED edges, `G_unobs=(V,E\F)`. Its connected components are C1,...,Ck. Using the underlying undirected graph is essential because currents are signed; edge orientation is a coordinate convention in this calculation.

### Proposition 2: the unobserved-component criterion

The two source preparations have disjoint attainable edge records exactly when

    sum_{v in Ci} delta_s(v) != 0

for at least one unobserved component Ci.

Proof of sufficiency. No unobserved edge leaves Ci. Summing BJ=s over its vertices cancels internal edges and leaves only the observed signed boundary flux:

    L_Ci(J) = sum_{e in F} (1_Ci(head(e))-1_Ci(tail(e))) J_e
             = sum_{v in Ci} s(v).

If its source sums differ, this accessible-coordinate combination separates every pair of compatible currents.

Proof of necessity. Suppose delta_s sums to zero in every unobserved component. The incidence map of a connected component has image equal to the vectors whose entries sum to zero. One can see this directly on a spanning tree by moving each subtree's required net amount through its parent edge. Thus there is a signed current delta_J supported entirely on unobserved edges with B delta_J=delta_s. Given any J in C(s0), J+delta_J lies in C(s1) with exactly the same observed coordinates. The reverse correspondence also holds. Hence the attainable output sets are identical. QED.

All forced linear combinations of the observed coordinates arise from these component boundary sums. Indeed, `B^T phi` vanishes on unobserved edges precisely when phi is constant on each unobserved component. Because the original graph is connected, constants on all vertices give the only redundancy; the space of forced observed linear combinations has dimension k-1.

Consequently an edge interface need not resolve cycles to force a source distinction. It must cut the unobserved routes capable of absorbing that particular source contrast. A component sum can vanish for the actual delta_s even when other source contrasts would be visible; a nonzero interface rank alone is not a pair-specific signal.

## 4. Exact control on the inherited five-node graph

Use the archived edge order, indexed here from zero:

| Edge | Tail to head |
|---|---|
| e0 | 0 to 1 |
| e1 | 1 to 3 |
| e2 | 0 to 2 |
| e3 | 2 to 4 |
| e4 | 4 to 3 |
| e5 | 1 to 2 |
| e6 | 0 to 4 |

The archived source is `s1=(-1,0,0,1,0)`. For this analytical comparison, declare `s0=(-1,0,1,0,0)`: the same unit leaves node 0 and is received at node 2 instead of node 3. This second preparation is an explicit mathematical control, not an archived outcome or a newly derived native preparation. Both source vectors are nonzero and conserve total grade.

Take F={e1,e4}, the two edges entering node 3. The unobserved graph has components {0,1,2,4} and {3}. Hence every compatible signed current obeys

    J_e1 + J_e4 = 0 for s0,
    J_e1 + J_e4 = 1 for s1.

This is a source contrast forced by balance for the entire declared current class, with no current selector. Two edges are the minimum number of RAW EDGE coordinates sufficient for this pair in this graph. To see that a single edge cannot suffice, the underlying graph has two edge-disjoint paths from node 2 to node 3: 2-4-3 and 2-1-3. Deleting any one observed edge leaves those two contrast vertices in one unobserved component, so Proposition 2 applies. This is not a minimum number of arbitrary aggregate measurement channels: a supplied device that directly reads the sum would use one scalar channel.

Explicit positive examples also make clear that no identity operation is being used. Let Q have unit current on e2 and zero elsewhere; then BQ=s0. Let P have unit current on e0,e1, and let H have unit current on e6,e4. Then BP=BH=s1. All three are nonnegative currents along actual paths of the declared graph. The two receiver records for P and H differ, `(1,0)` versus `(0,1)`, but their sum is always 1. The source-zero LABEL here means s0, not a zero source or zero current.

For a negative single-edge control, both 0-to-2 and 0-to-3 have two edge-disjoint directed paths: 0-2 versus 0-1-2, and 0-1-3 versus 0-4-3. For any one observed edge, select one path in each pair avoiding it. The corresponding nonzero currents realize s0 and s1 but both read zero on that edge. Thus the failure of one edge is not merely an all-NOOP example and survives even in these nonnegative path controls.

For F={e1,e4}, the cycle vector P-H has observed coordinates `(1,-1)`. Every circulation has zero sum of those coordinates by the node-3 balance equation. Therefore R(ker B) is exactly the one-dimensional span of `(1,-1)`, so `rank(RZ)=1`, while `dim ker B=7-5+1=3`. Full current reconstruction fails, but the source contrast remains exact. The complete two-coordinate output sets are the parallel lines

    Y_R(s0) = {(t,-t): t real},
    Y_R(s1) = {(t,1-t): t real}.

These are analytical derivations, not numerical outputs or independently enumerated campaigns.

## 5. Why the inherited strong probe answers a different question

The lab's `R_full=Z.T` has `rank(R_full Z)=3`. It resolves every cycle coefficient GIVEN s and a corresponding particular current. That valid conditional reconstruction is preserved.

But as an interface for an UNKNOWN source, its attainable output set is all of R^3 for every feasible s: Z^T maps ker B onto R^3. In particular, taking the orthogonal particular solution gives Z^T J_s=0, and adding arbitrary cycles fills every response value. Proposition 1 therefore gives no uniform source separation for this probe alone.

Conversely, the two-edge cut interface above does separate the two declared sources despite `rank(RZ)=1<3`. Thus the full-cycle rank condition is neither necessary nor sufficient for this DIFFERENT task of guaranteed source discrimination over unrestricted cycle currents. It remains the correct condition for current recovery with the source already supplied. No defect in the lab or earlier conditional theorem follows.

A narrower, independently justified relation between source and cycle current could make the cycle probe source-informative. No such selection or probability law is inferred from the balance equation here.

## 6. What is earned and what still has to become physical

| Item | Status in this screen |
|---|---|
| Retained source identity, relative grade and balance | Preserved within the inherited retained contracts; no absolute observer unit is demanded |
| Particular five-node carrier and edge incidence | Explicit finite fixture in phi lab.py; not a derived physical network |
| Source preparations used above | s1 explicitly supplied by the archive; s0 explicitly supplied analytical control |
| Common readout consequence | Derived for all currents satisfying the stated balance relation and fixed interface |
| Which actual event enforces or realizes such a current | Not established by this inspected lab or the algebraic criterion |
| Receiver access to the edge currents or their sum | Supplied mathematical R; no native detector, record-write or retention mechanism derived |
| Actual receiver initially lacking the source answer | Not established by the static source/current equations |
| Actual record and error contract | Not derived; the exact interface above is a conditional contract |
| Physical force, duration, metric or gravity | Not derived |

In particular, `s(3)` already specifies the net receipt required at node 3. Computing it from a supplied source array is an answer-bearing input calculation, not information acquisition. The nontrivial conditional statement is that a separately available edge record would reveal the same value despite arbitrary cycle freedom. The existence, acquisition and retention of that edge record remain distinct obligations. We do not assume the receiver can read its source entry, the global balance verifier, or the full current.

The native source identity/grade constructions are not discarded because this finite graph is supplied. Rather, their identification with this graph's nodes, current variables and receiver must be established for an actual candidate. The earlier v15.02 carrier audit is not repaired by relabeling these five nodes as quantum sites. This screen uses no quantum identification at all and does not reopen that stopped embedding search.

The exact zero/nonzero cut contrast survives a common positive rescaling of grade. Absolute stress-energy calibration is therefore not required to state this mathematical distinction. Finite error tolerance is a separate requirement: if the declared net source difference is q>0 and each of the two edge readings has absolute error at most epsilon in the same units, the possible sums lie within 2 epsilon of 0 or q. They are disjoint when q>4 epsilon. Neither q in physical units nor such an error bound is supplied by this calculation. Unknown rescaling does not by itself provide a calibrated noise margin.

## 7. Research consequence and stopping rule

The useful change is to the next admission test. Do not demand a unique current, a full-rank cycle probe, or an absolute observer calibration if the intended consequence is a source contrast that a justified interface already forces. For this class, first determine `row(R) intersect im(B^T)` and evaluate it on the ACTUAL source difference; for edge records, use unobserved-component source sums. This tests the information needed for the task rather than reconstructing everything.

The missing next object is an inherited native event-to-receiver realization: bind the actual informational alternatives to the carrier/source variables; justify the realized balance constraint or narrower admissible family; and derive the accessible retained cut record with its own error contract. This could be probabilistic and need not select a unique microscopic current. The source/current arrays and global response calculation in the inspected lab do not provide it.

Do not rerun the supplied current lab, choose a cost metric to pick a current, or label the cut sum itself a new physical law. Do not count another derivation of BJ=s as origin of BJ=s. If new evidence supplies a native relation or restricted current family, evaluate that evidence on its own terms rather than impose the unrestricted signed-current class as a universal physical gate.

**Native milestone: NOT ACHIEVED.** The result is a conditional observability criterion with a concrete positive contrast and rejecting controls. It is neither an archive-wide impossibility nor a claim of newly discovered conservation mathematics. No scientific code was executed, no historical test count increased, and no main merge or numbered-stage CLOSED/CERTIFIED status is claimed. Time remains pruning / ordered recoverability update; no fundamental clock, geometry, dark-matter primitive or gravitational fit is introduced.

Nine exact source texts are pinned in source_packet.json and source_identities.json. The full argument and its claim limits are submitted to independent analytical review; publication provenance is audited separately.
