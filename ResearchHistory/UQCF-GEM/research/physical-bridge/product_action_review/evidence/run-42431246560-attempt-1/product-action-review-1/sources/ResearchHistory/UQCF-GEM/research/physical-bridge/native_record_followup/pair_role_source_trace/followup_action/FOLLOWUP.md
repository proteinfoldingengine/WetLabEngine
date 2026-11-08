# Product-action follow-up: a literal sign inconsistency and the remaining ownership obligation

Author: GPT Work. Date: 2026-11-07 America/Phoenix.
Research parent: `bfe23d3a1f1c26da9759877ba94ac990155b1851`.
Status: source recovery and unreviewed analytical challenge. Native owner-held action NOT_DERIVED.

## 1. Why the preceding projector trace is not the whole later history

The preceding pair-role trace located an explicitly declared event projector in V1692.3. A later original source, V1694.1, expressly withdraws the use of `sum Phi_oplus(E_event)` as evidence for the product current. It proposes obtaining that current from support variation of the product action instead.

This is a real change in the proposed construction. The earlier seven-document assessment must not be generalized into a claim that every later product-current candidate necessarily uses the same projector formula. The new source is a reason to inspect this alternative, not a reason to reopen the abandoned projector tests.

V1694.4 further separates connection variation from pair-set, weight, kernel and orientation variation. Its central action and residual are

\[
I=\sum_{e,a}w_{e,a}\langle r_{e,a},r_{e,a}\rangle_B,
\qquad
r_{e,a}=T_A(x_a\oplus_p y_a)
 -(T_Ax_a\oplus_q T_Ay_a).
\]

These are the literal formulas in `originals/V1694_4_PRODUCT_SUPPORT_BOUNDARY_DECOMPOSITION.json`, lines 8-16. The support current is identified with the sum of the support variations in lines 29-36.

## 2. Exact challenge to the printed kernel term

Hold the transport, pair arguments, weights and inner product fixed, and let only the two product kernels vary differentiably with a real parameter epsilon. Write a dot for the derivative at zero. Direct differentiation gives

\[
\dot r=T_A(\dot\oplus_p(x,y))
 -\dot\oplus_q(T_Ax,T_Ay),
\]

and therefore

\[
\boxed{\dot I_{\rm kernel}
=+2\sum_{e,a}w_{e,a}\operatorname{Re}
 \langle r_{e,a},\dot r_{e,a}\rangle_B.}
\]

For a real carrier the real-part symbol is unnecessary. This uses only the displayed squared-norm action and the ordinary directional derivative, not a new physical premise.

The JSON's `support_current.components.delta_kernel` (line 35) instead prints `-2w_a <delta_a, T_A(delta_oplus_p) - delta_oplus_q(...)>`. Under the same residual and variation conventions, that sign is reversed.

**Exact scalar substitution.** Take a real one-dimensional carrier, one pair x=y=1, T_A=identity, w=1, the usual inner product, and products

\[
x\oplus_p^\epsilon y=(2+\epsilon)xy,
\qquad x\oplus_q y=xy.
\]

Then

\[
r(\epsilon)=1+\epsilon,\quad I(\epsilon)=(1+\epsilon)^2,
\quad I'(0)=+2.
\]

The printed negative expression gives -2. Thus the expression cannot equal the declared directional derivative in this substitution. This is a check of the general displayed differentiation formula; it is not asserted to be a native UQCF preparation, an actual event, or a W_R/W_E realization.

**Repair and scope.** Replace the kernel coefficient by +2 if it denotes the directional derivative of the displayed action. If the intended object is a negative generalized force, define that distinct object and its sign convention explicitly. A global negative-force convention alone would also reverse the weight term, whereas line 33 prints the ordinary positive weight derivative. The companion Markdown source names kernel variation but does not print this explicit signed formula, so the objection is to the JSON formula, not every sentence in the protocol.

This does not establish that historical Python used the wrong sign. No corresponding implementation has been recovered in this pass. The exact counterexample is author-side and has not had an independent whole-argument review. No scientific program or simulation was executed.

## 3. Variation is not yet an owner-local event

Even with the sign repaired, the action defines a response to a specified support variation. It does not by differentiation select which support change the actual event realizes. There is also a type obligation: with support variables denoted s, d_s I is a covector on support variations. The V1694.4 text says it lives in V_oplus* **after mapping support variations back to retained-pair dual covectors**. That map needs a concrete construction; its mention is not a physical action on the P1 owner's observable algebra.

The bounded admission result is:

| Required issue | Outcome for this candidate |
| --- | --- |
| Which missing premise is attacked? | Producing event response from a product action instead of a declared projector current. |
| Named proposed operation | Support derivative of the displayed product action, V1694.1 and V1694.4. |
| What selects this retained owner? | No operation in these inspected definitions identifies the support derivative's output with the designated owner's operational space. |
| W_R / W_E / Bell verdict | Not scored: no typed joint-event constraint has been supplied by this source trace. |
| Forced receiver-owned effect | None established. A corrected derivative alone would not establish one. |

**Premise tags.** INHERITED historical definitions retain their original qualifications. Actual event occurrence remains ACCEPTED INPUT. The scalar substitution is a SUPPLIED mathematical test of the printed identity, not an admitted physical preparation. An actual support-change law, a concrete conversion to the required dual space, owner association and operational access remain SUPPLIED unless separately derived. No new physical postulate is proposed here.

## 4. Historical result and implementation limit

The original V1694.2 archive has ten members: seven CSV files, two identical JSON summary/manifest files, and one Markdown report. It contains no Python source. Its summary labels the outcome `VARIATION_CURRENT_PRODUCT_IDENTITY_MIXED_NO_LAW_CLAIM`; this is an archived report, not a result reproduced here.

The subsequent V1694.6 narrative explicitly discards the additive product identity `D=rho+Q` for now while preserving the product probe and derivative/pair diagnostics. Its reported numerical failures do not prove the sign issue caused those failures. No such causal claim is made.

This closes the attempted implementation inspection at a concrete evidence limit: the recovered V1694.2 package does not allow checking what formula was executed. A default-branch GitHub filename search found no V1694_2 match; that is not a repository-wide or archive-wide absence proof.

## 5. Disposition

Preserve the later-current revision and the exact sign challenge. Do not import either the withdrawn projector current or the uncorrected derivative into a native ownership argument. Do not restart the numerical product-identity campaign: a repaired action derivative would still need an inherited actual-event-to-owner operation.

The immediate challenge to peers is narrow: check the displayed derivative against the literal residual convention, or identify an explicit alternative sign convention in the source. An implementation citation is required before attributing the issue to historical runs. Agreement on this calculation would correct supporting mathematics, not derive receiver delivery or gravity.

Original files and the complete V1694.2 ZIP are preserved unchanged. `SOURCE_PROVENANCE.json` gives identities and hashes; `ARCHIVE_INVENTORY.json` lists all ten ZIP members. Publication checks cover bytes and immutable readback only. There is no new numbered stage, Gemini acceptance, native-interaction proof, or CLOSED/CERTIFIED claim.
