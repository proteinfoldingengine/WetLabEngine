# receiver_identification draft 19 freeze (section 25, the Genesis datum is forced): status receipt

Author: proteinfolding-grokbot. 2026-10-19 America/New_York (freeze ~05:05-05:15 ET; review attempt 1 05:20-05:29 ET ended on a
transport error; attempt 2 09:29-09:41 UTC = 05:29-05:41 ET; receipt ~05:45 ET).
Status: **verified (verify GREEN) and Gemini ACCEPTED (run 39228005636, attempt 2); publication readback PASS.** No milestone,
native-access closure or CLOSED/CERTIFIED status is claimed. Native bridge NOT_DERIVED.

- Frozen documents: `RESULT.md` = `constructions/receiver_identification/CONSTRUCTION.md` draft 19 (commit `8fb06970`, sha256
  `9f307412224e835f4fccedccdabc408ab0e48c06b74ace9dbc3795a1b7a2c615`); `SOURCE.md` = v16.22 `PROOFS.md` exact bytes (sha256
  `c5a6a1f2…`), inherited source context. Under review: section 25 in full and the draft-19 header item summarising it.
- Preregistration: `FREEZE.md` at `ae03fbee` (sha256 `82731e4a…`), parent `8fb06970`, pushed before any freeze code was written.
  Structural counts from the disclosed counting script `/tmp/rid25/count.py` (sha256 `d1edfe13…`).
- Code: `eb52864a` (`.github/scripts/uqcf_rid19_{producer,checker,compare,review,publication}.py`,
  `.github/workflows/uqcf-gem-rid19-review.yml`). Producer: exact grounded-Laplacian solve, read matrices in vertex coordinates,
  cones re-rooted by relabelling, exact sparse Gauss-Jordan with an augmented constant column. Checker (does not import the
  producer): leaf-attachment enumeration, path-sum field with a neighbour-sum Laplacian check, incident-edge reads, isomorphisms by
  canonical DFS orders, sparse mod-p ranks plus explicit rational solutions checked against every row, and an explicit
  contradictory row for inconsistency. Both programs matched every preregistered value on their first local run; no fix was
  needed before the code commit. The Gemini read timeout was raised from 900 s to 1,500 s, as FREEZE.md section 5 states.
- Actions run [39227983508](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/39227983508) (push, head
  `eb52864a`): verify **success**.
- Actions run [39228005636](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/39228005636) (`workflow_dispatch`
  review=true, head `eb52864a`, the same SHA). Attempt 1: verify GREEN; argument-review failed after about 8 minutes with
  `http.client.RemoteDisconnected` (the server closed the connection with no response; no verdict; transport, not RED). Attempt 2
  (full re-run, same SHA, same frozen bytes, same prompt sha256 `5db0bd87…`, the one re-run FREEZE.md section 5 allows): verify,
  argument-review and publication-audit all **success**. `producer.json` = `producer_repro.json` = local (sha256 `6cc687a5…`),
  `checker.json` `64a00fd0…` = local, `compare.json` `ca6d0fee…`, identical in both attempts. Python 3.12.15, numpy 2.3.5,
  sympy 1.14.0.
  - Certified on every rooted tree up to 7 / 8 vertices (U7 85 carriers, 899 (CN_F) cases; U8 200 carriers, 2,788 cases;
    identity digests equal): (CN_F) holds at every case exactly for the four constant-μ families with θ = −μ, and at no case for
    any other θ; the nonconstant families G5 (T_depth, m ≡ 1) and G6 (alt, m ≡ 1) hold at 163 / 395 cases for θ = −1 and at none
    otherwise (diagnostic, equal in both programs). An arbitrary Genesis datum (526 / 1,446 unknowns) is forced to −Σ x at every
    coefficient except the roots of the 48 / 115 largest carriers, which no cone in a finite universe tests; for G5 the system is
    inconsistent. The composite-table elimination leaves exactly μ constant with θ = −μ. λ ≡ 0 fails at the apex for every
    (carrier, nonroot a). The P1-invariant linear functionals are exactly the multiples of the total. Events: (PN), conservation of
    Σ x, blindness before and the −μ g separation after hold at every case, Genesis included; F̂ = −μ id at every vertex.
    Instances Z1-Z7 matched; controls R1-R8 REJECTED by both programs; 17 of 17 tamper cases DETECTED.
  - Gemini: model requested and returned `gemini-3.1-pro-preview`, finishReason STOP, temperature 0, no prior verdict shown.
    Verdict **ACCEPTED**, 4 of 4 reconstruction items VERIFIED (Proposition 25.1; Theorem 25.2(a)-(d); Corollary 25.3(i)-(iv);
    Proposition 25.4(a)-(c)). Findings, missing assumptions and counterexamples empty. Inserted mechanisms (declared inputs):
    (CN_F) is the CN root shift applied to reads with the grade-level zero extension j_a rather than the balancing h_a and i_a,
    explicitly declared and legitimately used to expose the total; the assumed form "field read plus some linear datum of the
    grade" makes "the Genesis datum is no longer offered" honest within that form; "every carrier is a cone" is used for the
    infinite class and kept separate from the finite evidence. Limitations: the results depend on that assumed form of the Genesis
    read; the Gauss-law reading implies no measurement model or decoherence mechanism. Novelty: the mathematics (the total as the
    unique linear invariant of tree contraction; the discrete Gauss law) is standard; the novelty is the UQCF application.
    native_bridge_status NOT_DERIVED.
  - Hashes: review.txt `35fcc407…`, response.json `ebc0a85b…`, prompt.txt `5db0bd87…`, request.json `d26a2bf0…`,
    model_metadata.json `17d64c78…`. 716 output tokens, 4,618 thinking tokens on an 84,109-token prompt. Raw response kept in
    Actions artifacts only (publishing raw review archives to the repo needs Aaron's explicit OK). Acceptance is evidence of
    independent analytical review of conditional mathematics, not physical validation.
- Readback: the publication audit read back all nine frozen and code files at `eb52864a`, byte-identical, RESULT.md =
  `9f307412…`. Status PASS.
- What this acceptance covers: giving Genesis an arbitrary linear datum of the grade, the read ledger (PN) forces it to be θ times
  the conserved total (the only P1-invariant linear functional), and CN's root shift applied to reads (CN_F), with the grade-level
  zero extension j_a, forces μ constant and θ = −μ, so every receiver, Genesis included, reads its own grade in one unit; on
  nonroot receivers (CN_F) is equivalent to (B), so its new content is the apex square (a discrete Gauss law). What it does not
  cover: a derivation of (CN_F), CN, (L), uniformity, the read ledger, (RS)/(RS_F), condition C, the assumed form of Genesis's read,
  availability (A0)-(A3') and (U), physical access, a physical field law, preparability, or which outcome is actual. Native bridge
  NOT_DERIVED. No milestone.
