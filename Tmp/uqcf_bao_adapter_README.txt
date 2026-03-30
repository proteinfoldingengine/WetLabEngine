
Files created:
- uqcf_lattice_hz_adapter.py
- run_uqcf_bao_with_adapter.py

What these do:
- uqcf_lattice_hz_adapter.py defines a transparent effective bridge from fixed
  low-regime lattice parameters to H(z).
- run_uqcf_bao_with_adapter.py plugs that bridge into the DESI DR2 BAO blind-test module.

Important:
- This is an EFFECTIVE bridge for testing, not a claimed first-principles derivation.
- The goal is to let you run a fixed-parameter BAO audit immediately and then improve
  the mapping later if deeper derivation work succeeds.
