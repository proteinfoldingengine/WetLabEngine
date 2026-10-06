# A12.1 scope — native signed response of admissible relational moves

Date: 2026-10-06 UTC.

Status: prospective analytical physics-bridge scope. No physical force, geometry, energy, metric, probability, numerical campaign, implementation, benchmark, integration merge, or numbered certification is claimed.

Accepted mathematical basis only: the native root/incidence state space and protected target-four band used throughout accepted A11 work. Pending X62-X64 are not dependencies.

## Scientific objective

Define an operational response quantity directly from the relational mathematics:

    how does one legal local incidence change alter the legality of another possible local incidence change?

This is the minimum physics-facing notion of interaction needed before asking for a force law. It must be:
- defined without spatial coordinates or fundamental time;
- invariant under relabeling of roots and labels;
- zero when the first edit does not change the second edit's admissibility;
- signed by whether the first edit enables or suppresses the second;
- derived from the native floor and hitting-number constraints, not fitted to Newton/Einstein behavior.

## Native state and legal moves

Let E=(E_i) be any finite labelled root state with original floors f_i and protected band 3<=tau(E)<=4.

For a root i and label x:
- Add(i,x) is syntactically available when x notin E_i.
- Del(i,x) is syntactically available when x in E_i and |E_i|>f_i.

A syntactically available move is LEGAL when its resulting state still has 3<=tau<=4.

For two distinct-incidence moves e,f such that f remains syntactically defined after e, define the one-step response

    R_E(e->f)=1_legal(f after e)-1_legal(f at E),

provided e itself is legal.

Thus R is in {-1,0,+1}. It is a response of admissible continuation structure, not force magnitude.

## Proposed exact sign law to prove or refute

Use monotonicity of transversal number under componentwise root inclusion:
- adding an incidence can only weakly DECREASE tau;
- deleting an incidence can only weakly INCREASE tau.

Conjectured consequences for every legal e and distinct f:

1. Add -> Add:
       R<=0.
   A legal addition can leave another addition legal or suppress it, but cannot newly enable it.

2. Del -> Del:
       R<=0.
   A legal deletion can leave another deletion legal or suppress it, but cannot newly enable it.

3. Add -> Del:
       R>=0.
   A legal addition can leave a deletion unchanged or enable it, but cannot suppress it.

4. Del -> Add:
       R>=0.
   A legal deletion can leave an addition unchanged or enable it, but cannot suppress it.

Floor effects must be included, especially same-root Add->Del enabling and Del->Del suppression. Do not silently assume distinct roots.

## Derived response objects if the sign law holds

Define the directed response graph on currently syntactically available moves, with edge e->f iff R_E(e->f) !=0.

Define relabeling-invariant scalars:
- suppression degree S_E(e)=#{f:R=-1};
- facilitation degree F_E(e)=#{f:R=+1};
- net signed response Q_E(e)=F_E(e)-S_E(e);
- total response magnitude M_E(e)=F_E(e)+S_E(e).

These are dimensionless combinatorial response observables. They are not energy, acceleration, curvature, charge or physical time.

## Required analytical obligations

1. Prove transversal monotonicity exactly.
2. Prove all four response-sign cases including floor legality and same-root distinct-incidence cases.
3. Characterize when nonzero cross-root response is necessarily GLOBAL-constraint-mediated rather than floor-mediated.
4. Prove covariance of R under arbitrary simultaneous root and label relabeling; prove S,F,Q,M are invariant scalars under that action.
5. Give exact small symbolic examples of:
   - Add suppressing Add through loss of the last pair witness;
   - Del enabling Add by restoring a pair witness;
   - Del suppressing Del through the upper-cover boundary or floor;
   - Add enabling Del through the upper bound or floor.
   Examples are analytical controls, not numerical evidence.
6. Define a paired null: if e leaves both f's root-floor status and the relevant hitting-number legality unchanged, R=0 tautologically. Seek a stronger structural sufficient null if derivable; do not invent locality.
7. State clearly what is still missing for physics: autonomous move selection, composition/coarse-graining, observer-accessible measurement, scale/dimension, and any continuum/geometric law.

## Falsification / boundary

Any counterexample to a sign quadrant refutes the proposed response law. Repair by narrowing assumptions only if the exact cause is identified.

Even a proved signed response law is NOT a force law. The result would establish a native, relabeling-invariant interaction/response structure in the relational state graph. Calling it physical requires an additional operational bridge and selection law.

## Relation to prior response work

Older UQCF response-geometry work may motivate paired perturbation discipline but supplies no theorem here. In particular do not import BKM metrics, graph embeddings, holonomy, GR/ADM variables, or fitted source laws into this A12.1 proof.

v16.54/v16.55 and A11 accepted results remain unchanged. Efficiency work remains separately scoped.
