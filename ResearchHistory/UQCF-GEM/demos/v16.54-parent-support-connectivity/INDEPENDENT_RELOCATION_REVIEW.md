# Independent review — hyperedge star relocation

Reviewer: /root/v1654_relocation_review. Verdict: ACCEPT.
Artifact: HYPEREDGE_STAR_RELOCATION.md at 8a63b59c5104eab214052dbbc6e7a8a944a72f9a.
Verified SHA256: 70cc9abe8e63f48820b656b95cb1a4a6a359bea4360090ceb1028ff05ce12251.
Critical: none. Important: none. Minor: none.

## Checks

- X directly proves both bounds: fixed roots force q-1, and their minimum cover plus u supplies q. Union paths respect each slot's floor.
- Redundant-root normalization retains all core representatives and remains exact-q.
- Relocation fits because binomial(b,h-1)<=binomial(a-1,h-1). Fixed duplicates remain redundant in the non-u core; editable duplicates and P fillers retain u.
- Completed relocations restore complete cores and exact q. The integer size potential strictly decreases and core counts never increase.
- Canonicalization properly invokes the label/root permutation lemmas. Reversed endpoint paths retain the band.
- Cross-module clones give f=lambda=q-1, including minimal modules: deleting a size-h source star leaves no root, of hitting number zero; contracting a size-h destination leaves one (h-1)-root, of hitting number one.
- Within-module clones preserve the pure core. The restricted completed-operation system remains in the same symmetry class.
- The h=3,k=8,r=11,q=4 construction correctly replaces six old triples with three new triples and three fillers under a fixed guard of three.
- Restricted-operation incompleteness is not described as native disconnection; branching inside a primitive clone path is explicitly outside that restricted system.

## Declined / outside review and executor rulings

- Numerical enumeration: not performed. Ruling: symbolic theorem only, no passing-case claim.
- Scientific execution: not performed. Ruling: no execution/certification claim.
- Simulations: not performed. Ruling: none used as evidence.
- Tests: not performed. Ruling: no test-passing claim; a future implementation needs its own protocol.
- File mutation: review was read-only. Ruling: executor handles publication and verifies bytes separately.
- Implementation certification: outside scope. Ruling: not CLOSED/CERTIFIED.
- Arbitrary-endpoint connectivity: not proved. Ruling: OPEN outside the scoped module family and earlier theorems.
- Efficiency: not proved. Ruling: explicit finite progress only, no complexity guarantee.
- Physical claims: excluded. Ruling: none inferred.

The executor separately checks exact Git publication, ancestry, changed-file scope and draft state. No unresolved findings remain.
