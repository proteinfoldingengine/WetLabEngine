# v15.44: exact intrinsic curvature-response characterization

This additive demonstration derives the complete rational map from scalar
fields on each of four inherited finite carriers to the four row-major entries
of each based face-curvature matrix. It independently evaluates the frozen
transport/holonomy on every basis field, certifies rational rank, kernel,
image and orthogonal projector, checks full presentation controls, and
compares every archived response field and canonical-control pair. The
operator acts on all \(\mathbb Q^{L^2}\); the known archived fields are centered.

The four carriers are L=5 and L=7 at work scales 1 and 7/3. The finite
certificate records the observed rank and nullity for each, its full matrix,
every row operation, complete kernel and image bases, and exact verification
receipts in [RESULTS.json](docs/RESULTS.json). There are 740 archived fields,
592 paired canonical-control comparisons, and 370 matched scale pairs.
Earlier nonzero outcomes and L7 exposure were known; this is not a fresh
holdout or an inference of a family winner. The exact derivation and the
boundary between algebraic proof and finite calculation are in
[DERIVATION.md](docs/DERIVATION.md).

With CPython 3.13.5, run from this directory:

```bash
/root/.local/bin/python3.13 -m unittest -v test_evidence test_exact_matrix test_operator test_kernel test_presentations test_compare test_gate
/root/.local/bin/python3.13 -I gate.py --out docs/RESULTS.json
/root/.local/bin/python3.13 -I gate.py --check docs/RESULTS.json
/root/.local/bin/python3.13 -m compileall -q .
```

The coordinator checks pinned parent evidence, reconstructs geometry before
the pure algebra access guard, seals the derived operators and independently
replayed certificates, then reads the archive only in a later comparison
process. Four full presentation controls run in isolated processes. Each
stage fails closed and records only accepted work; the canonical ledger has
no timing, host, or cost metadata. Successful replay checks byte identity.

The interpretation applies only to these four carriers and these frozen
fields. Scale pairs are matched dependencies, not independent samples. The
carrier and scalar-lift rules are inherited assumptions. Source
correspondence is NOT_EVALUATED; physical curvature, gravity, spacetime,
Einstein equations, continuum behavior, foundational uniqueness, and a
scientific breakthrough are not established. Pillar 3 remains OPEN. The next
unresolved scientific question is whether an independently specified source
correspondence can be tested without fitting the geometric response to its
target.
