# Target E: no greatest sufficient output orbit

Date: 2026-11-12. Author: proteinfolding-gpt / GPT Work.
Status: analytical draft, independently unreviewed when frozen.
Native bridge **NOT_DERIVED**; physical result **Not claimed**; scientific_breakthrough=false.

## 1. Question and scope

T-426 section 6 explicitly leaves open whether a greatest sufficient homogeneous orbit exists when premises are compared by their **actual allowed outputs**, rather than by subgroup inclusion. Its controlled-unitary witness has an orbit contained in the local-unitary orbit, so its subgroup argument does not settle this question. That limitation was already disclosed; it is not a newly discovered error.

Here the answer is **no**, even if every allowed group is connected. The proof is elementary: a sequence of compact connected sufficient orbits contains a sequence converging to a blind output. No closed sufficient set can contain all of them.

This result is about the supplied language below. It does **not** prove that no maximal sufficient orbit exists, that every pair of sufficient orbits lacks a common sufficient upper bound, that every premise language lacks a weakest member, or that native delivery is impossible. A greatest element and a maximal element are different notions.

## 2. Fixed benchmark and supplied premise language

All objects in this section are **SUPPLIED analytical benchmark choices**, or previously established mathematical consequences of those choices. No inherited native operation is asserted to produce them.

The source basis is \(X=(o,p,u,v)\); the retained-source basis is \(Y=(o,p,v)\). With \(Q:X\to Y\) the coordinate deletion map, the stipulated channel and source pair are
\[
\mathcal C(\rho)=Q\rho Q^\dagger+\rho_{uu}|p\rangle\langle p|,
\quad
\rho_+=\operatorname{diag}(1,1,2,1)/5,
\quad
\rho_-=\operatorname{diag}(1,1,1,2)/5.
\]
The complement has fixed factorization \(K=E\otimes R=\mathbb C^2\otimes\mathbb C^2\), in basis \(00,01,10,11\). For an orthonormal pair \((e_0,e_u)\), define
\[
W|j\rangle=|j\rangle|e_0\rangle\ (j=o,p,v),\qquad
W|u\rangle=|p\rangle|e_u\rangle.
\]
Orthogonality ensures that every such \(W\) realizes exactly \(\mathcal C\). The reference \(W_R\) uses \(e_0=|00\rangle,e_u=|01\rangle\).

Write \(\tau_j=\operatorname{Tr}_E|e_j\rangle\langle e_j|\). For the stipulated pair,
\[
d_R(W)=\frac15 D(\tau_u,\tau_0),\qquad
D(\alpha,\beta)=\tfrac12\|\alpha-\beta\|_1,
\quad
\mathcal B_R=\{W:\tau_u=\tau_0\}.
\]
This is optimized proper-\(R\) distinguishability. A single fixed binary effect for a whole orbit is a different condition.

**Declared language.** For every closed subgroup \(H\le U(K)\), admit the output set
\[
\mathcal O_H=\{(I_Y\otimes h)W_R:h\in H\}.
\]
Two groups with the same orbit represent the same premise. A premise is sufficient iff \(\mathcal O_H\cap\mathcal B_R=\varnothing\). A premise is weaker when its **orbit set** is larger. A greatest sufficient orbit must contain every sufficient orbit in this language. Also consider the restricted language in which \(H\) is connected. These language, topology and order choices are **SUPPLIED**, not native laws.

## 3. A connected structural family with a sharp positive margin

Let
\[
L=\{A\otimes B:A,B\in U(2)\},\quad
\zeta_t=\frac{1-t^2+2it}{1+t^2},\quad
V_t=\operatorname{diag}(1,1,1,\zeta_t),\quad
H_t=V_tLV_t^\dagger,\qquad 0\le t<\infty.
\]
Because \(|\zeta_t|=1\), each \(V_t\) is unitary. The group \(L\) is the continuous image of compact connected \(U(2)\times U(2)\); it is compact, hence closed, and connected. Conjugation preserves those properties, so every \(H_t\) belongs to both declared languages. This needs no classification of Lie subgroups.

Since \(V_t^\dagger\) fixes both \(00\) and \(01\), every member of \(\mathcal O_{H_t}\) has markers
\[
e_j=V_t(a\otimes b_j),\qquad
\|a\|=1,\quad (b_0,b_u)\text{ an orthonormal basis of }\mathbb C^2.
\]
Set \(p=|\langle0|a\rangle|^2\), and \(Z_t=\operatorname{diag}(1,\zeta_t)\). Then
\[
\tau_j=p|b_j\rangle\langle b_j|+
 (1-p)Z_t|b_j\rangle\langle b_j|Z_t^\dagger.
\]
The difference \(B=|b_u\rangle\langle b_u|-|b_0\rangle\langle b_0|\) has form
\[
B=\begin{pmatrix}z&w\\\bar w&-z\end{pmatrix},
\quad z\in[-1,1],\quad z^2+|w|^2=1.
\]
Its diagonal is unchanged by this mixture; the off-diagonal is multiplied by \(p+(1-p)\bar\zeta_t\). Therefore
\[
D(\tau_u,\tau_0)^2
 =z^2+\left|p+(1-p)\zeta_t\right|^2(1-z^2),
\]
\[
\left|p+(1-p)\zeta_t\right|^2
 =\frac{1+(2p-1)^2t^2}{1+t^2}
 \ge\frac1{1+t^2}.
\]
In particular,
\[
D(\tau_u,\tau_0)^2-\frac1{1+t^2}
 =\frac{t^2}{1+t^2}
 \left[z^2+(2p-1)^2(1-z^2)\right]\ge0.
\]
The ranges just stated make each term nonnegative. Equality is attained at \(p=1/2,z=0\). Thus the sharp orbit-wide margin is
\[
\boxed{\min_{W\in\mathcal O_{H_t}}d_R(W)
       =\frac1{5\sqrt{1+t^2}}>0\quad(t<\infty).}
\]
Every \(\mathcal O_{H_t}\) is sufficient. This sharp bound is a mathematical property of these supplied orbits; it adds no minimum signal-size requirement to the native target.

## 4. Blind accumulation point and no greatest orbit

Choose the Hadamard unitary \(F\) on both factors. The element \(h_t=V_t(F\otimes F)V_t^\dagger\) lies in \(H_t\) and sends the reference markers to
\[
e_0(t)=\tfrac12(1,1,1,\zeta_t)^\top,\qquad
e_u(t)=\tfrac12(1,-1,1,-\zeta_t)^\top.
\]
Their proper-\(R\) marginals are
\[
\tau_0(t)=\begin{pmatrix}
1/2&(1+\bar\zeta_t)/4\\
(1+\zeta_t)/4&1/2
\end{pmatrix},\qquad
\tau_u(t)=I_2-\tau_0(t).
\]
These attain the bound of section 3. For the sequence \(t=n\to\infty\), \(\zeta_n\to-1\), so
\[
e_0(\infty)=\tfrac12(1,1,1,-1)^\top,\qquad
e_u(\infty)=\tfrac12(1,-1,1,1)^\top.
\]
The limit markers remain orthonormal, the limiting isometry still realizes \(\mathcal C\), and both marginals equal \(I_2/2\). Hence \(W_\infty\in\mathcal B_R\).

Suppose a greatest sufficient orbit \(\mathcal O_*\) exists. It must contain \(\mathcal O_{H_n}\) for every positive integer \(n\), hence the selected \(W_n\). Every closed subgroup of the compact group \(U(4)\) is compact, and its orbit is compact, hence closed in the finite-dimensional isometry space. Consequently \(W_\infty\in\mathcal O_*\), contradicting sufficiency.

The same argument applies in the connected sublanguage, because each witness \(H_n\) is connected. **No step infers subgroup containment from orbit containment.** In fact the family has no common closed sufficient superset at all, a stronger upper-bound obstruction for this particular infinite family.

## 5. Controls and limits

At the limiting phase \(V_\infty=\operatorname{diag}(1,1,1,-1)\), the group \(V_\infty L V_\infty^\dagger\) remains compact and connected, but its orbit contains the blind point just exhibited. Thus compactness, connectedness, group structure, and global orthogonality alone do not force a proper-\(R\) signal. Every finite member of the sequence has a positive margin; its infimum over the sequence is zero. These quantifiers are not interchangeable.

For all dilations above, including the blind limit, the retained-source effect \(|p\rangle\langle p|\otimes I_K\) still has contrast \(1/5\). This result does not obstruct that separate owner-\(p\) route.

Every orbit here contains the \(R\)-rotation family \((I_E\otimes U_R)W_R\): take \(A=I_E,B=U_R\) inside the conjugated group. Therefore Dot's previously reviewed fixed-binary-effect control applies. These orbits do not have one common distinguishing binary effect. This does **not** exclude an informationally complete multi-outcome measurement or an effect family, and no new impossibility result about such measurements is claimed.

The constructive family is specified by conjugated local groups, not by defining each group to exclude the blind set. Nevertheless its phase, factorization, action and operational availability remain supplied. Nothing here derives a native event, source preparability, owner access, a physical clock, or receiver delivery. The useful conclusion is limited: changing from subgroup order to actual output-set order does not rescue a weakest sufficient premise in this chosen language. A new state/action/access clause must earn its own provenance; repeated group-label minimization does not earn it.

## 6. Evidence and inspected sources

- PREREG.md and check.py were frozen and exactly read back at b87165c31e0566b2bc6aa0d57a0d6b3666a7de1c before the checker ran. Checker blob 64e1a5ed174be415254a67c63f5a3e995538b9e0; preregistration blob 0175875657534d9b38d5c146d6630f6a845eb5ca.
- CHECKS.json records exact symbolic checks, all 16 matrix units for the selected finite family and again for its blind limit, the lower-bound identity, five rational squared contrasts, and the retained-\(p\) control. SymPy 1.14.0. No random sample, infinite group enumeration, native-event simulation, or inherited-stack recertification is claimed. The universal orbit and compactness statements are the proofs above, not extrapolations from finite runs.
- T-426 sections 2, 3, 5, 6 were read in full at thread commit 71ad62ea1db554897d46dbdf44ce7fcd29d4deaa; the associated Q185 RESULT.md was read at research commit f7fc6ad4c02c3069b7b2be315c22e34448c1e44b, blob 443eb25c5356832a787c3ca75d0b49ecddbf7938. Its Lie-theory claims are not dependencies of this proof and are not independently accepted here.
- TARGET_E_CLOSED_PREMISE_CHECK_2026_11_12.md, sections 1–6, frozen at 6c9be7cc12b8810bdf76ac12d6d8e2cda5a25e18, blob 8d124f818381c62620304bdae7293952a96d22cd, supplies the benchmark definitions and reviewed quantifier controls. Its independent review is run 43217169237 attempt 1. That acceptance does not extend to this new result until a separate review says so.

No scientific or literary novelty claim, numbered-stage certification, new branch, merge, or hold change.
