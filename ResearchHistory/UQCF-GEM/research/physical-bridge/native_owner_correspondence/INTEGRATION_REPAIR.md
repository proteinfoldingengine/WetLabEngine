# Integration audit repair after failed run 41572489600

Date: 2026-11-02, America/Phoenix. No scientific inputs, output values or original review are changed.

The first integration run at 2b7a9f7e39cf16ed8a9d87870f553a00789c91a1 failed after all 39 inherited tests, producer, independent verifier and nine owner controls passed. Six deterministic output files had already matched the original archive. Its strict comparison of REPRODUCED_1615F.json failed. The original gate.py writes git HEAD into execution_head; the old file contains c721762f4890a81036fb2bff11d394881384496f, while an integration run must contain its current checkout SHA. Whole-file equality across these commits was an invalid integration expectation. The original same-commit publication replay remains valid.

The revised prospective comparison requires six exact byte matches and equality of every parsed historical scientific field after separately checking both execution_head values against their exact expected commits. It preserves the new raw historical file rather than rewriting its provenance. A local reproduction using the archived fixture demonstrated the byte mismatch from the changed identity; three tests now accept only changed legitimate provenance and reject changed scientific records or a forged execution identity. The original byte comparison and failed run are preserved.

The artifact uploader also warned that verification.json and VERIFICATION.json collide case-insensitively. Download inspection found all 43 manifest members present with correct lengths and hashes despite that warning. Subsequent integration outputs place inherited evidence in an inherited/ subdirectory and reject any case-folded path collision before upload.

Failed original ZIP: evidence/integration-failed-41572489600/owner-integration-1.zip; 325740 bytes; SHA256 61190ede8d51894126302d4b11f579431b0d703b39f08ff48419eaf417dda86d. Artifact ID 13202346371. Full job 125708381254 log is preserved beside it. No failure is erased or relabelled success. The next dispatch is a logged integration-utility repair, as permitted by INTEGRATION_PLAN.md; it does not change the scientific domain or invoke Gemini.
