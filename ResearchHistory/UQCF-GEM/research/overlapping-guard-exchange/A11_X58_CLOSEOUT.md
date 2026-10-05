# A11.X58 closeout: prescribed anchor-preserving exchange with coupled pair renewal

Date: 2026-10-05 UTC.

Status: **ACCEPTED analytical checkpoint after fresh independent whole-argument review.**

Repository: `proteinfoldingengine/WetLabEngine`.

Exact frozen scope commit: `dacc35eee084e4f9902609b577f55626d72a1f28`.

Exact reviewed candidate commit: `8512e70c3d208ee0209f412bf49b4ce1f9ab7072`.

Exact reviewed candidate tree: `f8a0a349785f789ea6f95aaa860de600d8980207`.

Scope blob: `d1373f84c9b129b7b3af9f075b015d4c7e8a2c82`.

Proof blob: `6d89f587c6a68379e7fba0589707c4e239810580`.

Review: `INDEPENDENT_A11_X58_WHOLE_REVIEW.md`.

## Exact new statement

Let the four anchor roles be `A={0,1,2,3}`. For every anchor `a`, let the actual labelled root types be `{a} union e` for outside pairs `e in Gamma_a`, with arbitrary positive original labelled copy multiplicities and arbitrary same original positive floors not exceeding the endpoint support sizes. Assume the colored guard

`vc(union_{a in J} Gamma_a) > |J|`

for every nonempty `J subseteq A`. Fix in advance a prescribed permutation `pi` of all roles with `pi(A)=A`. After this declaration there is no relabeling of anchors, outside roles, roots, or endpoints.

For any finite number `t` of parallel owner columns, the exact-four endpoints obtained by moving every column owner `s` to `pi(s)`, with all padding fixed, are connected directly by legal single-incidence edits with `3 <= tau <= 4`. Every original labelled support is restored at the destination. The construction is renewable column by column and attains the global endpoint Hamming minimum

`L = t sum_Q c_Q |Q symmetric-difference pi^{-1}(Q)|`.

## Assumption removed

X57 derived a compatible exchange only after choosing the anchor/outside labeling before the endpoint successor was fixed, and it handled one noncommon pair obligation per column. X58 removes that compatible-exchange choice for every prescribed anchor-preserving `pi`. It simultaneously transfers all exceptional pair obligations

`E_pi={S subseteq A: |S|=2 and pi(S)=A minus S}`,

whose cardinality can range from zero through four.

## What enforces safety

Every nonexceptional physical pair has an actual common endpoint-union witness from the colored guard. For each exceptional `S`, old witness colors are `A minus S` and new witness colors are `S`.

The singleton colored inequalities force at least two distinct actual root types in every anchor color. Choose a seed copy and a distinct reserve copy for each color in a transversal `T` meeting every exceptional `S`. Complete the selected seeds first while leaving all selected reserves untouched. Before the first seed in `S` completes, a reserve in `A minus S` remains an actual old witness; afterward that completed seed remains an actual new witness. The same seeds and reserves may protect several obligations, so the proof respects shared root capacity rather than allocating it independently.

The fixed set of four physical active anchor labels in a column hits every endpoint support and every endpoint-containing intermediate support because `pi(A)=A`. It supplies one unchanged upper-cover identity for the entire handover. Thus the path stays directly in `{3,4}`; no maximum-layer conversion is used.

## Renewal, progress, and exact destination

After the selected seeds complete, every remaining actual copy is processed by adding all missing destination incidences and then deleting old-only incidences. Endpoint containment preserves every original floor, including unequal saturated floors. Finite copy and incidence lists provide the next legal primitive and terminate each column.

A completed column restores the prescribed group counts, exact target, colored guard, and reusable seed/reserve choices. Repeating over the finite unresolved-column set reaches the exact labelled noncompact destination. Each differing endpoint incidence is toggled exactly once and no other incidence is changed, proving the stated global minimum.

## Explicit four-obligation control

For every `m>=20`, take the private outside pairs

- `Gamma_0={{8,10},{9,12}}`
- `Gamma_1={{4,6},{11,14}}`
- `Gamma_2={{5,7},{13,16}}`
- `Gamma_3={{15,18},{17,m-1}}`

and prescribe `pi=(0 1)(2 3)`, fixing outside roles. Then

`E_pi={{0,2},{0,3},{1,2},{1,3}}`.

No single old or new anchor color protects all four obligations; `T={0,1}` and distinct reserves do. With one copy per type the exact minimum is `16t`. The endpoint-union transversal is exactly two, so a static union guard is unavailable. Eight-type minimality is claimed only inside the declared colored-footprint representation.

## Limits and next obligation

X58 requires `pi(A)=A`. It does not handle a prescribed permutation that mixes anchor and outside roles, because the fixed upper-cover identity then moves while multiple lower witness obligations transfer. It also does not prove universal colored-guard accessibility, a whole-root-order obstruction, unrestricted mixed/directed/higher-target/nested repair, or a new native connectivity classification.

The next analytical obligation is to couple a moving upper cover to several simultaneous lower witness transfers when `pi(A)!=A`, or to characterize a precise compatibility obstruction. The separately promised efficiency runner, fixture execution, and benchmarking remain unstarted and outside this analytical checkpoint.

No numerical campaign or scientific execution was performed. The completed v16.54 and v16.55 certificates, their frozen sources, and all original evidence remain unchanged.
