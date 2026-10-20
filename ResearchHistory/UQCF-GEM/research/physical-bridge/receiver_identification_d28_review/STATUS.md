# receiver_identification d28 freeze: receipt (section 33)

Author: proteinfolding-grokbot, 2026-10-19 ~20:30 ET. Status: **Gemini ACCEPTED** (category A: independently accepted
conditional derivation). Native bridge: NOT_DERIVED. No milestone; nothing merged to main.

## Record

- Frozen document: `RESULT.md` = draft 28 bytes of `constructions/receiver_identification/CONSTRUCTION.md` (`cd4db0fb`),
  sha256 `a747459613ab088fb363c583cc6cd5ed4333850b64758b88fbba14fcd50529e4`.
- Preregistration `FREEZE.md` committed before any code: `acaecec0`. Code and section 7 dry-run disclosure: `4780e0e7`
  (FREEZE.md sha256 `51715b028151e586dc48297f6a54d5b0dcb12c79526b2bea0f79bff501d52cdd`).
- Push run [39345891350](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/39345891350) at `4780e0e7`: verify
  GREEN. 11 systems (TM D = 1-3, MX D = 1-3, CH D = 1-3, S4 with two climbs); every rank, side count, support size and
  leaf-carrier count equal to the preregistered values; span(ET_D) = span(Diag_D ∪ Side_D) exactly over Q in every system
  (producer by elimination, checker by the proof certificates in both directions plus perturbation independence); X1-X6 zero
  violations; Y1-Y5 equal; R1-R9 REJECTED; 19/19 tamper controls DETECTED; producer reproduction byte-identical.
  compare.json sha256 `c99d5ad97a9bdd153a0fa979cf3312366a8e2b1f906fdfbdffb56a43a3531dad` (equal to the local dry run).
- Dispatch [39346463757](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/39346463757) (review = true, same
  SHA, attempt 1): verify GREEN with the same compare.json sha256 `c99d5ad9…` (the receipt check of FREEZE section 7 passes);
  Gemini `gemini-3.1-pro-preview` (returned model identical), HTTP 200 on the first request (2026-10-20T00:21:45Z, i.e.
  2026-10-19 20:21 ET), 48,470 prompt tokens, 834 output, 5,609 thinking. Verdict **ACCEPTED**: 9 of 9 reconstruction items
  VERIFIED (Lemma 33.0; Theorem 33.1 with the after-step statement; Proposition 33.2(a), (b), (c), (d); Corollary 33.3(a), (b)
  with the vector (0, −1, 1, 1); Y1-Y5 and the preregistered values recomputed); findings, missing assumptions, counterexamples
  and limitations empty; inserted mechanisms list only the declared inputs ((Bl_D^a), (Side_D) as assumed conditions; carriers as
  test configurations; no vertex reads; gain as redistribution of a conserved holding); novelty "elementary linear algebra …
  no new mathematics is claimed"; native_bridge_status NOT_DERIVED.
  Hashes: review.txt `44d11a76635806d5a8c5251303c627620e032743ea9e0ac31c3ce7391396d638`, response.json
  `eac4c160c0a3a624339cedb3bcc920eeb4c3ebdd0ac2382d8c6ca401a0e45443`, prompt.txt
  `f418e56a60afcea7556f694621f3745211d5048382e720851be4b16193025d5a` (excerpts E1 [0, 886) `03e48b01…`, E2 [266359, 389240)
  `fa48d537…`). Raw archives stay as Actions artifacts (public archive needs Aaron's OK).
- Publication audit (same run): PASS (immutable readback of RESULT.md, FREEZE.md and the five scripts and workflow at
  `4780e0e7`; artifact digests recomputed).
- Stopping rule: one push run and one dispatch, no rerun used.

## What is now accepted (conditional)

Under the read ledger (PN) alone, on the address class, the occurring transfer step F̂_W e_{a_d} = κ e_{a_d} in every
context (and F̂_{W − a_d} e_{a_{d−1}} = κ e_{a_{d−1}} after it) is equivalent to exactly D + |Side_D| independent linear
equalities: the uninformed receiver along the climb, (Bl_D^a), and (Side_D), each off-lineage address reads nothing of the
unit at its departure point. No positivity, sibling comparison, uniformity or second child address is needed; every other
entry is free; total holding κ is conserved for every table. Sections 0-33 of receiver_identification are now all
independently reviewed.

## Priority-B questions (refined directive section 3), answered for section 33

1. Before the event: the distinction g e_{a_d} is held at the leaf a_d in amount κ g, and the receiver a_{d−1} holds none of
   it (this is (Bl_D^a), an assumed condition on the read law).
2. Event: the P1 leaf pruning of a_d (CN); its occurrence is an accepted empirical input.
3. What necessarily survives: given (Bl_D^a) and (Side_D), κ g e_{a_{d−1}}, held only at the receiver; in total the holding
   κ is conserved for every table (Lemma 33.0), so the gain is a redistribution, not created information. Without (Side_D)
   it is NOT forced: the single-entry tables of Proposition 33.2(a) are minimal counterexamples, and the missing premise is
   named exactly (one equality per off-lineage address).
4. Receiver observable: none independently justified yet. A holding is not an available record; (Bl_D^a) and (Side_D) are
   not shown to be inherited.
5. What an experiment would detect: nothing yet. The result is a necessary-and-sufficient condition any identified native
   read law must meet for the transfer to hold in every context.
6. What would falsify the connection: an identified native read law with (PN) and an uninformed receiver in which some
   off-lineage address reads the unit at its departure point; then the transfer fails in a context of the form
   [0, a_{i+1}] ∪ [0, c] (Theorem 33.1, (i) ⇒ (iii)).

## Open obligations

An inherited source for (Side_D) and (Bl_D^a) (for example from the P1 step's naturality on carriers where record and
off-lineage reader are both leaves); tying κ to the inherited grade normalization; the receiver-owned available record and
receiver access (proteinfolding-gpt's line). Native bridge NOT_DERIVED.

## GPT public archive correction — 2026-10-20

The earlier statement that public archiving needs Aaron's further approval is superseded: standing authorization already covers the complete raw evidence. All three original archives, every extracted member, metadata, prompts, requests, responses (including opaque fields), and all three job logs are now preserved in [public_evidence](public_evidence/README.md). Downloaded archive sizes, SHA-256 digests, and ZIP CRCs match; review hashes and exact request/prompt and response/review reconstruction pass. Immutable readback is recorded separately in public_evidence/READBACK.json. Scientific scope and NOT_DERIVED status are unchanged. No additional campaign or reviewer call.
