# 16.16 — First-principles information-exhaust classification

## Frozen question

Starting only from the complete published 16.15 response records, classify what first-order distinctions survive after quotienting the *measured local invariant differential map*. Do not insert a metric, area, connection, curvature, embedding, alignment, threshold, fitted weight, or preferred geometric target.

For each of the 72 before/after order pairs, form two exact linear readout maps on the two-dimensional affine coefficient space spanned by [constant, coherence coefficient]:

- L: stack the 24 local scalar contrasts (six edges × Gram1, Gram2, Gram3, determinant);
- R: stack the seven closed-network total contrasts.

Compute exact ranks and nullspaces of L, R, and the stacked map [L;R]. The primary additionality test is whether rank([L;R]) > rank(L), equivalently whether R is nonzero on ker(L). This is stronger than 16.15's binary nonzero comparison but remains restricted to the frozen two-coefficient response family and measured local scalar set.

Also classify the normal-network map separately, but do not substitute it for the total physical response.

## Required outcomes

For every pair report rank(L), rank(R), rank([L;R]), dim ker(L), dim ker([L;R]), and whether the network adds a first-order quotient direction beyond L. Aggregate by identity/nonidentity, preparation arm and middle parameter.

Possible verdicts:

- NETWORK_ADDS_QUOTIENT_DIRECTION
- LOCAL_DIFFERENTIAL_SPANS_FROZEN_RESPONSE
- MIXED_INFORMATION_EXHAUST
- INVALID

A null result is final for this frozen response family. It must not be rescued by adding observables after measurement.

## Controls

Bind the exact 16.15 compressed result SHA256 3b3f5e075ef129640f135b76780544ea268bd22bbc2efb17cd4d3b3dbebe2b81 and publication commit 175debdf2944e1633d9ae87e5b121ffb511d3872. Reconstruct every contrast from archived before/after coefficients. Require complete 72-pair, 1728-local-record, 504-loop-record coverage. Verify identity-middle nulls and coherence-zero coefficients exactly. Use rational arithmetic only for adjudication.

## Interpretation firewall

This gate classifies information. It does not assume that the quotient is geometry. No area, metric, connection, curvature, source law, gravity law, Einstein/ADM object, fundamental time, dark-matter primitive, or external alignment may enter the implementation or interpretation.

Time remains pruning / ordered recoverability update.
