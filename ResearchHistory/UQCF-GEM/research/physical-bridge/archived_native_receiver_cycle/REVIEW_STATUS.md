# Independent review status — source-cleared ternary receiver

- Scientific input commit: `f9622b8671d42001dc0379daf761facb5388c497`.
- First frozen review infrastructure: `8e96078ab534f3ac232182d12c894f2282c1674c`.
- Actions run: [46105178620](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/46105178620).
- Replay result: original v16.51 certificate and source-cleared controls reproduced exactly at `PYTHONHASHSEED=91` and `17`.
- Review result: no verdict. Gemini returned HTTP 429 before a response was written; the audit step was skipped.
- Preserved artifact: `15247291775`, ZIP digest `sha256:e9522e2a3cc91b522a0d619456074abb27544c2f85001627ce606786b72d5698`.
- The artifact contains the deterministic replay, exact review request and prompt, but no `review.txt`. This attempt is neither acceptance nor rejection and must not be rerun.
- One fresh Actions attempt may use the same scientific files and review question. Any result requires its own audit and immutable publication readback.

## Fresh attempt

- Fresh Actions run: [46105288688](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/46105288688), infrastructure commit `3b95470f33b6ff0a852b23bbc317a0ad01aed41b`.
- Replay again passed at both fixed hash seeds.
- Gemini again returned HTTP 429 before producing any verdict; audit was skipped.
- Preserved artifact: `15246759864`, ZIP digest `sha256:0869d4f40a2eed686511d33735af854cafc33cdd17ec0da50e9ff3d03e6b3b06`.
- This second attempt is also neither acceptance nor rejection. No further review attempt should be launched until the external quota condition changes; scientific input remains frozen.
