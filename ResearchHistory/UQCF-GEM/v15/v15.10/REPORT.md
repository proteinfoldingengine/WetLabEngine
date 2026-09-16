# v15.10 — Pruning-Order / Emergent-Time Bridge Reassessment

**Status:** CLOSED ON BRANCH / integration pending  
**Primary outcome:** `FROZEN_PRUNING_DOES_NOT_YET_DERIVE_INTRINSIC_TIME_ORDER`  
**Secondary:** `V1153_REWEIGHTING_IS_SUPPORT_PRESERVING_AND_INVERTIBLE_ON_SIMPLEX_INTERIOR`  
**Tertiary:** `PROVENANCE_LEDGER_HAS_INTRINSIC_ANCESTRY_ORDER_BUT_NO_FROZEN_IDENTIFICATION_WITH_PRUNING_TIME`  
**Major structural result:** `true`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`

## Question

The intended ontology is not that physical time is primitive. The intended bridge is

```text
pre-pruning relational/information structure
    -> irreversible pruning / recoverability loss
    -> intrinsic ordering / arrow
    -> emergent time
    -> later geometry / spacetime correspondence
```

v15.10 asks the first exact question needed by that ontology:

> Does the already-frozen recoverability/pruning stack itself contain an intrinsically oriented, composable, irreversible update law from which an emergent order can be read without importing an external clock?

The answer is currently **no**.

That negative result does **not** refute the thesis that time is pruning. It localizes the missing mathematical step.

The frozen archive presently contains two different positive structures:

1. recoverability-weighted **selection pressure** in V1153;
2. an intrinsic rooted **provenance ancestry order** in the append-only Genesis/ledger stack.

But it does not yet contain a frozen law identifying those two structures as one and the same pruning-generated temporal order.

Therefore

\[
\boxed{
\texttt{FROZEN\_PRUNING\_DOES\_NOT\_YET\_DERIVE\_INTRINSIC\_TIME\_ORDER}
}
\]

is the primary adjudication.

---

# I. Minimum requirements for an emergent ordering variable

This gate deliberately does **not** require a metric duration, lapse, Lorentzian signature, or spacetime coordinate. Those would be later correspondence questions.

It requires only three minimal properties.

## 1. Intrinsic orientation

The direction of succession must be readable from the relational/information transformation itself.

An external loop variable

```text
n = 0,1,2,...
```

can label an already-ordered computation, but it does not explain why one state is intrinsically before another.

## 2. Composable ordering

If

\[
A\to B,
\qquad
B\to C,
\]

then the ordering structure must support the composite relation

\[
A\to C.
\]

This is the minimal reachability/ancestry structure required for an ordered history.

## 3. Irrecoverability asymmetry

If the arrow is supposed to arise from pruning as information loss, the relevant pruning operation cannot possess a two-sided inverse on the retained description.

The forward update must identify, remove, or render unrecoverable distinctions that were present before the update.

These requirements are upstream of physical time calibration.

---

# II. Exact audit of V1153 pruning

V1153 describes its pruning mechanism as recoverability-weighted redistribution:

\[
w_i'=
\frac{w_i\exp[-\beta(U_i-\min U)]}
{\sum_jw_j\exp[-\beta(U_j-\min U)]}.
\]

The engine explicitly says:

```text
Pruning emerges from weight redistribution under primitive informational pressure.
```

and explicitly disables a hard accept/reject filter.

This is a genuine selection-pressure mechanism. The question here is whether it is also an irreversible information-loss operation.

## 1. Support-preservation theorem

For every strictly positive initial weight

\[
w_i>0
\]

and every finite potential \(U_i\),

\[
\exp[-\beta(U_i-\min U)]>0.
\]

Therefore

\[
w_i'>0.
\]

So finite V1153 reweighting maps the interior of the probability simplex to itself and does not delete any history from support.

The deterministic v15.10 controls use seven histories and give

```text
support cardinality before = 7
support cardinality after  = 7
```

The archived V1153 final state is consistent with this: the invalid histories become extremely small in weight, but their total weight remains nonzero,

```text
1.467017487634064e-10.
```

Hence this is **soft selection pressure**, not literal support pruning.

Classification:

```text
SELECTION_PRESSURE_WITHOUT_IRREVERSIBLE_SUPPORT_PRUNING
```

## 2. Exact inverse theorem on the simplex interior

For known potential \(U\), define

\[
R_U(w)_i
=\frac{w_i e^{-\beta U_i}}{\sum_j w_j e^{-\beta U_j}},
\]

where an additive constant in \(U\) is irrelevant.

Then

\[
R_{-U}(R_U(w))=w.
\]

So the reweighting operation is a bijection on the simplex interior.

Executed maximum inverse error:

```text
8.554842949272357e-17
```

This is numerical verification of the exact algebraic identity.

Therefore the weight map alone cannot define an intrinsic irreversible arrow.

## 3. Composition law

The same family composes as

\[
R_V\circ R_U = R_{U+V}
\]

up to the projectively irrelevant additive constants removed by normalization.

Executed maximum composition error:

```text
1.468815065250206e-16.
```

This is a useful positive property—there is a clean compositional update algebra—but it is a reversible composition law, not yet a pruning arrow.

## 4. The V1153 sequence is externally indexed

The frozen V1153 engine contains the explicit control structure

```python
for ordered_update in range(N_ORDERED_UPDATES):
```

with

```text
N_ORDERED_UPDATES = 160.
```

The update label is therefore supplied by the computational loop.

V1153 correctly says that it uses no physical-time primitive. But v15.10 sharpens the distinction:

```text
not using physical time as the update index
```

is not the same theorem as

```text
the update order is generated intrinsically by pruning.
```

The latter remains underived.

---

# III. Important scope boundary: what counts as the V1153 pruning operation

The V1153 simulator also updates geometry, source, order-memory, flow, and accessibility fields through repair, diffusion, normalization, and deterministic pseudorandom perturbations.

Those numerical field-update maps are not what V1153 itself identifies as its pruning rule. The archived report explicitly identifies pruning with **weight redistribution under informational pressure**.

v15.10 therefore does not try to manufacture an arrow by pointing to incidental noninvertibility in an auxiliary numerical update.

Doing so would change the ontology after seeing the desired result.

The scientifically relevant question is whether the **declared pruning operation** supplies irreversible information loss. For V1153 weight redistribution, it does not.

---

# IV. The frozen stack already contains an intrinsic provenance order

The negative V1153 result does not mean the archive lacks all intrinsic ordering.

V995 contains:

```text
symbol_emission_event_ledger
anchored_append_only_freshness_ledger
append_only_one_successor_registry_update_ledger
anchored_registry_update_ledger_root
genesis pins
```

and V997 requires append-only continuity anchored to a pinned non-circular Genesis root.

That structure naturally defines an ancestry relation.

For a rooted chain

\[
g\to e_1\to e_2\to e_3\to e_4,
\]

reachability is transitive and antisymmetric in the absence of cycles.

The deterministic control gives

```text
direct edges                 = 4
transitive ancestry relations= 10
rooted orientation           = true
antisymmetric                = true
composable                    = true
```

So there is already an ontology-native notion of **before/after in provenance**.

Classification:

```text
INTRINSIC_PROVENANCE_ORDER_EXISTS_BUT_IS_NOT_DERIVED_FROM_PRUNING
```

This is a positive result, but its type must be respected.

The append-only ledger certifies generative-history legitimacy. The frozen archive does not state that each ledger edge is created by an irreversible pruning event, nor that ledger ancestry itself is physical time.

V997 explicitly warns:

```text
Do not interpret the update index as physical time.
```

v15.10 preserves that guardrail.

---

# V. Conditional theorem: actual information-loss pruning can generate an arrow

The central positive mathematical result of v15.10 is that the intended ontology has a clean theorem-shaped realization.

Consider composable recoverability maps

\[
X_0\xrightarrow{\pi_0}X_1
\xrightarrow{\pi_1}X_2
\xrightarrow{\pi_2}X_3
\]

where each \(\pi_k\) is noninjective.

A noninjective map identifies at least two previously distinguishable states. Therefore no two-sided inverse exists on the retained description.

The v15.10 control uses finite information classes

```text
8 -> 4 -> 2 -> 1
```

with three explicit many-to-one maps.

Results:

```text
map count                  = 3
all maps noninjective      = true
full composition noninjective = true
two-sided inverse exists   = false
```

The direction

\[
X_0\to X_1\to X_2\to X_3
\]

is then intrinsically distinguished by recoverable-information loss.

This supplies an order/arrow candidate without assuming physical time first.

Classification:

```text
NONINJECTIVE_RECOVERABILITY_UPDATE_INDUCES_ORIENTED_INFORMATION_ORDER_CONDITIONALLY
```

The word **conditionally** is load-bearing: the frozen V1153 pruning map does not yet realize this noninjective structure.

Also, this theorem derives an **ordering arrow**, not a clock rate or duration.

---

# VI. What the archive now says about “time is pruning”

The current result is not

```text
time is not pruning.
```

The current result is:

```text
The frozen archive has not yet implemented the kind of pruning
required for pruning itself to generate the order.
```

More precisely:

```text
V1153 informational pressure
    -> nonuniform recoverability weights
    -> strong selection
    -> but support preserved
    -> and weight map invertible given U
    -> no intrinsic arrow from the pruning map

V995/V997 provenance
    -> pinned Genesis
    -> append-only succession
    -> intrinsic ancestry order
    -> but not shown to be generated by pruning

conditional information-loss theorem
    -> noninjective recoverability update
    -> composable loss of distinctions
    -> no two-sided inverse
    -> intrinsic information arrow
    -> viable mathematical shape for emergent order
```

The missing bridge is now extremely specific:

\[
\boxed{
\text{actual pruning event}
\longrightarrow
\text{noninjective recoverability loss}
\longrightarrow
\text{certified provenance successor}
}
\]

No such frozen identification law was found in the audited dependency set.

---

# VII. Frozen dependency audit

v15.10 hash-binds the following artifacts:

```text
V1153 engine
c473e6f750577a5e63d2481c1d702031edfb99b6

V1153 report
1fe4248b71fd9e6628b7aee52eacbab96830bfde

V1153 summary
9c6ba1cc26031c2b4063e7e06e1fcd205a903dc4

V995 closure synthesis
a0cb9a17344800ebfee1cbe3f724da2ac418e164

V997 Genesis/recoverability report
8f4ee48cbaf6c822b87dd5e30a5dfee4d596e26e

v15.09 report
ec73ef9240dcef062c95a82c511a874d0d2923ef
```

The resulting frozen classification is

```text
ORDER_AND_PRUNING_EXIST_AS_SEPARATE_FROZEN_STRUCTURES_WITHOUT_AN_IDENTIFICATION_LAW
```

The audit confirms:

```text
V1153 external ordered-update loop       : FOUND
V1153 positive reweighting pruning       : FOUND
V1153 support-reduction pruning rule     : NOT FOUND
V1153 hard accept/reject driving pruning : EXPLICITLY ABSENT
V995 append-only provenance order        : FOUND
V997 update-index physical-time warning  : FOUND
pruning -> provenance-order law          : NOT FOUND
```

---

# VIII. Relation to the broader stack

## v15.09 remains closed

No carrier/functor principle is imported from the time branch.

## v15.08 remains closed

The missing source-semantics axiom is not reused as a pruning or time selector.

## V1153 is preserved, not invalidated

V1153 still demonstrates a valuable result in its intended scope: recoverability-weighted selection can emerge from primitive informational pressure without a final hard certification filter.

v15.10 only narrows what that result licenses regarding emergent time.

## V995/V997 are strengthened as ordering evidence

Their append-only rooted history structure already supplies an intrinsic provenance order. What remains open is a first-principles identification between that order and irreversible pruning events.

## Pillar 3 remains open

Nothing in v15.10 derives a physical lapse, metric duration, spacetime foliation, Lorentzian causal cone, ADM time variable, or Einstein evolution law.

Those questions should not be asked until the upstream ordering bridge itself is lawful.

---

# IX. Claim boundary

## Derived / preserved

- V1153 contains real recoverability-weighted selection pressure;
- its declared weight-pruning map preserves positive support for finite potentials;
- that map is exactly invertible on the simplex interior when the potential is known;
- the reweighting family composes cleanly;
- V1153 applies these updates under an externally supplied ordered loop;
- V995/V997 supply a rooted append-only provenance ancestry order;
- that ancestry relation is composable and intrinsically oriented by Genesis/append structure;
- a sequence of noninjective recoverability maps would conditionally induce an intrinsic information-loss arrow;
- therefore the missing object is a pruning-to-order identification / irreversible pruning-event law.

## Not derived

- that V1153 soft reweighting is irreversible state reduction;
- that a vanishingly small weight is equivalent to a deleted alternative;
- an ontology-native support-reducing pruning event in the audited frozen stack;
- a frozen law identifying pruning events with V995/V997 ledger successors;
- an emergent physical-time variable;
- metric duration or clock calibration;
- Lorentzian causal structure;
- ADM lapse/shift or spacetime foliation from pruning;
- Einstein evolution equations;
- Pillar 3 closure.

Entropy is not used as a selector in this gate. V1153 records a weight-entropy diagnostic, but its pruning weights are selected by the primitive informational potential rather than by entropy.

No downstream gravity/ADM/Einstein/cosmology behavior is used to choose an ordering law.

---

# X. Stop rule / next lawful frontier

Do **not**:

```text
rename the V1153 loop counter as emergent time;
treat an arbitrarily tiny positive weight as a deleted state;
call reversible exponential reweighting irreversible collapse;
use incidental numerical noninvertibility in auxiliary field updates as the pruning event;
identify append-only ledger ancestry with physical time by terminology alone;
use entropy, ADM, Einstein, or gravitational fit quality to choose the arrow.
```

A lawful continuation should search only for one of two objects:

1. a **frozen ontology-native noninjective recoverability/pruning operation** already present elsewhere in the archive; or
2. a **frozen typed law connecting an actual pruning event to the append-only provenance successor relation**.

If neither exists, continuing this bridge requires one explicit **NEW PRUNING-EVENT / ORDER-IDENTIFICATION LAW**.

Only after an intrinsic pruning-generated order is earned should the program ask how that order acquires metric duration or maps into spacetime/ADM structure.

---

# XI. TDD / reproducibility evidence

RED:

```text
checker commit  d6b9ffe90e3e70146c8b4b64fd843478fff0bd77
workflow head   7dad4f1acc4e802aa48c81a8c2153e2aeb74a327
run             34775816721
job             103773603616
result          intended ModuleNotFoundError
```

First GREEN:

```text
implementation  7697b38b2055951f01173ab56ec7f2fc4e26408e
run             34775890308
job             103773802329
result          SUCCESS
```

Live telemetry:

```text
head            b81c467589e48546ef2e823c2430371f9c5143a6
run             34775964430
job             103774000126
result          SUCCESS
```

Frozen-summary binding:

```text
head            6f291b3abebcd6d2c050a2edc3d48eb87cc95892
run             34776022518
job             103774161156
result          SUCCESS
```

Final exact-head certification is performed after this report and the top-level frontier documents are frozen.

---

# Status

```text
recoverability-weighted pruning pressure       : DERIVED IN V1153 TOY STACK
V1153 weight-map support reduction             : NO
V1153 weight-map invertibility                 : YES ON SIMPLEX INTERIOR
V1153 intrinsic pruning-generated order        : NO
rooted append-only provenance order            : YES
pruning -> provenance successor identification : NOT DERIVED
conditional noninjective-pruning arrow theorem : YES
emergent time order in frozen ontology         : NOT YET DERIVED
metric duration                                : NOT DERIVED
physical-time primitive used                   : NO
Pillar 3                                       : OPEN
```

No broad scientific breakthrough is declared.

v15.10 is a **major structural localization result**: it shows exactly what is still missing for the program's “time is pruning” ontology to become a derived mathematical bridge rather than an interpretive statement.
