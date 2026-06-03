# V1210 — Review Rubric

## PASS

A PASS means:

```text
The evidence supports the narrow claim:
admissibility → B-like/source-flow closure propagation
```

and the reviewer agrees ADM-like recovery is not established.

Requirements:

- V1201 shows closure ablation damages the branch.
- V1202 shows closure strengthening improves the branch.
- V1203 shows ordered-slice propagation.
- V1204 shows no-closure vs closure necessity.
- Manuscript does not overclaim ADM/GR.

## WEAK PASS

A WEAK PASS means:

```text
The direction is supported, but methodology needs stronger held-out tests.
```

Common reasons:

- closure term and B-like metric are too closely related
- candidate families are too narrow
- valid retained weight is not dominant enough
- flow coherence improvement is modest

## FAIL

A FAIL means:

```text
The evidence does not support even the narrow B-like/source-flow claim.
```

Common reasons:

- B-like closure was only a final classifier
- adversaries were too weak
- result is tautological
- no independent propagation evidence
- claim exceeds evidence

## Automatic fail flags

- Claims physical GR was derived.
- Claims Einstein equations were recovered.
- Claims full ADM-like recovery from current evidence.
- Ignores unresolved ADM_M branch.
