# UQCF-GEM bridge verification dossier

## Purpose
This dossier packages the final math, physics, figures, and data needed for humans or AI systems to verify, critique, reproduce, and extend the current UQCF-GEM bridge result.

## Canonical claim
A frozen UQCF-GEM bridge implementation (`v9`) produces a reproducible, measurable **pre-classical structural-ordering effect** in protein folding trajectories across small real-protein targets, and bridge-preconditioned states improve downstream classical folding outcomes relative to classical-only runs.

## Boundaries
This dossier does **not** claim:
- solved protein folding
- full long-range closure solved
- proof of the entire TOE
- universal generalization beyond the tested small-protein regime

It does claim:
- a real bridge-layer signal
- cross-target transfer on 1UAO and 1L2Y
- a trajectory-level operator trace
- a positive bridge-to-classical handoff result

---

## Physics interpretation
The bridge layer is treated as an intermediate multiscale selection regime between microscopic possibility and classical realization.

### Microscopic / local observables
- `dir_pen`: directional disorder in local bond propagation
- `angle_var`: angular spread
- `dihed_smooth`: local dihedral roughness

These are compressed into:

\[
R_{micro} = \exp[-(0.60\,dir\_pen + 0.20\,angle\_var + 0.26\,dihed\_smooth)]
\]

### Mesoscopic observables
- `soft_contacts`
- `density_var`
- `compactness`

These are compressed into:

\[
C_{meso} = \sigma(1.8(soft\_contacts-0.40)-0.42\,density\_var+0.8\,compactness)
\]

### Nonlocal organization term
\[
loop\_compat = \langle c_{ij}\,opp_{ij}\,bend_{ij}\,seq_{ij} \rangle
\]

### Bridge-state compression
\[
\sigma_{bridge}
=
\sigma\left(6\left[(0.36R_{micro}+0.24C_{meso}+0.40loop\_compat)-0.45\right]\right)
\]

\[
closure = \sigma_{bridge}(0.32R_{micro}+0.20C_{meso}+0.48loop\_compat)
\]

### Frozen v9 injected energy
\[
E_{v9} = E_{classical}
+ \sigma_{bridge}(0.29\,dir\_pen + 0.09\,angle\_var + 0.18\,dihed\_smooth)
-0.70\,\sigma_{bridge}\,loop\_compat
\]

\[
\quad
-2.6\,closure\,compat\_field
-0.8\,closure\,dihedral\_preserve
-1.7\,closure\,productive\_contact
-0.8\,closure\,soft\_contacts
-0.0065\,closure\,e^{-0.10R_g}
+0.78\,false\_closure
+0.024(1-\sigma_{bridge})\,density\_var
\]

with classical base:

\[
E_{classical} = 10E_{bond} + 0.5E_{repulsion} + 0.02R_g
\]

### Minimal pseudocode
```python
obs = bridge_observables(X)
sigma = sigma_bridge(obs)
closure = closure_ready(obs, sigma)

E = E_classical(X)
E += sigma * local_order_penalty(obs)
E -= sigma * loop_compat(obs)
E -= closure * compat_field(obs)
E -= closure * dihedral_preserve(obs)
E -= closure * productive_contact(obs)
E -= closure * soft_contacts(obs)
E += anti_trap_terms(obs, sigma)
```

The bridge therefore acts as a **conformation-dependent pre-classical gating layer**, not a direct final-fold solver.

---

## Final result highlights
### Cross-target frozen v9 packet
The pooled frozen v9 packet showed:
- significant pooled **best RMSD** improvement over baseline
- significant pooled **angle RMS** improvement over baseline

### Bridge-to-classical handoff packet
The pooled handoff packet showed bridge preconditioning vs classical-only:
- **best RMSD** improvement: p = 0.037175
- **contact recovery** improvement: p = 0.000765

That is the clearest evidence that the bridge creates a better starting manifold for downstream classical realization.

---

## Verification suggestions
1. Recompute all paired statistics from the CSV files.
2. Inspect whether `sigma_bridge` and `closure_ready` rise in tandem with reductions in `dir_pen` / angle disorder.
3. Compare baseline vs v9 RMSD traces to check that the effect is not endpoint-only.
4. Re-run the handoff test with the same seeds and compare bridge-preconditioned vs classical-only outcomes.
5. Test whether branch-family variants improve any single metric without replacing the frozen mainline.
6. Extend to a next topology class only with the canonical frozen v9 operator.

---

## Extension suggestions
The cleanest extension is:
- new protein topology class
- same frozen v9
- same baseline
- same handoff test

This avoids moving the mainline while testing whether the bridge effect generalizes further.

---

## One-sentence conclusion
The current evidence supports a **bounded, testable UQCF-GEM bridge-layer effect**: a multiscale pre-classical selection regime that measurably improves structural ordering and downstream classical folding outcomes in a small-protein setting, while leaving robust final long-range closure as an open problem.
