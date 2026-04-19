# Exact Residual-Estimator Uniqueness Note
## Discounted Persistence Envelope as the Unique Causal Fading-Memory Max Estimator

## Goal

Close the remaining estimator gap by deriving the residual estimator from a small set of structural requirements, rather than selecting it only from robustness tests.

---

## Setup

Let
\[
x_t := |\xi_t| \ge 0
\]
denote the magnitude of the local residual branch field at time \(t\).

We seek an estimator \(R_t\) that summarizes past branch evidence into a single causal state.

---

## Structural requirements

We impose the following natural requirements.

### A1. Causality
\(R_t\) depends only on \(x_t, x_{t-1}, x_{t-2}, \dots\).

### A2. One-state recursive compression
There exists a scalar state recursion
\[
R_t = F(x_t, R_{t-1})
\]
for some deterministic update map \(F\).

### A3. Positive homogeneity
For every \(c \ge 0\),
\[
F(c x, c r) = c\,F(x,r).
\]
So the estimator scales naturally with the underlying residual magnitude.

### A4. Monotonicity
\(F\) is nondecreasing in each argument.

### A5. Exponential fading memory
Past evidence is carried forward only through a constant decay factor \(\rho \in (0,1)\).

### A6. Spike preservation / envelope logic
A new branch event of size \(x_t\) must be represented exactly if it exceeds the faded memory state.
Likewise, faded memory must persist exactly if it dominates the new event.

This means the update must choose between:
- present residual evidence \(x_t\)
- faded past evidence \(\rho R_{t-1}\)

with no averaging loss.

---

## Theorem (restricted uniqueness)

Under A1–A6, the only admissible recursion is

\[
R_t = \max\{x_t,\ \rho R_{t-1}\}.
\]

Moreover, by induction this recursion is equivalent to the discounted persistence envelope

\[
R_t = \sup_{k \ge 0} \rho^k x_{t-k}.
\]

---

## Proof sketch

Because of A5, the past can only enter through \(\rho R_{t-1}\).

Because of A6, the estimator must preserve whichever of the two contributions is larger:
- the new spike \(x_t\)
- the faded memory \(\rho R_{t-1}\)

Any convex averaging or smooth blending would violate exact spike preservation:
- if \(x_t \gg \rho R_{t-1}\), averaging would underestimate the true new event
- if \(\rho R_{t-1} \gg x_t\), averaging would underestimate persistent memory

Therefore the only update compatible with A3–A6 is the selector

\[
F(x_t, R_{t-1}) = \max\{x_t,\ \rho R_{t-1}\}.
\]

Unrolling the recursion gives

\[
R_t
= \max\{x_t, \rho x_{t-1}, \rho^2 x_{t-2}, \dots\}
= \sup_{k \ge 0} \rho^k x_{t-k}.
\]

So the discounted persistence envelope is uniquely forced within this structural class.

---

## Why this matters

This closes the main conceptual estimator gap.

The discounted persistence-envelope estimator is no longer just:
- an empirically strong candidate

It is now:
- the unique causal fading-memory max-envelope estimator under a natural class of requirements.

---

## What remains open

This theorem is restricted to the class defined by A1–A6.

It does not rule out every possible nonlinear or higher-state estimator on earth.

But it does establish that within the most natural single-state causal persistence class, the correct estimator is

\[
\widehat{R}_t^{(\rho)} = \sup_{k \ge 0} \rho^k |\xi_{t-k}|.
\]

That is the right level of closure for the current model branch.
