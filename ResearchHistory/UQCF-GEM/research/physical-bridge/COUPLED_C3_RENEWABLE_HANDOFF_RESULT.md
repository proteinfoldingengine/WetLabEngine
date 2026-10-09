# Admissibility-derived spectator separation and renewable four-root handoff
Status: analytical argument frozen before new computation; independent gates pending.
Scope: e51e7333c581b1b343c2e6311b97d898b33e3203. This is a bounded repair result; native record origin remains OPEN.

## 1. Exact structural classification
Let A,B,C,D,E be five distinct core labels, w a reserved fresh label, and T a finite disjoint spectator palette. The labelled source is
S1={A,B} union Z1; S2={B,C} union Z2; S3={A,C} union Z3; S4={D,E} union Z4,
where each Z_i is an arbitrary subset of T. No Z_i is supplied to the controller. Let positive immutable original floors satisfy f_i<=2+|Z_i|.

Claim: tau(S)>=3 if and only if (i) Z4 is disjoint from Z1 union Z2 union Z3, and (ii) Z1 intersect Z2 intersect Z3 is empty. In that case tau(S)=3.

Necessity: a spectator z on roots1 and4 gives the two-cover {C,z}; on roots2 and4 it gives {A,z}; on roots3 and4 it gives {B,z}. Thus tau>=3 forces (i). A spectator z on all first three roots gives the two-cover {D,z}, forcing (ii).

Sufficiency: root4 is disjoint from the union of the first three supports. The first three have empty common intersection: no core label is in all three and (ii) excludes a common spectator. They therefore require at least two labels, and {B,C} hits all three. Root4 is nonempty and requires one further label, so tau=2+1=3. This also proves tau<=3 for every protected member; no tau4 member of this augmented core exists.

Equivalently each spectator's occurrence mask is a subset of {1,2,3} of cardinality at most two, or the singleton {4}. The empty mask is allowed. These are consequences of the native lower bound, not extra independence/separation assumptions. Shared spectators between any two triangle roots are allowed, with arbitrary multiplicity of such spectator labels.

## 2. Uniform eight-edit handoff
Take any admissible source above. Execute the following actual incidence edits:
+w(r4), -D(r4), +D(r1), -A(r1), +D(r3), -A(r3), +A(r4), -w(r4).

Syntax follows solely from the known core phase and freshness; T contains none of these labels. At every slice {B,C} still hits the first three roots. Their common core intersection stays empty, as the displayed core phases show:
(AB,BC,AC), (ABD,BC,AC), (BD,BC,AC), (BD,BC,ACD), (BD,BC,CD).
Their spectator triple intersection remains empty by section1. Thus their hitting number is exactly two at every slice.

Root4 remains disjoint from those three roots throughout. It loses D before D is introduced in the triangle; A is introduced to root4 only after A has been removed from both triangle roots; E never enters the triangle; w occurs only in root4; section1 excludes shared spectators involving root4. Hence its nonempty support contributes exactly one independent hit. The entire family has tau=3 after every primitive.

Roots1 and3 each add before deleting and return to their source size. Root4 has sizes 2+|Z4|,3+|Z4|,2+|Z4|,...,3+|Z4|,2+|Z4|. Root2 never changes. The minimum size of EVERY root over the path equals its original size. Therefore EVERY original admissible positive floor vector, including unequal saturated floors, is preserved. No floor slack has been silently required.

The endpoint is exactly
({B,D} union Z1, {B,C} union Z2, {C,D} union Z3, {A,E} union Z4).
Every hidden incidence remains in its original labelled root and w is absent.

## 3. Retained controller and renewal
Keep fixed triangle base labels B,C and a three-label apex pool {a,d,e}. At a prepared boundary, the known current apex A occurs in roots1 and3; root4 has the other two pool labels D,E. The controller is supplied the next desired apex D, knows these core roles, and tracks the eight phases. It never evaluates tau, any Z_i, spectator cardinality, or a hypothetical hidden-state legality query.

Section1 applies from the native-admissible domain promise, uniformly across all hidden states consistent with that retained core. Section2 transfers the apex to D. The endpoint is the SAME family with A and D exchanged, unchanged Z_i and floors, and w fresh again. This is a structural handoff of the role conditions, not an observer write.

Induction therefore permits every finite prescribed sequence of apex goals in the pool, skipping a goal equal to the current apex. Each actual apex change takes eight actual edits. After each completed macro, w is removed and all original support sizes and hidden incidences are restored. A rank counting remaining prescribed nontrivial exchanges decreases once per completed macro; the finite committed-edit schedule terminates at the exact labelled goal.

If operational requests may return NOOP or have unobservable outcomes, this path theorem does NOT establish actual completion, phase recognition, or an actuator. Under a separately supplied resolved-execution interface, retries may be possible; that interface is not derived here. The result is a uniformly legal committed-path specification from retained roles. It does not require hidden-state information for prospective legality.

## 4. Why this is stronger than the earlier bounded repair
The closed hidden-optimality result put arbitrary spectators only on root4 and fixed all floors to two. Here all four roots may carry arbitrary unknown spectator sets, including shared labels on two triangle roots. The native initial lower bound itself forces precisely the separation needed for handoff. All admissible original floor vectors are covered, and the role conditions are renewed for arbitrary finite goal words.

The earlier fresh-probe theorem proves fresh-addition safety for general nonempty families and reconstructs support using an assumed count channel. This argument completes an exact repair and reuses its auxiliary WITHOUT acquiring or reconstructing spectator information. It does not solve that theorem's observer-origin obligation.

The uniform eight-edit schedule need not be shortest: hidden slack may permit a six-edit route in the inherited special family. No optimality or uniqueness is claimed.

## 5. Sharp boundaries and rejecting controls
Dropping initial lower protection admits spectators shared by root4 and a triangle root, or shared by all triangle roots; the explicit two-covers in section1 reject those states. Individual floors and a fresh marker alone do not supply lower protection.
Changing spectator incidences during execution can destroy the separation and is outside this theorem. Unknown additional core incidences, different root skeletons and goal labels outside the specified pool require new arguments. Reserved-marker freshness is required; no existence of a free palette label is derived.

## 6. Bounded verification and scientific status
The prospective domain has two labelled spectators with all 16^2 occurrence-mask assignments and three initial apexes. It checks exact source classification, all 384 protected one-exchange paths and all 768 two-exchange words, reconstructing entire canonical identities independently. The arbitrary-palette and arbitrary-length claims follow from the arguments above, not from those finite checks.
No independent acceptance or publication closeout is claimed by this candidate. Path A remains active. Broader C3 record generation, accessibility, enforcement and progress remain OPEN; this only advances the expressly bounded original C3/C4 repair obligations. No force, geometry, physical clock, dark-matter variable or GR derivation is introduced.
