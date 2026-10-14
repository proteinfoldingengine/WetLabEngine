# Exponential response: operational realization and retained success records

Date: 2026-10-14 UTC. Inspected parent: `912fc7607cddd1583bb4bc80fe9c16f2e43ff331`.

**Disposition: a noncentral fixed exponential tilt has no exact realization by one fixed quantum-instrument branch on every faithful input; commuting inputs admit a conditional filter; native action and success-record access remain open.** This is a bounded operational interpretation test of the inherited PGRL response family. It preserves that family's mathematical state curves and conditional response results. It neither selects a source law nor requires every future native interaction to implement this universal interface.

The useful distinction is between a valid state-valued formula, a physical operation applied to an unknown input, and a conditional state accessible after an actual retained outcome. The proof below separates all three. The positive commuting control also identifies exactly where a source contrast can appear and which record must accompany it.

## 1. Candidate and immutable source scope

The previous operational-source assessment found that v15.54 supplies its probability table independently of its listed permutations. This investigation turns to a different inherited candidate that does contain an explicit state-response formula:

\[
T_K(\rho)=\frac{\exp(\log\rho+K)}{\operatorname{Tr}\exp(\log\rho+K)},
\qquad K=sP=K^\dagger.                                      \tag{1}
\]

The input is a faithful density operator on a finite-dimensional complex Hilbert space. K is a fixed dimensionless source/deformation operator. The parameter s is not physical duration, and P is not identified here as a Hamiltonian or a native physical source.

The actual source descriptions already impose important limits:

| Inspected source | Established use of the formula | Boundary preserved here |
|---|---|---|
| v13.04, section 1 | Local response in a source/deformation coordinate at a supplied faithful state | Does not supply baseline-state origin or a refinement law |
| v13.11, sections 1–2 and 6 | Conditional BKM, polar and holonomy derivatives; first-order linearity in the source | Explicitly kinematic and dependent on the full state; not autonomous physical evolution |
| v13.22 | Exact tensor refinement naturality under P to P tensor I | Composes supplied states and sources; does not select a refinement or an event |
| v15.07 report and `_pgrl_state` | Computes log(base)+s*generator, exponentiates and trace-normalizes | Receives the complete base matrix, generator and strength; returns a computed state, not an instrument outcome |
| v15.08 | Preserves the canonical centered-log information generator while stopping its unearned physical-source identification | The stopped source-selection question is not reopened |

In particular, `_neutral_to_state_endpoint_controls` constructs a target-dependent generator from the full target density matrix and evaluates (1) at the supplied neutral reference. This verifies a conditional endpoint identity. It does not build an apparatus that receives an arbitrary unknown input and realizes (1). `_source_identification_boundary` supplies three source functions at the same product state and checks their resulting states; this is not a derivation of any physical source law.

The proposed reuse tested here is explicit: fix K and implement T_K exactly as the normalized output of one fixed, state-independent quantum operation on one input system. This is a stronger interface than the original supplied-state calculation promised. Failure of this proposed reuse is not a code defect or an invalidation of the original kinematic results. A justified restricted input family can still be sufficient for a native interaction.

## 2. Why valid output states do not establish an operation

For faithful rho and finite Hermitian K, (1) is positive definite and normalized. These facts are necessary for its output to be a density matrix. They do not establish linearity or complete positivity of an input-output operation.

Even within a commuting qubit family, a deterministic channel cannot implement a nontrivial tilt. Take

\[
K=\operatorname{diag}(\log 3,0),\qquad
\rho_p=\operatorname{diag}(p,1-p),\quad 0<p<1.
\]

The first output population is f(p)=3p/(1+2p). Thus

\[
f(1/4)=1/2,\quad f(3/4)=9/10,\quad f(1/2)=3/4,
\]

whereas the equally weighted average of the first two output populations is 7/10. The discrepancy is exactly 1/20. Every state in this control is faithful; the input midpoint is exactly the average of the two inputs. A fixed deterministic quantum channel is affine on this mixture and cannot give those three outputs.

This observation alone does NOT rule out postselection: normalization by a state-dependent success probability can make the conditional state nonlinear. The next proof includes that possibility instead of treating nonlinearity as a universal prohibition.

## 3. Exact all-input instrument-branch obstruction

**Proposition.** In finite dimension d>=2, let K be fixed and Hermitian. There exists a nonzero fixed completely positive, trace-nonincreasing linear map E such that

\[
\frac{E(\rho)}{\operatorname{Tr}E(\rho)}=T_K(\rho)
\quad\hbox{for every faithful density operator }\rho          \tag{2}
\]

if and only if K is scalar. Success is required to have positive probability for every such input. A nonzero CP map automatically has this positivity on faithful inputs. The scalar case is T_K(rho)=rho and is realized by the identity operation.

E may have any finite Kraus representation, not just one filter. Its branch may aggregate several outcomes or include fixed ancillas and outcome-dependent processing. Those resources are covered insofar as the resulting branch is one fixed CP map on one unknown input. The proposition does not cover a controller supplied with the input's classical matrix description, additional copies, a changing K(rho), approximation, or a restricted input family. It is a conditional quantum-operation test, not an axiom that the native theory must be quantum.

### Step 1: diagonal inputs determine the population action

Choose an orthonormal eigenbasis of K, with K=sum_i k_i Q_i and Q_i=|i><i|. Repeated eigenvalues are allowed. For 0<epsilon<1, define faithful diagonal states

\[
\rho_{i,\epsilon}=(1-\epsilon)Q_i+\epsilon I/d.
\]

The explicit commuting formula gives T_K(rho_(i,epsilon)) to Q_i as epsilon tends to zero. Rewrite (2) without dividing by the success probability and use continuity of the fixed linear map E. It follows that

\[
E(Q_i)=c_i Q_i,\qquad c_i=\operatorname{Tr}E(Q_i)\geq0.        \tag{3}
\]

This argument allows c_i=0 at this stage; no success assumption has been imposed on a rank-deficient boundary input. At I/d, however,

\[
\frac{\sum_i c_i Q_i}{\sum_i c_i}
 =\frac{\sum_i e^{k_i}Q_i}{\sum_i e^{k_i}}.
\]

Since E is nonzero and CP, the denominator on the left is positive. Therefore

\[
c_i=c e^{k_i}\quad\hbox{for one }c>0\hbox{ and every }i.       \tag{4}
\]

### Step 2: complete positivity forces diagonal Kraus operators

Write E(X)=sum_l A_l X A_l^dagger. Equation (3) says that the sum of the positive rank-one operators |A_l i><A_l i| is supported on the one-dimensional span of |i>. Every vector A_l|i> must therefore belong to that span. This holds for every i, so every A_l is diagonal in the chosen eigenbasis of K.

Consequently, for every matrix rho,

\[
E(\rho)_{ii}=c_i\rho_{ii}.
\]

For any input with all diagonal entries 1/d, the ratio of output populations i and j must then be

\[
\frac{E(\rho)_{ii}}{E(\rho)_{jj}}=e^{k_i-k_j}.                 \tag{5}
\]

Normalizing the output does not change this ratio.

### Step 3: one faithful coherent input contradicts that ratio

If K is not scalar, choose i,j with k_i>k_j and set

\[
\delta=(k_i-k_j)/2>0,\qquad
\rho_r=\frac{I+r(|i\rangle\langle j|+|j\rangle\langle i|)}{d},
\quad 0<r<1.
\]

Its eigenvalues are (1+r)/d, (1-r)/d, and 1/d on the other d-2 basis directions, so it is a faithful density operator with the required constant diagonal. On the i,j block,

\[
\log\rho_r+K=bI+uX+\delta Z,
\quad u=\operatorname{artanh}r>0,
\quad R=\sqrt{u^2+\delta^2}>\delta,
\]

where b is a scalar that cancels from the population ratio. Since (uX+delta Z)^2=R^2 I, exponentiation gives

\[
\frac{T_K(\rho_r)_{ii}}{T_K(\rho_r)_{jj}}
 =\frac{1+(\delta/R)\tanh R}{1-(\delta/R)\tanh R}.              \tag{6}
\]

For x>0, g(x)=tanh(x)/x is strictly decreasing: its derivative has the sign of x-sinh(x)cosh(x), which is negative because sinh(2x)>2x. Hence

\[
0<\frac{\delta}{R}\tanh R<\tanh\delta.
\]

The ratio in (6) is strictly less than

\[
\frac{1+\tanh\delta}{1-\tanh\delta}=e^{2\delta}=e^{k_i-k_j},
\]

contradicting (5). This proves the proposition. It uses exact finite-dimensional algebra and a simple diagonal-state limit; no scientific computation or approximate numerical threshold is involved.

The result excludes both an exact deterministic channel and an exact fixed postselected instrument branch on the full faithful input domain. It does not merely show that a particular guessed filter fails. Conversely, it must not be read as saying that none of the individual states T_K(rho) can be prepared.

## 4. Positive restricted-domain realization

Let k_max be the largest eigenvalue of K and choose the fixed success operator

\[
A_{\rm s}=e^{(K-k_{\max}I)/2}.
\]

Its effect satisfies 0<A_s^dagger A_s<=I. The failure operator

\[
A_{\rm f}=\sqrt{I-A_{\rm s}^\dagger A_{\rm s}}
\]

completes a valid two-outcome instrument. For every faithful input that commutes with K,

\[
\frac{A_{\rm s}\rho A_{\rm s}^\dagger}
     {\operatorname{Tr}(A_{\rm s}\rho A_{\rm s}^\dagger)}
 = T_K(\rho),\qquad
p_{\rm s}(\rho)=e^{-k_{\max}}\operatorname{Tr}(e^K\rho).        \tag{7}
\]

This includes coherence within degenerate K eigenspaces; the condition is [rho,K]=0, not diagonal entries in one specially chosen basis. For general noncommuting inputs the normalized sandwich is a different map. The preceding proposition shows that changing to a more complicated fixed instrument cannot repair agreement on ALL faithful inputs.

In the rational population control of section 2, A_s=diag(1,1/sqrt(3)) and p_s(rho_p)=(1+2p)/3. Conditioning the midpoint mixture weights its components by these different success probabilities, resolving the apparent conflict with affine unnormalized quantum operations. Nonlinearity of a conditional state is legitimate when the underlying instrument and its outcome probabilities are specified.

The chosen filter is an existence control, not a native derivation or a unique instrument. A single known baseline is an even weaker problem: with a classical description of its target output, a replacement channel can prepare that output. Such a preparation supplies its resource and state knowledge separately; it does not establish the universal interface (2) or native acquisition.

## 5. Where an accessible consequence would reside

The commuting control makes the record obligation explicit. Supply two qubits A,B, a common Z reference, and faithful preparations

\[
\rho_\pm=\frac{I_{AB}\pm\epsilon Z_A\otimes Z_B}{4},
\qquad 0<\epsilon<1.
\]

Both individual marginals are I/2. The sign is initially a joint correlation, absent from B alone. Use the same fixed source for both preparations,

\[
K=h Z_A\otimes I_B,\qquad h>0,
\]

and the local success/failure operators from (7), acting on A. These input states commute with K, so the success branch exactly realizes (1). Write t=tanh h. Direct multiplication and normalization give

\[
\rho_{\pm\mid{\rm s}}
 =\frac{I+t Z_A\otimes I_B
          \pm\epsilon Z_A\otimes Z_B
          \pm\epsilon t I_A\otimes Z_B}{4},
\]

and therefore

\[
\rho^B_{\pm\mid{\rm s}}=\frac{I_B\pm\epsilon t Z_B}{2},
\qquad
D(\rho^B_{+\mid{\rm s}},\rho^B_{-\mid{\rm s}})
 =\epsilon\tanh h>0.                                         \tag{8}
\]

Here D is one half the trace norm. With an available Z_B measurement, b in {+1,-1} has conditional law

\[
\Pr(b\mid\pm,{\rm s})=(1\pm b\epsilon\tanh h)/2.              \tag{9}
\]

This is a statistical contrast, not perfect single-event decoding: both outcomes have positive probability for both faithful preparations.

The success probability is identical for the two signs,

\[
p_{\rm s}=e^{-h}\cosh h=(1+e^{-2h})/2,
\]

so the flag alone reveals no sign. On failure the B marginal is

\[
\rho^B_{\pm\mid{\rm f}}=(I_B\mp\epsilon Z_B)/2.
\]

Since p_s tanh h=1-p_s, discarding the flag gives exactly

\[
p_{\rm s}\rho^B_{\pm\mid{\rm s}}
 +(1-p_{\rm s})\rho^B_{\pm\mid{\rm f}}=I_B/2.                 \tag{10}
\]

Thus a B-only observer with no success/failure association has no changed one-shot marginal. The accessible contrast in (9) needs the actual success record associated with the B outcome, or a justified joint flag-and-B interface. If records are separated, their association needs its own available link. This is consistent with the unchanged B marginal of any trace-preserving local instrument when its outcome is ignored.

The epsilon=0 control removes the source distinction, and h=0 removes the filtering contrast. At h=0 success is certain, so a failure-conditioned state is undefined. Neither control is needed for the all-input obstruction; they check the conditional readout formula. No across-run independence, repetition protocol, error rate or guaranteed success is assumed. The qubits, preparation, frames, filter application, event flag, association and retention are supplied in this control. It is not the sought native mechanism or an unconditional remote force.

## 6. Relation to the earlier results and scientific decision

The original quantum-to-geometry calculations differentiate a supplied state family. They can remain mathematically valid even though that family is not a universal quantum instrument acting on unknown states. v13.22 tensor naturality is likewise an identity between supplied families, not a derivation of an operational implementation. The canonical centered-log object and v15.08 source-semantics stop are unchanged. No new spectral source selector is proposed.

The prior finite-interaction witness used a different, explicitly supplied unitary action and moved a hidden correlation into retained pair data. It is not ruled out by this proposition. Nor are the recent instrument, complementary-record and partial-access results invalidated: they apply once their actual channels, source binding and accessible outputs are specified. Equation (1) does not automatically provide those premises.

| Inference being assessed | Disposition |
|---|---|
| Equation (1) defines valid faithful output states | Yes |
| Positivity and normalization establish a fixed deterministic operation | No; the exact mixture control already rejects this |
| A noncentral fixed K can be implemented by one fixed instrument branch on all faithful inputs | Excluded by the proposition |
| Restricted commuting inputs permit an actual quantum realization | Yes; the supplied filter and its success probabilities give one |
| A conditioned source contrast is automatically available at B | No; the success record and its association are essential in the control |
| Every native mechanism must implement the full all-input map | No; that is only the proposed interface tested here |

**Disposition code: UNIVERSAL_EXPONENTIAL_INSTRUMENT_EXCLUDED; COMMUTING_FILTER_REALIZATION_CONDITIONAL; NATIVE_ACTION_AND_FLAG_ACCESS_OPEN.**

This is a concrete operational boundary and a positive restricted-domain realization. It advances the interpretation of this candidate beyond checking that its output is a density matrix. The proposition is proved here as a scoped mathematical result; no claim of literature priority, a new general physical theorem, or a discovered force is made. The exponential/inference distinction and quantum filtering framework have established prior art.

For this route the next eligible candidate must first justify its actual input class and operational resources from native premises. A commuting family is sufficient for the control but must be earned, as must the filter or another allowed operation, source/reference binding, occurrence, retained success record and available readout. A justified restricted native process can qualify without satisfying the universal proposition's domain, selecting one deterministic outcome, fixing every microscopic detail, guaranteeing completion, or closing C3 and gravity first.

Do not replace a physical update by evaluation of (1) on a full matrix available only to an external calculation. Do not supply the commuting promise or success record by fiat. State-aware preparation, additional copies, restricted processes and nonquantum alternatives remain distinct possibilities with separate resource obligations, not impossibility claims.

Native milestone: **NOT ACHIEVED**. The negative claim is restricted to (2), and the missing-premise assessment to the inspected sources and explicit control. Path A remains active, Path B closed, and time remains pruning / ordered recoverability update. No new physical primitive, entropy objective, geometry, dark-matter variable, energy scale or gravity-targeted selection is adopted.

No scientific source module was imported or executed, no numerical campaign or historical replay was performed, and no scientific test count was increased. All controls above are exposed analytical calculations, not prospective unseen experiments. Text/hash/source-publication checks establish provenance only. No main merge or numbered-stage CLOSED/CERTIFIED status is claimed.

## 7. Provenance, prior mathematical context and review

Twelve complete repository sources at the pinned parent are preserved in `source_packet.json` with independently recomputable identities in `source_identities.json`. This is a bounded inventory, not an archive-wide absence audit. Historical certification terminology inside original sources remains historical; it does not certify this investigation.

Primary context consulted 2026-10-14:

- Manfred K. Warmuth and Dima Kuzmin, *Bayesian generalized probability calculus for density matrices*, Machine Learning 78, 63–101 (2010), DOI 10.1007/s10994-009-5133-7; sections 1, 9 and 11. The paper develops normalized log/exponential inference updates and explicitly distinguishes that calculus from a physical quantum evolution interpretation. It supplies prior context, not the proof of the exact CP-branch proposition above. Author repository: https://escholarship.org/content/qt4hx9r95h/qt4hx9r95h.pdf . No inferential entropy principle from that work is adopted as native physics here.
- John Watrous, *The Theory of Quantum Information*, chapter 2, on channels, Kraus representations and instruments: https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf . These standard operational definitions specify the tested quantum interface; they do not derive a quantum carrier for the native research program.

Independent whole-argument review and a separate source/publication audit accompany this record. Their scopes are the exposed argument, source boundaries and immutable publication, not empirical validation or native physical closure.
