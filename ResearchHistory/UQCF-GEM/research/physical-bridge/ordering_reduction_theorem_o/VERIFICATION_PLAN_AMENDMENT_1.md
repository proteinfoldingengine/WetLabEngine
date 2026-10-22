# Amendment 1 to the prospective verification declaration (Theorem O witness check)

- **Author:** proteinfolding-grokbot (Grok), 2026-10-22 ~2:05 PM America/Phoenix.
- **Status:** prospective. Written BEFORE any producer or checker code exists and before any execution. VERIFICATION_PLAN.md (SHA-256 078ea964…ba21, commit 90e98032) is preserved unchanged; where this amendment conflicts with it, this amendment governs.
- **Reason:** dot's challenge T-060-dot (PR #111 comment 6350125009, transcribed in AGENT_THREAD/THREAD.md at 323adfe1). Replay of every listed history plus an equal independent count does not establish set equality when duplicates are allowed: replacing one valid stopped history h2 by a second copy of another valid h1 keeps the length and passes every replay. VERIFICATION_PLAN.md §4 is therefore insufficient as written. The challenge is accepted in full.
- **Scope unchanged:** finite six-vertex witness of RESULT.md §7 only; no change to Theorem O, its premises, controls or limits; native bridge NOT_DERIVED.

## A1. Canonical identities

Each command is written as the string `<sign><colour>(<vertex>)` with sign in {+,−}, colour in {a,b,r}, vertex in {o,u,v,w,x,y}. A history is identified by the tuple (s, C3flag, c_1, …, c_n) of its source index s, its universe tag (`O` for U_O(s), `C3` for the restricted C3 class) and its full ordered command sequence. The canonical identity string is these fields joined by `|`. Two histories are the same iff their identity strings are equal. NOOP resolutions (C1 semantics) are recorded as a separate field and are not part of the identity, because they are determined by the command sequence and the state.

## A2. Checker obligations (replacing the replay-plus-recount clause of §4)

The checker, written without importing the producer, must:
1. **Construct the full canonical set independently.** Enumerate every stopped history of U_O(s) (s = 0, 1) and of the C3 class by breadth-first search over **history prefixes**, not over states. Each frontier node carries the full command prefix, the position reached in σ, the identity of the first r-command (or none), and for C3 whether the single permitted inverse has been used. No two prefixes are merged because their supports coincide. Dead ends (prefixes with no legal admissible extension before the stopping condition) are collected as their own canonical set.
2. **Require exact identity equality.** Reject the producer output unless (a) it contains no duplicate identity string, (b) its set of identity strings equals the checker's set exactly for each universe (missing and extra identities are listed on failure), and (c) its dead-end set equals the checker's dead-end set exactly. Count equality is reported but is not a pass condition by itself.
3. **Re-verify each record.** Replay every producer history with the checker's own support-set legality, check that it meets the stopping condition at its last command and not earlier (no truncation, no extension past the first stopping boundary), and recompute its first r-command and decoded value; any mismatch with the producer's recorded values rejects.
4. **Menus and controls** exactly as VERIFICATION_PLAN.md §§2–3, computed by the checker independently.

## A3. Mandatory mutation controls on the checker

Before reporting a pass, the checker is run on deliberately corrupted copies of the producer output and must REJECT each one; a checker that accepts any corrupted copy is unsound and the run is RED. The corruptions, each applied once per universe where applicable:
1. omission of one stopped history;
2. duplicate-for-omission substitution: one stopped history replaced by a second copy of another valid stopped history (the T-060-dot case; e.g. in source 0, σ followed by −r(v) and −r(v) followed by σ);
3. truncation of one history to a proper prefix (stopping condition not met);
4. extension of one history by one further legal command past its first stopping boundary;
5. a wrong decoded value on one history;
6. an illegal command spliced into one history;
7. one history moved to the wrong source index s;
8. false coverage metadata: a declared count or universe hash that disagrees with the listed records.
Each corruption is generated deterministically (fixed choice: the lexicographically first eligible record) and the rejection reason is logged.

## A4. Inherited foundational stack

Theorem O and its witness use only the one-command legality grammar of RESULT.md §2; they do not call or modify any inherited operation, so the inherited stack is a regression gate, not evidence for the witness. Applicable inherited check: the FCV-1 foundational-closure behavioral and deliberate-defect suite (ResearchHistory/UQCF-GEM/foundational-closure-verification, workflow uqcf-foundational-closure-verification.yml, sympy==1.13.3, mpmath==1.3.0) run unchanged as a job of the same workflow at the same checked-out SHA. Its exact log is published with the witness evidence. A failing inherited job makes the run RED regardless of the witness result.

## A5. Execution and publication (adds to §4)

Pinned actions and Python 3.11 with the standard library only for producer and checker. One run on a frozen commit; workflow SHA and checked-out scientific SHA recorded; producer JSON, checker report, mutation-control log, inherited-suite log and SHA-256 checksums uploaded as artifacts; the deterministic producer bytes are regenerated in a separate publication job and must match byte-for-byte; downloaded artifact digests are inspected before evidence is committed. Any failure is published as an adverse finding; neither this declaration nor VERIFICATION_PLAN.md is revised after results are seen.

## A6. Role (unchanged)

This finite check is a consistency check of one witness and its rejecting controls. No finite no-counterexample result is a universal theorem; the gate for Theorem O itself remains the independent whole-argument review of RESULT.md r1.
