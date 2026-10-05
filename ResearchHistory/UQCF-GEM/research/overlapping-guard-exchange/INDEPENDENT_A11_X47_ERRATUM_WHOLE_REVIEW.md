# Independent whole-argument and source-integrity review - A11.X47 erratum

Reviewer: independent Codex review agent `/root/x47_whole_argument_review`  
Date: 2026-10-05 UTC  
Repository: `proteinfoldingengine/WetLabEngine`  
Exact corrected candidate: `4372e9fc280ed0fd7f4b9c21c796bcc84d96dff4`  
Exact corrected tree: `82f74f55179a2683e90047c8e905c1406fb4c5be`

Reviewed sources:

- `A11_X47_SOURCE_INTEGRITY_ERRATUM_SCOPE.md`, blob `b8afd699f1004dd1bf3ba9b10f94992fb99507f1`
- `A11_X47_REDUNDANCY_ORBIT_OBSTRUCTION_CORRECTED.md`, blob `29d5a612862d84c85a47a56ee47409f029e96719`
- historical accepted X47 publication head `6414a606bba86712faa89222ef5f7d5203085acd`
- historical accepted X47 proof and whole review
- inherited X40, X45, X46 and maximum-layer Theorem A sources

## Verdict

**ACCEPTED.** The candidate is a faithful source-integrity correction of the accepted X47 theorem. The incident diagnosis is reproduced exactly, the new scope and corrected proof contain no forbidden control or replacement characters, the mathematical statement is equivalent to accepted X47, the historical corrupted artifacts remain unchanged, and no new theorem or certification claim is introduced.

## 1. Incident diagnosis and preservation boundary

I independently scanned the accepted publication head. Counting C0 characters below code point 32 while permitting tab, line feed and carriage return gives:

- historical proof: 39 forbidden controls;
- historical whole review: 19 forbidden controls;
- historical closeout: 4 forbidden controls;
- X47 block in `KNOWN_RESULTS.md`: 5 forbidden controls;
- X47 block in `NEXT_OBLIGATION.md`: 5 forbidden controls;
- X47 block in `A11_PROGRESS.md`: 5 forbidden controls.

The historical proof and whole review each contain zero literal backslashes. The forbidden characters are the expected backspace, vertical-tab and form-feed values produced when ordinary JavaScript template literals interpreted intended mathematical escape prefixes. Carriage-return escape damage is consistent with the visibly split source but is correctly excluded from the forbidden-count rule stated by the erratum scope.

This confirms the diagnosed failure mode: byte identity was checked against an already escaped in-memory string, so the former readback could succeed without proving readable mathematical source integrity.

The candidate is exactly two commits ahead of the accepted X47 publication head and adds only:

- `A11_X47_SOURCE_INTEGRITY_ERRATUM_SCOPE.md`;
- `A11_X47_REDUNDANCY_ORBIT_OBSTRUCTION_CORRECTED.md`.

No historical file is deleted, rewritten or relabelled. The historical X47 proof remains blob `64cc6db67bda2bf3e2dfa0db37107f099fd6fb98` and is explicitly retained as incident evidence. The corrected file uses a new filename and states that it is the authoritative readable rendering.

## 2. Corrected-source integrity

Fresh scans of both new files found:

- zero forbidden C0 characters;
- zero replacement characters;
- zero literal backslashes, as intended by the ASCII-math policy.

The corrected proof contains the required literal source tokens for:

- `beta(C) < ceil(ell/2)`;
- `H_alt intersect pi^(-1)(H_alt) = empty`;
- `beta = m/2`;
- `Gamma = d m/2`;
- `rho = d [C(m-2,2) - 2]`;
- applying Theorem A only after the complete lower-protected endpoint path exists;
- the explicit non-disconnection limit.

The GitHub blobs read back as `b8afd699f1004dd1bf3ba9b10f94992fb99507f1` for the scope and `29d5a612862d84c85a47a56ee47409f029e96719` for the corrected proof.

## 3. Exact mathematical equivalence

The corrected X47B statement is unchanged. The union of the rootwise bad-start sets is exactly the bad-start set, so beta is exact and beta <= Gamma is the union bound. If beta < ceil(ell/2), more than floor(ell/2) cyclic starts are good, forcing two adjacent good starts. Forward rotation sends W_t to W_(t+1), which gives the X45 same-representative intersection. The even alternating construction realizes equality with no adjacent good pair, while the proof continues to state that the scalar condition is sufficient rather than necessary.

The corrected X47O family is the same accepted family. For every even m >= 8 and d >= 1, it declares d labelled copies of G minus J for each four-set J that is not an even-start cyclic window, with saturated floor m-4 and singleton role groups.

The exact-four proof is unchanged:

- a four-set I misses G minus J exactly when I = J, so the omitted even windows are exactly all four-covers;
- every three-set has at least five four-set extensions and lies in at most two cyclic four-windows, so some declared complementary root misses it;
- smaller sets extend to three-sets and are missed as well.

The ownership statement is unchanged. The one-step destination rotation gives one full directed m-cycle. It sends every even-start cover window to an odd-start non-cover, so the X45 intersection is empty for the only ownership cycle.

The exact quantities are unchanged:

- beta = m/2;
- Gamma = d m/2;
- rho = d [C(m-2,2) - 2].

The rho formula remains exact because a pair is contained in C(m-2,2) four-sets and in at most two even-start windows, with two attained by an appropriately placed adjacent pair. The inherited X40 inequality is also unchanged: rho >= m-2, and the central-binomial bound is strictly greater than m(m-3)/2 for m >= 8.

## 4. Lower path, upper conversion and controls

The corrected proof retains the accepted dependency order. X40L first supplies a complete lower-protected endpoint-to-endpoint path with actual pair witnesses, tau >= 3, same-floor legality, eligible continuation, renewal, finite progress and exact labelled restoration. Only after that complete path exists may maximum-layer Theorem A convert it to a path with 3 <= tau <= 4. The corrected proof does not transfer the preliminary schedule, event minimum or unfinished waypoints through that conversion.

The prior-method separations are mathematically unchanged and correctly scoped:

- X38 is excluded by the unique cycle length m >= 8;
- X39 is excluded by mask width m-4 < m-3;
- X40U is excluded by singleton role groups, while X40L remains the lower dependency;
- X41 is excluded by distinct role incidence profiles and roots containing at least four profiles;
- X43 would require 4 >= m-1;
- X44 is excluded by cover density below one half;
- X45 has empty exact representative intersection;
- X46 has Gamma = d m/2, not below m/2.

The saturated controls are also preserved: four disjoint floor-safe supports would require 4(m-4) > m; two labels with footprints forming an even window hit every whole endpoint-union root; and every root changes because no proper nonempty four-set is invariant under the transitive full rotation.

These are controls on earlier sufficient methods, not a native no-path theorem. The corrected proof continues to note the X40L-plus-Theorem-A band path and theorem L connectivity.

## 5. No new claim

The corrected source preserves all accepted limits. It does not claim arbitrary endpoint accessibility, unequal corresponding group sizes, below-X40 lower repair, failure of every direct upper strategy, native disconnection, unrestricted mixed-floor, directed, higher-target or nested universality, originality, physical interpretation, numerical execution, implementation, benchmark, integration merge or numbered certification.

The next mathematical obligation remains a joint condition linking actual lower witnesses to transitions among actual four-covers. The erratum authorizes only readable-source repair. Certified v16.55 and v16.54, their frozen evidence, integration history and the separately unstarted efficiency work remain outside this correction.

## Publication gate

The exact corrected candidate and tree named above are accepted without mathematical revision. Reporting may now identify the historical rendering as superseded for reading, reference the corrected authoritative file, preserve the historical artifacts and accepted theorem status, and proceed through the separately required reporting review and immutable readback gates.
