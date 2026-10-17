# Two-location preparation and order-independent present-record contrast

Date: 2026-10-17 America/Phoenix.
Author: proteinfolding-gpt.
Baseline: 2e2023aeef8ad63d286aa9fdc0f7a1156f4aa88a.
Status: AUTHOR ANALYTICAL EXTENSION / INDEPENDENT REVIEW PENDING.
Extends Grok's CONSTRUCTION.md draft 1 (blob 888e8b754da10641c42dc6c1592948e0c307975a). No mechanism implementation or scientific execution.

## Positive construction

Grok's inside-versus-outside witness can be strengthened in two ways:

1. It needs only two legitimate append locations, not location-free append legitimacy.
2. With complete collapse of the receiver's strict descendants and a common retained root reference, the resulting present-state ratio distinguishes the two cases independently of the pruning order. It does not require a history log or a chosen order between incomparable branches.

These are conditional deductions. The original Genesis audit earns certificate continuity for supplied events, not permission to append at either carrier location. That missing typed link is identified below using the original implementation rather than its prose description.

## 1. What the original Genesis implementation actually earns

Inspected at the baseline:
- Tmp/TOE/Einstein 4/v997_genesis_pin_publication_audit/v997_genesis_pin_publication_audit.py, blob 282b08b79b82be65391e1251a97891ad9c742b2f.
- Its v997_genesis_pin_outputs/CLAIM_BOUNDARIES.md, blob 8ce06f173a949fb36ca9219d902583238868996b.
- ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/source_binding.py, blob a1df8db6c1d1b3fd4491a5f502267841725f3f32.
- ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md, blob a21acad73c80cb748f2e42c244f6db53146c2bf2.

V997 defines chained_transition(prev_root, registry, step, event, witnesses). The transition hashes those supplied fields. validate_append_only_chain reconstructs them successively from the pinned root. Registry equality, root equality, witness quorum and absence of modeled circular bootstrap are checked separately. build_path also checks a supplied/generated final visible-state condition.

**Certificate extension lemma.** Take a prefix with equally many events and witness sets, exactly one more root than events, and all its checks satisfied. Append a supplied event string E, a quorum-valid witness set W, and the root

    r_next = chained_transition(r_last, registry, n+1, E, W).   (1)

Then the extended hash chain passes validate_append_only_chain; all prior roots remain unchanged, registry/root checks are unchanged, and all witness-quorum checks pass. If the separate visible-state condition remains true, the conjunction used by build_path accepts it.

Proof: the first n validation iterations reproduce the old prefix; the final iteration is exactly (1). No hash collision assumption is needed for this validation identity. This lemma concerns syntactic consistency, not security or occurrence. Equal event/witness lengths are an explicit precondition; it does not generalize from zip truncation.

There is no carrier tree, parent-location parameter, grade, semantic append permission, or event-to-tree action in those functions. The hash predecessor is the previous chronological ledger commitment; it must not be identified with the parent of a new carrier vertex. An event string could encode a location, but such an encoding and its interpretation are not supplied by this validator.

Thus the implementation positively supplies a common-prefix certificate-extension procedure for supplied events and witnesses. It does NOT by itself prove that changing a tree parent preserves native legitimacy. Lack of a location check is not a semantic permission theorem.

The v15.56 binding supplies the distinct type

    source_event -> (genesis_id, full_lineage_address).

It explicitly earns no amplitude. It classifies the fields of an already certified binding; it does not construct the binding, certify an append operation, or show that the addressed vertex is the parent of a newly generated entry.

## 2. Replace universal N2 by a two-location obligation

Let P be the common finite prefix carrier and a its retained receiver. Let tau be an entry type with equal positive grade w in both preparations.

Write L(P,tau) for the set of parent locations for which an actual inherited semantic append certificate exists. This is notation for the unresolved domain, not a newly declared primitive or a computed set.

The needed obligation is only

    u belongs to L(P,tau), o belongs to L(P,tau),               (2)

where u is a strict descendant of a and o is the common root outside a's subtree. Fresh child addresses are required in both cases. Both append operations preserve old entries and grades, and have the same type/grade contract.

Universal location freedom is sufficient but unnecessary. A candidate proof of (2) should exhibit two certificates and their semantic validation rule. The certificate-extension lemma can then preserve their common pinned ancestry. No assertion that L contains either location is made from the current sources.

This is the precise separation:
- ledger chain continuation: derived at the syntactic model level;
- semantic permission and typed effect at the two locations: open;
- occurrence and accessible receiver output: open.

Grok's statement that lack of a selector supplies all alternate orders or placements must not replace (2). Nonuniqueness of a selector does not alone establish permission for a specified alternative.

## 3. Complete-fiber contraction removes the order choice

Take P={o,a,u,v}, with a below o and u,v below a. The base grades are c>0 at o, alpha>0 at a, beta>=0 at u and gamma>=0 at v. Put

    A = alpha + beta + gamma > 0.                              (3)

Preparation I appends an entry e of grade w>0 below u.
Preparation O appends an entry f of the same grade w below o.
This is Grok's W1, subject to the two-location obligation (2).
Total initial grade is c+A+w in both cases.

The proposed receiver record is the pair of present grades at a and o, modulo a common positive scale. This is an explicit extension from a single-owner scalar to a receiver/reference pair; access to both coordinates is an OPEN premise. It is not inferred from knowing the root's address.

Initially the pair is (alpha,c) in both preparations. The receiver is blind on this interface, even projectively.

Consider ANY finite sequence of inherited ancestral retractions satisfying:
- o and a remain retained throughout;
- at its terminal state all strict descendants of a are removed;
- in preparation O, f may either remain retained or be removed into o.

No sequence of intermediate removals, ordering between u and v, or history-storage architecture is prescribed.

By FCV P1 composition, the terminal pushforward equals the direct retraction to its terminal retained set. Therefore the final receiver/reference pairs are

    I: (A+w, c);
    O: (A, c) if f remains;
       (A, c+w) if f is removed.                              (4)

Every atom originally below a maps to a at this endpoint. An outside atom cannot map into a: its ancestry does not contain a. Removal of f instead maps it to o. These statements use actual prefix ancestry, not a proposed current or channel.

Consequently the present-state ratios obey

    q_I = (A+w)/c > A/c >= q_O.                                (5)

The separation holds for any positive w, without an external absolute scale. It survives all admissible intermediate orders and either fate of f. There is no history log in (4)-(5). For counting grades c=alpha=beta=gamma=w=1:

    initial q = 1 in both;
    final q_I = 4;
    final q_O = 3 or 3/2.                                     (6)

The common threshold A/c is part of the declared comparison contract. Pairwise separation itself does not assume the receiver was given a numerical threshold. A physically usable decoder still needs a justified reference/readout contract.

The source distinction survives rooted isomorphisms fixing a and o: e is a descendant of a, f is not. Both preparations have the same total grade. All pushforwards conserve it. Local gain therefore does not imply global information creation.

This endpoint theorem does not claim separation at every partially contracted stage. Before full contraction, differing amounts of common base grade may have arrived, and raw values can overlap across differing schedules. The complete-fiber endpoint condition is load-bearing.

## 4. What is and is not forced

Complete-fiber contraction is an allowed inherited retraction, and FCV P1 makes (4) independent of its factorization. The source primitives do not yet force it to occur.

A finite capacity limit alone would not prove this endpoint. Overflow might be handled by removing an outside entry, refusing an append, changing retention, or another allowed operation. To use capacity positively, derive that the specified retained-state constraint forces completion of the receiver fiber while retaining a and the reference. No such capacity law is added here.

Similarly, retaining o and a as addresses does not give access to their grades. The two-coordinate present-state interface avoids a numerical-history assumption only by explicitly retaining the unresolved two-coordinate access obligation. A single positive scalar up to arbitrary rescaling cannot distinguish (A+w) from A; (5) uses a common scale for the pair.

## 5. Preparation and certification contract for the next proof

A sufficient continuation should provide:

1. One common pinned prefix with the specified carrier and nonnegative grade object.
2. Two native semantic append certificates at u and o, of equal positive grade w, preserving the old receiver/reference pair.
3. A typed relation from the certified append event to the prefix-tree extension. Hash strings and source addresses alone do not supply it.
4. An inherited condition causing complete-fiber contraction, or a justified positive-probability occurrence class satisfying it.
5. Actual access to the two retained grade coordinates under a common scale.

Items 2-3 are the immediate preparability target. Items 4-5 are the enactment/access target. Equation (1) handles the certificate-continuity component once the events and witnesses exist; equations (4)-(5) handle the consequence once the endpoint and readout exist.

## Status and verification

This extension uses direct symbolic proofs and source inspection. No scientific code, test campaign, changed V997 validator, or new event mechanism was implemented. Original source code was read, not executed. The algebra was checked directly for both terminal outside-entry cases and for the zero-beta/gamma boundary. Independent Gemini review and publication audit of this new argument remain pending; earlier ledger acceptance does not cover it.

The new constructive result is a weaker two-location preparation requirement together with an order-independent, projectively separating present-record endpoint. Preparability and native interaction are not declared closed.
