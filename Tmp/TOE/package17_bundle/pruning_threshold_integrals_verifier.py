
"""
pruning_threshold_integrals_verifier.py

Verifier for PRUNING_THRESHOLD_INTEGRALS.md.

Goal:
Evaluate the slow/fast retained-memory input integrals:

    I_s = E[|xi|]
    I_f(eps*) = E[|xi| Theta(|xi|-eps*)]

for assumed noise laws.

Primary case:
    xi ~ N(0, sigma^2)

Closed forms:
    I_s = sigma sqrt(2/pi)
    I_f = sigma sqrt(2/pi) exp(-eps*^2/(2 sigma^2))

Thus:
    I_f/I_s = exp(-eps*^2/(2 sigma^2))

Checks:
    - analytic vs Monte Carlo match
    - I_f <= I_s
    - monotone decreasing in eps*
    - target chi condition can be rewritten with explicit I_f(eps*)
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from math import sqrt, pi, exp


@dataclass(frozen=True)
class IntegralConfig:
    sigma: float = 1.0
    eps_star: float = 0.5
    n_samples: int = 200000
    seed: int = 1801


@dataclass(frozen=True)
class IntegralResult:
    I_s_analytic: float
    I_f_analytic: float
    ratio_analytic: float
    I_s_mc: float
    I_f_mc: float
    rel_err_s: float
    rel_err_f: float
    monotone: bool
    stable: bool


def analytic_integrals(sigma, eps):
    I_s = sigma * sqrt(2.0/pi)
    I_f = sigma * sqrt(2.0/pi) * exp(-(eps**2)/(2*sigma**2))
    return I_s, I_f, I_f/I_s


def monte_carlo(cfg):
    rng = np.random.default_rng(cfg.seed)
    xi = rng.normal(0.0, cfg.sigma, size=cfg.n_samples)
    absx = np.abs(xi)
    I_s = float(np.mean(absx))
    I_f = float(np.mean(absx * (absx >= cfg.eps_star)))
    return I_s, I_f


def verify(cfg):
    Is_a, If_a, ratio = analytic_integrals(cfg.sigma, cfg.eps_star)
    Is_m, If_m = monte_carlo(cfg)

    rel_s = abs(Is_m - Is_a)/(abs(Is_a)+1e-12)
    rel_f = abs(If_m - If_a)/(abs(If_a)+1e-12)

    eps_grid = np.linspace(0, 5*cfg.sigma, 200)
    If_vals = np.array([analytic_integrals(cfg.sigma, e)[1] for e in eps_grid])
    monotone = bool(np.all(np.diff(If_vals) <= 1e-12))

    stable = bool(
        cfg.sigma > 0
        and 0 <= If_a <= Is_a
        and 0 <= ratio <= 1
        and rel_s < 0.01
        and rel_f < 0.03
        and monotone
    )

    return IntegralResult(Is_a, If_a, ratio, Is_m, If_m, rel_s, rel_f, monotone, stable)


def classify(cfg):
    r = verify(cfg)
    if not np.isfinite([r.I_s_analytic, r.I_f_analytic, r.I_s_mc, r.I_f_mc]).all():
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=200, seed=1807):
    rng = np.random.default_rng(seed)
    counts = {"PASS":0, "SOFT_FAIL":0, "HARD_FAIL":0}
    vals = {k: [] for k in [
        "I_s_analytic","I_f_analytic","ratio_analytic",
        "rel_err_s","rel_err_f"
    ]}
    for _ in range(n_sweeps):
        sigma = float(10**rng.uniform(-1, 1))
        eps = float(rng.uniform(0, 4*sigma))
        cfg = IntegralConfig(sigma=sigma, eps_star=eps, n_samples=100000, seed=int(rng.integers(0, 10_000_000)))
        label, r = classify(cfg)
        counts[label] += 1
        if label in {"PASS","SOFT_FAIL"}:
            for k in vals:
                vals[k].append(getattr(r, k))
    out = {k:100*v/n_sweeps for k,v in counts.items()}
    for k, arr in vals.items():
        if arr:
            out[k+"_median"] = float(np.nanmedian(arr))
    return out


def main():
    print("Pruning threshold integrals verifier")
    print("="*50)
    print("Route:")
    print("Gaussian noise -> I_s and I_f(eps*) closed forms")
    print()
    for k,v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
