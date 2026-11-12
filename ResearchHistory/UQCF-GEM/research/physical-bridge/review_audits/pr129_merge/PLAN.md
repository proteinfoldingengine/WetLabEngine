# PR129 actual-merge integration audit

Frozen before this Actions execution. This is an integration audit, not a new
scientific domain or a replacement for the preserved preregistrations.

Scientific checkout: `084617b4c392b8955f0a19d2c2b2c02dfa8d9d91`.
Parents: research `1f1394d1a8708464bab064c787d396a28d0c5a86` and reviewed
PR head `324183d11baec30926e8e995ce033d0c07ea06af`.
Record the separate workflow/controller SHA in every receipt.

1. Require precisely the 67 merged paths, with exact PR-head blobs; audit all
   61 document records from the three preserved reviews against merged bytes
   and their original prompts. Check all review artifact manifests and preserved
   T249 review/failure ZIPs. The latest independent Gemini review must retain its
   clean acceptance gate and NOT_DERIVED status. Earlier results are preserved,
   including T246's seven findings and the pre-model infrastructure failure.
2. Python 3.11, Sympy 1.13.3, mpmath 1.3.0. Run all 22 FCV tests, 15 inherited
   pruning tests, historical selected-chain tests/reproduction, full FCV producer,
   independent verifier and rejecting controls. Check original publication
   checksums before mutation. Require the frozen decompressed certificate hash.
3. Rerun both original and successor producers, independent stdlib checkers and
   all their rejecting controls, byte-comparing each output with the published
   scientific evidence. The original corrected/withdrawn theorem text is not
   rehabilitated by replaying its computations; T241/T242/T249 govern scope.
4. A separate publication job starts from the same actual merge and repeats the
   entire deterministic stack. Require scientific bytes to match the first job.
   Upload sources, complete outputs, commands/logs, environment and checksums,
   including failure evidence on any failure. Download and verify API artifact
   digests, then commit durable evidence and perform exact publication readback.

Stopping rule: any mismatch or nonzero command fails the audit. Preserve it;
diagnose infrastructure separately from scientific failure. No repeated model
request, new parameter sweep, source edit, physical claim, or default merge.

INHERITED: repository AGENTS.md closure requirements and existing frozen tests.
DERIVED: only the integration/byte-identity verdict if all checks pass.
SUPPLIED: unchanged quantum benchmark, receiver interface and access premises.
NEW ASSUMPTION: none. Native receiver-delivery bridge remains NOT_DERIVED.
