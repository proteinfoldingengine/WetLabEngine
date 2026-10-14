# Independent analytical review — pinching instrument access boundary

Date: 2026-10-14 UTC.

Reviewer: Codex analytical-review agent `/root/instrument_access_math_review`, independently dispatched by `/root`. This is an agent-authored analytical assessment, not a human peer-review or cryptographic-signature claim.

**Verdict: ACCEPT the exact report and index-append bytes bound below. No blocking flaw or required revision found.** Acceptance is for the conditional mathematics and stated scientific scope. It does not certify a native physical mechanism, occurrence, outcome actuality, receiver access, historical numerical runs, publication, or a numbered research stage.

## Exact reviewed objects

Declared repository: `proteinfoldingengine/WetLabEngine`.

Declared branch: `research/uqcf-overlapping-guard-exchange`.

Source parent: `b498bb1e4e610cfc68c0b630db75498029c002fe`.

Source tree: `fb6a3ed2dc89493327fa1220b37934af1a56f743`.

| Object | SHA-256 of exact local bytes |
|---|---|
| `RESULT.md` | `4e477d218cc217940e9430a645d74ff57ac4ece2ba5c26da31f57036f72cbfe9` |
| `INDEX_APPEND.md` | `b29520172b653935a3389e53008563ca25b2523355bd5bb974ce741d382d35f5` |
| `source_packet.json` | `1c88e2ff0a54d8f25e44984b377ab1fcc103140c7a40f12f9e170286512cf4b1` |
| `source_identities.json` | `72a3c8ff37e59cc4aca6ca103ad90fdfdeb92809f99729ea0f18c1928c96395d` |

All six source contents were decoded as UTF-8 and checked against their manifest byte lengths, SHA-256 digests, and Git blob SHA-1 values, computed with the Git `blob <length>\0` header. All six matched; source paths and immutable-parent URLs agree with the manifest. Both JSON objects declare the same parent and tree. This verifies the supplied packet's internal identities. I did not independently fetch the parent tree from GitHub, so remote placement and publication integrity remain a separate audit.

## Mathematical assessment

1. **The complete finite instrument classification is correct.** For nonzero mutually orthogonal projections resolving identity, the unnormalized Choi matrix of E is VV*, with columns vec(P_i). Their Gram matrix is diagonal with strictly positive entries rank(P_i), so V has full column rank for arbitrary unequal block ranks. From B_r >= 0 and sum B_r = VV*, each B_r annihilates ker(VV*) and is supported on range(V). With L=(V*V)^(-1)V*, LV=I and VL the orthogonal range projection; hence C_r=LB_rL* is positive, B_r=VC_rV*, and sum C_r=I. Multiplication by L and L* also proves uniqueness. This checks the support step, which is essential to excluding branch Kraus operators outside the span of the supplied projections.

2. **Sufficiency is correct with the stated complex coefficient convention.** Factoring C_r as sum c c* yields Kraus operators sum_i c_i P_i and therefore exactly the terms C_ij P_i X P_j. The identity coefficient sum gives E on every matrix. Each branch is trace nonincreasing because the positive branch outputs sum to a trace-preserving output. The report does not assume equal block rank, rank-one sectors, a special basis, or a physical coefficient-space environment.

3. **The label-law classification and exact extrema are correct.** Cyclicity of trace and orthogonality remove every i != j term. The branch effect is sum_i C_ii P_i, so its probabilities depend precisely on a column-stochastic processing T of the sector weights. Conversely diagonal coefficient matrices realize every such finite T. Classical l1 contraction gives the asserted total-variation ceiling. Sector branches attain that ceiling, and alpha_r E attains zero. These are attained extrema over the stated class, not merely bounds. The zero floor remains valid with several nonzero labels and after assuming application of E. Equal sector weights are indistinguishable by the label interface even when within-sector states or intersector coherences differ.

4. **The extra all-input sector-output requirement uniquely forces the stated branches.** A normalized state supported in sector j != i forces C^(i)_jj=0. Positivity then kills its entire j-th row and column. Only the i-th diagonal coefficient remains, and the instrument sum fixes it to one. Linearity extends the resulting branch identity to all matrices. The same reasoning for fine labels assigned to sectors gives scalar classical splitting, whose sector-wise sum is the Lüders branch. Nonzero sectors, exact same-carrier channel equality, complete positivity, and the all-input output-support condition are all load-bearing and explicitly stated. This does not derive a selective record merely from a nonselective action.

5. **The controls are valid.** The roots-of-unity construction supplies n distinct phase-unitary channels for n >= 2, works for unequal sector ranks, and averages to E. Each branch has constant probability 1/n. Its full flagged quantum output is reversibly decodable by the controlled inverse, while the label marginal carries no input information. In contrast, the alpha_r E flagged channel factors through E, so distinctions erased by E remain erased in that enlarged output. The binary plus/minus example and the n=1 identity-channel edge case are correct. No control relies on a numerical sample or on an unrealized alternative being physically selected.

## Source and scientific-scope assessment

- The v15.11 report and implementation support the supplied sharp pinching, explicit positive-weight record selection, projective-versus-random-unitary control, retained-description loss, center-preserving record compatibility, and conditional ordinal history. The new report retains these positive conditional results and does not reinstate the earlier overbroad absence claim.
- The v15.23 source fixes complete sharp branches and classifies CPTP preprocessors that preserve them. Its coefficient matrices have unit diagonal. The new problem fixes E and classifies CP summands, whose positive coefficient matrices sum to identity. The report clearly distinguishes these interfaces; it does not import the former source's already-supplied instrument as a derived record.
- The preceding compatibility-tree result derives V(q) strictly inside V(p) only after a strict compatible q < p is supplied. Its fixed-union requirement concerns retained alternatives in other views. The new report preserves those conditional results and does not assert that either q or cross-view access has been acquired. It also does not promote the fixed-union C3 route to a universal requirement for a valid native interaction.
- The continuation's stated milestone permits probabilistic consequences and nonunique microscopic outcomes. The new report follows that scope: nonuniqueness by itself is not called disqualifying, and direct retained-algebra access and other justified architectures remain eligible. The constant-label instruments establish the absence of a forced informative label from E alone. They do not establish a physical impossibility theorem for every admissible native interface.
- Quantum carriers, CP maps, trace probabilities, exact pinching, application, and outcome accessibility are distinguished. The exact-sector result is not presented as a derivation of the Born rule from bare information, a physical selector, an actual delivered record, or global information destruction. The conclusion that this note does not achieve the native milestone is supported by its explicit unearned premises.
- `INDEX_APPEND.md` accurately condenses the reviewed result and limitations. No contradictory strengthened claim was found there. No force, metric, energy, elapsed-time law, numerical campaign, historical test-count increase, or numbered-stage closure is claimed.

The cited primary mathematical reference was checked at [Watrous, Chapter 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.2.pdf), specifically Proposition 2.20 and Theorem 2.22. Those are appropriate support for the Choi/Kraus correspondence and CP/Choi-positivity equivalence. The zero map is harmless despite the theorem's nonzero-map presentation. The report exposes its actual support argument and makes no mathematical novelty-priority claim.

## Nonblocking continuation caution and review limitations

Excluding globally input-independent T is necessary to exclude that immediate counterexample, but does not alone prove separation for a chosen pair. An input-dependent T may still satisfy T(w(rho)-w(sigma))=0. Any later native candidate must establish the needed pair-specific separation on its justified actual interface; if a uniform positive lower bound is claimed, that stronger bound must also be proved. The present report already asks for the additional derivation, so this is a continuation caution, not a requested correction.

This review is hand-derived analytical checking plus file-identity verification. No source scientific module was imported or executed; no new numerical evidence, formal proof-checking, historical rerun, archive-wide absence result, GitHub publication, or merge is asserted. I did not alter either reviewed document. Future changes to either bound report object require fresh review or an addendum bound to the changed hashes; this original assessment should remain preserved.

Signed in text: `/root/instrument_access_math_review` — Codex analytical-review agent — 2026-10-14 UTC.


## Final-hash acceptance addendum — 2026-10-14 UTC

**Verdict: ACCEPTED.**

I inspected the revised section 6 and checked the exact final bytes. The sole report change is the paragraph explaining that a nonconstant T can still erase the specified source-pair difference. Removing exactly that paragraph restores the original accepted report hash. The clarification is mathematically correct and accurately incorporates the nonblocking continuation caution; it introduces no stronger claim or new premise. The index append is unchanged. No additional scientific execution or broad source review was performed.

| Final reviewed object | SHA-256 |
|---|---|
| `RESULT.md` | `fa665b14f19204a8615a4cd6ddc7655ff91d64687ee339116d5a6cb6293721f7` |
| `INDEX_APPEND.md` | `b29520172b653935a3389e53008563ca25b2523355bd5bb974ce741d382d35f5` |

The original 9,302-byte review is preserved verbatim as this file's prefix, with SHA-256 `517db7b73c5342c0b91d0ae18aaaf7cf5f4d5feee6bb652c3b8f5a1b419f61b2`. Its acceptance scope and limitations remain applicable to these final hashes. No blocking issue or required revision remains; the native milestone is still not achieved.

Signed in text: `/root/instrument_access_math_review` — Codex analytical-review agent — 2026-10-14 UTC.
