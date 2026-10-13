# Concurrent publication-audit preservation

Date: 2026-10-13 UTC.

Both audit records concern the same analytical publication `5379f09f94cd176912a806685619ebab593c758a`, tree `8837cb4e41884528538a8abc02a83393a94d8d33`, with source parent `c96ff8b9ae0d3b3c07d4e56b51c28e4f256f3f5a`. The accepted manuscript and index addition are unchanged.

While this session prepared its audit-preservation bundle, a guarded branch check found that `019e40683cf58f7eccab7270b49e0e6ddea2a87a` had already added a publication audit, evidence, receipt and manifest. That commit has sole parent `5379f09f94cd176912a806685619ebab593c758a` and tree `c7336d5d2fb4afdd53f3e866e21f17cfed231260`. The guarded check stopped this session's planned write before tree/commit/ref mutation. The publication actor is not inferred from the shared GitHub identity or commit message.

The author independently fetched the four existing files at that immutable commit. Each UTF-8 byte string reproduced its returned Git blob ID. The existing manifest's three payload lengths, SHA256 digests and Git blob IDs matched exactly. Its evidence records PASS_PUBLICATION_ONLY, the exact seven analytical paths, eleven source matches, exact parent-plus-append and no discrepancies. The report preserves the same conditional scope and adverse controls.

| Existing file at 019e406 | SHA256 |
| --- | --- |
| `PUBLICATION_AUDIT.md` | `e0c8b16f5bf3acdd4cdcaf20cf219a8472f9cdc205f90dc2717cd0b5acaea2fa` |
| `publication_audit_evidence.json` | `f11d8c33ede43c383b5d1e87a324c5e807eb733c685dc5771ab1f1524a316539` |
| `PUBLICATION_RECEIPT.md` | `2825be90b64fe35c262f6578e1ea5376e66cdf51e81c1839f5ff52118af74320` |
| `RECEIPT_MANIFEST.json` | `a2ba13d31143835d2c997b4a4509872f1c7747cdddfe475ecb548bf049e195f1` |

This session had separately requested and received a fresh independent publication audit. Its raw report SHA256 is `3f1490e4fd83c00fb81256c6a6f871f21178a0465fb3e159ddc5c5c265439921`; its compact evidence SHA256 is `6f6d6c47f7cc509fe645ea4e72ccfc1bd0c785e20f24440d998ee1de61d2fd3e`. That audit also returns PASS_PUBLICATION_ONLY after seven immutable publication-file and eleven parent-source readbacks. Both raw artifacts are preserved verbatim in `additional_publication_audit/`, together with this session's author readback and receipt. The earlier four files are not replaced or relabelled as this session's review.

The extra preservation adds no scientific claim, numerical evidence, test count or physical milestone. It does not require another round of mathematical review: the reviewed mathematical bytes are identical, and no new theorem is introduced. A terminal author readback checks the exact newly added paths and parent/tree after publication. Native action/access and the milestone remain OPEN / NOT ACHIEVED.
