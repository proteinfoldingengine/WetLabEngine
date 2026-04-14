# Minimal Math Note
## UQCF-GEM retained-information state formulation

Let:
- \(G_t\): instantaneous visible/geometric state
- \(R_t\): retained-information state
- \(S_t\): entropy/pruning ledger
- \(\Pi_t\): pruning/loss process
- \(\mathcal{A}_t\): accessible future / realizability class

### Standard reduced model
\[
\mathcal{A}_{t+1} = \Psi(G_t)
\]

### UQCF-GEM next-step model
\[
\mathcal{A}_{t+1} = \Psi(G_t, R_t)
\]

### State evolution
\[
G_{t+1} = F(G_t, R_t)
\]
\[
R_{t+1} = \Phi(R_t, G_t, \Pi_t)
\]
\[
S_{t+1} = S_t + \Delta S_{\mathrm{prune}}(t)
\]

### Interpretation
- \(G_t\) describes the present visible state.
- \(R_t\) describes structured path information not recoverable from \(G_t\) alone.
- \(S_t\) records irreversible pruning/loss.
- Time is the ordered accumulation of pruning.

### Required properties of \(R_t\)
1. Non-redundant with \(G_t\)
2. Predictive of future realizability
3. Directionally historical
4. Connected to entropy/pruning/stabilization

### Next falsifier
Test whether:
\[
Y_{t\to t+H} = \Psi(G_t, R_t)
\]
outperforms:
\[
Y_{t\to t+H} = \Psi(G_t)
\]
on a real system.
