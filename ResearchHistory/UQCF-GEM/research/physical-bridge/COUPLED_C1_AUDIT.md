# C1 audit — minimum overlapping protected carrier

Date: 2026-10-07.
Status: AUTHOR-SIDE WHOLE-ARGUMENT AUDIT PASSED; C1 independent review not yet completed.

Scope: COUPLED_AUXILIARY_SCOPE.md at f95cdfef30b452e1688172b978ee2e25fb1924d8.
Lemma: COUPLED_C1_MINIMAL_OVERLAP.md at 5836e007044372fd61316a360a0b224e2fd1c8ea.

## Checked proof obligations

- Nonempty roots imply tau<=n by selecting one label from each root.
- Pairwise disjointness forces >=n distinct labels in any transversal.
- One overlap gives a transversal of size at most n-1 by hitting the overlapping pair with one label.
- Therefore tau=n iff pairwise disjoint.
- For n=3 protected tau>=3 implies disjointness.
- For n=4 overlap implies tau<=3, and protected lower bound forces equality3.
- Positive four-root overlap control has forced d,e and a common hit a, giving tau3.
- Rejecting control has two-cover {a,e}, giving tau<=2.

## Padding trap for the next checkpoint

Take four roots
    r1={x}, r2={y}, r3={z}, r4={x,z}
and target
    r1={y}, r2={x}, r3={z}, r4={x,z},
all floors1.

Both endpoints have tau=3 because the first three singleton roots force three distinct labels. There is genuine overlap through r4.

The six-edit buffer path from the earlier singleton swap still works:
    +w(r1), -x(r1), +x(r2), -y(r2), +y(r1), -w(r1).

At every state, the first three roots require three distinct hitting labels (with the buffered root always using w when needed), and a three-cover can be chosen that also hits r4: use z for r3/r4, the current singleton/available label for r2, and one label for r1. Thus tau=3 throughout.

BUT r4 is unchanged and introduces no additional endpoint obligation. This is only a padded singleton-swap construction, not evidence of genuinely coupled-cycle repair. It must be rejected as satisfying C2's coupled-obligation requirement.

This is a methodological rejecting control: overlap alone is insufficient evidence of interacting dependency cycles.

## Outcome

C1 is a valid bounded structural candidate by author-side proof. C2 remains OPEN and requires a carrier with at least two genuinely interacting endpoint obligations, not a passive overlapping root. No numerical campaign or independent acceptance is claimed.
