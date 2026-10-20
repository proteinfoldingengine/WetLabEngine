# Original review evidence and publication verification

This directory preserves the complete original evidence for the independently accepted [one-event receiver-gain result](../ACCEPTANCE.md). The native bridge remains NOT_DERIVED.

## Immutable identities

- Scientific freeze: 86ea348c5886005431413eefd2207a293438f8fc.
- Review/workflow checkout: af114e24727f82c6e632ffce74452e9c62c323d3.
- [Actions run 39429834992, attempt 1](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/39429834992).
- Source parent: aa5aa96c002c181fb2e833f12fcabb15d94c5d6f.
- Prompt SHA-256: 55ee81516115cec5161584f339c7d8d4f32cbf3e6a9fe9fdc8dd42ff62188e93.
- Raw response SHA-256: 5612d94f931e88fecbf0a800382c22dadb48b2fedf915a9574165f3c2f63613a.

## Original archives

| Artifact | ID | Bytes | Original SHA-256 |
| --- | ---: | ---: | --- |
| single-event-gain-integrity-1 | 12267302142 | 1823 | f5ef4f01b8b978c88166d45d6d34f7e24292472bd4aa4cc92518115b19140e10 |
| single-event-gain-review-1 | 12267004861 | 143847 | daa6a669c5740998d150e3614ec33001370951a84ff18738544fde29cc45cb9d |
| single-event-gain-publication-1 | 12268250079 | 1972 | 3dd96f9436d5e98a9480ba0e0477c866f102e694691c6b213766b35ac03bbf03 |

The three ZIPs in [archives](archives) are the original Actions artifact bytes, with no recompression. All thirteen members are preserved in [artifacts](artifacts), including each original artifact_manifest.json. Their bytes are identical to the corresponding ZIP members. Original raw response fields, including opaque provider fields, have not been removed.

## Inspection entry points

- [Full reviewer answer](artifacts/single-event-gain-review-1/review.txt) and [parsed verdict](artifacts/single-event-gain-review-1/verdict.json).
- [Original raw response](artifacts/single-event-gain-review-1/response.json), [exact request](artifacts/single-event-gain-review-1/request.json), and [exact prompt](artifacts/single-event-gain-review-1/prompt.txt).
- [Model availability metadata](artifacts/single-event-gain-review-1/model_metadata.json) and [review identity](artifacts/single-event-gain-review-1/review_identity.json).
- [Original integrity result](artifacts/single-event-gain-integrity-1/integrity.json).
- [Separate publication audit](artifacts/single-event-gain-publication-1/publication.json).
- [Full job logs](logs) and [workflow/artifact metadata](metadata).
- [Local archive and member verification](ARCHIVE_VERIFICATION.json).
- [Public-file manifest](MANIFEST.json).
- [Immutable publication readback](READBACK.json).

The manifest covers this publication's evidence files except itself and the later readback receipt, avoiding circular hashes. The readback receipt binds the evidence publication commit and checks every published evidence file, the frozen scientific bytes, and the appended continuation. It is added in a separate commit after those checks.

Scientific acceptance comes from the external Gemini review of the frozen argument. Integrity and publication checks establish provenance and consistency; they do not turn a conditional theorem into a native physical record. The independent review explicitly returns NOT_DERIVED. The complete scientific boundary and next native obligation are in ACCEPTANCE.md and RESULT.md.
