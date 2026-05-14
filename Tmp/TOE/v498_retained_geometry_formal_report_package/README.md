# V498 Retained-Geometry Formal Report Package

Included files:

- `V498_FORMAL_RETAINED_GEOMETRY_REPORT.md`
- `v498_retained_geometry_proof.py`
- `V498_GROK_UPDATE.md`

Run:

```bash
pip install networkx scikit-learn pandas matplotlib
python v498_retained_geometry_proof.py
```

Outputs:

- `v498_outputs/v498_summary.csv`
- `v498_outputs/v498_summary.json`
- `v498_outputs/*.png`

Main law:

\[
C_t = M_tR_tL_t + \lambda_0\eta_{\mathrm{convert}}B_t
\]

\[
\partial_t g_{\mathrm{eff}}
=
G_L * \left[
T_{\mathrm{retained}}/(C_t-C_{\mathrm{floor}}+\epsilon)
\right]
-
R_{\mathrm{repair}}
-
D_{\mathrm{leakage}}
\]

\[
K_{\mathrm{eff}}=\mathrm{Curv}(g_{\mathrm{eff}})
\]
