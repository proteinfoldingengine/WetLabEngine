# C3 perfect-matching escape obstruction evidence index

Campaign event commit: `857803fb97e80a9d7b4f9338ebf9ef2de4d5f8e1`  
Successful Actions run: `38167992780`  
Canonical stream: `b6b53398b5ec82f9552284b93cdb2e10ef357bc277e27054eda3aee41af77610`

Original artifacts:

- `verification.zip.part-000` and `verification.zip.part-001` — byte-exact split of artifact `11713195272`; concatenate in lexical order to reconstruct the original ZIP (SHA-256 `2f4c17e9dd94046e0e8a540e533c1578ac08d45d5040aeadb514b80c93be2c71`), including the complete 32,576,926-byte canonical JSONL stream, producer/checker, tests, certificate, and SHA256SUMS;
- `mathematical-review.zip` — artifact `11712918971`, Gemini 3.1 Pro ACCEPTED;
- `publication-audit.zip` — artifact `11713200934`, separate ACCEPTED audit.

Preserved full job logs:

- `logs/run-38167334252-job-114552511434-red.log` — intentional missing-checker RED;
- `logs/run-38167717768-job-114553649731-workflow-failure.log` — inherited test filename failure;
- `logs/run-38167992780-job-114554457103-verification.log`;
- `logs/run-38167992780-job-114555337876-reproduction.log`;
- `logs/run-38167992780-job-114555669811-mathematical-review.log`;
- `logs/run-38167992780-job-114556303328-publication-audit.log`.

`MANIFEST.json` records artifact hashes and committed Git blob identities. The original ZIP bytes are retained without repacking; the verification ZIP is split only to fit the repository write transport.
