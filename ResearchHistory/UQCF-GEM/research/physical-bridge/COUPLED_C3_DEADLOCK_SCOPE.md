# C3 triangle-plus-edge coupled deadlock — prospective scope

Date: 2026-10-07.
Status: FROZEN PROSPECTIVE ANALYTICAL SCOPE. No numerical campaign or certification.

Parents:
- C2 independently accepted closeout 787467cc6a1bfc9f09f586809948ebfe16d32742.
- C3 anchor no-initial-deadlock lemma, independently accepted 3069106e708714fcaac36553cc39ef5967938b05.
- C1-C6 program f95cdfef30b452e1688172b978ee2e25fb1924d8.

## Objective

Find a genuinely coupled overlapping four-root source and target in 3<=tau<=4 where NO endpoint-only native first edit is legal, but ONE temporary auxiliary label permits an exact protected repair. Do not mistake a chosen macro deadlock for endpoint-only native deadlock.

## Frozen carrier

Palette P={a,b,c,d,e,w}, with w absent from both endpoints. Four labelled roots with original floors f1=f2=f3=f4=2.

Source:
 r1={a,b}
 r2={b,c}
 r3={a,c}
 r4={d,e}

Target:
 r1={b,d}
 r2={b,c}
 r3={c,d}
 r4={a,e}

This is a triangle of pair supports plus a disjoint edge at source, and a changed triangle plus disjoint edge at target. There are no singleton roots. Three roots have endpoint changes: r1,r3,r4. The same label d must move from r4 into r1 and r3, while a moves from r1/r3 to r4. This is an interacting dependency, not disjoint singleton permutation padding.

Endpoint-only events:
 r1: +d,-a;
 r3: +d,-a;
 r4: +a,-d;
 r2 unchanged.

## Required negative theorem

Prove source and target each have tau=3.

Prove that at source each endpoint-only deletion violates floor2; each endpoint-only addition (+d to r1, +d to r3, +a to r4) creates an explicit two-cover and tau=2. Therefore NO endpoint-only native path can leave the source while preserving 3<=tau<=4 and floors.

## Proposed single-buffer bypass

Use one temporary label w, only on r4:
 1. +w(r4)
 2. -d(r4)
 3. +d(r1)
 4. -a(r1)
 5. +d(r3)
 6. -a(r3)
 7. +a(r4)
 8. -w(r4)

Prove exact tau=3 and floor2 after EVERY primitive, exact target, and complete removal of w. Prove w is globally fresh at the source and that no additional auxiliary labels are used.

## Witness/certificate mechanism

Track the three triangle roots r1,r2,r3 and fourth root r4. Prove at every primitive:
- triangle subfamily has hitting number2;
- r4 is disjoint from the union of the current triangle labels, except where specifically checked;
- hence full tau=3.
If the proposed invariant fails at any intermediate state, replace it with exact per-state cover/missed-pair checks rather than asserting it.

Explain why moving d out of r4 before installing it in triangle roots prevents a two-cover, and why w temporarily preserves the floor and the disjoint-edge witness. Prove this from actual supports.

## Limits and rejecting controls

One example does NOT prove a general retained host-selection rule, renewable use across coupled cycles, a universal one-buffer theorem, or physical forces.

Rejecting controls must include all three endpoint-only additions and original-floor deletion failures. Compare the earlier three-singleton-anchor no-go and explain why it does not apply.

## Review gate

Freeze scope, publish author-side proof, audit every intermediate tau, then request fresh independent adversarial mathematical review of exact pinned files. No final C3 certification until independent review and publication reconciliation. C4-C6 remain open.
