# Four-child fork publication audit — run 45731071551

The separate publication workflow at commit `163d8c53445a52b1096411ea2e738132224f01b0` completed successfully in [run 45731071551](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45731071551).

## Scope

- Scientific argument: `1de3107f13acdc4e07f5e8e59fa15575948bded8`.
- Historical implementation: `e61d5b0e827f7b412824ad46021e2ad6cc6f7875`.
- Independent whole-argument review: run `45729381481`, verdict **ACCEPTED**, native bridge **OPEN**.
- Foundational regression: passed at job `139612908761`.
- Separate publication audit and fresh byte reproduction: passed at job `139613327495`.
- The earlier publication attempt `45730739531` is preserved. It correctly rejected applying a review receipt pinned to the scientific commit against a later workflow-only checkout; the successful audit instead verifies both archived review receipts at their own pinned heads before reproducing the scientific bytes.

## Durable artifacts

- `foundation.zip`: artifact `15076284394`, SHA-256 `2c94dd5ba8206b396100387562b3662f0cf2bad6bfa33218006ed08d4514d13b`.
- `publication.zip`: artifact `15076098557`, SHA-256 `9bf4dfbf6651f7765aee42785727bb35ba3a929cec7c07775d85334bb7940961`.

The publication archive contains both preserved review ZIPs, their manifest and readback verifier, the fresh exact replay, the full positive-row record, the foundational checksum receipt and an internal `SHA256SUMS` file. The native handoff remains underived: the source atom and the normalization producer calculate the same cover number independently, but no inherited source-to-producer call or continuation-phase carrier has been identified.
