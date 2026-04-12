# UQCF-GEM Branch Family Stop Memo
## v13–v16 conclusion and next-action boundary

## Executive decision

**Stop this branch family here.**

This family includes:
- **v13** weak routing-aware productive-contact modifier
- **v14** segment-routing compatibility
- **v15** closure-opportunity field
- **v16** contact outcome discriminator

None of these branches earned promotion over frozen **v9** under the loop protocol.

So the correct action is:

> **freeze v9 as mainline and stop iterating this specific branch family.**

---

## Why this stop decision is justified

The branch loop was designed to answer one question:

> Can a narrow contact-selection modifier close the productive long-range contact gap without sacrificing the backbone-ordering gains of v9?

Across v13–v16, the answer is now:

> **Not in this branch family.**

The branches were informative, but not promotable.

---

## What each branch showed

### v13 — weak routing-aware productive-contact modifier
Result:
- improved over baseline on several metrics
- stayed stable
- but did **not** beat v9 on the screen target

Meaning:
- routing-aware modifiers can create a stable branch effect
- but the effect was too weak to matter against the mainline

Decision:
- **branch-only**
- not promoted

---

### v14 — segment-routing compatibility
Result:
- improved local ordering
- but worsened RMSD
- was significantly worse than v9 on RMSD

Meaning:
- segment-routing regularized the structure too hard
- it harmed global placement more than it helped contact-side selection

Decision:
- **rejected**

---

### v15 — closure-opportunity field
Result:
- helped dihedral RMS and contact recovery somewhat
- but hurt RMSD and angle RMS too much

Meaning:
- closure opportunity in this form nudged contact-side behavior
- but still could not preserve global foldability strongly enough

Decision:
- **branch-only**
- not promoted

---

### v16 — contact outcome discriminator
Result:
- beat that specific v9 run on RMSD and contact recovery
- but still lost to baseline on contact recovery
- and gave back too much in dihedral quality

Meaning:
- consequence-based contact scoring is directionally interesting
- but the current implementation still does not solve the real tradeoff

Decision:
- **branch-only**
- not promoted

---

## Repeating pattern across the family

This is the important scientific pattern:

### Repeatedly improved or influenced
- local/mesoscale ordering
- dihedral-side or angle-side metrics in some runs
- occasional contact-side metrics

### Repeatedly failed to preserve together
- RMSD
- angle RMS
- dihedral RMS
- contact recovery

In other words:

> the family can move the system, but not in a way that consistently dominates the frozen mainline.

That is exactly the signal the loop was meant to detect.

---

## What the family taught us scientifically

### 1. Contact-selection modifiers are not enough by themselves
These branches all tried to improve contacts via local or mesoscopic proxies:
- routing
- segment-routing
- closure opportunity
- outcome discrimination

None of them robustly closed the gap.

### 2. The current bridge still prefers ordering over full selection
The system continues to be better at:
- organizing local and mesoscale structure

than at:
- choosing the right long-range contacts

### 3. Near-neighbor hypothesis variants are no longer efficient
These branches are now too similar in failure mode:
- they reshape tradeoffs
- but do not escape the same tradeoff class

That means another small variation in this same family is unlikely to be the best use of time.

---

## Why v9 still stays mainline

Frozen **v9** remains the best current mainline because it has:
- the strongest pooled cross-target evidence
- significant pooled RMSD gain over baseline
- significant pooled angle RMS gain over baseline
- the best current balance between ordering and placement

No branch in v13–v16 beat that standard cleanly enough to replace it.

So:

> **v9 remains the acceptance baseline.**

---

## What should NOT happen next

Do **not**:
- keep iterating routing/closure/outcome micro-variants in the same family
- blur mainline and branch logic
- retune v9 casually
- claim the family almost won and just needs one more tiny tweak

The evidence says this family has been meaningfully explored.

---

## Correct next boundary

There are now only two clean options:

### Option A — Pause branching and consolidate
- keep v9 frozen
- use it as the bridge baseline in future acceptance packets
- stop branch exploration until a truly different hypothesis class is ready

### Option B — Pivot to a different hypothesis class
Only continue if the next branch is **not** another small routing/contact proxy variant.

That next class must be conceptually different.

---

## What would count as a real pivot

A real pivot would mean changing the question from:

- “Which contact looks best locally?”

to something like:

- “Which global latent state makes correct contacts inevitable?”
or
- “Which compactification regime allows productive contacts to emerge naturally?”
or
- “Which hidden variable is upstream of both ordering and contact formation?”

That would be a new hypothesis class.

This family was still trying to solve contact choice too directly.

---

## Final conclusion

> **v13–v16 should be treated as a closed exploratory family.**
>
> The family produced useful scientific narrowing, but it did not produce a promotable replacement for frozen **v9**.
>
> The correct action now is to keep **v9** as mainline and only continue if the next idea is a true hypothesis-class pivot.
