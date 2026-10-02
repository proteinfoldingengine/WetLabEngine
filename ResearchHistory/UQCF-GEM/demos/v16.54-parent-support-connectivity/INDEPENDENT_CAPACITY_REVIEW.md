# Independent review — exact-endpoint capacity extension

Reviewer: /root/v1654_capacity_review. Read-only, manual analytical review; no scientific execution or file/Git mutation.

Artifact: EXACT_ENDPOINT_CAPACITY.md at b1ebe5df4f534c8813797d5a3b2ccc430e757126.
Verified SHA256: 37556dd879d80b1301395fbc89b8ec1ee442a0497459c659accbf776fa604ff8.
The reviewer read the exact local artifact and GENERAL_PARENT_CONNECTIVITY.md. The executor verified exact remote file readback at that commit.

Verdict: ACCEPT the scoped analytical claims. No Critical, Important, or Minor findings. This is not implementation certification or merge approval.

## Review findings

- G/G1: The hitting-set completion argument establishes local redundancy; incidence double counting gives the localized capacity inequalities, including the empty-set case.
- G2: Untouched blocks retain every required lower-level cover. When both tuples are exact-q, expansion and contraction supply the upper bound independently. The warning against unrestricted iteration is necessary and correctly stated.
- H: Saturation forces every row to its floor and every label to degree d. The pair-union bound and common-core-or-small-union classification are valid, including repeated supports and d=1. Nonempty roots and q>=3 exclude the small-union alternative. The floor vector uniquely identifies the full-palette roots.
- I: Each swap respects floors and changes one incidence per move. The unaffected partition parts force q-2 separate hitting labels, and the affected pair requires one or two more. The correctly placed label count strictly increases, proving termination.
- Positive slack: Compaction preserves exact-q; the defect identity and bound follow. The restricted classification of degree-d supports is sound. The document correctly avoids promoting these endpoint facts to path invariants or a general exchange theorem.
- Native scope: The new result supplies the abstract root path required by the preceding document's conditional lifting statement. It does not establish a necessary native obstruction or remove the child-interface assumptions.

## Declined to judge and executor dispositions

1. Full native lifting/interface validity: the underlying six-clause interface and v16.53 replacement argument were not independently re-established in this review. Ruling: retain those as the previously accepted conditional hypotheses; no new recertification claim. Risk: improperly importing an interface outside its proved domain.
2. General positive-slack connectivity: explicitly remains unproved; the supplied arguments do not settle it. Ruling: remain OPEN; the defect count is an endpoint identity, not an exchange algorithm. Risk: confusing total or localized redundancy with a path-preserved buffer.
3. Implementation correctness, computational certification, PR state and merge readiness: outside this analytical review and unsupported by implementation execution or repository-state verification. Ruling: no implementation or certification claim; keep PR draft and verify publication separately through GitHub readback. Risk: falsely declaring scientific closure from proof review alone.
