# Admission decision: v15.24 composition contracts do not force P1 receiver delivery

Date: 2026-11-01 (America/Phoenix).
Inspected research snapshot: 4620496534617a877e23dc0068369c4b98570903.
Disposition: DEPRIORITIZED at the typing/adversarial gate.
Evidence: source inspection and elementary analytical checks; no scientific execution, new model request or general certification.
Native bridge: NOT_DERIVED.

## Admission questions

1. Missing premise attacked: an inherited constraint on the full joint event that forces a source distinction into the designated R output.
2. Candidate primitive: v15.24's batch-retention, marginal-independence and independent-product composition contracts.
3. Adversary: W_E of the accepted P1 receiver-location result, with informative W_R as control.
4. Successful consequence: nonzero contrast on the same initially blind R for every allowed joint realization.
5. Falsifier: the contracts use supplied factors/instruments; the imported condition admits a blind realization, excludes the informative control, or is incompatible with the benchmark channel.

This is a bounded admission check, not a proposed new compositional dilation or coupling.

## Source operations and status

All paths here are relative to ResearchHistory/UQCF-GEM/ at the pinned snapshot.

- demos/v15.24-composition-gate/README.md §§1–3,6 and ontology boundary: the A/B factorization, ready instruments, prerequisites and outcome scripts are supplied. Batch retention, non-signalling and independent composition are distinct conditional contracts; none is adopted as a physical law or actual-event selector.
- composition_gate.py::local_effects extracts local projectors from the declared stream factors and checks their tensor forms. It does not derive the stream-to-native-owner correspondence.
- composition_gate.py::classify checks equalities of correlation-matrix entries for the two marginal-independence directions and tests C=C_A tensor C_B.
- composition_gate.py::no_signal_operator_error verifies adjoint marginal identities on matrix units for candidate maps; signalling_witness compares equal local inputs and different remote preparations.
- baseline/retention_family.py::apply computes Phi_c(X)=sum_ij c_ij Q_i X Q_j, with a complete orthogonal projector family and c_ii=1. batch constructs projectors and Kraus products for two already supplied ready events.

These are genuine joint-channel tests within their declared model. They are not just P1 pushforward identities. But importing their A/B factors as the P1 source/designated receiver, or importing the tests as laws of the actual event, would be SUPPLIED.

## First adversarial check: transport the marginal-independence condition

For this paragraph only, explicitly SUPPLY A=S and B=R and consider a full channel Lambda on S tensor R whose restriction to a blank receiver agrees with a candidate P1 event.

“No influence from S to R” means there is a receiver channel Lambda_R such that

    Tr_S Lambda(omega_SR) = Lambda_R(Tr_S omega_SR)

for every joint input. The benchmark inputs rho_plus tensor |0><0| and rho_minus tensor |0><0| have the same R input. The displayed condition therefore makes their R outputs equal.

Consequently W_R cannot satisfy this condition under any full-channel extension agreeing on the benchmark blank-input pair: its R contrast is 1/5. This is a mathematical marginal-independence statement, not a claim about spacetime locality or faster-than-light communication.

Conversely, the abstract channel Lambda=C tensor id_R is a countermodel to forcing delivery by generic independent-product composition or two-way marginal independence. It agrees with the source channel C, preserves the blank R, and is non-signalling in both directions. A dilation acting on S and E alone realizes the accepted W_E restriction. This supplied countermodel is used only to falsify the proposed implication; it is not proposed as native dynamics.

Generic transported-contract verdict: W_E admitted, W_R excluded by source-to-receiver marginal independence. Thus this is the wrong condition for forcing the requested receiver contrast. The reverse direction, “no R-to-S influence,” must not be confused with it; that condition alone is not a source-to-R delivery requirement.

## Second type check: do not identify the generic countermodel with the literal v15.24 family

The specific Phi_c preprocessor family is unital:

    Phi_c(I)=sum_i c_ii Q_i=sum_i Q_i=I.

In contrast the accepted coherent P1 benchmark channel, on H_S=span{o,p,u,v}, has

    C(I_S)=Q+pi_p=diag(1,2,0,1) != I_S,

where Q=I_S-pi_u and coordinates are ordered o,p,u,v.

This already prevents identifying the source-only C directly with a member of the same-space Phi_c family. More precisely, suppose a full Phi_c on S tensor R is non-signalling from R to S and its induced S channel is the benchmark C for the blank receiver. Non-signalling fixes that same local channel for every R input. For d_R=dim R, linearity and unitality then give

    C(I_S)=Tr_R Phi_c(I_S tensor I_R/d_R)=I_S,

a contradiction. Therefore the literal two-way-non-signalling v15.24 preprocessor subfamily cannot implement the required C under this supplied factor identification: neither benchmark realization qualifies through that route.

This is deliberately narrower than saying all v15.24 maps or every possible joint completion fail. Signalling members, downstream instruments, postselected branches, changed algebras, or different input/output identifications are different contracts and require their own source-backed typing. The generic blind countermodel C tensor id_R is not represented as a member of the unital v15.24 family.

## Decision and reopening criterion

The candidate fails before a numerical campaign:

- literal preprocessor-family plus marginal-independence identification: incompatible with the benchmark source channel;
- generic independent-product or two-way marginal-independence condition after dropping that family restriction: permits the blind product channel and rules out the informative control;
- actual event selection, factor ownership and the instrument-to-P1 association remain supplied.

No inherited condition eliminating W_E while retaining W_R was found here. No receiver-owned effect is newly earned. The older batch-retention and composition results remain valid within their original scope.

Reopen only on an exact inherited joint-event relation that supplies the relevant source/receiver typing and demonstrably changes the blind-realization verdict. Do not promote mathematical no-signalling to a native physical postulate, identify a scheduled instrument with the actual native event by name, or add a product coupling simply to obtain the desired response.
