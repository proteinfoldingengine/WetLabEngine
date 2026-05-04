# ROUND16_PRECOMMIT.md

## Round 16 — Pre-Registered Cluster/Merger Expansion Round

### Status
**Precommit draft**  
No Round 16 system may be counted as analyzed until this document is frozen.

---

## 1. Purpose
Round 16 is the pre-registered frozen-scaffold expansion of the cluster/merger regime following Round 15’s **conditional hardened prototype win**.

Round 15 ended with:
- **Abell 2261** → positive
- **Abell 1689** → neutral
- **Bullet Cluster** → positive
- **0 catastrophic failures**

Round 16 exists to test whether that result generalizes across a broader, precommitted cluster sample without per-object retuning.

---

## 2. Core rule
The exact same frozen UQCF-GEM / restricted-bridge / gas-first scaffold used in Round 15 will be carried into Round 16.

### Frozen-round rule
No per-object retuning is allowed.

That means:
- no object-specific parameter fitting
- no cluster-by-cluster threshold changes
- no adding special-case physics for individual systems
- no modifying scoring logic after seeing outcomes

Only the source set expands. The scaffold stays frozen.

---

## 3. Scope of Round 16
Round 16 remains entirely inside the **cluster/merger regime**.

It is **not** a galaxy round, BAO round, CMB round, or cosmology-closeout round.

The round has two tiers:

### Tier 1 — Relaxed clusters
Purpose:
- test bounded profile agreement on source-locked, page-anchored X-ray/lensing cluster data

### Tier 2 — Merger/offset systems
Purpose:
- test whether gas–mass offset behavior remains recoverable under the same frozen scaffold

---

## 4. Two-gate structure

### Gate A — Source-lock gate
A system may only enter scoring if all of the following are true:
1. a valid public gas/X-ray anchor is found
2. a valid public lensing/mass anchor is found
3. exact pages are locked
4. extraction is feasible
5. the sources are not generic reviews, unrelated papers, or non-scoreable placeholders

If any of the above fail, the system is marked:
- `candidate_found` or
- `active_candidate_not_locked`

but it does **not** count toward scoring.

### Gate B — Scoring gate
Only systems that pass Gate A count toward Round 16 scoring and win/loss determination.

This prevents bad PDFs or source-quality failure from being misread as model failure.

---

## 5. Sample plan

### Sample target
Round 16 targets **8–12 systems**.

### Minimum valid scored sample
A valid round requires at least **6 source-locked systems** to enter scoring.

If fewer than 6 systems become source-locked, the round is **incomplete**, not failed.

---

## 6. Precommitted candidate list

### Tier 2 merger systems
1. **1E 0657-56 (Bullet Cluster)**
2. **MACS J0025.4-1222**
3. **Abell 2744**
4. **Abell 520**
5. **ACT-CL J0102-4915 (El Gordo)**
6. **One additional merger analog or holdout system**

### Tier 1 relaxed clusters
1. **Abell 2261**
2. **Abell 1689**
3. **Abell 1835**
4. **3–5 additional relaxed clusters** with valid page-lockable X-ray + lensing anchors

---

## 7. Holdout rule
Round 16 should include at least **one holdout system** if feasible.

The holdout may be named in advance, but its locked source pages should not be opened until after scaffold and scoring rules are frozen.

---

## 8. Scoring rules

### Tier 1 scoring
Primary metric:
- **mean absolute normalized gap**

Interpretation:
- **positive** if mean gap < 0.10
- **neutral** if 0.10 ≤ mean gap < 0.25
- **destructive** if mean gap ≥ 0.25

### Tier 2 scoring
Tier 2 uses gas–mass offset reporting in **kpc**.

Prototype interpretation:
- **positive** if clear nonzero bounded offsets are recovered for the key merger structure
- **neutral** if the signal is partial, weak, or ambiguous
- **destructive** if offsets collapse, reverse nonsensically, or fail in a way that breaks the intended test

### Catastrophic failure rule
A catastrophic failure is:
- large destructive mismatch
- unphysical output pattern
- or complete breakdown of intended bounded behavior relative to the locked observable target

---

## 9. Round 16 win criteria
Round 16 is declared a **win** only if all of the following are true:

1. at least **6 source-locked systems** are scored
2. **0 catastrophic failures**
3. at least **70% of scored systems** are positive or neutral
4. at least **2 Tier 2 systems** are positive or neutral  
   or at minimum:
   - **1 strong Tier 2 positive** plus strong Tier 1 support
5. no evidence that success depends on per-object retuning

### No-win conditions
Round 16 is **not won** if:
- catastrophic failures occur repeatedly
- positive/neutral rate falls below threshold
- too few systems become source-locked to constitute a valid round
- or frozen-scaffold discipline is violated

---

## 10. Optional baseline comparator
A frozen comparator against standard halo-model scoring is strongly recommended.

If included:
- it must be defined before scoring
- it must be applied on a declared subset
- post-hoc comparator design is not allowed

---

## 11. Required artifacts
Round 16 must produce:
- `ROUND16_PRECOMMIT.md`
- locked target list
- source-lock records
- extraction templates
- scoring JSON files
- checkpoint JSON
- methods/math note
- Python replication note
- closeout memo
- zip bundle

---

## 12. Scientific posture
Round 16 is not designed to prove everything.

It is designed to answer:

> Does the frozen gas-first scaffold remain bounded, inspectable, and non-catastrophic as the cluster/merger sample expands under precommitted conditions?

---

## 13. Summary statement
Round 16 is a disciplined expansion round.

It inherits the Round 15 checkpoint:
- **2 positive**
- **1 neutral**
- **0 catastrophic failures**

and tests whether that structure survives a larger, precommitted, source-locked cluster sample under the same frozen scaffold.
