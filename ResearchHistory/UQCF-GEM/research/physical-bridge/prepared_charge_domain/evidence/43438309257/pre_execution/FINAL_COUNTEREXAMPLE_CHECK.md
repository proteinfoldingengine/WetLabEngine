# Final editorial check of the prepared-input counterexample

**Disposition: no blocker found in section 2.** Checked the final draft at
`package/ResearchHistory/UQCF-GEM/research/physical-bridge/prepared_charge_domain/ARGUMENT.md`
against the explicit algebra. This check uses exact arithmetic and direct
reasoning, without numerical or scientific execution.

The bath spectrum excludes a unit gap. The displayed T is unitary between
`A_0` and `B_0`; the exchange V with the identity on its orthogonal complement
is a global self-adjoint unitary. The identities `Ta=b` and `a perpendicular b`
give precisely C on every source matrix unit, including all coherences. The
receiver is exactly blank for every input because U acts trivially on it.

With the draft's convention `D=KU-UK`, its defect block

\[
B=\frac14\begin{pmatrix}\sqrt{15}&-3\\-5&\sqrt{15}\end{pmatrix}
\]

is correct. It has `Ba=0`. The retained prepared vectors and their images under
`K_SE` are in V's fixed complement, so `DP_L=0` follows as a vector identity on
the entire prepared source subspace.

The proposed companion identity has the correct sign and normalization:

\[
\begin{aligned}
B a_\perp
&=\frac1{4\sqrt8}
  \begin{pmatrix}-\sqrt{75}-3\sqrt3\\5\sqrt5+\sqrt{45}\end{pmatrix}\\
&=\frac1{4\sqrt8}
  \begin{pmatrix}-8\sqrt3\\8\sqrt5\end{pmatrix}
 =2b_\perp.
\end{aligned}
\]

Consequently `D|u,a_perp,0_R>=2|p,b_perp,0_R>` is nonzero. Both companion
vectors are normalized and orthogonal to their corresponding prepared/output
vectors. The separate `B e_0` witness in the draft is also correct.

For input `|u,a,0_R>`, the total-charge distributions in section 2.3 yield:

| Moment | Input: probabilities 3/8 at 1, 5/8 at 5 | Output: probabilities 5/8 at 2, 3/8 at 6 |
|---|---|---|
| First | `(3+25)/8 = 7/2` | `(10+18)/8 = 7/2` |
| Second | `(3+125)/8 = 16` | `(20+108)/8 = 16` |
| Third | `(3+625)/8 = 157/2` | `(40+648)/8 = 86` |

The output-minus-input third-moment difference is `15/2`. All numbers stated
in the draft are exact. The unequal distributions correctly illustrate that
prepared-vector commutation does not entail full spectral conservation when
the prepared support is not charge-invariant.

The scope language is sound: this defeats the specified weakening, leaves
the global PR147 theorem intact, and claims neither a physical implementation
nor a native producing operation. No edit is required for the checked section.
