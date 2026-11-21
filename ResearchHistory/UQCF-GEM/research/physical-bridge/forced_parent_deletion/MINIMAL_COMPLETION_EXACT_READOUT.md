# Fractional-source readout and minimum-claim verification

This amendment answers [PR153 comment 7067552656](https://github.com/proteinfoldingengine/WetLabEngine/pull/153#issuecomment-7067552656). The accepted counting argument and its original Gemini receipt concern the frozen scientific packet at `0b9866f5d826c1e9c6560b2d0836cbeae5401a9b`. Two implementation defects in that packet affect verification.

The frozen helper calls `int` on the exact root grade. With all source coordinates equal to one except `g8 = 1/2`, the frozen helper gives high and low roots of 1 and 1. Native P1 and an independent ancestral sum give 3/2 and 1. The corrected readout retains the exact value throughout. JSON encodes nonintegral rationals as reduced fraction strings and integral rationals as integers. The round trip recovers each exact rational.

The frozen integrity tests also omitted two rejection scenarios listed in the original protocol. The supplementary checker independently constructs the profile domains and computes minimum incidence before checking endpoint claims. For the valid low state `[1,3,455,63]`, the test supplies its correct root and falsely claims minimum status. Its incidence of 15 fails the minimum of 14. For the genuine low minimum `[1,455,1,63]`, the test supplies a false positive1 root of 2. P1 returns 1 and the validator rejects the record. A third test passes the frozen helper's truncated fractional root to the same validator and confirms rejection. A correct claim runs through the same validator.

Run the two commands from this directory in a checkout that includes the original repository sources and their Python dependencies.

~~~sh
python check_minimal_completion.py > /tmp/minimum_integer_replay.json
python check_minimal_completion_exact.py > /tmp/minimum_exact_readout.json
~~~

The independent local run of the frozen checker regenerated its 525,209-byte output byte for byte, SHA-256 `99145e89948a91a3d92bbc8c0b3f41170f4d7ecf41eed9bf75ae15ee6b928998`. The supplementary checker recomputed all 175 serialized minimum and path root values in the archived integer test cases (85 high, 90 low). All matched. Positive fractional, signed rational and zero-source-amplitude cases also passed at every minimum, including lossless serialization. The [output](evidence/minimal_completion/exact_readout.json) records each result.

Use [check_minimal_completion_exact.py](check_minimal_completion_exact.py) for exact rational claims. [check_minimal_completion.py](check_minimal_completion.py) reproduces the historical integer archive including its original truncating helper. This supplement provides a local execution and inherited-component verification. The (g_8) contrast still depends on the stated completion and grade conditions. Native selection and physical receiver access remain open.
