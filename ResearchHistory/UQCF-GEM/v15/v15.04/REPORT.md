# v15.04 — Equivariant Source-Law Classification / Spectral Freedom Gate

**Status:** CLOSED / measured and archive-bound; final exact-SHA certification pending  
**Primary outcome:** `COVARIANCE_LEAVES_SPECTRAL_SOURCE_FREEDOM`  
**Major structural result:** `true`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`

## Question

Does the already-earned local-frame covariance law

\[
F(U\rho U^\dagger)=U F(\rho)U^\dagger
\]

select a unique operator-valued local source response once quantum-state context is admitted, or does an irreducible spectral response freedom remain? And if covariance leaves freedom, do any already-frozen source axioms remove it without importing downstream physics?

v15.03 had already shown by examples that lawful state-dependent source lifts can be noncentral yet projectively nonunique. v15.04 replaces that example-based observation with an exact classification theorem and then audits the frozen source-law constraints against the remaining freedom.

The result is

\[
\boxed{\texttt{COVARIANCE\_LEAVES\_SPECTRAL\_SOURCE\_FREEDOM}}.
\]

Covariance determines the quantum eigenspaces/direction available to the source law. It does **not** determine the spectral response values. For a qubit, after removing the projectively irrelevant central part, all remaining freedom is exactly one scalar function \(a(r)\) of Bloch radius.

---

# I. EXACT CLASSIFICATION THEOREM

Let \(\rho\) be a faithful finite-dimensional density operator and let

\[
F(\rho)\in\mathrm{Herm}(\mathcal H)
\]

satisfy conjugation equivariance for every local unitary \(U\):

\[
F(U\rho U^\dagger)=UF(\rho)U^\dagger.
\]

Write the spectral decomposition

\[
\rho=\sum_\alpha \lambda_\alpha\Pi_\alpha,
\]

where \(\Pi_\alpha\) projects onto the eigenspace \(E_\alpha\).

Every unitary in the stabilizer of \(\rho\), including every independent block unitary

\[
V=\bigoplus_\alpha V_\alpha,
\qquad V_\alpha\in U(E_\alpha),
\]

obeys

\[
V\rho V^\dagger=\rho.
\]

Equivariance therefore gives

\[
F(\rho)=VF(\rho)V^\dagger
\]

for the full stabilizer. The commutant of the full unitary group on each eigenspace is scalar on that eigenspace, so

\[
\boxed{
F(\rho)=\sum_\alpha \mu_\alpha(\operatorname{spec}\rho)\Pi_\alpha
}.
\]

Thus \(F(\rho)\) is scalar on, and therefore preserves, every spectral eigenspace of \(\rho\). Its maximal eigenspaces may be coarser if distinct \(\rho\)-blocks receive the same output value. In particular,

\[
\boxed{[F(\rho),\rho]=0}.
\]

For nondegenerate \(\rho\), this says \(F(\rho)\) is diagonal in the eigenbasis of \(\rho\). For degenerate \(\rho\), the stronger stabilizer statement matters: mere commutation would allow an arbitrary operator within a degenerate eigenspace, but full conjugation equivariance forces \(F(\rho)\) to be scalar on that whole eigenspace.

Equivariance under basis changes and eigenvalue permutations means the eigenvalue assignment is a real permutation-equivariant spectral function \(\Phi\):

\[
\rho=V\operatorname{diag}(\lambda)V^\dagger
\quad\Longrightarrow\quad
F(\rho)=V\operatorname{diag}(\Phi(\lambda))V^\dagger,
\]

with equal input eigenvalues receiving equal output values.

Conversely, every well-defined real permutation-equivariant spectral assignment with that equal-eigenvalue consistency defines a conjugation-equivariant Hermitian map. No continuity, differentiability, entropy, dynamics, pruning, or time assumption is needed for this classification.

Therefore

\[
\boxed{\texttt{COVARIANCE\_FIXES\_EIGENSPACES\_NOT\_SPECTRAL\_RESPONSE\_VALUES}}.
\]

The numerical controls in this gate corroborate the implementation; they are not the theorem's foundation.

---

# II. QUBIT COROLLARY

For

\[
\rho=\frac12(I+\mathbf r\cdot\boldsymbol\sigma),
\qquad r=|\mathbf r|<1,
\]

conjugation equivariance implies

\[
F(\rho)=c(r)I+a(r)\left(\rho-\frac12I\right).
\]

At the traceless/projective source level, the central term disappears, leaving

\[
\boxed{
F_{\rm traceless}(\rho)=a(r)\left(\rho-\frac12I\right)
}.
\]

The maximally mixed state \(r=0\) has no nonzero traceless equivariant direction, so the traceless part vanishes there. Away from \(r=0\), covariance selects the Bloch direction but leaves \(a(r)\) arbitrary.

This gives an exact explanation of the v15.03 candidate behavior.

## Linear versus square

For every qubit density matrix,

\[
\rho^2
=\frac14\left[(1+r^2)I+2\mathbf r\cdot\boldsymbol\sigma\right]
\]

and

\[
\operatorname{Tr}\rho^2=\frac{1+r^2}{2}.
\]

Hence

\[
\boxed{
\rho^2-\frac{\operatorname{Tr}\rho^2}{2}I
=\rho-\frac12I
}.
\]

So the centered linear and square laws are not merely numerically close: for qubits they are exactly the same operator law.

The executed maximum identity error was

`7.850462293418876e-17`.

## Logarithmic law

The qubit eigenvalues are \((1\pm r)/2\). Therefore

\[
\log\rho-\frac{\operatorname{Tr}\log\rho}{2}I
=\operatorname{artanh}(r)\,\hat{\mathbf r}\cdot\boldsymbol\sigma.
\]

Relative to \(\rho-I/2=(r/2)\hat{\mathbf r}\cdot\boldsymbol\sigma\),

\[
\boxed{
a_{\log}(r)=\frac{2\operatorname{artanh}(r)}{r}
}.
\]

The executed maximum formula error was

`1.2412670766236366e-16`.

This response is nonconstant and strictly increasing for \(0<r<1\). Therefore unequal local spectra generally change the relative source weights compared with the linear law.

---

# III. EXACT GLOBAL PROJECTIVE-RAY CONSEQUENCE

On the supplied graph-site carrier, define

\[
\Delta_i=\iota_i\!\left(\rho_i-\frac12I\right)
\]

and

\[
P_a(s,\rho)=\sum_i s_i a(r_i)\Delta_i.
\]

The nonzero embedded single-site traceless terms are Hilbert-Schmidt orthogonal across distinct sites. Since each \(P_a\) is traceless, projective equivalence

\[
P_a\sim cP_b+bI,
\qquad c>0,
\]

reduces to \(b=0\), and orthogonality gives the exact coincidence criterion:

\[
\boxed{
[P_a]=[P_b]
\iff
\exists c>0:\ a(r_i)=c\,b(r_i)
\ \text{for every source-support site }i
}.
\]

Thus unequal source-support radii plus a nonconstant ratio \(a(r)/b(r)\) split the global projective ray.

For the frozen source \(s=(-1,0,0,+1,0)\), only sites `0` and `3` contribute.

Control A has source-support radii

\[
(0.15,0.63),
\]

with

\[
a_{\log}=(2.015205812486224,\ 2.353702044702441).
\]

Control B has source-support radii

\[
(0.52,0.47),
\]

with

\[
a_{\log}=(2.2166913652661258,\ 2.1705120706949246).
\]

Because these coefficient pairs are not common positive multiples of the linear pair \((1,1)\), the linear and logarithmic projective rays are **exactly distinct** in both controls.

The measured residuals were

- A, linear vs log: `0.032643436536906496`;
- B, linear vs log: `0.010460821683241906`.

Those reproduce the frozen v15.03 values to `9.020562075079397e-17` and `6.418476861114186e-17`, respectively.

A third independently declared witness

\[
a_{\rm poly}(r)=1+r^2
\]

also gives distinct rays:

- A, linear vs polynomial: `0.061186205628391485`;
- B, linear vs polynomial: `0.01972566676052767`.

So nonuniqueness is not special to choosing `log rho` as the alternative.

---

# IV. FROZEN-AXIOM AUDIT

The audit bound the already-frozen source-law constraints carried by v13.26, v14.03, and v15.03 and asked whether they impose a functional equation on \(a(r)\).

The tested frozen requirements were:

1. retained source amount/extensivity and homogeneous source-current scaling;
2. positive projective source rescaling;
3. independent local-unitary/frame covariance;
4. additivity/linearity in the retained scalar source coefficients;
5. null-source compatibility.

All three witness laws—linear, logarithmic, and \(1+r^2\)—satisfy all of them simultaneously.

Worst executed errors were:

```text
max local-unitary covariance error       = 3.434312402059545e-16
max null-source norm                     = 0.0
max positive-scale projective residual   = 2.603703785810335e-16
max source-additivity error              = 3.510833468576701e-16
max source-homogeneity error             = 1.7763568394002505e-15
```

The key distinction is structural. Source extensivity/additivity constrains how the operator responds to the scalar coefficients \(s_i\); it does not, by itself, impose a functional equation on the state-spectrum dependence \(a(r)\). For any fixed lawful \(a\),

\[
P_a(s+t,\rho)=P_a(s,\rho)+P_a(t,\rho)
\]

and

\[
P_a(cs,\rho)=cP_a(s,\rho).
\]

Likewise, local-unitary covariance holds for every spectral \(a(r)\) because \(r\) is conjugation invariant and \(\rho-I/2\) transforms covariantly.

The audited dependencies contain no certified tensor-state composition functional equation for this source map. A new condition such as a monoidal/tensor composition law could reduce the spectral freedom, but unless such a law is independently recovered from the frozen ontology it would be a **NEW ASSUMPTION**, not a consequence of covariance or existing source extensivity.

Therefore

\[
\boxed{\texttt{FROZEN\_SOURCE\_AXIOMS\_DO\_NOT\_SELECT\_SPECTRAL\_RESPONSE\_FUNCTION}}.
\]

and

\[
\boxed{\texttt{NO\_UNIQUE\_A\_OF\_R}}.
\]

---

# V. RELATION TO v15.03

v15.03 measured lawful nonuniqueness on two frozen controls. v15.04 shows why it had to occur.

The v15.03 linear/square near-zero residuals are now explained by an exact qubit identity. The v15.03 linear/log nonzero residuals are now explained by the exact spectral response coefficient

\[
a_{\log}(r)=2\operatorname{artanh}(r)/r
\]

combined with unequal source-support spectra.

Thus

`V15_03_NUMERICS_ARE_ILLUSTRATIONS_OF_V15_04_THEOREM`.

This is stronger than saying that three candidate functions happened to disagree. It classifies the full conjugation-equivariant local source-law family and isolates the precise missing datum: a principle that selects the spectral response values.

---

# VI. INTERPRETATION

The source-law obstruction has now been localized one level further.

State-independent retained scalar/current data have no internal quantum-frame direction and are forced into the center by independent local gauge (v15.03). Quantum-state context supplies a lawful direction because the state itself carries frame-covariant spectral projectors. But the same covariance that permits that direction does not determine how strongly different spectra should be weighted.

For qubits, the unresolved freedom is exactly

\[
a:[0,1)\to\mathbb R.
\]

So the missing operator-valued source principle is not merely “pick an operator.” It must supply a lawful reason for the spectral response function—or a stronger composition law that derives it—without choosing the function because it improves a downstream gravity, ADM, Einstein, cosmology, or empirical score.

This gate does **not** show that no deeper law can select \(a(r)\). It shows that local-unitary covariance plus the audited frozen source constraints do not.

---

# VII. UNRESOLVED PHYSICAL CLAIMS

v15.04 does **not** derive:

- a unique operator-valued source response law \(a(r)\);
- a certified exact retained-node-to-quantum-site factorization;
- a natural graph-site-to-`C^125` compatibility-parent map;
- Genesis/provenance selection of a spectral response law;
- an absolute source magnitude or observer source calibration;
- physical stress-energy;
- a source-to-coframe/solder law;
- physical metric or spacetime;
- an absolute gravitational coupling;
- Einstein equations;
- a physical time primitive;
- Pillar 3 closure.

The primitive/pre-pruning ontology remains atemporal. No entropy, pruning, or physical time is used as a source-law selector in this gate.

---

# Stop rule

Do not continue by privileging `log(rho)`, linear `rho`, or any other \(a(r)\) because of downstream PGRL/ADM/Einstein/gravity behavior.

The lawful next question is narrower:

> Does the frozen ontology independently contain a **state-composition / monoidal / functional law** strong enough to constrain the spectral response \(a(r)\)?

If such a law is found, it must be hash-bound and tested upstream of all gravitational targets. If no such frozen law exists, the current branch should stop with the operator-valued spectral response law marked irreducible relative to the frozen source axioms, and any chosen \(a(r)\) must enter explicitly as **NEW ASSUMPTION**.

## CI evidence before archive binding

TDD RED:

- SHA `8353235929180cb8ecb7a5a50bdf6df7fb3b0d31`
- workflow run `34762496996`
- job `103737656392`
- intended `ModuleNotFoundError: equivariant_source_law_audit`

First implementation GREEN:

- SHA `b78add449ed5daca2d70b3fcbe774f29ec657ad3`
- workflow run `34762622049`
- job `103737982559`
- SUCCESS

Telemetry exposure GREEN:

- SHA `c4a9edf15be8c6317c274e8443cb24237d199256`
- workflow run `34762688828`
- job `103738165948`
- checker step SUCCESS; full deterministic telemetry exposed for `SUMMARY.json` binding

Final exact-SHA certification is performed after `SUMMARY.json`, this report, checker binding, and research index/status updates are frozen.
