# PROSPECTIVE_REMEDIATION_PLAN_T289 — PR #130 (E-α bounded test): GitHub producer/checker and resource contract

- **Author:** proteinfolding-grokbot (Grok, UQCF Science Agent). **Date:** 2026-11-02, America/Phoenix (run 8:13 PM MST).
- **Remediation step:** T-284 item 2 (freeze a prospective GitHub producer/checker and resource contract disclosing all known local outcomes). Step 1 was `CORRECTIONS_T275.md` (commit c627631a).
- **Committed before:** any new code for this plan is written, any workflow file for it exists, or any GitHub execution of this package. Nothing in this file has been run.
- **Parent heads verified this run:** package branch `grok/ealpha-premise-test` c627631aee42e2eba73c8a741a8ebea373c0a4d0; research `1fed0b997ce2dde2596c376138386987b9bff4b3`; agent-thread `9922b13b43e8cbe808ad50836a0a47540a00058f`; AGENTS.md blob `e5407215a81b914fc02f5c107333a2f0261634ee`.
- **Status:** no scientific status change. Sharp E-α stays NEW ASSUMPTION; the benchmark stays ACCEPTED-CONDITIONAL/SUPPLIED; native receiver delivery NOT_DERIVED. A green workflow will not upgrade anything.

## 1. Frozen inputs (blob / sha256 at c627631a)

| file | git blob | sha256 |
|---|---|---|
| PREREGISTRATION.md | cd005b2f | d0127d64d23f58c0e817d6a7c267a25f7cb797d3403f5c374fd253c4246f2997 |
| RESULT.md | 3745831a | 2de0aa99b58e1d39f84f44dedbe248ed969186c452264a14559d4d124448997c |
| CORRECTIONS_T275.md | 22f383e2 | e25dce41093247015ff7652f2b5ddb8fd192ecea89755c7c3206202fdc723c07 |
| t269_ealpha.py (producer, sympy/mpmath) | eb87879e | cfd294437424781f5a31d1476376922c01b05db98debc5c23dc22760f1021c5d |
| t269_verify_np.py (checker, numpy) | f74b695c | 57cf92007f9e7465c566e3c9d565fc1994f3630a8f693b90350f7ecaaf7837bc |

The two scripts are run unchanged. No original file, failed run or raw review is edited.

## 2. Disclosed known local outcomes (not preregistered predictions)

All were obtained on the shared box (python 3.13.5, sympy 1.14.0, mpmath 1.3.0, numpy 2.5.4, seed 269) and are already published in `evidence/local-run-1/`:
- `run1_stdout.json` sha256 152715e0bbd1e761d4ee3e821969ec69ad552263c1608c48ba7dbea5966bd967 (producer).
- `verify3_stdout.json` sha256 4bb87bac67c1d355d5bb7cdcb4591e0e0110154905beb600cf068a14cde8bb06 (checker, third attempt).
- FAILED checker attempts, preserved: verify1 (checker bug; script sha256 2a731233…), verify2 (wrong reference channel on carrier B; script sha256 13a03fa2…). These are checker errors, not scientific failures, and they stay on record.
- Reported verdicts: admission controls as preregistered; P-a headline carrier A "PASS, non-discriminating", carrier B PASS (X3 non-trivial); X2 FAIL (ill-posed) from Choi rank 3 (A), 4 (B); P-b DOWNGRADED to consistency check; P-c regression R(π_p)=R(π_v) under W_R.
- Corrected analytic claims C1, C2 (CORRECTIONS_T275) were checked only by the local scratch script `/workspace/uqcf_scratch/t275/t275_check.py` (sha256 c849c2c4…). That is REVIEWED-NOWHERE local evidence; it is not part of this contract's evidence.

Because every outcome above is already known, the GitHub run of §3 J1 is a **reproduction**, not a test, and is reported as such.

## 3. Jobs (one workflow, `workflow_dispatch` only, on the package branch)

**J0 — inherited foundational stack** (pins exactly as `uqcf-foundational-closure-verification.yml` at research 1fed0b99: actions/checkout@11d5960a…, actions/setup-python@a26af69b…, python 3.11, sympy==1.13.3, mpmath==1.3.0): `foundational-closure-verification/tests/test_fcv.py`; `demos/v15.56-response-selector-obstruction` unittest `test_pruning_consistency_audit`; `demos/v16.15F-graded-obstruction-descent` unittest + `gate.py`. PASS iff every exit status is 0. This is the inherited tree / P1 contraction / zero-extension stack; it does not test the SUPPLIED benchmark.

**J1 — original package reproduction** (same action SHAs, python 3.13, sympy==1.14.0, mpmath==1.3.0, numpy==2.5.4): run `t269_ealpha.py` → `producer.json`; run `t269_verify_np.py` against it → `checker.json`. Frozen criteria: (a) both exit 0; (b) every boolean verdict and every exact (string/rational) field of `producer.json` equals `run1_stdout.json`; the `python` field may differ and is excluded and reported; floating fields must agree to 1e-12 absolute; (c) every verdict field of `checker.json` equals `verify3_stdout.json` under the same rule. Byte equality is additionally reported but is not required (version string field).

**J2 — corrected-claim producer and independent checker (new code, written after this commit, hashes posted before dispatch).**
- Producer `t289_c1c2.py` (sympy, exact): C1(i) Choi rank of C_1C_2 equals 3 on carrier A and 4 on carrier B, computed as the rank of the Gram matrix of a Kraus family; C1(ii) the qutrit witness U_i = swap(|u_i,0⟩, |p_i,i⟩) gives commuting U_1, U_2 and ⟨k|U_1U_2|0⟩ = {Q_1Q_2, |p_1⟩⟨u_1|, |p_2⟩⟨u_2|} with Σ K_k ρ K_k† = C_1C_2(ρ) on every matrix unit of carrier A, E untouched; C1(iii) N disjoint one-hot erasures have Choi rank N+1 for N = 1, 2, 3; C1(iv) the E-writing mirror of (ii) gives the same rank and composite channel (W_R/W_E-neutral). C2(i) symbolic identity P(A∧B) − P(A)P(B) = z_u(z_o+z_v) with A = 1_{u}, B = 1_{p,u}; C2(ii) slack h(z_u) − (z_p+z_u)h(z_u/(z_p+z_u)) equals I(A;B) exactly on the simplex; C2(iii) slack = 0 at (0,½,½,0) and = 1 bit at (0,0,½,½).
- Checker `t289_c1c2_np.py` (numpy only, algorithmically independent): builds the Choi matrix of C_1C_2 directly from the channel definition on matrix units (no Kraus family) and takes numerical rank by SVD with tolerance 1e-10; builds the witness unitaries as permutation matrices and compares channels on all matrix units; evaluates C2 on a fixed grid of 1771 rational simplex points (denominator 20) plus the two named points.
- Agreement criterion: every C1/C2 verdict in producer and checker is identical and TRUE.

**J3 — rejecting controls (each must be REJECTED; a control that is accepted fails the job and is preserved, not rerun).**
- R1 corrupted output: flip one boolean verdict in a copy of `producer.json` (J1) and of the J2 producer output; the respective checker comparison must fail.
- R2 substituted record: replace carrier-A `choi_rank_C1C2` 3 by 2 in a copy; must fail.
- R3 withdrawn claim: the old disjunct "equality iff z_o+z_v=0 or z_p z_u=0" evaluated on (0,0,½,½) must be refuted (predicts equality; slack is 1 bit).
- R4 qubit receiver: any R of dimension 2 must fail to realize C_1C_2 on carrier A (rank 3 > 2), checked as "rank > dim R".
- R5 wrong witness: U_2 = swap(|u_2,0⟩,|p_2,1⟩) (same slot as event 1) must fail the channel equality on a u_1–u_2 coherent input.
- R6 missing record: a copy of the J2 output with the C1(iii) N=3 entry deleted must fail the checker's coverage check.

**J4 — publication and immutable readback (separate job, needs J0–J3).** Re-run J1 and J2 producers fresh; require byte equality of the deterministic outputs with the J1/J2 artifacts; write SHA256SUMS of every artifact, logs, `pip freeze`, workflow SHA and checked-out SHA; commit them under `evidence/github-remediation-<run_id>/` on the package branch; then fetch the pushed commit by SHA from the remote and require every listed file's sha256 to match. Downloaded artifact digests are compared with the uploaded digests.

## 4. Resource and stopping rules

ubuntu-latest, timeout 20 min per job. One dispatch. One rerun is allowed only for an infrastructure failure (runner, network, package download) shown in the log; a scientific or control failure is never rerun and is preserved as RED evidence. If J1 does not reproduce, the package verdict is "LOCAL RESULT NOT REPRODUCED" and is reported as such. No change to criteria after results are seen.

## 5. Review scope (T-284 item 5)

After J0–J4, one fresh independent whole-argument review (gemini-3.1-pro-preview via Actions) restricted to the corrected substantive claims C1 and C2 and their place in the amended argument, given the frozen PREREGISTRATION, RESULT, CORRECTIONS_T275 and this plan, without any prior verdict. PR #132 is not used to certify them; Gemini run 41512469271 is not rebound. The package stays open and unmerged; no merge without an accepted fresh review.

## 6. Directive categories

- Native premises: tree, P1 contraction P, zero extension I, owner/address data (INHERITED; J0).
- New derived consequence: none; this is a verification contract.
- Still supplied: benchmark channel C, K = E⊗R, receiver algebra, dimensions, carriers; sharp E-α is NEW ASSUMPTION.
- Constrains receiver delivery: no; C1 and C2 are E↔R symmetric (C1(iv) checks this).
- Accessible observable distinction: none.
- Physical vs mathematical: supporting mathematics and its publication hygiene. Class C. Native bridge NOT_DERIVED.

PR #131 gets its own plan of the same shape in a later run.
