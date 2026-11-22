# Where V1698 records source changes and where geometry reads them

This checkpoint follows the surviving-source search from [the pruning-compatibility result](PRUNING_COMPATIBLE_PATCH_REVIEW.md), parent `afb3d35b0220a788d5724450b5ab57b27c199a22`. It traces the historical V1698.75 emitter and validator and checks the original V1698.76 replication output. V1698.77 limits the freeze to the protocol and records non-scaffold emitter equivalence as unresolved. The present source audit is within that boundary.

## Source and scope

- INHERITED as historical software: `V1698_75_full_stack_ledger_emitter_final_aligned.py` and `V1698_75_full_stack_ledger_validator_final_aligned.py`, the complete members in the pinned V1698.75 archive. V1698.76 preserves its per-case scaffold files and a merged ledger labeled `V1698.76_direct_full_stack`. The two sets have separate manifest identities. This audit makes no unstated identification between their producers.
- SUPPLIED in the reconstruction: the grid seed, size, source preparations and direct matrix edit used as rejecting controls. ACCEPTED INPUT: actual atemporal occurrence, unused here. A connection from native pruning to either calculation and a physical receiver's access are open.
- Known before freezing: the source-code dependencies, the archived seed difference, and the reported and stored fields described below were inspected. The matched emitter, genuine source edit, direct matrix edit and independent verifier runs are prospective checks of those findings.

## 1. A numeric source read outside the transport and curvature calculation

In the emitter, `build_nodes` sets `source_value` from index-dependent sine and cosine plus seeded noise (lines 64–85). There is no call from a retained event. For an edge \(p\to q\), `build_edges` computes the actual scalar difference \(d_{pq}=s_q-s_p\) and records it in the edge and witness data. The transport formula uses a different set of arguments:

\[
 T_{pq}=I+0.01 M_{\mathrm{seed}(p,q)}
             +0.001(\Delta\mathrm{support})\,\mathbf1^\top
             +0.001\mathbf1\,(\Delta\mathrm{order})^\top .
\]

This is the implemented elementwise construction at lines 104–128. Changing source values with positions, seed, support and order fixed changes the recorded differences and can change edge identifiers. All numeric transport matrices stay identical. `build_gamma`, `build_R2` and `build_R3` use these matrices (lines 136–222). For unchanged endpoint pairs and cycle sequences, their numeric outputs are therefore invariant for every such source edit. The edge identifiers carry provenance, while matrices and defects use the indicated constants and numeric products.

The original `build_signed_boundary_pairing` does consume source differences. With source variation, it sets \(\delta A_R=0\) and returns \(C_{\rm signed}=-|E|^{-1}\sum_{e\in E}|\mathrm{exposure}_e(s_{q_e}-s_{p_e})|\) for a nonempty edge set (lines 321–351). On a bidirectional \(2\times2\) grid the fixed exposure is \(1/10\). For \(s=(0,1,2,3)\), the four undirected absolute differences sum to 6. For \(s'=(0,3,2,1)\), with the same total grade 6, they sum to 8. The signed values are \(-3/20\) and \(-1/5\). The unsigned diagnostic is source-sensitive under this edit. In the same program, `build_W3` inserts zero current (lines 270–295) and `build_bianchi` copies a curvature field while assigning the Bianchi residual matrix and norm literal zeros (lines 354–380). Even a direct change of an input transport can therefore change the stored F3 matrix while leaving the reported Bianchi norm at zero.

The ordinary `emit` body builds all these objects before `mode` reaches the manifest, null log and thresholds (lines 445–496). At a common seed, `valid` and `source_shuffle` use the same source data. Their displayed curvature rates can still differ by the branch at lines 410–432. This is a statement about the pinned emitter.

## 2. What the original replication ledger certifies

The archived open per-case baseline and source-shuffle manifests use seeds 169876 and 169976, respectively. Those are different draws from the source initializer. Compare the source multisets and reproduce each from its own seed. In the distinct merged V1698.76 ledger, the recorded pair of source values is \((0,1)\) in each mode in both domains. Its single directed edge per case carries source difference 1 and identity transport. The saved W3 source current and Bianchi residual are zero. Namespace-specific signatures differ with the case identity, so numeric equivalence is compared by local endpoint or object role.

Every archived merged R3 row names the vertex sequence \(n_0,n_1,n_0\) while listing only the forward edge \(e_{01}\). The sole edge row has endpoints \(n_0\to n_1\). The second step is missing under the original emitter's ordered directed-edge contract. The R2 rows likewise list that same forward edge for both legs of \(n_0,n_1,n_0\). Under an alternative convention supplying the unrecorded inverse, this out-and-back pair would always have identity holonomy. Either reading provides no nontrivial source-curvature comparison in these rows.

The historical validator checks schema, witness references, and the reported pass against numerical thresholds in `gate_checks.csv` (lines 138–256). It neither walks the directed R2/R3 paths nor reconstructs the three rates from numerical baseline/null comparisons. The original `validate(..., "multi")` call can therefore reproduce the archived pass for these rows. That pass concerns the represented contract and thresholds. It supplies no evidence of a numerical source-to-curvature contrast or of a native event writing the source.

## Frozen check

Pin the three ZIPs by SHA-256. Use the original emitter with the same seed 169876, a \(2\times2\) closed grid and two mode strings. Check exact equality in all twelve numerical and witness tables, and the expected curvature-rate change from 1 to \(1/2\) in the gate output. Separately feed the two explicit source preparations above to the same functions at seed 169876, keeping support/order fixed, and match edges, paths and cycles by their retained endpoints. Compare the complete transition, R2 and R3 matrices, and check the two signed scalar predictions independently. Add \(1/8\) to entry (0,0) of the forward \(0\to1\) transport as a direct control on the existing reader. Assert a change in at least one F3 matrix and equality of the reported Bianchi norms.

Read the original V1698.76 merged CSVs exhaustively for the twelve manifest cases. Compare the node values and edge data at matching suffix roles, verify the opened per-case seed pairs and source multisets, walk each R2 and R3 record according to its ordered directed edge IDs, and replay the preserved validator on the unchanged merged inputs. The result must retain both the historical validator's acceptance and any failures of the independent scientific comparison. No physical preparation or unarchived emitter is inferred.
