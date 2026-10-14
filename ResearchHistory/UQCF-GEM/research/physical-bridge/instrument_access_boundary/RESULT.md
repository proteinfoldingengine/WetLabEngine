# What a supplied pinching action forces about a record

Date: 2026-10-14 UTC. Inspected parent: `b498bb1e4e610cfc68c0b630db75498029c002fe`.

**Disposition: exact conditional instrument classification; native record access unresolved.** This analytical note classifies the classical outcome information compatible with the existing pinching action. It strengthens the inherited two-instrument control to an all-instrument statement in a specified finite scope. It is an application of standard completely positive map machinery, with no mathematical novelty-priority claim, new physical axiom, numerical campaign, or numbered-stage certification.

The question is whether the existing retained action itself forces an accessible consequence, even when its implementation is not unique. Nonuniqueness alone would not defeat that possibility: different implementations could share an informative output law. Here the complete classification shows exactly what is shared and what is not.

## 1. Fixed premises and the interface being classified

Supply a finite-dimensional complex Hilbert space H and nonzero mutually orthogonal projections P_1,...,P_n resolving I. Fix the channel

    E(X) = sum_i P_i X P_i.

Its retained algebra is the full block algebra A = direct_sum_i B(P_i H). These are the sharp pinching objects in the v15.11 implementation. The result does not cover every trace-preserving expectation onto a general finite-dimensional subalgebra with multiplicities, every changing-carrier map, or arbitrary nonlinear event dynamics.

A finite-outcome instrument compatible with E means CP linear maps J_r on B(H) such that sum_r J_r = E on EVERY matrix X. The output carrier H is fixed. Trace nonincrease of each branch follows from positivity and the trace-preserving sum. The associated classical label law, if this instrument is applied and its label is made accessible, is

    Pr(r | rho) = Tr J_r(rho).

An instrument is a mathematical specification of branches and probabilities. Its existence does not prove physical implementation, application, outcome actuality, retention, or delivery to another event. No such step is assumed in the conclusion.

This classification differs from v15.23. That source fixes an entire sharp instrument and classifies PREPROCESSORS preserving all its branches. We instead fix only its possible nonselective pinching action and classify INSTRUMENTS summing to that action. Mixing these two interfaces would silently supply the record we are trying to explain.

## 2. Complete classification of the instrument freedom

**Proposition.** Every compatible instrument, and only such an instrument, has the unique form

    J_r(X) = sum_(i,j) C^(r)_ij P_i X P_j,
    C^(r) >= 0,                 sum_r C^(r) = I_n.

Thus the remaining coefficients form a finite POVM on the n-dimensional coefficient space. That space is a mathematical parameter space; it is not an independently justified physical environment or native event carrier.

**Necessity.** Use an unnormalized Choi convention for which the map X -> K X K^dagger has Choi matrix |K>><<K|. Let V be the matrix whose ith column is |P_i>>. Nonzero orthogonal projections are Hilbert-Schmidt orthogonal, so V has full column rank even when their ranks differ. Then

    J_Choi(E) = V V^dagger.

Write B_r = J_Choi(J_r). Complete positivity and the sum imply 0 <= B_r <= V V^dagger. If v lies in the kernel of V V^dagger, then 0 <= <v,B_r v> <= 0; positivity implies B_r v=0. Therefore B_r is supported on range(V). Put L=(V^dagger V)^(-1)V^dagger. The unique coefficients are

    C^(r) = L B_r L^dagger >= 0,
    B_r = V C^(r) V^dagger,
    sum_r C^(r) = L V V^dagger L^dagger = I_n.

The Choi correspondence gives the displayed branch formula. No equal-rank normalization was used.

**Sufficiency.** Factor each positive C^(r) as a sum of vector outer products. A vector c supplies the Kraus operator K_c=sum_i c_i P_i. These operators give the branch formula and complete positivity. Summing the coefficient matrices to I_n leaves exactly E. Uniqueness follows because V has full column rank. This proves the full finite class, without a numerical sweep.

## 3. Exact classical information ceiling and zero guaranteed floor

Taking the trace removes the off-diagonal terms because P_j P_i=0 for i!=j. Define the sector-weight vector and stochastic matrix

    w_i(rho) = Tr(P_i rho),        T_ri = C^(r)_ii.

Then T_ri>=0, sum_r T_ri=1, and

    Pr(r | rho) = sum_i T_ri w_i(rho).

Conversely EVERY finite column-stochastic T is possible: choose C^(r)=diag(T_r1,...,T_rn). Therefore the possible classical label laws are exactly all stochastic processing of the supplied sector weights. This statement concerns probabilities only. The complete quantum branches need not be stochastic mixtures of P_i X P_i, since allowed C^(r) may have off-diagonal entries.

For two input states rho and sigma, let TV denote half the sum of absolute differences of classical probabilities. Over all compatible finite-outcome instruments,

    0 <= TV(p(rho),p(sigma)) <= (1/2) sum_i |w_i(rho)-w_i(sigma)|.

The upper bound follows directly from the triangle inequality and the column sums of T. It is attained by the sector instrument J_i(X)=P_i X P_i. The lower bound zero is attained by any input-independent label law, for example C^(r)=alpha_r I_n with fixed probabilities alpha_r. Hence the exact infimum is zero and the exact supremum is the sector-weight distance. For n>=2 the uninformative law may have multiple nonzero labels; the conclusion does not depend on allowing a single dummy outcome.

Two consequences locate the boundary:

- Equal sector weights imply identical label distributions for EVERY compatible instrument, even if the input states differ within sectors or in coherences between them. This is a theorem about the classical label alone, not every joint quantum output or reference.
- Different sector weights permit an informative label, but pinching alone guarantees no positive label distinction. The counterexample alpha_r E retains the same channel, retained algebra, and channel-level loss. No absence of pinching or lack of occurrence is needed for this conditional counterexample.

One may assume the operation occurs for this comparison and still obtain a completely uninformative accessible label. Conversely, if direct access to the system algebra A was already justified, its surviving distinctions remain available there: Tr(a E(rho))=Tr(a rho) for every a in A. Such preservation is not the creation or delivery of a new record. We do not infer universal inaccessibility from a bound on one interface.

## 4. What an exact sector-record requirement WOULD force

There is a useful positive conditional result. Suppose the outcomes are labelled 1,...,n and impose the additional, all-input requirement

    J_i(X) = P_i J_i(X) P_i             for every positive X.

This says that a label i reliably accompanies an output in sector i. It is stronger than merely adding an outcome label, or observing one state already confined to a sector. It is an operational record-correlation requirement, not a consequence of E alone.

Take a normalized input supported in sector j!=i. The general formula gives J_i(rho_j)=C^(i)_jj rho_j. The output-support requirement forces C^(i)_jj=0. Positivity gives |C^(i)_jk|^2<=C^(i)_jj C^(i)_kk, so every corresponding row and column vanishes. Only the ii entry remains, and sum_i C^(i)=I forces that entry to be one. Thus, uniquely,

    J_i(X) = P_i X P_i,
    Pr(i | rho) = Tr(P_i rho),
    rho_i = P_i rho P_i / Tr(P_i rho)    when the weight is positive.

Allowing several fine labels for the same exact sector adds classical splitting within that sector; after combining those labels the same J_i is forced. Nothing chooses an actual outcome or supplies the reader of it.

This recovers the branch formula used by RCR without selecting a branch index. It is not a derivation of the Born rule from bare information: the quantum carrier, complete positivity, trace probability rule, E, and exact sector correlation are explicit premises. Once these premises are earned, a probabilistic law is sufficient for a meaningful physical consequence; a unique microscopic outcome is not required by the research milestone.

## 5. Controls that prevent stronger readings

**Distinct uninformative branches.** For n>=2 label sectors i=0,...,n-1, let omega=exp(2 pi i/n), and set

    U_k = sum_i omega^(k i) P_i,
    J_k(X) = (1/n) U_k X U_k^dagger,     k=0,...,n-1.

Each U_k is unitary, and the finite roots-of-unity sum makes sum_k J_k=E. Every label has probability 1/n for every normalized input. This works for unequal block ranks. It generalizes the v15.11 binary projective-versus-random-unitary control; it is a countermodel, not a proposed native mechanism.

**Classical label versus joint access.** With the random-unitary instrument, retaining both k and the full conditional quantum output permits the controlled inverse U_k^dagger and exact input recovery. Label k by itself remains uninformative. With J_r=alpha_r E, retaining both label and system instead yields only alpha_r E(rho), so a pair erased by E remains erased even jointly. The same forgotten-label channel thus allows very different recovery properties for the enlarged output. Neither enlarged physical interface is adopted here.

**Actual loss need not produce a sector distinction.** In the binary rank-one case, rho_plus/minus=(I +/- X)/2 have equal sector weights and E(rho_plus)=E(rho_minus)=I/2. Every compatible classical label law is identical for the two inputs. The random-unitary joint output can nevertheless retain their distinction. The theorem does not turn retained loss into global destruction, or imply that every flag destroys phase information jointly with the system.

**Correct-sector labels are extra.** The random-unitary example violates the exact sector-output condition on coherent inputs and is therefore rejected by that condition. The sector instrument satisfies it. Selecting the latter because it gives a desired record would insert the mechanism unless the condition has an independent native justification.

**Degenerate one-sector case.** For n=1, E is identity and every compatible branch is alpha_r times identity. There is no channel loss and no input-dependent label. The formulas include this case without treating it as a pruning event.

All these are exact symbolic controls. No code from the scientific sources was executed, no sample size changed, and no new numerical evidence or preregistered holdout is claimed.

## 6. Consequence for the current discovery program

The previous record-compatibility result derives V(q) strictly inside V(p) from a SUPPLIED strict central record refinement q<p. It also identifies when excluded alternatives remain in other views. This note does not modify those proofs. It asks what precedes the supplied q: can the already specified nonselective action force an informative classical label?

In the pinching scope, the answer is bounded and exact. The channel restricts every label to stochastic information about sector weights, but supplies no positive lower bound on that information. A reliable sector-output association would force the usual selective instrument; the action E itself does not force that association. Even the forced selective instrument would still require application and justified access to its outcome interface. Refinement of a pre-existing record p would require its existing compatibility conditions as well.

This is a sharper location of the missing physical premise, not a new physical obstruction covering all possible informational theories. It does not disqualify changing-carrier mechanisms, derived interactions outside pinching, direct native retained-algebra access, or consequences shared by a nonunique family of dynamics. Nor does it make a deterministic selector, guaranteed progress, gravity, or the full C3 protocol a prerequisite for the user's milestone.

**Next admissible target:** identify previously justified native relational data that constrain the actual output interface enough to exclude input-independent label laws, then derive a nonzero accessible consequence on that interface. Exact sector correlation is one sufficient condition, not a required or minimal one. A weaker derived restriction on T could already force a statistical distinction for a specified native source pair. Merely naming q, stipulating a sector measurement, retaining a convenient dilation, or choosing T after seeing the desired signal does not meet that target.

Excluding input-independent label laws alone is insufficient for a specified source pair: a nonconstant T can still satisfy T(w(rho)-w(sigma))=0. Any candidate must establish separation for its actual native inputs under its justified output law or family, not merely show that the interface is informative about some inputs.

Until such evidence exists, further simulations of the instruments above add no native-origin evidence. The current advance is a complete conditional accounting of record freedom and a sufficient condition for its removal. The native informational-difference-to-accessible-consequence milestone remains **NOT ACHIEVED**. Time remains pruning / ordered recoverability update; no force, geometry, energy, or elapsed-time law is inferred.

## 7. Source and verification scope

Six exact repository inputs are bound in source_packet.json and source_identities.json: AGENTS.md; the v15.11 report and implementation; the v15.23 family report; the preceding record-compatibility result; and the continuation index. Source inspection preserves their conditional results and does not recertify historical numerical runs. The all-instrument proof and controls above are exposed analytical work, subject to independent review before publication.

Standard mathematical context: John Watrous, *The Theory of Quantum Information*, Chapter 2, Proposition 2.20 and Theorem 2.22, gives the Choi/Kraus correspondence and the equivalence between complete positivity and Choi positivity. The coefficient-support argument and its application to this research interface are written out here. Primary reference: https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.2.pdf (consulted 2026-10-14). This citation supports the mathematical machinery, not native quantum ontology or physical access.
