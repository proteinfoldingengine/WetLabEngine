# UQCF-GEM Next Sprints Charter
## Objective
Raise the project from **certified local closure + empirical global non-branching** to a **minimum scientific publication standard** before the next memorandum.

## Publication gate
No new memorandum until at least **3 of 4** are complete, and one of the completed items **must** be the observable pipeline.

### Gate items
1. **First-principles advance**
   - At least one upstream derivation result from RG / lattice / flow dynamics that trends toward the observed fixed point or derives part of the kernel / exponent structure.

2. **Minimal observable pipeline**
   - One locked bridge-to-observable map producing a falsifiable number or curve.
   - Candidate outputs: growth-response curve, transfer-function deformation, lensing-response prediction, or DESI-linked observable.

3. **Reproducibility bundle**
   - External user can reproduce:
     - baseline local closure theorem
     - one family monotonicity / non-branching result
     - one microscopic basin result

4. **Hard falsification statement**
   - At least one explicit statement of the form:
     - “If X is observed, this bridge version is wrong.”

---
# Sprint structure

## Sprint A — First-principles derivation
### Goal
Derive why the bridge flows toward the observed fixed point, rather than merely showing that the fixed point is stable.

### Main question
What upstream dynamical rule generates:
- the screened pruning-flow rate
- the lagged diffusion term
- the selected fixed point gamma_*, chi_*, m_*

### Deliverables
- A formal candidate upstream flow
- One derivation note showing trend / compression toward the fixed point
- One explicit failure mode if the flow does not select the observed branch

### Immediate tasks
A1. Define a coarse RG / iterative flow ansatz for gamma, chi, W
A2. Test whether repeated flow steps compress toward the known closure point
A3. Identify which terms are load-bearing for fixed-point selection
A4. Write “selection theorem” draft if compression is robust

### Success criterion
A compact derivation note showing that the observed closure point is generated or selected by an upstream flow, not only fitted after the fact.

## Sprint B — Minimal observable pipeline
### Goal
Turn the bridge into one falsifiable observable.

### Candidate pipeline priority
1. DESI-linked growth / expansion observable
2. Lensing-response deformation
3. Transfer-function deformation

### Deliverables
- One locked parameter pipeline
- One predicted curve / number
- One out-of-sample evaluation plan

### Immediate tasks
B1. Pick the easiest observable with the shortest bridge-to-data path
B2. Write the minimal forward map from bridge variables to observable
B3. Identify public data source and test metric
B4. Lock a falsification target

### Success criterion
A stranger can see:
bridge -> observable -> prediction -> failure condition

## Sprint C — Reproducibility bundle
### Goal
Make the closure results independently runnable.

### Deliverables
- Baseline closure script
- Family monotonicity / non-branching script
- Microscopic basin script
- README with expected outputs

### Immediate tasks
C1. Freeze exact baseline parameters
C2. Separate scripts into theorem / family / microscopic folders
C3. Add expected output values and tolerances
C4. Create one-command run instructions

## Sprint D — Hard falsification statement
### Goal
State clearly how this version of the bridge can fail.

### Deliverables
- One primary falsification criterion
- One secondary falsification criterion
- One regime boundary statement

### Immediate tasks
D1. Define the strongest observable failure condition
D2. Define the strongest structural failure condition
D3. State domain-of-validity assumptions explicitly

---
# Execution order
1. Sprint A first
2. Sprint B second
3. Sprint C in parallel
4. Sprint D last

---
# First move now
## Sprint A / Task A1
Define a minimal upstream flow ansatz for fixed-point selection.

### Proposed ansatz family
Treat the bridge not as a static map but as an iterative flow in an abstract scale / RG step n:

gamma_(n+1) = gamma_n + f_gamma(gamma_n, W_n, chi_n)
chi_(n+1)   = chi_n   + f_chi(gamma_n, W_n, chi_n)
W_(n+1)     = W_n     + f_W(gamma_n, W_n, chi_n)

with target constraints:
- screening suppresses chi as gamma grows
- retained coherence raises W
- lagged diffusion lowers effective escape from the retained branch
- the closure point is a stable attractor of the coupled flow

### Minimal first test
Use the closure laws already discovered as the zeroth-order flow:
- chi ~ (1 - gamma/d_eff)W
- m = 1 + chi
- x_diff = chi - lag(gamma)

and rewrite them as a dynamical relaxation system:
- chi relaxes toward screened coherence
- W relaxes toward participation implied by the current backbone
- gamma relaxes toward 1 - sigma

### First scientific question
Does this coupled relaxation flow converge to the observed closure point from a broad set of initial conditions?

If yes, that is the first genuine upstream selection result.
If no, then the bridge still lacks a true generative rule.

Prepared as the execution charter for the next UQCF-GEM sprint cycle.
