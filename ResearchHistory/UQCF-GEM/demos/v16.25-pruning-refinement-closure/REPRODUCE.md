# v16.25 reproduction

From repository root on Python 3.11:

    cd ResearchHistory/UQCF-GEM/demos/v16.25-pruning-refinement-closure
    python test_gate.py
    python engine.py
    python verify.py

Then run inherited regressions from .github/workflows/uqcf-v1625-pruning-refinement.yml.

Expected complete-universe values:
- refinements: 488307
- strict increases: 318719
- raw certificate SHA-256: 523c07b4d539b2512228457eb4c8216e15d87c17bd5df5582542c7a4c932e12b

General claims rest on TYPE_AND_PROOF.md; enumeration audits the implementation.
