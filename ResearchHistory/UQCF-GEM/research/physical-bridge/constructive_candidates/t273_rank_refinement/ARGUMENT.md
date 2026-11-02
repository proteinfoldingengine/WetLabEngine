# T-273 rank refinement — frozen whole-argument review target

Date frozen: 2026-11-02 UTC.
Base scientific SHA: `750554de424a1e12e2d14c6665920bda31163dfc`.
Status before review: POSTED, not adopted. Native bridge **NOT_DERIVED**.

## Provenance and scope

This freezes the strongest positive theorem first posted in [T-272-dot](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6587373426) and independently reconstructed by Grok in [T-273 at `f4f8b3e744c00ae3760e60baaf67019b94b7c96e`](https://github.com/proteinfoldingengine/WetLabEngine/commit/f4f8b3e744c00ae3760e60baaf67019b94b7c96e).

The theorem is conditional on the **SUPPLIED** finite-dimensional benchmark and the **NEW ASSUMPTION** TB. It is not an inherited native-delivery theorem.

## Exact supplied benchmark

Let the system contain orthogonal basis states (|p\rangle,|u\rangle). The supplied channel is
[
C(\rho)=Q\rho Q+\rho_{uu}|p\rangle\langle p|,
]
so for
[
\rho_*=(|p\rangle\langle p|+|u\rangle\langle u|)/2
]
one has (C(\rho_*)=|p\rangle\langle p|).

The supplied joint realization class has finite systems (S,E,R), fixed output dimensions (dim E=d_E), and an arbitrary unitary (U) on (S\otimes E\otimes R). Initially (E) is in (	au_E) of rank (k), and (R) is in a pure blank (|0\rangle\langle0|). A realization satisfies
[
\operatorname{Tr}_{ER}U(\rho\otimes\tau_E\otimes|0\rangle\langle0|)U^\dagger=C(\rho)
]
for every system input (ho).

TB is the new premise that (	au_E) is a finite positive-temperature Gibbs density, hence full rank (k=d_E). The weaker rank-(k) form below does not require Gibbs structure.

## Theorem T273-R

For any realizing unitary (U), if the final (R) marginal on input (ho_*) is pure, then
[
2k\le d_E.
]
Consequently, under full-rank TB ((k=d_E>0)), every realization sends the initially pure (R) to a mixed state on (ho_*).

### Proof

1. The initial total state (ho_*\otimes\tau_E\otimes|0\rangle\langle0|) has rank (2k).
2. Unitary conjugation preserves rank, so the final joint state has rank (2k).
3. Its (S) marginal is (C(ho_*)=|p\rangle\langle p|), which is pure.
4. Any joint density operator with a pure marginal factorizes across that marginal. Hence the final state is
   [
   |p\rangle\langle p|\otimes\omega_{ER}
   ]
   and (operatorname{rank}omega_{ER}=2k).
5. If the final (R) marginal is pure, the same factorization fact gives
   [
   \omega_{ER}=\omega_E\otimes|r\rangle\langle r|.
   ]
   Therefore (operatorname{rank}omega_{ER}=operatorname{rank}omega_E\le d_E).
6. Combining steps 4 and 5 yields (2k\le d_E). For full-rank TB, this would require (2d_E\le d_E), impossible for (d_E>0). QED.

## Entropic companion

On (ho_*), unitary invariance and the pure (S) output give
[
S(\omega_{ER})=1+S(\tau_E).
]
Subadditivity and (S(\omega_E)\le\log d_E) imply
[
S(\omega_R)\ge 1+S(\tau_E)-\log d_E.
]
For full-rank (	au_E), this lower bound need not be strictly positive; the rank theorem is the strict mixedness result.

## Sharp location control

Post-processing covariance remains decisive: if (U) realizes (C), then ((I_S\otimes V_{ER})U) also realizes (C). In the accepted benchmark, the explicit (W_R;\mathrm{SWAP}_{ER}) control leaves the erased-branch record in (E) while the final (R) state equals (	au_E) and has zero source contrast (D_R=0).

Thus T273-R forces a realization-invariant **system-side state change of R under NEW TB**, but it does not show that R owns the erased record. R may carry the bath spectrum rather than the source distinction.

## Explicit non-claims and corrections

- No inherited operation produces TB, the channel (C), the factorization (E\otimes R), the designated receiver algebra, an access law, or a probability law.
- The theorem does not derive native receiver delivery, record location, or event/state/record correspondence.
- (2k\le d_E) is a necessary condition for pure final R on (ho_*), not a general sufficiency theorem for realizing a multi-collision channel.
- The collision-local formula (operatorname{rank}\tau_E\le d_E/f) is not asserted globally. PR #131's multi-fiber extension is challenged by the Choi-rank-three carrier-A counterexample.
- A fixed receiver can realize a finite composite when its dimension reaches the composite Choi rank; fresh slots are sufficient, not necessary at a fixed finite horizon.
- The correct equality condition in PR #130's diagonal entropy comparison is (z_u=0) or (z_o+z_v=0).
- The finite-temperature statement is “the Gibbs density has no zero eigenvalues,” not “the bath has no pure component.”

## Review obligations

The independent reviewer must reconstruct every proof step, test the pure-marginal factorization uses, search for dimension/rank counterexamples, distinguish necessary from sufficient conditions, verify the location control, and grade the physical scope. An ACCEPTED verdict may certify only this conditional theorem and its non-claims. Sharp E-alpha and TB remain NEW; native bridge remains NOT_DERIVED.
