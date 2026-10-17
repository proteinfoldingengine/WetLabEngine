# Retained transport: invertibility is not norm preservation

Date: 2026-10-17 UTC. Author: proteinfolding-gpt.
Immutable source baseline: `0be10402dfb513cf836c60db2fc5b88f5a957faf`.
Status at freeze: exploratory analytical correction and candidate-specific admission screen; independent review and publication verification pending. No native interaction or numbered-stage closure.

## 1. Candidate, motivation and disposition

The later V1720 retained-bridge report presents a non-associative recombination kernel and a forward-only pruning/non-invertibility property P2 as the source of an irreversible informational arrow. Unlike the V1699.14 diagnostic correction, its accompanying scripts actually update a vector. This is a distinct, concrete lead for the user's native event/acquisition milestone.

The lead fails to establish that milestone in the inspected packet. The kernel, cyclic coordinate operation, coupling and random context draws are supplied. More specifically, the code's fixed-context transport is generically invertible: its non-unitarity and failure under a chosen forward-again operation do not demonstrate non-injectivity. This is a correction to an important inference in this particular source, not another all-NOOP argument.

The useful conclusion is constructive: an exact inverse exists on the nonsingular domain, and its domain and singular exceptions can be specified. This removes an unsupported basis for promoting these scripts to native pruning. It does NOT prove physical reversibility, supply access to the context, exclude information loss after context is discarded, or rule out native interaction elsewhere. Classification for the requested native-mechanism target: C, supplied dynamical model; no A admitted.

All calculations below were obtained analytically before this freeze. No archived scientific module or numerical trajectory was executed, and no historical output was reproduced.

## 2. Exact typed operator

The report and all four inspected scripts define, with indices modulo n,

    T_q(x) = x + g * (Sx ⊙ q - x ⊙ Sq),

where Sx has coordinate (Sx)_i=x_(i-1). Work over exact real vectors, n>=2, finite real g and q. The variable x is the transported vector and q is the context held fixed for this one map. Thus

    T_q(x) = A(q)x,
    A(q) = I + g J(q),
    J(q) = diag(q)S - diag(Sq).

This is linear in x. Randomly generating q in a simulation does not change the injectivity of the conditional map with that q fixed. Whether q or a context history is retained/known is a separate information contract.

The report also defines binary recombination

    op(x,q) = x + q + g * (Sx ⊙ q - x ⊙ Sq)
            = q + A(q)x.

For fixed q it is affine, with the same invertibility criterion. The joint map (x,q) -> op(x,q), where neither input is retained separately, is a different map; section 6 keeps that distinction explicit.

## 3. Determinant, nonsingular domain and exact inverse

In row i, A has diagonal 1-g*q_(i-1) and cyclic predecessor entry g*q_i. For n>=2 the only nonzero permutations in its determinant expansion are the identity and the full cyclic predecessor permutation: choosing any off-diagonal entry forces the preceding row's off-diagonal choice, continuing around the cycle. The n-cycle has sign (-1)^(n-1). Therefore

    det A(q) = product_i(1-g*q_i) + (-1)^(n-1) g^n product_i q_i.

Consequently T_q is invertible exactly when this scalar is nonzero. On that domain the constructive inverse is A(q)^(-1), and the affine inverse of op(·,q) is A(q)^(-1)(z-q). This is standard finite-dimensional linear algebra, not a novel theorem of physics.

For any fixed finite real g, the determinant is a polynomial in q that equals 1 at q=0. It is not the zero polynomial; its zero set has Lebesgue measure zero. Hence ideal absolutely continuous context draws give invertibility with probability one for each step, and a finite sequence of such nonsingular steps has a nonsingular product. This probability statement concerns ideal continuous distributions. It is NOT a certificate about any finite-precision RNG seed, a replay of the scripts, a guarantee of good conditioning, or a physical probability law.

There is also a deterministic sufficient domain:

    ||g J(q)||_infinity <= 2 |g| ||q||_infinity < 1.

The Neumann series then provides an inverse. Thus every context in this explicit neighborhood is invertible, not merely almost every sampled context.

### Exact positive and singular controls

Use the scripts' dimension n=8 and g=17/100.

1. q=e_0. Only A_(0,7)=g and A_(1,1)=1-g differ from the identity. Its determinant is 83/100. With x=e_1,

       T_q(e_1) = (83/100)e_1.

   The map changes the Euclidean norm but is invertible. Its inverse recovers e_1 exactly from that output, conditional on q and g.

2. q=(50/17) * 1. Now A=(I+S)/2. The alternating vector v_i=(-1)^i obeys Sv=-v, so Av=0. This is genuinely singular and rejects the overstatement that every context is invertible.

These are exact hand calculations, not finite sample statistics. The second context is a lawful real vector for the declared formula; no assertion is made that a seeded floating-point Gaussian run produces it.

For a known finite context sequence with forward product A(q_m)...A(q_1), reconstruction applies A(q_m)^(-1) first, then the earlier inverses in reverse order. The overall inverse product is A(q_1)^(-1)...A(q_m)^(-1). This identity supplies no physical permission to perform those inverses.

## 4. The inspected reverse tests do not compute this inverse

V1718's fwd_rev chooses independently generated qi,qj and computes

    fwd = transport(x,qj)
    rev = transport(fwd,qi).

For native_T this compares A(qi)A(qj)x with x. There is no premise or calculation making A(qi)=A(qj)^(-1). A failure to recover therefore tests that chosen two-step protocol, not existence of an inverse.

V1719's alleged non-invertibility defect uses

    back = transport(dx,q)

after dx has already become transport(prev,q). It compares A(q)^2 prev with prev. This tests involutivity, a stronger and different property from invertibility.

For the exact positive control q=e_0, x=e_1 above, this V1719 operation gives

    back = (6889/10000)e_1,
    ||back-x|| / ||x|| = 3111/10000,

although det A=83/100 and true inverse recovery is exact. The control decisively separates the diagnostic from non-injectivity. V1718 would give the same value if qi=qj=e_0; the logical defect of its test does not depend on equality of those contexts.

V1718's loop_drift measures only the final Euclidean norm ratio under a product of forward matrices. An invertible product can change a norm. Conversely, an orthogonal product preserves the norm without returning the vector to its initial value. A ratio of one therefore does not establish state-level loop closure. None of this denies the possibility of path-dependent transport or nontrivial holonomy.

Distance from the initial vector is likewise not a reconstruction error after an inverse has been attempted. V1719's L2 can diagnose displacement but does not by itself measure lost recoverable information.

## 5. What the comparison control actually isolates

The scripts' invertible_T is

    U(q) = exp(g * (J(q)-J(q)^T)/2).

For real J this is orthogonal, hence invertible and Euclidean-norm-preserving. The native A(q) is generally nonorthogonal but can also be invertible, as section 3 proves. Comparing them changes the symmetric generator component and the discretization (I+gJ versus an exponential), not solely injectivity.

Accordingly, the native-versus-invertible comparison can establish behavior relative to that supplied orthogonal comparator. It does not isolate non-invertibility as a causal source. The same reverse protocol with two unrelated U contexts is not generally U(qj)^(-1) either; its inverse is U(qj)^T.

No historical measured ratio, sign fraction or numerical pass/fail is recomputed or withdrawn as data here. What fails is the inference from those diagnostics to proved information erasure or an intrinsic irreversible arrow in the conditional x-map. Non-unitarity is a separate mathematical property and is not disputed.

V1720 reuses this comparator in a component-entropy test. Entropy of normalized squared components is basis-dependent and is not generally invariant under an orthogonal rotation merely because the norm is preserved. No claim about the actual sampled mean of that script is made here; its historical negative thermodynamic disposition is not reopened.

## 6. Retaining the context changes the question

For all nonsingular q, the augmented map

    (x,q) -> (A(q)x,q)

is injective and has the explicit conditional inverse above. Dropping q may make the visible output ambiguous. For example, at the same n=8,g=17/100,

    T_0((83/100)e_1) = T_(e_0)(e_1) = (83/100)e_1.

The two input/context pairs differ, so output alone need not identify the pair. This does not contradict fixed-q injectivity. It also does not derive a physical law that discards q.

Likewise joint binary recombination is noninjective: for any nonzero z,

    op(z,0) = op(0,z) = z.

This preserves the legitimate many-to-one possibility when both operands are forgotten. It prevents interpreting the present finding as proof that every reading of P2 or every recombination operation is invertible. The source report must distinguish this joint reduction from the transport tests, which use T_q and purport to diagnose its pruning. Neither argument establishes a retained receiver contract by itself.

Floating arithmetic, coarse graining, unavailable context, singular steps and restrictions on allowed recovery operations can all change operational recoverability. Their effect must be specified and derived for the claimed native record; they are not supplied by non-norm-preservation alone. The audit does not demand that every mathematically available inverse be physically available.

## 7. Native acquisition and the resulting research decision

The report labels the recombination kernel an assumption. The scripts explicitly choose its cyclic coordinates, g, Gaussian preparation/context sampling and diagnostic readers. They implement a dynamical model, but do not derive the kernel or an accessible receiver's record from the older retained-source/pruning primitives. This is a provenance observation, not a rule that scientific models may have no assumptions.

In particular, none of the inspected transport tests provides an independently justified initially blind receiver, a native event-origin law and a retained source contrast. Replacing the reverse test by a true inverse would correct the mathematical diagnostic, not originate a physical interaction. Adding context erasure, a memory register or a preferred reader to force acquisition would require the very derivation sought by the user.

Stop native promotion of this packet at the supplied kernel/access premises. Preserve its legitimate conditional nonorthogonality and order-dependent model questions. A future eligible lead must specify what is retained and what native event changes that retained description. It may yield a probabilistic or partial consequence without deterministic completion, a quantum carrier, unique full dynamics or gravity calibration.

## 8. Scope, provenance and review

The exact core report and four complete scripts are embedded in source_packet.json and pinned in source_lock.json at the immutable baseline. Their UTF-8 bytes were independently checked against Git blob identities. Historical sources are not edited. The general determinant proof, explicit controls and source tracing are the evidence for this analytical result; finite tests would not establish the theorem.

No scientific simulation, enumeration, numerical campaign, historical replay or increased scientific test count occurs in this checkpoint. Review infrastructure may execute source-integrity/plumbing checks only. The arguments precede the freeze and are not relabelled as prospective predictions.

Required independent review must reconstruct the determinant, sufficient bound and positive/singular controls; distinguish fixed-q, joint and context-forgetting maps; verify the exact source protocols; challenge the physical interpretation in both directions; and preserve all objections. Separate publication auditing and immutable readback follow acceptance.

Native interaction and broad C3/C4-C6 remain OPEN. This is a scoped correction and candidate screen, not an archive-wide no-go, new physical law, empirical result or numbered CLOSED/CERTIFIED stage. Time remains pruning/ordered recoverability update; no fundamental clock, geometry, dark-matter primitive, fit or new update law is adopted.
