# Sprint E — Equations Visibility Note
## UQCF-GEM retained-coherence bridge
## AI peer-review math spine

## Purpose

This note makes the current bridge mathematically inspectable in one place.

It separates the framework into three layers:

1. **Assumed structure**  
2. **Derived relations**  
3. **Empirically selected / numerically certified relations**

This is not a final theory paper. It is the explicit equation spine needed for AI peer review.

---

## 1. Core variables

The current bridge uses the following reduced variables:

- \(\gamma\): dimensional deficit
- \(\sigma\): effective retained diffusion / spectral response observable
- \(\chi\): screened pruning-flow rate
- \(W_{\rm nl}\): active nonlocal share
- \(\eta\): participation variable underlying \(W_{\rm nl}\)
- \(m\): retained backbone exponent
- \(x_{\rm diff}\): lagged diffusion exponent

Microscopic variables:

- \(q_n\): shell-level retained weight
- \(r_{n,a}\): microstate amplitude / radial-microstate weight
- \(K_{(n,a),(m,b)}\): shell–microstate coupling kernel

Observable-layer variables:

- \(E_0(z)\): baseline expansion proxy
- \(E_{\rm bridge}(z)\): bridge-modified expansion proxy
- \(D_M(z)\): comoving-distance proxy
- \(F_{AP}(z)\): Alcock–Paczynski-style proxy

---

## 2. Assumed reduced-law structure

These relations are currently **assumed as the bridge law family**, not yet derived from a fundamental action.

### 2.1 Nonlocal share
\[
W_{\rm nl}=\frac{\eta}{1+\eta}.
\]

### 2.2 Screened pruning-flow law
\[
\chi = \left(1-\frac{\gamma}{d_{\rm eff}}\right)W_{\rm nl}.
\]

This is the baseline screened-flow law.

### 2.3 Retained backbone exponent
\[
m = 1 + \chi.
\]

### 2.4 Lagged diffusion law
Baseline form:
\[
x_{\rm diff}
=
\chi - \frac{\gamma/d_{\rm eff}}{d_{\rm eff}-0.8}.
\]

Selector-refined form from Sprint A:
\[
x_{\rm diff}
=
\chi - \lambda\frac{(\gamma/d_{\rm eff})^{q}}{d_{\rm eff}-0.8}.
\]

Best current selector refinement:
\[
\lambda \approx 1.4,\qquad q \approx 0.75.
\]

### 2.5 Reduced fixed-point map
\[
F(\gamma)=\gamma_{\rm next}(\gamma)-\gamma
=1-\sigma(\gamma)-\gamma.
\]

The fixed-point condition is
\[
F(\gamma_*)=0.
\]

---

## 3. Derived reduced relations

These follow from the assumed bridge structure.

### 3.1 Closure point
At closure,
\[
\gamma_* \approx 0.26671093,
\]
\[
\chi_* \approx 0.40117290,
\]
\[
m_* \approx 1.40117290,
\]
\[
x_{{\rm diff},*} \approx 0.37911244.
\]

### 3.2 Raw bridge observable amplitude
The first observable-layer amplitude was defined from the closure mismatch
\[
A_{\rm bridge}=\chi_* - x_{{\rm diff},*}.
\]

Numerically,
\[
A_{\rm bridge} \approx 0.02206046.
\]

This is currently a **derived closure scalar**, not an independent fit parameter.

---

## 4. Upstream selector flow (Sprint A)

These equations define the current upstream relaxation / selector system.

### 4.1 Screening target
\[
\chi_{\rm target}
=
\left(1-\frac{\gamma}{d_{\rm eff}}\right)W.
\]

### 4.2 Participation target
Participation is induced from the current backbone:
\[
m = 1 + \chi.
\]

With shell continuum \(s\), backbone weight:
\[
C(s) \propto s^{-m}.
\]

Normalized shell probability:
\[
p(s)=\frac{C(s)}{\int C(s)\,ds}.
\]

Shape-weighted participation:
\[
Q_{\rm shape}
=
\left(\int C(s)\,ds\right)
\left(\int w(s)p(s)\,ds\right),
\]
with
\[
w(s)=\exp\left[-\frac{1}{2}\left(\frac{\log_2 s - \mu}{\sigma_w}\right)^2\right].
\]

Then
\[
\eta = \frac{Q_{\rm shape}}{Q_0 + Q_{\rm shape}},
\qquad
W = \frac{\eta}{1+\eta}.
\]

So the induced participation target is
\[
W_{\rm target}=W(\chi).
\]

### 4.3 Gamma target
Given \((\gamma,\chi)\), define
\[
x_{\rm diff}
=
\chi - \lambda\frac{(\gamma/d_{\rm eff})^{q}}{d_{\rm eff}-0.8},
\]
then compute \(\sigma(\gamma,\chi)\) from the retained diffusion probe, and set
\[
\gamma_{\rm target}=1-\sigma.
\]

### 4.4 Relaxation updates
The current selector flow is
\[
\chi_{n+1}=\chi_n + \alpha_\chi(\chi_{\rm target}-\chi_n),
\]
\[
W_{n+1}=W_n + \alpha_W(W_{\rm target}-W_n),
\]
\[
\gamma_{n+1}=\gamma_n + \alpha_\gamma(\gamma_{\rm target}-\gamma_n).
\]

Baseline selector update rates:
\[
\alpha_\gamma \approx 0.60,
\qquad
\alpha_W \approx 0.45,
\qquad
\alpha_\chi \approx 0.65.
\]

---

## 5. Derived selector findings

These are currently **numerically established**, not analytically proven from deeper dynamics.

### 5.1 Broad-attractor selection
The selector flow converged broadly toward a single attractor over the tested initialization box.

Zeroth-order selector attractor:
\[
\gamma_\infty \approx 0.273032,
\qquad
W_\infty \approx 0.430698,
\qquad
\chi_\infty \approx 0.400546.
\]

### 5.2 Load-bearing structure
Ablation showed:

- removing screening worsens the attractor substantially
- freezing \(W\)-relaxation is catastrophic away from near-solved initializations
- removing lag worsens accuracy but does not destroy branch selection

So the current selector hierarchy is:

\[
\boxed{
\text{screening + participation feedback are the core selector}
}
\]

with

\[
\boxed{
\text{lagged diffusion as a corrective refinement}
}
\]

### 5.3 Best current selector refinement
Best narrow lag refinement:
\[
\lambda \approx 1.4,
\qquad
q \approx 0.75,
\]
yielding selected attractor
\[
\gamma_\infty \approx 0.268643,
\qquad
W_\infty \approx 0.430646,
\qquad
\chi_\infty \approx 0.400982.
\]

This is the current best upstream selector result.

---

## 6. Microscopic kernel structure

These equations define the current shell–microstate bridge family.

### 6.1 Ideal kernel law
\[
K^{(0)}_{(n,a),(m,b)}
\propto
(q_n q_m)^{1/5}
(r_{n,a}r_{m,b})^{3/20}
(1+|n-m|)^{-1/2}
(1+|a-b|)^{-6/5}.
\]

### 6.2 Finite-resolution corrected kernel
\[
K_{(n,a),(m,b)}
\propto
(q_n q_m)^{\,1/5-\delta_a}
(r_{n,a}r_{m,b})^{\,3/20-(3/4)\delta_a}
(1+|n-m|)^{-(1/2+\delta_p)}
(1+|a-b|)^{-6/5}.
\]

Current interpretation:
- \(\delta_a\): finite-size amplitude softening
- \(\delta_p\): mainly finite shell-depth renormalization

---

## 7. Observable-layer ansatz (Sprint B)

These equations define the current minimal public-science bridge.

### 7.1 Expansion-response ansatz
\[
E_{\rm bridge}(z)=E_0(z)\,R_{\rm bridge}(z),
\]
with
\[
R_{\rm bridge}(z)=1+A_{\rm bridge}\frac{(z/z_c)^p}{1+(z/z_c)^p}.
\]

Current locked defaults:
\[
A_{\rm bridge}=\chi_* - x_{{\rm diff},*} \approx 0.02206046,
\qquad
z_c = 1,
\qquad
p = 2.
\]

So the first explicit ansatz is
\[
E_{\rm bridge}(z)=E_0(z)\left[1+0.02206046\frac{z^2}{1+z^2}\right].
\]

### 7.2 Proxy observables
\[
H_{\rm bridge}(z) \propto E_{\rm bridge}(z),
\]
\[
D_M^{\rm bridge}(z) \propto \int_0^z \frac{dz'}{E_{\rm bridge}(z')},
\]
\[
F_{AP}^{\rm bridge}(z) \propto D_M^{\rm bridge}(z)H_{\rm bridge}(z).
\]

### 7.3 Locked DESI-facing grid
Current comparison grid:
\[
z=\{0.51,0.71,0.93,1.32,1.48,2.10,2.33\}.
\]

Current proxy prediction:
strictly positive \(F_{AP}\)-style response across this grid, approximately from
\[
+0.2587\% \text{ to } +0.9111\%.
\]

---

## 8. Certified baseline closure result

These statements are currently the strongest **numerically certified** closure results.

### 8.1 Baseline local closure theorem
On the certified closure interval
\[
\gamma\in[0.18,0.36],
\]
the baseline reduced-law map satisfies:
- continuity
- strict monotonicity
- exactly one zero
- local attraction at the fixed point

### 8.2 Chain-rule structure
The full derivative decomposition is
\[
\sigma'(\gamma)
=
\frac{\partial \sigma}{\partial x_{\rm diff}}x'_{\rm diff}
+
\frac{\partial \sigma}{\partial m}m'
+
\frac{\partial \sigma}{\partial W}W'.
\]

Baseline certification showed the leading diffusion contribution dominates the sum of the corrections across the closure interval, giving
\[
F'(\gamma)<0.
\]

This is a numerical certification result, not yet a symbolic global theorem.

---

## 9. Hard falsification statements

### 9.1 Structural falsification
If an independently implemented upstream selector flow, using the same locked equations and parameter conventions, does not broadly regenerate the near-closure attractor, the current bridge version fails as a generative selector.

### 9.2 Observable falsification
If the DESI-facing target requires a negative \(F_{AP}\)-style response at any locked redshift point, the current bridge version fails immediately as an expansion-response theory.

If the required positive response is materially outside the locked \(+0.26\%\) to \(+0.91\%\) proxy band, the current bridge version fails as the present minimal expansion-response theory.

---

## 10. Status labels

### Assumed
- screened pruning-flow law
- reduced lag law family
- microscopic kernel family
- minimal expansion-response ansatz

### Derived / numerically certified
- baseline fixed point
- baseline local monotonicity
- selector attractor near closure
- load-bearing term hierarchy
- refined lag renormalization near \((\lambda,q)=(1.4,0.75)\)
- positive DESI-facing \(F_{AP}\)-style proxy band

### Not yet established
- fundamental action / Hamiltonian derivation
- full lattice RG derivation
- symbolic global proof
- production cosmology likelihood confrontation

---

## 11. Bottom line

This note makes the current bridge mathematically visible enough for AI peer review.

It does **not** claim:
- final derivation,
- final cosmology,
- or symbolic global proof.

It does claim that the bridge now has:
- explicit reduced-law equations,
- explicit selector equations,
- explicit microscopic kernel equations,
- explicit observable-layer equations,
- and explicit falsification rules.

That is the current math spine for the project.
