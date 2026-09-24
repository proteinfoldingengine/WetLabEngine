# v15.46 Stage-B native-record trace receipt

Stage B traced the strongest scoped existing joint-state candidate and stopped at the first unearned native interface.

- Candidate: `V13_27_SIX_QUBIT_THERMAL_DEMO`.
- Pinned source: `ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/uqcf_demo/quantum.py`, blob `bf0b84e3b3e627d7916a5fb1b46ab9bd5eba03e6`.
- RED run `35946636904`, job `107465933763`: failed exactly with `ModuleNotFoundError: native_record_trace`.
- Focused GREEN run `35946702506`: Stage-B trace tests passed.
- Complete run `35946791128`, job `107466426676`: SUCCESS on exact head `1211968aa97fd9b52476dfebbae419fb74df8ff4`.
- CPython 3.13.5; 35/35 current v15.46 tests passed in 1.090 seconds, with no skipped or expected-failure tests accepted.
- Stage-B result replay, the original 195-check proof output, and the original typing-probe result all replayed byte-for-byte.
- Compilation, clean-tree check, v15.44/v15.45 snapshot hashes and exact checkout identity passed.
- Runner receipt: `V1546_STAGE_B_VERIFIED_HEAD 1211968aa97fd9b52476dfebbae419fb74df8ff4`.

## Scientific result

The source file constructs a six-qubit thermal joint state using normalized `exp(-beta H)` and includes a graph, source operator and source-node labels. It is therefore a stronger concrete joint-state object than the selected compatibility completion for this particular trace.

However, the file is a supplied frozen demo model. It does not derive that joint state from primitive retained records. The Stage-B machine verdict is therefore:

`SUPPLIED_JOINT_STATE_PRESENT_NATIVE_PROVENANCE_UNESTABLISHED`

First unmet interface:

`B1_NATIVE_JOINT_STATE_PROVENANCE`

The trace deliberately stops there. It does not select subsystem overlaps, support treatment, an oriented incidence occurrence or a coupling law after the provenance failure. Doing so would convert missing information into authored physics.

This does not prove that no native source record exists elsewhere in the archive. It establishes only that this strongest scoped candidate does not earn native provenance from its frozen source artifact.

`source_correspondence=NOT_EVALUATED`; no physical source law or gravity claim is adopted; **Pillar 3 remains OPEN**.

This receipt is a documentation-only commit after the executed head above and is not represented as another tested scientific head.
