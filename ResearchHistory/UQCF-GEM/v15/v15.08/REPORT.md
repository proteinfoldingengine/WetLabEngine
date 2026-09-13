# v15.08 — Genesis Source-Semantics / Neutral-Preparation Identification Gate

**Status:** CLOSED ON BRANCH / integration pending  
**Primary outcome:** `GENESIS_PROVENANCE_DOES_NOT_IDENTIFY_NEUTRAL_PREPARATION_SOURCE`  
**Secondary:** `SOURCE_SEMANTICS_IRREDUCIBLE_RELATIVE_TO_FROZEN_ONTOLOGY`  
**Tertiary:** `LOG_PROJECTIVE_SOURCE_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM`  
**Major structural result:** `true`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`

## Question

v15.07 derived a canonical local quantum information generator without using downstream gravity:

\[
\tau_d=I_d/d,
\qquad
Q_d(\rho)=d\rho,
\qquad
K_d^0(\rho)=\log\rho-\frac{\operatorname{Tr}\log\rho}{d}I.
\]

It also proved the conditional endpoint statement that if the physical source is defined to be the PGRL generator taking the frame-neutral state \(\tau_d\) to a faithful state \(\rho\), then its positive projective ray is

\[
[P]_+=[K_d^0(\rho)]_+.
\]

v15.08 asks the remaining upstream question only:

> Does the already-frozen Genesis/provenance/source-role ontology itself force the identification “physical source = neutral-reference-to-state preparation generator”?

No gravity, ADM, Einstein equation, cosmology, entropy, pruning, or physical-time criterion is allowed to answer that question.

The result is

\[
\boxed{
\texttt{GENESIS\_PROVENANCE\_DOES\_NOT\_IDENTIFY\_NEUTRAL\_PREPARATION\_SOURCE}
}.
\]

This is a branch-stop result relative to the frozen ontology, not a theorem that no deeper source semantics can exist.

---

# I. TYPE AUDIT

The relevant frozen objects are not interchangeable.

## 1. Genesis Pin

The V997 Genesis Pin certifies recoverable-history legitimacy. Its operative data are of the form

```text
pinned witness registry
pinned genesis anchor root
witness quorum
append-only continuity
non-circular origin
```

Its principal result is that visible-state equivalence does not imply legitimate history.

The Genesis Pin therefore has type

```text
history / registry / root / witness legitimacy boundary
```

and not

```text
quantum density operator
```

or

```text
Hermitian state-preparation generator.
```

Nothing in the frozen V997 artifact identifies Genesis with

\[
\tau_d=I_d/d.
\]

Likewise, nothing in that artifact states that a source is the generator carrying \(\tau_d\) to the current quantum state.

Hence

\[
\boxed{
\texttt{GENESIS\_PIN\_CERTIFIES\_HISTORY\_LEGITIMACY\_NOT\_QUANTUM\_REFERENCE\_STATE}
}.
\]

## 2. Ternary source-role primitive

V923 establishes an exact finite source-legitimacy classification in its tested branch using three roles:

```text
source_active_role
source_basin_eligible_nonactive_role
source_rejected_or_broken_role
```

That is a discrete information primitive distinguishing source roles that observable endpoint/path data alone cannot distinguish.

It does **not** define a map

\[
S_{\rm ternary}\longrightarrow P\in\operatorname{Herm}(\mathcal H),
\]

and it does not define a spectral response function \(a(r)\).

Therefore source-role legitimacy information and an operator-valued source generator remain different typed objects.

## 3. V995 causal generator compatibility

V995 includes a layer called

```text
generator_compatibility_causal
```

whose documented purpose is compatible dynamics and event-to-symbol coupling inside its recoverability closure stack.

That layer is important for history legitimacy, but no frozen artifact supplies a typed identification between that model-level compatibility certificate and the PGRL Hermitian generator \(P\) used in the quantum source-response stack.

Accordingly, v15.08 does not reinterpret the word “generator” across those two constructions as though it established a common mathematical object.

## 4. Earlier source-origin boundaries

The certified v13.26 result already states that Genesis anchoring supplies identity/compatibility structure but does not provide an absolute source calibration.

The certified v14.04 representation theorem is even more restrictive: support-gauge-trivial provenance can map naturally only to a central projective support class, which is PGRL-null, while richer provenance carriers require a representation/intertwiner not supplied by the frozen archive.

Thus provenance legitimacy cannot silently be promoted to a noncentral operator source merely because both are called “source” in different layers of the program.

---

# II. COUNTERMODEL INDEPENDENCE THEOREM

The decisive result is stronger than a failed archive search.

Let \(D\) denote the relevant frozen provenance/source-role information used in this gate. Fix one admissible signature

```text
pinned_genesis_pass
source_active_role
append_only_valid
quorum_valid
same_retained_source_grade
```

and fix the same faithful two-site quantum state.

Now consider three local-unitary-equivariant Hermitian source laws already known to be lawful under the v15.04 source kinematics:

\[
a_{\rm lin}(r)=1,
\]

\[
a_{\log}(r)=\frac{2\operatorname{atanh}r}{r},
\]

and

\[
a_{\rm poly}(r)=1+r^2.
\]

For each law build

\[
P_a
=
F_a(\rho_1)\otimes I
+
I\otimes F_a(\rho_2),
\qquad
F_a(\rho)=a(r)(\rho-I/2).
\]

All three extensions retain the same declared Genesis/source-role/provenance signature.

All three generators are centered Hermitian sources and produce valid faithful finite PGRL states under the same source-coordinate step.

But their projective source rays are inequivalent.

Executed separations are

```text
linear vs log        = 0.06248625684944288
linear vs polynomial = 0.08772246091732862
log vs polynomial    = 0.025253513918714537
```

The minimum separation is

```text
0.025253513918714537
```

while the maximum trace-normalization error of the resulting finite PGRL states is

```text
0.0
```

and their minimum output eigenvalue is

```text
0.027251058487541124.
```

Therefore these are not invalid-source counterexamples.

They are multiple lawful operator-source extensions compatible with the same audited provenance/source-role facts.

This gives the exact logical implication:

> If two or more extensions satisfy every relevant frozen provenance/source-role certificate and the audited quantum source kinematics, but assign inequivalent Hermitian source rays to the same frozen data, then those frozen data do not entail any one of those rays.

Hence

\[
\boxed{
\texttt{COUNTERMODEL\_INDEPENDENCE\_PROVES\_SOURCE\_SEMANTICS\_NOT\_ENTAILED}
}.
\]

The theorem is about non-entailment by the present frozen ontology. It does not prohibit adding a deeper primitive that eliminates the countermodels.

---

# III. RELATION TO THE v15.07 CANONICAL LOG GENERATOR

The negative source-semantic result does **not** undo the positive v15.07 mathematics.

For the same test state, the v15.07 canonical centered relative-density generator agrees with the logarithmic source candidate to projective residual

```text
9.460671693549492e-16.
```

Thus

\[
K^0(\rho)
=
\log\rho-\frac{\operatorname{Tr}\log\rho}{d}I
\]

remains the canonical additive generator of the frame-neutral relative-density object.

What v15.08 blocks is the next semantic inference:

```text
canonical additive information generator
therefore
physical source generator.
```

That implication is not supplied by Genesis Pin, source-role classification, provenance identity, retained source grading, or current frozen PGRL semantics.

The correct status is therefore:

```text
canonical log information generator : DERIVED
log generator as physical source    : NOT DERIVED
```

---

# IV. WHY GENESIS DOES NOT CLOSE THE GAP

There are two distinct notions of “origin” in the current archive.

### A. Historical/provenance origin

Genesis Pin answers questions such as:

- Is this history anchored to the pinned root?
- Does it use the authorized witness registry?
- Does the append-only chain remain valid?
- Is the history non-circular?
- Does the source role remain legitimate in the tested classification stack?

### B. Quantum reference origin

v15.07 answers a different mathematical question:

- Which normalized local state has no preferred quantum frame?

That answer is

\[
\tau_d=I_d/d.
\]

Nothing in the frozen ontology identifies A and B.

Calling both “origins” does not create a lawful map between them.

Specifically, the archive contains no certified equation of the form

\[
\text{Genesis Pin}\mapsto \tau_d,
\]

nor

\[
\text{source role/provenance}\mapsto
\log\rho-\frac{\operatorname{Tr}\log\rho}{d}I.
\]

Any such identification would add information.

---

# V. IRREDUCIBILITY RESULT

The source-semantic problem is therefore irreducible relative to the current frozen ontology.

The present certified stack determines or constrains:

```text
history legitimacy
source-origin identity
source-role class
retained source grade / extensivity
source-current balance
conditional current selection
local-unitary source covariance
canonical frame-neutral quantum reference
canonical relative-density multiplicative operator
canonical centered-log additive generator
```

but it does not contain a rule equating the last generator with physical sourcehood.

Because explicit countermodels preserve the relevant prior certificates while changing \([P]\), this is not merely lack of imagination or lack of search coverage.

It is a non-entailment result for the frozen theory.

Therefore

\[
\boxed{
\texttt{SOURCE\_SEMANTICS\_IRREDUCIBLE\_RELATIVE\_TO\_FROZEN\_ONTOLOGY}
}.
\]

and

\[
\boxed{
\texttt{LOG\_PROJECTIVE\_SOURCE\_REQUIRES\_NEW\_SOURCE\_SEMANTICS\_AXIOM}
}.
\]

---

# VI. WHAT A NEW AXIOM WOULD HAVE TO SAY

v15.08 does **not** recommend silently adding an axiom. It identifies the exact missing content so that any future proposal can be judged honestly.

A sufficient new principle would have to state, in ontology-native terms, something equivalent to:

> The physical source associated with a faithful local relational state is the generator of its admissible preparation relative to the unique frame-neutral reference state.

Combined with v15.07, such a principle would immediately give the positive projective source ray

\[
[P]_+
=
\left[
\log\rho-\frac{\operatorname{Tr}\log\rho}{d}I
\right]_+.
\]

But that statement is not presently derived.

It would be a **NEW SOURCE-SEMANTICS AXIOM** and must be motivated independently of any downstream gravitational success.

Its absolute magnitude would still not be fixed, because the PGRL parameterization gauge from v13.26 remains:

\[
P\to aP,
\qquad
s\to s/a.
\]

So even a future source-semantic axiom would canonically select a projective source ray before it selected an absolute physical source unit.

---

# VII. CLAIM BOUNDARY

## Derived / preserved

- the v15.07 unique frame-neutral reference \(\tau_d=I_d/d\);
- the v15.07 canonical multiplicative relative-density operator \(Q_d=d\rho\);
- the v15.07 additive centered-log generator;
- Genesis Pin as a recoverable-history legitimacy boundary;
- the V923 ternary source-role primitive as finite source-legitimacy information;
- v13.26 Genesis/source-calibration boundary;
- v14.04 provenance representation / centrality obstruction;
- explicit countermodels showing the same audited provenance signature admits multiple inequivalent lawful operator source rays;
- therefore non-entailment of the neutral-preparation source semantics by the frozen ontology.

## Not derived

- Genesis Pin = maximally mixed quantum state;
- source role = local Hermitian source generator;
- causal-generator compatibility = PGRL Hermitian generator;
- physical source = neutral-reference preparation generator;
- `P = centered log rho` as a physical-source law;
- absolute source magnitude;
- retained-node-to-quantum-site carrier;
- a natural graph/provenance-to-compatibility-parent source map;
- physical stress-energy;
- physical coframe/spacetime;
- Einstein equations;
- physical time as a primitive;
- Pillar 3 closure.

No downstream gravitational target was used to obtain the v15.08 classification.

---

# VIII. STOP RULE

The logarithmic source-origin branch stops here under the current frozen ontology.

Do **not**:

```text
identify Genesis Pin with tau_d=I/d by analogy;
identify the V923 source-role symbol with a Hermitian generator;
interpret V995 generator compatibility as the PGRL operator source without a typed map;
choose centered log rho because it improves downstream gravity/ADM/Einstein behavior;
continue searching the same frozen dependency set for a selector already ruled out by the countermodels.
```

A lawful continuation has exactly two forms:

1. introduce one explicit, independently motivated **NEW SOURCE-SEMANTICS AXIOM**, then test its consequences without downstream tuning; or
2. preserve the canonical log generator only as an information-geometric object and redirect research to an independent unresolved bridge.

For current governance, option 2 is the default unless the new axiom is explicitly approved.

---

# Status

```text
Genesis Pin -> history legitimacy                         : CERTIFIED IN ITS TESTED STACK
ternary source role -> source-legitimacy class           : CERTIFIED IN ITS TESTED STACK
Genesis / source role -> neutral quantum reference       : NOT DERIVED
Genesis / source role -> local Hermitian source generator: NOT DERIVED
frame symmetry -> tau_d=I/d                              : DERIVED (v15.07)
tau_d,rho -> centered log information generator          : DERIVED (v15.07)
centered log generator -> physical source                : NOT ENTAILED
source semantics in frozen ontology                      : IRREDUCIBLE / BRANCH STOP
new source-semantics axiom                               : REQUIRED TO CONTINUE THIS BRANCH
absolute source scale                                    : NOT DERIVED
Pillar 3                                                 : OPEN
```

No broad scientific breakthrough is declared.

v15.08 is a **major structural no-go / irreducibility result**: the mathematical log generator is now canonical, but the frozen Genesis/provenance ontology does not confer physical-source semantics on it.
