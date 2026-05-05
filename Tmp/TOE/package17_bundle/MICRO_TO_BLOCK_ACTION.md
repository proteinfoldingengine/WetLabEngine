# MICRO_TO_BLOCK_ACTION.md

# Micro to Block Action
## Candidate derivation program from microscopic retained-memory recursion to block-level action constants

## Status
**Live derivation target. First micro-to-block pass. Not yet closed.**

This file sits downstream of:

```text
CHI_FIXED_POINT.md
```

and upstream of:

```text
DISCRETE_MEMORY_ACTION.md
```

Its purpose is to attack the next closure seam:

> can the block-action constants \(K_t,K_U,K_x,K_{\mathrm{int}}\) be derived or constrained from the microscopic retained-memory / pruning dynamics?

`DISCRETE_MEMORY_ACTION.md` mapped the block-action constants to continuum coefficient scales:

\[
\mu_R^2=\frac{K_U}{K_t},
\]

\[
Z_0=\frac{K_x}{K_t}\left(\frac{dx}{dt}\right)^2,
\]

\[
\lambda_0=\frac{K_{\mathrm{int}}}{K_t}.
\]

This file now attempts the upstream map:

\[
(\alpha_s,\alpha_f,\beta_s,\beta_f,w_s,w_f,c_s,c_f,\mu_G,I_s,I_f,\mathcal G_*)
\quad\Rightarrow\quad
K_t,K_U,K_x,K_{\mathrm{int}}.
\]

This is not a final microscopic derivation. It is the first theorem-shaped candidate map.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Assumption**
- **Definition**
- **Lemma candidate**
- **Theorem candidate**
- **Derivation target**
- **Failure condition**

Nothing here should be interpreted as a completed proof unless explicitly stated.

---

# 1. Goal of this file

The goal is to bridge:

\[
\text{two-mode retained-memory recursion}
\]

to:

\[
\text{block-level memory action}.
\]

The block-level memory action from `DISCRETE_MEMORY_ACTION.md` is:

\[
S_{\mathrm{mem}}^{\mathrm{disc}}
=
\sum_n
\left[
\frac12 K_t(\Lambda_{n+1}-\Lambda_n)^2
+
U(\Lambda_n)
\right]
+
\sum_{n,\langle ij\rangle}
\frac12 K_x(\Lambda_i^n-\Lambda_j^n)^2
+
\sum_n
K_{\mathrm{int}}\Lambda_n\mathcal O_{\mathrm{mat},n}.
\]

The missing step is to derive or constrain:

\[
K_t,\qquad K_U,\qquad K_x,\qquad K_{\mathrm{int}}.
\]

---

# 2. Microscopic retained-memory inputs

## Definition 1
The retained-memory recursion contains slow and fast channels:

\[
R_{t+1}^{(s)}
=
\alpha_s R_t^{(s)}
+
\beta_s|\xi_t|,
\]

\[
R_{t+1}^{(f)}
=
\alpha_f R_t^{(f)}
+
\beta_f|\xi_t|\Theta(|\xi_t|-\varepsilon^*).
\]

The coarse-grained retained-memory magnitude is:

\[
M_t=w_sR_t^{(s)}+w_fR_t^{(f)}.
\]

Under block closure:

\[
\overline R_n^{(s)}\approx c_s\overline M_n,
\]

\[
\overline R_n^{(f)}\approx c_f\overline M_n.
\]

The geometry channel satisfies:

\[
\mathcal G_{n+1}=\mu_G\mathcal G_n.
\]

---

# 3. Loading map inherited from the microscopic recursion

## Definition 2
The loading ratio is:

\[
\Lambda_n=\frac{\mathcal M_n}{\mathcal G_n}.
\]

The derived loading map is:

\[
\Lambda_{n+1}=a\Lambda_n+b,
\]

where:

\[
a
=
\frac{w_s\alpha_s c_s+w_f\alpha_f c_f}{\mu_G},
\]

and:

\[
b
=
\frac{
w_s\beta_s I_s+
w_f\beta_f I_f
}
{\mu_G\mathcal G_*}.
\]

Here:

\[
I_s=\overline I_*^{(s)},
\qquad
I_f=\overline I_*^{(f)}.
\]

The stationary loading fixed point is:

\[
\Lambda_*=\frac{b}{1-a}.
\]

The bridge coefficient is:

\[
\chi_*=\frac{1}{1+\Lambda_*}.
\]

---

# 4. Candidate derivation of \(K_t\): retained-memory inertia

## Definition 3
The first candidate block inertia is:

\[
K_t
=
1+w_s\alpha_s+w_f\alpha_f.
\]

## Rationale
The time/update penalty:

\[
\frac12K_t(\Lambda_{n+1}-\Lambda_n)^2
\]

measures resistance to abrupt block-level loading changes.

Retained persistence increases memory inertia. Therefore the simplest positive candidate is:

\[
K_t=1+\text{weighted persistence}.
\]

The constant \(1\) represents the baseline update cost.

## Derivation target A
Derive the additive baseline and weighted-persistence form from the microscopic update norm or an information-distance functional.

## Failure condition 1
If the microscopic law implies no update inertia, then the block action cannot contain this local kinetic term.

---

# 5. Candidate derivation of \(K_U\): restoring stiffness

## Definition 4
The first candidate local restoring stiffness is:

\[
K_U=K_t(1-a).
\]

## Rationale
The loading fixed point satisfies:

\[
\delta\Lambda_{n+1}=a\delta\Lambda_n.
\]

The stability margin is:

\[
1-a.
\]

Thus the local potential curvature should scale with the stability margin. With \(K_t\) acting as inertia normalization:

\[
K_U=K_t(1-a).
\]

## Lemma candidate 1
If:

\[
K_t>0,
\qquad
0\le a<1,
\]

then:

\[
K_U>0.
\]

Thus the block potential is locally stable.

---

# 6. Candidate derivation of \(K_x\): neighbor-block coherence penalty

## Definition 5
Let \(\sigma_{\nabla\Lambda}\) denote the neighbor-block loading mismatch scale.

The first candidate neighbor stiffness is:

\[
K_x
=
K_t\chi_*(1-\chi_*)\sigma_{\nabla\Lambda}^2.
\]

## Rationale
The gradient penalty should scale with:

1. update inertia \(K_t\),
2. geometry-memory overlap \(\chi(1-\chi)\),
3. observed neighbor mismatch strength \(\sigma_{\nabla\Lambda}^2\).

Thus local coherence is penalized only when:
- there is retained-memory inertia,
- geometry and memory are mixed,
- and neighbor-block loading differences exist.

## Failure condition 2
If neighbor-block memory mismatch does not exist or is fundamentally nonlocal, then \(K_x\) cannot be derived locally and Class C should be revisited.

---

# 7. Candidate derivation of \(K_{\mathrm{int}}\): matter loading coupling

## Definition 6
Let \(\rho_{\mathrm{mat}}\) denote the microscopic matter-source loading strength.

The first candidate matter coupling is:

\[
K_{\mathrm{int}}
=
K_t\chi_*(1-\chi_*)\rho_{\mathrm{mat}}.
\]

## Rationale
The matter-memory coupling should scale with:

1. update inertia \(K_t\),
2. geometry-memory overlap,
3. matter-source loading strength.

This mirrors the continuum envelope:

\[
\lambda_{\mathrm{int}}(\chi)=\lambda_0\chi(1-\chi).
\]

## Failure condition 3
If matter does not source retained-memory loading in the microscopic law, then:

\[
K_{\mathrm{int}}=0.
\]

---

# 8. Full micro-to-block candidate map

## Definition 7
The first micro-to-block map is:

\[
a
=
\frac{w_s\alpha_s c_s+w_f\alpha_f c_f}{\mu_G},
\]

\[
b
=
\frac{
w_s\beta_sI_s+w_f\beta_fI_f
}
{\mu_G\mathcal G_*},
\]

\[
\Lambda_*=\frac{b}{1-a},
\]

\[
\chi_*=\frac{1}{1+\Lambda_*},
\]

\[
K_t=1+w_s\alpha_s+w_f\alpha_f,
\]

\[
K_U=K_t(1-a),
\]

\[
K_x=K_t\chi_*(1-\chi_*)\sigma_{\nabla\Lambda}^2,
\]

\[
K_{\mathrm{int}}
=
K_t\chi_*(1-\chi_*)\rho_{\mathrm{mat}}.
\]

This is the first full candidate bridge from microscopic retained-memory parameters to block-action constants.

---

# 9. Structural theorem candidate

## Theorem candidate 1
Suppose:

1. the two-mode retained-memory recursion is valid;
2. the closure fractions \(c_s,c_f\) exist;
3. the geometry channel satisfies \(\mu_G>0\);
4. the stationary innovation statistics \(I_s,I_f\) exist and are nonnegative;
5. the derived loading map satisfies \(0\le a<1\), \(b>0\);
6. \(\sigma_{\nabla\Lambda}\ge0\);
7. \(\rho_{\mathrm{mat}}\ge0\).

Then the micro-to-block map produces:

\[
K_t>0,
\]

\[
K_U>0,
\]

\[
K_x\ge0,
\]

\[
K_{\mathrm{int}}\ge0,
\]

and:

\[
0<\chi_*<1.
\]

Therefore the block memory action is structurally admissible.

This theorem is **not yet a microscopic proof**, because the specific functional forms for \(K_t,K_x,K_{\mathrm{int}}\) are still candidate identifications.

---

# 10. Verifier implementation

## Status
**Implemented as `micro_to_block_action_verifier.py`. Execution log captured.**

The verifier checks whether sampled microscopic parameter sets produce structurally admissible block constants.

It tests:

- \(\alpha_s,\alpha_f\in[0,1)\),
- \(\beta_s,\beta_f\ge0\),
- normalized \(w_s,w_f,c_s,c_f\),
- \(\mu_G>0\),
- \(I_s,I_f\ge0\),
- \(\mathcal G_*>0\),
- \(0\le a<1\),
- \(b>0\),
- \(K_t>0\),
- \(K_U>0\),
- \(K_x\ge0\),
- \(K_{\mathrm{int}}\ge0\),
- \(0<\chi_*<1\).

## Captured verifier output

```text
Micro-to-block action verifier
==================================================
Candidate map:
a     = (w_s alpha_s c_s + w_f alpha_f c_f) / mu_G
b     = (w_s beta_s I_s + w_f beta_f I_f) / (mu_G G_star)
K_t   = 1 + w_s alpha_s + w_f alpha_f
K_U   = K_t * (1-a)
K_x   = K_t * chi*(1-chi) * sigma_neighbor^2
K_int = K_t * chi*(1-chi) * rho_mat

Sweep results:
PASS: 96.479
SOFT_FAIL: 0.197
HARD_FAIL: 3.324
a_median: 0.2094273095088997
b_median: 0.022478946055010322
chi_median: 0.9688470147427344
chi_min: 0.00017794652866240872
chi_max: 0.9999998632711617
K_t_median: 1.4832378459808226
K_U_median: 1.1243411709620674
K_x_median: 7.075977820578564e-05
K_int_median: 0.0004262693777977181
```

---

# 11. What this file establishes

### Established at current proof level

1. A first explicit map from microscopic recursion parameters to block-action constants has been written.
2. \(K_U\) is tied directly to the loading-map stability margin \(1-a\).
3. \(K_t\) is tied to retained-memory persistence.
4. \(K_x\) is tied to neighbor-block loading mismatch and geometry-memory overlap.
5. \(K_{\mathrm{int}}\) is tied to matter-source loading and geometry-memory overlap.
6. The verifier shows broad structural admissibility for sampled stable regimes.

### Not yet proved

1. \(K_t=1+w_s\alpha_s+w_f\alpha_f\) is not uniquely derived.
2. \(K_x\) assumes locality of neighbor-block loading mismatch.
3. \(K_{\mathrm{int}}\) assumes matter-source loading exists.
4. \(\sigma_{\nabla\Lambda}\) and \(\rho_{\mathrm{mat}}\) need microscopic definitions.
5. The map is not yet covariant.
6. Nonlocal retained memory may invalidate the local block-action form.

---

# 12. Failure modes

This route fails if:

1. no stable loading map \(0\le a<1,b>0\) can be derived from the microscopic law;
2. closure fractions \(c_s,c_f\) are not well-defined;
3. stationary innovation statistics \(I_s,I_f\) do not exist;
4. retained-memory persistence does not produce update inertia;
5. local neighbor-block loading mismatch does not exist;
6. matter does not source retained-memory loading;
7. \(\sigma_{\nabla\Lambda}\) or \(\rho_{\mathrm{mat}}\) must be chosen by hand from phenomenology;
8. the true memory sector is nonlocal.

---

# 13. Next derivation target

The next file should be:

```text
COARSE_GRAINING_MAP.md
```

Its job is to construct:

\[
(\{G_e\},\{R_e\},\{\phi_e\})
\longmapsto
(g_{\mu\nu},R_{\mathrm{eff}},\phi_{\mathrm{eff}})
\]

and specifically prove or falsify:

\[
R_{\mathrm{eff}}\sim\Lambda.
\]

That is now the critical seam.

---

# Honest status line

> `MICRO_TO_BLOCK_ACTION.md` supplies the first theorem-shaped candidate map from two-mode retained-memory recursion parameters into the block-action constants \(K_t,K_U,K_x,K_{\mathrm{int}}\). It makes the coefficient chain much less arbitrary, but it is not yet closed: update inertia, neighbor locality, matter-source loading, and covariant coarse-graining still require derivation from the microscopic law.

**End of file.**
