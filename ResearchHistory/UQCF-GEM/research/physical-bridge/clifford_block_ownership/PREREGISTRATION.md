# Prospective verification contract

Parent: 1a18308a026c06882b428fbe201b4634c34dfd8f. Existing accepted input document: 4a57f4d52025fc4dc1e1302352b3d9fdbf311ea2.

Disclosure: the analytical argument and identities in ARGUMENT.md were worked out before this freeze. They are not preregistered discoveries. No new scientific computation has run. This contract prospectively fixes the finite verification and review.

Primary claim: the frozen block rotation algebras are commuting M2 factors, while the vector effects require a common M2 commutant; the rho(r) family has tracial restrictions on every local factor before and after all reviewed Spin(9) actions. General scope rests on the proof, not finite checks.

Finite verification universe: the specified nine four-qubit Pauli strings; all nine L generators, all three Omega operators; all 3*3*3=27 within-block ordered products (including equal indices); all 3*3*3=27 cross-block generator commutators for unordered pairs of blocks; 9 Omega-L factorization identities; all 9*9=81 traces Tr(gamma_i L_j); the 64 products obtained by selecting I or one of three L generators in each of three blocks, with all 64*64 Gram entries; all nine Omega versus block-generator commutators for each Omega (27); three Omega-pair anticommutators.

Producer: exact integer-phase Pauli-string multiplication. Independent checker: reconstruct all operators and the full expected record universe using exact SymPy Kronecker matrices; no producer imports. Check full identity equality, not counts alone.
Rejecting controls: missing, duplicated, substituted record; wrong Pauli value; wrong phase; invalid word; false source binding; false count. Preserve rejection outputs.
No numerical state/orbit sweep. Positivity, all-r traces and all-X action follow analytically from frozen source and proof.
Run inherited foundational tests, historical parent tests, certificate producer and independent verifier with pinned dependencies. Preserve logs and failed runs.
One independent Gemini whole-argument review after successful verification. Preserve raw request/response/model metadata, verdict and hashes. REVISE/FAIL is not acceptance.
Publication: reproduce deterministic records/checker outputs independently, validate raw review parsing and immutable GitHub source reads. Retain artifacts and durable raw archives with checksums.
Stop after this bounded check. No new coupling, representation or receiver-selection campaign; no merge or physical upgrade is authorized by this verification.
