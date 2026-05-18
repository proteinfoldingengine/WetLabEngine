# V549 Theorem Boundary Update

## Purpose

V549 updates the retained-geometry theorem after the selective-fragility audits.

The central question was:

> Are we discovering a first-principles recoverability structure, or overlaying geometry onto behavior?

The new answer is stronger:

> The law has boundary conditions. It survives admissible transformations and fails under principle-breaking transformations.

That is the selective-fragility signature.

---

# Current theorem object

\[
g_{\mathrm{eff}}(x,t)=\Omega(x,t)^2g_0(x)
\]

\[
\partial_t\Omega
=
\mathrm{Source}
-
\mathrm{Repair}
-
\mu_{\mathrm{defect}}
\]

\[
C_t = M_tR_tL_t+\lambda_0\eta_{\mathrm{convert}}B_t
\]

with:

\[
\eta_{\mathrm{convert}}
=
\frac{\sum_i w_i}{\sum_i w_i/\eta_i}
\exp[-C_{\mathrm{repair,min}}]
\]

---

# Selective-fragility result

A fitted overlay often either survives too much or fails randomly.

The retained-geometry system showed a more structured pattern.

## It survived admissible transformations

The system remained coherent under:

1. coordinate relabeling,
2. \(\Omega\) rescaling,
3. topology-preserving smoothing,
4. admissible metric deformation,
5. moderate field noise.

These transformations may change raw values, but they should preserve:

- source/reserve \(\rightarrow \Omega\),
- \(\Omega^2g_0 \rightarrow K_{\mathrm{eff}}\),
- localized \(\mu_{\mathrm{defect}}\),
- \(\eta_{\mathrm{convert}}\) reserve accounting,
- constrained \(V[\Omega,C,\mu]\) stability.

## It failed under principle-breaking attacks

The system broke when assumptions were violated:

1. source/reserve relation destroyed,
2. branch volume \(B_t\) faked,
3. repair burden hidden,
4. defects scrambled away from lineage/pinch seams,
5. coordinated fake recovery introduced.

This is scientifically important because these are exactly the attacks that should break a real recoverability law.

---

# Why V546 mattered

V545 exposed a blind spot: fake branch liquidity and hidden repair burden were not detected strongly enough.

V546 fixed the calibration.

After calibration:

- honest baseline error fell to zero,
- fake \(B_t\) liquidity produced high \(B_t\) error,
- hidden repair burden produced high repair error,
- coordinated liquidity trap was detected,
- audited reserve accounting corrected the naive liquidity trap.

This strengthened the theorem boundary:

\[
B_t \neq \text{usable reserve}
\]

unless it passes independent liquidity and repair-burden audit.

---

# Why V547 mattered

V547 consolidated all guards:

1. geometry consistency,
2. weak-form residual,
3. defect accounting,
4. \(B_t\) liquidity audit,
5. repair burden audit,
6. Lyapunov \(V\) accounting.

The consolidated selective-fragility audit separated admissible transformations from principle-breaking attacks with a strong synthetic signal.

---

# Updated validity conditions

Conformal recoverability flow is valid only when:

1. source/reserve relation is preserved,
2. \(B_t\) is independently liquid and recoverable,
3. \(C_{\mathrm{repair,min}}\) is honestly measured,
4. \(\mu_{\mathrm{defect}}\) is localized and accounted for,
5. \(V[\Omega,C,\mu]\) does not hide reserve or defect failure,
6. \(\eta_{\mathrm{convert}}\) is calibrated and identifiable.

---

# Updated theorem-shaped statement

Let an adaptive branch system admit a conformal effective metric:

\[
g_{\mathrm{eff}}=\Omega^2g_0
\]

and weak-form evolution:

\[
\partial_t\Omega
=
\mathrm{Source}
-
\mathrm{Repair}
-
\mu_{\mathrm{defect}}
\]

with recoverability reserve:

\[
C_t=M_tR_tL_t+\lambda_0\eta_{\mathrm{convert}}B_t
\]

If:

1. \(V[\Omega,C,\mu]\) decreases,
2. \(C_t>C_{\mathrm{floor}}\),
3. \(\mu_{\mathrm{defect}}\) is non-increasing,
4. bottleneck leakage is bounded,
5. \(B_t\) passes independent liquidity audit,
6. \(C_{\mathrm{repair,min}}\) passes repair-burden audit,

then the trajectory remains inside or enters the retained recovery basin.

---

# Current status

Strengthened:

- first-principles boundary,
- selective invariance,
- selective fragility,
- \(B_t\) liquidity guard,
- repair-burden guard,
- \(\eta_{\mathrm{convert}}\) validity conditions.

Still open:

1. rigorous continuum proof,
2. rigorous measure convergence theorem,
3. full Lyapunov theorem,
4. uniqueness of channel basis,
5. exact relation to known geometric flows.

---

# One-line update

The retained bridge now behaves less like a geometric overlay and more like a constrained recoverability law: it survives admissible transformations and fails when its first-principles assumptions are broken.
