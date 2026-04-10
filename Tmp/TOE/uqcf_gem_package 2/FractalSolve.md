## Novelty and Prior Art

### Positioning in Existing Literature

The problem of constructing paths through point sets has been extensively studied across multiple domains, most prominently in:

- **Traveling Salesman Problem (TSP)** literature, where the objective is to minimize total Euclidean tour length.
- **Robotics and motion planning**, where path smoothness is sometimes considered, but typically as a secondary constraint.
- **Fractal-inspired optimization**, which introduces scale-aware heuristics but generally within stochastic or population-based frameworks.
- **Protein backbone and structure generation**, where modern approaches are dominated by learned generative models (e.g., diffusion, flow-based methods).

These approaches differ fundamentally in objective, mechanism, and interpretation.

---

### Distinguishing Characteristics of This Work

The method introduced here departs from these traditions through a specific and non-standard synthesis of ideas:

1. **Coherence-First Objective**  
   The primary optimization target is not Euclidean distance but **directional coherence**, defined through an explicit path-order observable (coherence flow).

2. **Directional Memory Propagation**  
   The path is constructed through a **local propagation rule with memory**, where each step depends on the previous direction.

3. **Density-Modulated Fractal Scaling**  
   A local effective fractal dimension \( D_f \) is modulated by point density, introducing **scale-sensitive weighting** into the edge selection process.

4. **Explicit Order Parameter (Coherence Flow)**  
   \[
   C = \frac{1}{n-2} \sum_{k=0}^{n-3} \hat{\mathbf{e}}_k \cdot \hat{\mathbf{e}}_{k+1}
   \]

5. **Cross-Domain Toy Model of Emergence**  
   Applicable to arbitrary 2D/3D point clouds without domain priors.

---

### Novelty Claim

To our knowledge, the **combination** of:

- coherence-first optimization,
- directional memory propagation,
- density-modulated fractal scaling, and
- an explicit path-order observable,

has not been previously formalized as a unified framework for generating Hamiltonian-style paths.

---

### Scientific Interpretation

This work is not a shortest-path algorithm, but a **structure-first generative mechanism**.

It demonstrates:

> **Local rules + memory + scale sensitivity → emergent global geometric order**

---

## Falsifiable Predictions

This framework makes concrete, testable predictions:

### 1. Logarithmic Coherence Growth

For uniformly distributed point clouds:

\[
\mathbb{E}[C(n)] = a + b \log n
\]

**Test:**
- Generate random point clouds (n = 20 → 1000)
- Run ensemble solver
- Fit \( C(n) \)
- Verify positive logarithmic trend

**Falsification condition:**
- No systematic increase of coherence with \( n \)

---

### 2. Coherence Dominance Over Distance

Coherence-first models should produce:

- Higher coherence flow than distance-only baselines
- Longer Euclidean path lengths

**Test:**
- Compare:
  - nearest neighbor
  - distance-only
  - coherence-first

**Falsification condition:**
- No statistically significant coherence advantage

---

### 3. Ensemble Amplification Effect

Multiple random starts should produce:

- Higher **max coherence**
- Low variance in coherence distribution

**Test:**
- Run 20–100 seeds
- Compare best vs mean coherence

**Falsification condition:**
- Ensemble does not improve best coherence

---

### 4. Structural Smoothness Emergence

Coherence-first paths should exhibit:

- Reduced angular variance
- Visually smooth backbone geometry

**Test:**
- Measure angle distributions vs baselines

**Falsification condition:**
- No measurable smoothness difference

---

### 5. Cross-Domain Transfer

The same rules should produce structured outputs on:

- Random point clouds
- Protein alpha-carbon coordinates
- Other geometric datasets

**Falsification condition:**
- Behavior fails outside synthetic datasets

---

## Appendix A: Mathematical Derivation of Coherence Scaling

The coherence flow score is:

\[
C(n) = \frac{1}{n-2} \sum_{k=0}^{n-3} \hat{\mathbf{e}}_k \cdot \hat{\mathbf{e}}_{k+1}
\]

Each term represents cosine alignment between consecutive edges.

---

### Local Optimization Behavior

At each step, the solver selects:

\[
j = \arg\min \left( w_c (1 - \hat{\mathbf{e}}_{\text{prev}} \cdot \hat{\mathbf{e}}_{ij}) + \text{entropy term} \right)
\]

Thus, alignment is locally maximized.

---

### Candidate Density Scaling

In a uniform field:

- Density \( \rho \propto n \)
- Angular candidate resolution increases
- Effective candidate set:

\[
m_{\text{eff}}(n) \sim \log n
\]

---

### Expected Maximum Alignment

For \( m \) random directions:

\[
\mathbb{E}[\max a_i] \approx 1 - \frac{\pi^2}{12 m^2}
\]

Substituting:

\[
\mathbb{E}[a(n)] \approx 1 - O\left(\frac{1}{(\log n)^2}\right)
\]

---

### First-Order Approximation

For moderate \( n \):

\[
\mathbb{E}[C(n)] \approx a + b \log n
\]

---

### Empirical Fit (Example)

From ablation data:

- \( n = 20 \): \( C \approx 0.425 \)
- \( n = 50 \): \( C \approx 0.552 \)
- \( n = 100 \): \( C \approx 0.629 \)

Fit:

\[
C(n) \approx 0.0465 + 0.1274 \log n
\]

---

### Interpretation

- Each increase in system scale adds **new resolution levels**
- Local coherence propagation becomes more effective
- The path encodes **increasing geometric information**

---

## Summary

This framework provides:

- A new **optimization primitive** (coherence-first)
- A measurable **emergent order parameter**
- A falsifiable **scaling law**
- A minimal **toy model of structure formation**

It reframes path construction as:

> **an emergent, observable-driven process rather than a purely distance-minimization problem**
