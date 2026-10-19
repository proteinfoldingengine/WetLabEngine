# Singleton support endpoints determine sector responses without a chosen state encoding

Author: proteinfolding-gpt. Date: 2026-10-18 America/Phoenix.
Source baseline: `a832f8fb242386603963878abed9f792edb1e010`.
Status: AUTHOR ANALYTICAL CONSTRUCTION; INDEPENDENT REVIEW PENDING.
Mathematical support for the accepted source-withdrawal candidate. Native access and event realization remain open.

## 1. Constructive target

The accepted profile-preserving witness has a receiver support {a} before the interaction in both preparations. After the specified source withdrawal commits, nesting forces the receiver support to be {b0} or {b1}. Its common fixed reference is R={a,b0}. Preparation and one complete interaction path preserve the all-one hitting profile.

The earlier grade-to-quantum route sought a native family of input density operators. This support witness permits a weaker target: identify its labels with existing record sectors and establish confinement to the indicated sector. The readout response then follows for every compatible state; no choice of density operator inside a sector is needed.

This does not derive the label-to-sector association. It specifies exactly how little state correspondence would suffice once that association and the actual event are justified.

## 2. Canonical Boolean representation of the supplied palette

For the finite palette P={a,b0,b1}, let C(P) be the algebra of complex functions on P. For S subset P let e_S be its indicator. Then

    e_S e_T = e_(S intersection T),
    e_S <= e_T iff S subset T,
    sum_(i in P) e_{i} = 1.                                (1)

This is the canonical function algebra of an existing finite set, not a physical choice of a basis or a claim that it is the receiver's available algebra.

A positive normalized state omega on C(P) is determined by

    p_i=omega(e_{i}) >= 0, sum_i p_i=1.                     (2)

Say that omega is confined to S when omega(e_S)=1. If S={i}, (2) forces p_i=1 and p_j=0 for j!=i, hence

    omega(f)=f(i) for every f in C(P).                     (3)

Therefore singleton support determines the entire state on this mathematical algebra. For a larger S, all probability vectors supported on S are allowed; no uniform weighting is inferred.

For the accepted witness and f=e_R, equations (2)-(3) give

    initial response = 1 in both preparations;
    completed response = 1 for b0, 0 for b1.              (4)

Equation (4) is a representation consequence on singleton endpoints. It is NOT a general identification between the Boolean claim S intersection R != empty and a measurement probability of one. For example S={a,b1} intersects R, but a state concentrated at b1 has response zero. Nor does this construction derive Born probabilities for intermediate supports.

## 3. Existing record sectors can have arbitrary rank

Suppose an already specified finite-dimensional receiver algebra A_R contains mutually orthogonal projections Z_i, i in P, with sum_i Z_i=I. For the record interpretation these may be existing central sector projections. The calculation below only needs their orthogonality and that the tested effect is actually available.

The label-to-sector correspondence induces the unital Boolean representation

    iota(e_S)=Z_S=sum_(i in S) Z_i.                        (5)

It preserves intersection, inclusion and the unit by direct multiplication. It is uniquely determined once the labelled Z_i are fixed. Equation (5) must be tied to the native labels by inherited sources; choosing the Z_i after seeing the desired answer does not earn a correspondence.

Let rho be any positive trace-one matrix confined to sector Z_i:

    Z_i rho Z_i = rho.                                    (6)

For R={a,b0}, orthogonality gives

    Tr(rho Z_R) = 1 if i in R, 0 otherwise.                (7)

Proof: Z_R Z_i equals Z_i or zero. Substitute (6) and use cyclicity of trace. This proof does not assume purity, rank-one sectors or a preferred microscopic state within a sector.

For a fixed already available binary effect

    E = alpha(I-Z_R) + beta Z_R,  0<=alpha,beta<=1,         (8)

the same calculation yields

    Tr(rho E) = beta if i in R, alpha otherwise.           (9)

Thus any two completed receiver states confined respectively to Z_b0 and Z_b1 give output-law total variation |beta-alpha|. A sharp existing reference effect has alpha=0,beta=1. An imperfect existing effect with alpha!=beta also suffices. The coefficients belong to that actual effect; they are not selected here to manufacture a signal. Availability of E does not imply availability of the sharp Z_R.

Equations (7)-(9) concern one available outcome distribution. They require no algebra-completeness premise, state tomography or repeated independent preparations.

## 4. Compose with the accepted native-support endpoint

A sufficient correspondence for the SAME support witness is now:

1. Native labels a,b0,b1 are associated, by an inherited rule, with fixed existing receiver sectors Z_a,Z_b0,Z_b1.
2. The same complete initial receiver state rho_* occurs in both preparations and is confined to Z_a.
3. The actual event implements the specified support withdrawal, and the actual output state is confined to the sector named by the receiver's resulting singleton support.
4. The fixed separating effect E in (8), or another independently justified separating effect, is actually available to that receiver.

Then the accepted support theorem forces output confinement to Z_b_s. Equation (9) gives initial probability beta in both cases and completed probabilities beta versus alpha. If alpha!=beta, the receiver acquires a distinction.

No map assigning a particular density operator to every native configuration is needed. Arbitrary microscopic states within the forced endpoint sectors give the same result. This replaces an unnecessarily strong full state-assignment target with a support-confinement target; it does not prove confinement from the abstract support notation.

Initial blindness must not be weakened silently. In C(P), the initial singleton fixes the whole algebraic state by (3). In a larger actual A_R with rank-greater-than-one sectors, confinement to the same Z_a does not imply equal full states. For example, two orthogonal pure states within a rank-two Z_a can be distinguished by available internal effects. Hence item 2 requires full initial equality, or a separately proved equality on the entire actually available algebra. Matching the one readout in (8) is insufficient.

The accepted support witness already has identical declared receiver/reference support histories during preparation. Identifying those histories with complete physical receiver states is precisely part of the outstanding correspondence, not a consequence of this theorem.

## 5. What this adds and what remains

The positive advance is state-independent within-sector response: the native singleton endpoint can determine a record statistic without choosing a density-matrix encoding or a probability measure on nonsingleton supports. The common reference R and branch labels are inherited from the accepted witness; they were not fitted in this continuation.

These are elementary Boolean-algebra and projection identities, not a new general theorem or a physical breakthrough. They provide B support for the existing source-withdrawal candidate, and do not claim that the frozen v15.16 encoding has the required sectors or label association.

The v15.11 RAS premise already supplies a retained observable algebra in its declared setting. It need not be rederived from nothing for this conditional construction. What remains is to identify the native support labels and actual event with appropriate sectors and confinement in a particular existing receiver algebra, and to establish availability of a separating effect. Neither the function algebra C(P) nor equation (5) makes those identifications automatically.

The source-withdrawal event remains a joint-completion condition: receiver changes precede the final source deletion. No actuator, copying gate, source-blind policy, outcome law or physical clock is introduced. Actual preparation/event realization remains open.

## 6. Sources and independent review scope

Exact sources at the baseline are preserved in SOURCE_PACKET.json:

- The accepted PROFILE_PRESERVING_RELATIONAL_WITNESS.md and its acceptance receipt: fixed palette/reference, common preparation, forced singleton endpoint and scope.
- v15/v15.11/REPORT.md: supplied RAS/RCR and their retained-record interpretation.
- GPT_DRAFT14_FIXED_EFFECT_FOLLOWUP.md: one existing imperfect effect may suffice; no sharp-readout inference.

Review should reconstruct (1)-(9), challenge every state-support inference, check the rank-two initial-blindness control, and determine whether the proposed sufficient correspondence actually avoids selecting microscopic states while keeping access and enactment open. The earlier acceptance does not cover this new manuscript.

No scientific code, enumeration, numerical campaign, new physical primitive, main merge or numbered-stage closure is claimed. All analytical findings precede any future execution.
