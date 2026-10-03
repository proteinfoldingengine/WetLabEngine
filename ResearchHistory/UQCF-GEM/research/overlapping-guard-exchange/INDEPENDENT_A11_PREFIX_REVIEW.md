# Independent analytical review receipt: A11.X1

**Verdict: ACCEPT for the bounded safe-prefix nonextension result. No critical, important, or minor scientific issues found. A11 primary universal schedule existence remains OPEN.**

Reviewer: independent Codex scientific reviewer `/root/a11_prefix_review`, dispatched under `superpowers:requesting-code-review`. Signed 2026-10-03 UTC. This is an analytical review, not implementation certification.

## Immutable provenance

- Repository: `proteinfoldingengine/WetLabEngine`.
- Candidate: `da356a65f1be3443343d0604031a615f343ba52e`.
- Scope parent: `ca6908bd04ef35bf9f297c42c8878f156d7c6263`.
- Prior publication named in scope: `fe3f2db4cce284c2318bf929e9f13d451675fbdf`.
- Reviewed subtree: `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/`.
- Independently fetched `A11_SAFE_PREFIX_NONEXTENSION.md` and `A11_EXTENSION_SCOPE.md` through the GitHub plugin at the immutable candidate. Also fetched the scope at its immutable parent.
- Proof: 12116 UTF-8 bytes; SHA256 `572bb12a70b46ce31a3f9b677ba67b17e5bca85f7cf5a6e899addabcefeb429b`, matching the requested value.
- Scope: 1659 UTF-8 bytes; SHA256 `4b0eb0a9dbf65334a156eeb5041bcbe5977ea94b6248541536792e4201ce0c82`.
- GitHub immutable comparison reports one commit ahead, zero behind, and exactly one changed file: the proof added with 114 additions and no deletions. The scope is unchanged and has the same Git blob `6b57de774d2d455659d3f9e43b4929c61e0d563d` at parent and candidate.

## Scientific checks

1. The carrier counts are correct: 15 roots, two distinct labels per eight-subset, 12870 labels, complementary-block sizes 6864, and support sizes 6006. The eight-subset intersection argument excludes two-label transversals of D. The three displayed codes have empty total intersection, establishing tau(D)=3.
2. For every missing incidence at any root i, the complementary seven-subset plus i is an eight-subset meeting the original code exactly at i. Its distinct palette label produces the asserted pair with precisely one missed root. Every proposed addition destroys that unique protection. Deletions at roots 2 through 14 violate their tight original floors.
3. The singleton source requires both distinct R-coded labels. Any possible third label shares a code index with R outside roots 0 and 1, so a root misses all three. The two codes meeting only at 0 supply the upper four-label witness. Thus tau(A)=4. The 12010 additions are genuine, use the original carrier, respect the destination incidences, and remain componentwise between A and D, proving the stated {3,4} prefix.
4. The normal allocation balances all 15 nonzero F2^4 normals at 858 labels each. Its first-coordinate implications prove K0 is contained in B0 and K1 in B1. The homogeneous-equation argument gives triple coverage for all palette triples, including repeated normals. The displayed four independent normals, with the 1100 label outside both B0 and B1, give a valid four-label transversal. Consequently tau(C)=4 and its floors hold.
5. At D, roots 0 and 1 are completed, while every remaining addition is pair-blocked and every remaining deletion is floor-blocked. Since D and C have different transversal numbers, there are remaining events, and none can legally occur first. In the unrestricted native graph every legal first move must delete a destination incidence at root 0 or 1. This establishes compulsory completed-root revisitation for any native exit leading to C.
6. The alternative schedule is complete and destination-directed. With singleton roots held fixed, the only possible two-label transversal is their forced pair. An unchanged old protecting root protects repair of a distinct new protecting root. The common orthogonal subspace supplies at least three candidate destination protecting roots outside 0 and 1. Keeping one completed protecting root then permits all other nonsingleton repairs by individual additions followed by individual deletions. Their floors hold throughout. Finally, expansion of the singletons occurs entirely inside C and therefore preserves tau at least four. All symmetric-difference incidences toggle exactly once, common incidences stay fixed, and the finite primitive decomposition is explicit.

## Claim boundary and inherited dependency

The candidate disproves EVERY SAFE PREFIX EXTENDS. It does not disprove existence of SOME destination-directed schedule; it explicitly constructs one for these same endpoints. A11 primary remains OPEN. The example is separate from the original uniform-floor-three diagnostic and does not prove general q>=4 primitive or nested connectivity.

The accepted maximum-layer removal theorem is treated strictly as inherited, not recertified. The complete lower paths and forced first-exit statement are established directly; the further native {3,4} conversion is conditional on that accepted theorem and may leave the directed class. No upward-restoration guarantee is asserted for the alternative directed path.

The scope explicitly says the analytical pattern preceded the scope record. The parent-before-proof chronology supports a frozen review scope; it does not establish prospective numerical preregistration. No enumeration, numerical campaign, implementation, tests, workflows, or repository publication was performed in this review. Hashing fetched source bytes was provenance verification only.

Signed: **Independent Codex reviewer `/root/a11_prefix_review`**, 2026-10-03 UTC.
