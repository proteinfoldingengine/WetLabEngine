# V1059 Reviewer Prompt Brief

**Status:** copy/paste external reviewer prompt  
**Purpose:** Give an independent reviewer a clean falsification task.

## Prompt

```text
You are an independent scientific reviewer. Your task is to falsify, not extend, the following finite it-from-bit recoverability model claim.

Core frame:
- Do not assume physical spacetime.
- Do not assume physical clock time.
- In this model, tau is pruning / recoverability order.
- Geometry-like Omega is the invariant residue of admissible pruning.

Law under review:
T ~Omega identity iff [Pi_sum(T(E)) = Pi_sum(E)] and [Pi_moment(T(E)) = Pi_moment(E)].

Definitions:
- E: finite expressed event/order ensemble.
- T: pruning / recoverability transformation acting on E.
- Omega(E): partition-memory observable.
- Pi_sum(E): partition-sum spectrum over E.
- Pi_moment(E): partition-moment spectrum over E.
- T ~Omega identity: Omega(T(E)) and Omega(E) generate the same class set.

Your job:
1. Reimplement from these definitions only.
2. Do not reuse prior code.
3. Generate your own transform families.
4. Try to find counterexamples:
   a. Pi_sum and Pi_moment preserved but Omega-gauge equivalence fails.
   b. Pi_sum or Pi_moment broken but Omega-gauge equivalence still holds.
5. Verify whether the partition-sum-only law fails.
6. Verify whether adding partition-moment repairs the failure.
7. Run at least one tiny exhaustive transform family.
8. Report all false positives and false negatives.

Pass condition:
The refined two-invariant law predicts Omega-gauge equivalence with zero FP/FN across your independent tests.

Failure condition:
Any transformation T where the refined law prediction disagrees with Omega-gauge equivalence.

Strict boundary:
Do not claim physical spacetime, physical clock time, General Relativity, Einstein equations, ADM recovery, quantum gravity, or a universal theorem over all maps.

```
