# CHI_FIXED_POINT.md

# \(\chi\) Fixed Point
## Candidate derivation program for the leading-order geometry weight in the affine GEM Bridge

## Status
**Blueprint for closure. Not yet closed.**

This file defines the mathematical role of \(\chi\), states the candidate fixed-point problem that must determine it, and specifies the exact proof obligations required for \(\chi\) to count as a derived quantity rather than a phenomenological convenience.

This file does **not** yet claim that \(\chi\approx 0.2667\) has been fully derived from the microscopic law.

Its purpose is narrower:

> to define the fixed-point or renormalization problem sharply enough that existence, uniqueness, stability, and independence from phenomenology can be attacked directly.

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

The bridge-operator file isolates the leading-order affine form
\[
\Psi(G_t,R_t)=\chi G_t+(1-\chi)R_t.
\]

That does **not** yet determine the value of \(\chi\).

The purpose of this file is to answer the next question:

> Is \(\chi\) fixed by a microscopic or coarse-grained stability principle, or is it still being inserted phenomenologically?

This is the seam that separates:
- a derived bridge coefficient,
from
- a fitted bridge coefficient.

---

# 2. Definition of \(\chi\)

## Definition 1
\(\chi\in[0,1]\) is the leading-order geometry weight in the normalized affine bridge:
\[
\Psi(G_t,R_t)=\chi G_t+(1-\chi)R_t.
\]

Equivalent interpretations:
- geometry-memory mixing weight,
- coarse-grained persistence/innovation balance parameter,
- retained-coherence bridge coefficient.

## Assumption 1
\(\chi\) is not free in the fully closed theory.

That is, once the microscopic law and admissible operator class are fixed, \(\chi\) should be determined by:
- a fixed-point condition,
- a renormalization-group condition,
- a stability balance,
- or another explicit mathematical principle.

---

# 3. What must be shown

For \(\chi\) to count as derived, this file must ultimately supply:

1. an explicit map or equation determining \(\chi\),
2. existence of a fixed point,
3. uniqueness of the physically admissible fixed point,
4. stability of that fixed point,
5. and a demonstration that the value is not back-fit from galaxy/cluster phenomenology.

Anything less than that should be described honestly as:
- a conjectured fixed point,
- a candidate attractor,
- or a phenomenological calibration.

---

# 4. Source of the fixed-point problem

The guiding hypothesis is that \(\chi\) is set by the same coarse-grained pruning dynamics that produce:
- the slow retained-memory backbone,
- the fast seam mode,
- and the effective bridge between geometry and memory.

## Assumption 2
The microscopic collapse/pruning law induces a scale-dependent flow on the geometry-memory mixing ratio.

Equivalently, under coarse-graining or lattice blocking,
\[
\chi \mapsto F(\chi;\, d_h,\varepsilon^*,\alpha_s,\alpha_f,\beta,\dots),
\]
where:
- \(d_h\) is an effective lattice Hausdorff or scaling dimension,
- \(\varepsilon^*\) is the pruning threshold,
- \(\alpha_s,\alpha_f\) are slow/fast persistence parameters,
- \(\beta\) is threshold sharpness or equivalent collapse-law parameter.

## Definition 2
A fixed point \(\chi_*\) satisfies
\[
\chi_* = F(\chi_*;\, d_h,\varepsilon^*,\alpha_s,\alpha_f,\beta,\dots).
\]

## Definition 3
A stable fixed point satisfies
\[
|F'(\chi_*)| < 1
\]
in the one-dimensional case, or the corresponding spectral-radius condition in the multi-parameter case.

---

# 5. Candidate derivation routes

This file does not assume there is only one possible route. It organizes the main candidates.

## Route A: slow/fast mode ratio
The simplest candidate is that \(\chi\) is set by the ratio of slow to total retained influence:
\[
\chi = \frac{\alpha_s}{\alpha_s+\alpha_f}
\]
or a weighted variant
\[
\chi = \frac{w_s\alpha_s}{w_s\alpha_s + w_f\alpha_f}.
\]

### Derivation target A
Determine whether such a ratio follows from the admissible operator theorem plus the two-mode retained-memory recursion, or whether it is merely heuristic.

### Failure condition 1
If the slow/fast ratio form is chosen only because it numerically resembles the desired value, without being forced by the derivation, then it does not count.

---

## Route B: lattice dimension / volume scaling
A second candidate is that \(\chi\) is determined by geometric scaling under coarse-graining, for example through an effective dimension \(d_h\).

Prototype forms could include:
\[
\chi = f(d_h),
\]
or
\[
\chi_{n+1}=F(\chi_n;d_h),
\]
with \(d_h\) fixed by lattice pruning statistics.

### Derivation target B
State the exact meaning of \(d_h\):
- Hausdorff dimension,
- spectral dimension,
- fractal occupancy dimension,
- or another coarse-grained geometric scaling exponent.

### Derivation target C
Show how the pruning rule modifies cell counts, effective volume, or branching density under coarse-graining, and derive \(F\) from that process.

### Failure condition 2
If \(d_h\) is itself inferred from late-time phenomenology and then fed back into \(\chi\), the derivation becomes circular.

---

## Route C: free-energy or action minimization
A third route is variational.

## Assumption 3
The physically realized bridge weight minimizes or extremizes an effective functional
\[
\mathcal{J}(\chi)
\]
that balances:
- geometric fidelity,
- retained-memory coherence,
- contractive stability,
- and seam sparsity.

The fixed point would then satisfy
\[
\frac{d\mathcal{J}}{d\chi} = 0,
\]
with stability from
\[
\frac{d^2\mathcal{J}}{d\chi^2} > 0.
\]

### Derivation target D
Write the actual functional \(\mathcal{J}(\chi)\), not merely its intuition.

### Failure condition 3
If no explicit \(\mathcal{J}\) can be written without importing \(\chi\) by hand, this route fails.

---

## Route D: renormalization-group closure
A fourth route is explicit RG flow.

Under lattice blocking,
\[
(\alpha_s,\alpha_f,\varepsilon^*,\chi)\mapsto (\alpha_s',\alpha_f',\varepsilon^{*\,\prime},\chi').
\]

A fixed point is then defined by
\[
\chi'=\chi.
\]

### Derivation target E
Write the RG map explicitly or write a coarse-graining rule from which the RG map can be computed.

### Lemma candidate 1
If the operator theorem fixes the bridge to affine form and the microscopic pruning law fixes the slow/fast mode flow, then \(\chi\) must be the stable RG attractor of the induced coarse-grained geometry-memory ratio.

This lemma is **not yet proved**.

### Failure condition 4
If no RG map can be written or approximated, then the RG interpretation of \(\chi\) remains metaphorical rather than mathematical.

---

# 6. The fixed-point theorem candidate

This is the central theorem candidate of the file.

## Theorem candidate D
Suppose:
1. the microscopic law induces a finite-dimensional two-mode retained-memory recursion,
2. the operator theorem fixes the leading-order bridge to affine form,
3. and the induced coarse-graining map on the geometry-memory ratio is well-defined.

Then there exists a unique stable fixed point
\[
\chi_* \in (0,1)
\]
such that
\[
\chi_* = F(\chi_*;\, d_h,\varepsilon^*,\alpha_s,\alpha_f,\beta,\dots).
\]

Moreover, for the physically admissible scaling class, this fixed point satisfies
\[
\chi_* \approx 0.2667.
\]

This theorem is **not yet proved**.

---

# 7. First integrated proof draft for seam 2

## Status
**Live derivation target. First integrated proof pass. Not yet fully closed.**

`OPERATOR_THEOREM.md` now gives a conditional first-order bridge form:
\[
\Psi(G,R)=\chi G+(1-\chi)R+O(2)
\]
on irreducible isotropic symmetry sectors.

This section now attacks the next question:

> is \(\chi\) an inserted bridge weight, or can it be derived as the stable coarse-grained balance between geometry persistence and retained-memory carryover?

The result of this first pass is:

- \(\chi\) is tied to a **coarse-grained balance law** rather than treated as free,
- a **minimal fixed-point map** is identified,
- existence and stability become checkable,
- but uniqueness and non-circularity are still conditional on deriving the underlying persistence parameters from the microscopic law.

So seam 2 is now theorem-shaped, but not closed.

---

# 8. What \(\chi\) must mean

The operator theorem has already restricted \(\chi\) to be the scalar first-order geometry weight.

At this point, \(\chi\) cannot just be “a number between 0 and 1.” It must mean something dynamical.

The minimal consistent interpretation is:

- \(\chi\) measures the fraction of first-order update carried by **geometry persistence**, and
- \(1-\chi\) measures the fraction carried by **retained-memory persistence**.

So the fixed-point problem for \(\chi\) is fundamentally a **balance problem**:
- how much of the next coarse-grained state comes from the geometry channel,
- versus how much comes from accumulated retained-memory load.

That is the structural starting point.

---

# 9. Minimal balance ansatz

## Assumption B1
At the coarse-grained level, the next-step effective state receives two first-order contributions:
1. a geometry-persistence channel,
2. a retained-memory channel.

Write their effective magnitudes at scale \(n\) as:
\[
\mathcal G_n,
\qquad
\mathcal M_n.
\]

## Definition 4
Define the geometry fraction
\[
\chi_n := \frac{\mathcal G_n}{\mathcal G_n+\mathcal M_n}.
\]

Then automatically
\[
1-\chi_n = \frac{\mathcal M_n}{\mathcal G_n+\mathcal M_n}.
\]

This is the cleanest non-circular definition of \(\chi\) available at first pass.

---

# 10. First fixed-point map

## Assumption B2
Under coarse-graining, the geometry and memory channels renormalize according to
\[
\mathcal G_{n+1}=\mu_G\,\mathcal G_n,
\]
\[
\mathcal M_{n+1}=\mu_M\,\mathcal M_n,
\]
with effective persistence coefficients \(\mu_G,\mu_M>0\).

Then
\[
\chi_{n+1}
=
\frac{\mu_G \mathcal G_n}{\mu_G \mathcal G_n + \mu_M \mathcal M_n}.
\]

Using
\[
\chi_n=\frac{\mathcal G_n}{\mathcal G_n+\mathcal M_n},
\]
we get
\[
\chi_{n+1}
=
\frac{\mu_G \chi_n}{\mu_G \chi_n + \mu_M (1-\chi_n)}.
\]

This is the first explicit candidate fixed-point map:
\[
F(\chi)=\frac{\mu_G \chi}{\mu_G \chi + \mu_M (1-\chi)}.
\]

---

# 11. Why this map is not enough yet

This map has a problem: by itself, it tends to drive \(\chi\) to trivial endpoints unless \(\mu_G=\mu_M\). So it is too simple to capture a nontrivial interior fixed point robustly.

That means the physically relevant coarse-grained balance cannot be pure multiplicative renormalization of existing amplitudes. It must include **source loading** from innovation.

That is exactly where the retained-memory recursion enters.

So we refine.

---

# 12. Memory-loaded balance map

The two-mode retained-memory sector carries fresh innovation input. Therefore the effective memory channel at coarse-grained step \(n+1\) should have the structure
\[
\mathcal M_{n+1}
=
\mu_M \mathcal M_n + \mathcal I_n,
\]
where \(\mathcal I_n\) is the innovation loading induced by thresholded and unthresholded memory accumulation.

At minimal two-mode order:
\[
\mathcal I_n
=
w_s \beta_s \langle |\xi| \rangle_n
+
w_f \beta_f \langle |\xi|\Theta(|\xi|-\varepsilon^*)\rangle_n.
\]

Similarly, geometry persistence may be written as
\[
\mathcal G_{n+1}=\mu_G \mathcal G_n.
\]

Then
\[
\chi_{n+1}
=
\frac{\mu_G \mathcal G_n}
{\mu_G \mathcal G_n + \mu_M \mathcal M_n + \mathcal I_n}.
\]

## Definition 5
Define the coarse-grained memory-loading ratio
\[
\Lambda_n := \frac{\mu_M \mathcal M_n + \mathcal I_n}{\mu_G \mathcal G_n}.
\]

Then
\[
\chi_{n+1} = \frac{1}{1+\Lambda_n}.
\]

At fixed point,
\[
\chi_*=\frac{1}{1+\Lambda_*}.
\]

This is the first meaningful nontrivial formula.

---

# 13. Reduction to the minimal two-mode persistence ratio

Now impose the minimal first-pass closure.

## Assumption B3
At stationary coarse-grained balance, the loading ratio \(\Lambda_*\) is controlled by the already-persistent retained-memory weights, not by an extra sector.

Then
\[
\Lambda_* \approx \frac{w_s\alpha_s + w_f\alpha_f}{\mu_G},
\]
up to normalization convention.

Hence
\[
\chi_*
=
\frac{1}{1+\frac{w_s\alpha_s+w_f\alpha_f}{\mu_G}}
=
\frac{\mu_G}{\mu_G+w_s\alpha_s+w_f\alpha_f}.
\]

This is the minimal candidate fixed-point formula.

It is important because it does **not** come from matching galaxy data directly. It comes from the claim that the bridge weight is the stationary fraction of first-order update carried by geometry persistence relative to retained-memory persistence.

---

# 14. Existence and stability

Now check the fixed point structurally.

If
\[
\chi_{n+1}=\frac{1}{1+\Lambda_n},
\]
and \(\Lambda_n\) tends to a finite positive limit \(\Lambda_*>0\), then
\[
\chi_*\in(0,1).
\]

So interior existence is immediate if the coarse-grained loading ratio exists and is positive finite.

For stability, suppose the coarse-grained loading map is
\[
\Lambda_{n+1}=G(\Lambda_n)
\]
with stable fixed point \(\Lambda_*\), i.e.
\[
|G'(\Lambda_*)|<1.
\]

Then
\[
\chi = \frac{1}{1+\Lambda}
\]
is smooth and monotone, so \(\chi_*\) inherits stability from \(\Lambda_*\).

Thus the real stability problem is not directly in \(\chi\), but in whether the retained-memory loading ratio has a stable coarse-grained fixed point.

That is a cleaner formulation of seam 2.

---

# 15. What this actually proves

### Established at current proof level
- \(\chi\) can be defined non-circularly as the stationary fraction of first-order update carried by geometry persistence.
- A trivial pure-multiplicative ratio map is inadequate.
- A nontrivial interior fixed point naturally appears once fresh innovation loading is included.
- The minimal candidate formula is
  \[
  \chi_*=\frac{\mu_G}{\mu_G+w_s\alpha_s+w_f\alpha_f}
  \]
  at first-pass closure.

### Not yet proved
- that \(\mu_G,\alpha_s,\alpha_f,w_s,w_f\) are derivable from the microscopic law,
- that this is the unique admissible fixed-point map,
- that the resulting \(\chi_*\) equals the locked empirical value without hidden fitting,
- that \(d_h\) or RG flow is unnecessary or reducible to the same formula.

So this is not final closure. But it is now a theorem-shaped candidate rather than a placeholder family list.

---

# 16. Comparison to the earlier candidate routes

This first proof pass clarifies the route structure:

### Route A (slow/fast ratio)
Now sharpened into a genuine candidate:
\[
\chi_*=\frac{\mu_G}{\mu_G+w_s\alpha_s+w_f\alpha_f}.
\]

### Route B (dimension/scaling route)
Still open. It may determine \(\mu_G,\alpha_s,\alpha_f\) through lattice scaling, rather than directly determining \(\chi\).

### Route C (variational route)
Still open. It may justify the same fixed point as a stationary point of an effective balance functional.

### Route D (RG route)
Still open. It may provide the real derivation of \(\Lambda_*\).

So the package is now better organized:
- seam 2 is probably not “guess \(F\) directly,”
- it is more likely “derive the stationary loading ratio \(\Lambda_*\), then set \(\chi_*=1/(1+\Lambda_*)\).”

That is a conceptual advance.

---

# 17. Clean failure modes for seam 2

Seam 2 fails if any of the following happen:

1. the coarse-grained geometry/memory balance cannot be defined non-circularly;
2. the loading ratio \(\Lambda_n\) has no stable finite fixed point;
3. the microscopic law implies extra persistence channels beyond \(\mu_G,\alpha_s,\alpha_f\);
4. the derived \(\chi_*\) only matches the empirical value after hidden astrophysical calibration;
5. the memory-loading ratio must be made scale- or data-dependent by hand.

Those are now explicit and inspectable.

---

# 18. Derivation of \(a\) and \(b\) from the two-mode recursion

## Status
**Live derivation target. Seam-2 tightening pass.**

The seam-2 verifier introduced the loading map
\[
\Lambda_{n+1}=a\,\Lambda_n+b,
\qquad
\chi_*=\frac{1-a}{1-a+b}.
\]

This section now derives \(a\) and \(b\) explicitly as coarse-grained summaries of the two-mode retained-memory recursion already defined in the package.

This is the bridge from the microscopic recursion to the seam-2 stability engine.

---

## Step 1: define the coarse-grained loading variable

At the fine time index \(t\), define the total retained-memory magnitude
\[
M_t := w_s R_t^{(s)} + w_f R_t^{(f)}.
\]

Using the two recursions,
\[
M_{t+1}
=
w_s\alpha_s R_t^{(s)}
+
w_f\alpha_f R_t^{(f)}
+
w_s\beta_s |\xi_t|
+
w_f\beta_f |\xi_t|\Theta(|\xi_t|-\varepsilon^*).
\]

This is exact.

Now define a coarse-grained block average over a window \(B_n\):
\[
\overline M_n := \frac{1}{|B_n|}\sum_{t\in B_n} M_t.
\]

Similarly define coarse-grained innovation statistics
\[
\overline I_n^{(s)} := \frac{1}{|B_n|}\sum_{t\in B_n} |\xi_t|,
\qquad
\overline I_n^{(f)} := \frac{1}{|B_n|}\sum_{t\in B_n} |\xi_t|\Theta(|\xi_t|-\varepsilon^*).
\]

Then the coarse-grained memory update is
\[
\overline M_{n+1}
\approx
w_s\alpha_s\,\overline R_n^{(s)}
+
w_f\alpha_f\,\overline R_n^{(f)}
+
w_s\beta_s\,\overline I_n^{(s)}
+
w_f\beta_f\,\overline I_n^{(f)}.
\]

---

## Step 2: reduce to a one-variable loading recursion

To connect to the verifier model, we need a closed equation in one effective memory-loading variable.

So make the standard first-pass closure assumption.

### Closure C1
Within each coarse-grained block, the slow and fast retained-memory amplitudes contribute fixed fractions of the total retained-memory load:
\[
\overline R_n^{(s)} \approx c_s \overline M_n,
\qquad
\overline R_n^{(f)} \approx c_f \overline M_n,
\]
with
\[
c_s,c_f\ge 0.
\]

This is the minimal one-dimensional closure.

Substitute:
\[
\overline M_{n+1}
\approx
\big(w_s\alpha_s c_s + w_f\alpha_f c_f\big)\overline M_n
+
w_s\beta_s\,\overline I_n^{(s)}
+
w_f\beta_f\,\overline I_n^{(f)}.
\]

So the effective coarse-grained retained-memory carryover coefficient is

\[
a := w_s\alpha_s c_s + w_f\alpha_f c_f.
\]

And the effective innovation injection is

\[
b_{\text{raw},n}
:=
w_s\beta_s\,\overline I_n^{(s)}
+
w_f\beta_f\,\overline I_n^{(f)}.
\]

Thus
\[
\overline M_{n+1} \approx a\,\overline M_n + b_{\text{raw},n}.
\]

That is the actual origin of the toy model.

---

## Step 3: normalize by the geometry channel

Seam 2 was framed in terms of the loading ratio
\[
\Lambda_n := \frac{\mathcal M_n}{\mathcal G_n}.
\]

Let the geometry channel satisfy
\[
\mathcal G_{n+1}=\mu_G \mathcal G_n.
\]

Then
\[
\Lambda_{n+1}
=
\frac{\mathcal M_{n+1}}{\mathcal G_{n+1}}
\approx
\frac{a\,\mathcal M_n + b_{\text{raw},n}}{\mu_G \mathcal G_n}
=
\frac{a}{\mu_G}\Lambda_n
+
\frac{b_{\text{raw},n}}{\mu_G \mathcal G_n}.
\]

So the normalized loading map has coefficients

\[
a_\Lambda := \frac{a}{\mu_G}
=
\frac{w_s\alpha_s c_s + w_f\alpha_f c_f}{\mu_G},
\]

and

\[
b_\Lambda(n)
:=
\frac{
w_s\beta_s\,\overline I_n^{(s)}
+
w_f\beta_f\,\overline I_n^{(f)}
}{\mu_G \mathcal G_n}.
\]

Hence the seam-2 loading recursion is

\[
\Lambda_{n+1}
\approx
a_\Lambda\,\Lambda_n + b_\Lambda(n).
\]

This is the real reduction.

---

## Step 4: stationary approximation

To recover the linear verifier model, impose stationary coarse-grained innovation loading.

### Closure C2
On the fixed-point regime,
\[
b_\Lambda(n)\to b_\Lambda^* = b.
\]

Then
\[
\Lambda_{n+1}=a_\Lambda \Lambda_n + b.
\]

So the exact identifications are:

\[
a = a_\Lambda = \frac{w_s\alpha_s c_s + w_f\alpha_f c_f}{\mu_G},
\]

\[
b = \frac{
w_s\beta_s\,\overline I_*^{(s)}
+
w_f\beta_f\,\overline I_*^{(f)}
}{\mu_G \mathcal G_*}.
\]

where
\[
\overline I_*^{(s)}=\lim_{n\to\infty}\overline I_n^{(s)},
\qquad
\overline I_*^{(f)}=\lim_{n\to\infty}\overline I_n^{(f)}.
\]

Now the verifier parameters \(a,b\) are no longer free abstractions. They are explicit coarse-grained summaries of the two-mode recursion.

---

## Step 5: resulting fixed point

Provided
\[
0\le a<1,\qquad b>0,
\]
the loading fixed point is
\[
\Lambda_*=\frac{b}{1-a},
\]
and therefore
\[
\chi_*=\frac{1}{1+\Lambda_*}
=
\frac{1-a}{1-a+b}.
\]

Substituting the coarse-grained expressions:

\[
\chi_*
=
\frac{
1-\frac{w_s\alpha_s c_s + w_f\alpha_f c_f}{\mu_G}
}{
1-\frac{w_s\alpha_s c_s + w_f\alpha_f c_f}{\mu_G}
+
\frac{
w_s\beta_s\,\overline I_*^{(s)}
+
w_f\beta_f\,\overline I_*^{(f)}
}{\mu_G \mathcal G_*}
}.
\]

This is the first real microscopic-to-coarse-grained candidate formula for \(\chi_*\).

It is still not fully closed, because:
- \(c_s,c_f\) are closure coefficients,
- \(\mu_G\) still needs microscopic/coarse-grained derivation,
- and \(\overline I_*^{(s)},\overline I_*^{(f)}\) need explicit evaluation from \(\xi_t\).

But it is now structurally tied to the microscopic law.

---

## What this proves
At current proof level, this establishes:

1. the seam-2 verifier parameters \(a,b\) are not arbitrary;
2. they descend from the two-mode retained-memory recursion plus coarse-graining;
3. the fast thresholded channel contributes only through
   \[
   \overline I_*^{(f)} = \lim \overline{|\xi|\Theta(|\xi|-\varepsilon^*)},
   \]
   exactly as expected;
4. the bridge coefficient \(\chi_*\) is controlled by:
   - memory carryover strength,
   - innovation injection strength,
   - and geometry persistence strength.

That is a real reduction in ambiguity.

---

# 19. Verifier implementation

The structural fixed-point reduction can now be tested numerically without yet claiming microscopic closure of the persistence/loading parameters.

A verifier upgrade now computes:
1. \(a,b\) from the coarse-grained two-mode recursion summary,
2. the induced loading fixed point \(\Lambda_*=b/(1-a)\),
3. the induced bridge coefficient
   \[
   \chi_*=\frac{1-a}{1-a+b},
   \]
4. and sensitivity of \(\chi_*\) to \(a,b\).

At code level, this is implemented by:
- a derivation step `derive_ab(...)`,
- followed by a loading-map fixed-point step `loading_fixed_point(a,b)`.

This turns seam 2 into a runnable stability problem rather than a symbolic placeholder.

---

# 20. Numerical stability sweep – first pass

### Status
**Completed first verifier-backed pass.**

A first sweep was run in a geometry-dominant regime using the seam-2 loading model.

#### Summary
- tested parameter sets: **1728**
- stable sets: **1728**
- physical sets: **1728**
- physical \(\chi_*\) range:
  \[
  0.7123 \le \chi_* \le 0.9861
  \]

### Interpretation
The model was structurally stable in this sampled regime, but the sampled parameter window was too geometry-dominant to reach the locked empirical target
\[
\chi_{\mathrm{emp}} \approx 0.2667.
\]

This immediately implied that lower \(\chi_*\) would require:
- larger effective memory carryover,
- larger innovation loading,
- smaller geometry persistence,
- or some combination.

So the first sweep established stability, but not reachability of the empirical band.

---

# 21. Numerical stability sweep – targeted reachability pass

### Status
**Completed first targeted verifier pass.**

After deriving
\[
a=\frac{w_s\alpha_s c_s + w_f\alpha_f c_f}{\mu_G},
\qquad
b=\frac{w_s\beta_s\,\overline I_*^{(s)} + w_f\beta_f\,\overline I_*^{(f)}}{\mu_G \mathcal G_*},
\]
the seam-2 verifier was upgraded to test the induced loading map
\[
\Lambda_{n+1}=a\Lambda_n+b,
\qquad
\chi_*=\frac{1-a}{1-a+b}.
\]

### Targeted memory-heavy sweep

#### Summary
- total tested sets: **327,680**
- stable sets: **206,080**
- physical sets: **206,080**
- physical \(\chi_*\) range:
  \[
  0.000476 \le \chi_* \le 0.920354
  \]
- hits in the target band
  \[
  \chi_* \in [0.26,\,0.28]
  \]
  : **6,784**

### Main result
The locked empirical band is **reachable** inside the current seam-2 model while preserving:
\[
0 \le a < 1,
\qquad
b>0.
\]

So seam 2 does **not** currently force revision of the two-mode retained-memory backbone.

### Reasonableness of the hit region
All hit cases satisfy:
- \(\alpha_s < 1\),
- \(\alpha_f < 1\),
- \(w_s+w_f=1\),
- \(c_s+c_f=1\),
- nonnegative innovation statistics,
- stable/physical loading-map conditions.

Hit-band ranges:
\[
a \in [0.22,\,0.966667],
\qquad
b \in [0.09,\,2.1875].
\]

Representative hit cases show the same structural pattern:
- either moderately high \(a\) with moderate \(b\),
- or moderate \(a\) with stronger \(b\),

producing
\[
\lambda_* \approx 2.57 \text{ to } 2.85,
\qquad
\chi_* \approx 0.26 \text{ to } 0.28.
\]

### What this establishes
At current proof level, this numerical pass establishes:

1. the seam-2 fixed-point model is not merely formally stable;
2. the empirical target \(\chi_{\mathrm{emp}} \approx 0.2667\) is structurally reachable;
3. the reachability region is memory-heavier than the initial mild sweep;
4. seam 2 now reduces to a narrower question:

> can the microscopic law and equivariant coarse-graining actually produce hit-band values of
> \(\mu_G,\alpha_s,\alpha_f,\beta_s,\beta_f,w_s,w_f,c_s,c_f,\overline I_*^{(s)},\overline I_*^{(f)}\)
> without hidden calibration?

### What this does **not** yet establish
This sweep does **not** yet prove:
- that the hit-band parameters are the unique admissible ones,
- that the parameters are derived microscopically,
- or that the nonlinear loading map beyond the linearized stationary regime preserves the same fixed point.

So seam 2 is now **numerically supported**, but not yet fully closed.

---

# 22. Connection to the earlier candidate routes

This integrated proof pass clarifies the route structure.

### Route A (slow/fast ratio)
Now sharpened into a genuine candidate only after coarse-grained balance reduction:
\[
\chi_*=\frac{1}{1+\Lambda_*},
\]
with \(\Lambda_*\) determined by the geometry-to-memory loading ratio.

### Route B (dimension/scaling route)
Still open. It may determine \(\mu_G,\alpha_s,\alpha_f\) through lattice scaling, rather than directly determining \(\chi\).

### Route C (variational route)
Still open. It may justify the same fixed point as a stationary point of an effective balance functional.

### Route D (RG route)
Still open. It may provide the real derivation of \(\Lambda_*\) and therefore of \(\chi_*\).

So the package is now better organized:
- seam 2 is probably not “guess \(F\) directly,”
- it is more likely “derive the stationary loading ratio \(\Lambda_*\), then set \(\chi_*=1/(1+\Lambda_*)\).”

That is a conceptual advance.

---

# 23. Updated seam-2 failure modes

Seam 2 fails if any of the following happen:

1. the coarse-grained geometry/memory balance cannot be defined non-circularly;
2. the loading ratio \(\Lambda_n\) has no stable finite fixed point;
3. the microscopic law implies extra persistence channels beyond \(\mu_G,\alpha_s,\alpha_f\);
4. the derived \(\chi_*\) only matches the empirical value after hidden astrophysical calibration;
5. the memory-loading ratio must be made scale- or data-dependent by hand;
6. the hit-band parameter region cannot be realized by microscopic/coarse-grained admissible dynamics.

Those are now explicit and inspectable.

---

# 24. Honest status line

The correct public wording at this stage is:

> The first theorem pass for `CHI_FIXED_POINT.md` is now in place. It reframes \(\chi\) as a stationary geometry-to-memory loading ratio, derives the verifier parameters \(a,b\) from the two-mode recursion plus coarse-graining, and shows numerically that the empirical bridge coefficient is reachable inside the current seam-2 model without violating stability. This is not yet a finished derivation, because the persistence/load parameters are not yet fully derived from the microscopic law.

That is the honest interpretation.

---

# 25. Bottom line

Seam 2 is no longer just “find a nice map \(F\).”

It is now:

1. define \(\chi\) as the stationary geometry fraction,
2. derive the loading ratio \(\Lambda_n\),
3. derive \(a,b\) from the two-mode recursion plus coarse-graining,
4. verify stability and target-band reachability,
5. and then ask whether the required hit-band parameters are microscopically derivable.

That is a real reduction in ambiguity.

Seam 2 is now theorem-shaped and verifier-backed, but not yet fully closed.
