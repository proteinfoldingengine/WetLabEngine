
"""
causal_adm_field_equation_proxy_verifier.py

Verifier for CAUSAL_ADM_FIELD_EQUATION_PROXY.md.

Goal:
Define and test a discrete field-equation proxy:

    E_ab^(k) = S_ab^(mem,k)

where E_ab^(k) is the finite-difference Euler response of the causal ADM proxy
with respect to h_ab^(k), and S_ab^(mem,k) is a controlled weak-memory source.

This is NOT Einstein's equation.
It tests whether:
    - Euler response is finite
    - memory source is finite
    - residual E - S_mem is finite
    - weak-memory scaling behaves as expected
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class FieldProxyConfig:
    n_slices: int = 9
    dim: int = 3
    eps: float = 1e-4
    eta_mem: float = 1e-2
    seed: int = 733


@dataclass(frozen=True)
class FieldProxyResult:
    euler_norm_median: float
    source_norm_median: float
    residual_norm_median: float
    source_to_euler_ratio: float
    weak_scaling_ratio: float
    finite_fraction: float
    stable: bool


def random_spd(rng, dim):
    A = rng.normal(size=(dim, dim))
    return A.T @ A + dim * np.eye(dim)


def make_slices(cfg):
    rng = np.random.default_rng(cfg.seed)
    hs, R3s, Ns = [], [], []
    for _ in range(cfg.n_slices):
        h = random_spd(rng, cfg.dim)
        if hs:
            h = 0.75 * hs[-1] + 0.25 * h
        hs.append(h)
        R3s.append(float(rng.uniform(-0.2, 0.8)))
        Ns.append(float(rng.uniform(0.85, 1.15)))
    return hs, np.asarray(R3s), np.asarray(Ns)


def action(hs, R3s, Ns):
    terms = []
    for k in range(1, len(hs)-1):
        hprev, h, hnext = hs[k-1], hs[k], hs[k+1]
        sign, logdet = np.linalg.slogdet(h)
        if sign <= 0:
            return np.nan
        vol = np.sqrt(np.exp(logdet))
        N = Ns[k]
        hdot = (hnext - hprev) / 2.0
        Kcov = 0.5 * hdot / max(N, 1e-12)
        hinv = np.linalg.inv(h)
        Kmixed = hinv @ Kcov
        K_trace = float(np.trace(Kmixed))
        K_ab_Kab = float(np.trace(Kmixed @ Kmixed))
        scalar = R3s[k] + K_ab_Kab - K_trace**2
        terms.append(N * vol * scalar)
    return float(np.sum(terms))


def finite_euler_response(hs, R3s, Ns, eps):
    dim = hs[0].shape[0]
    responses = []
    for k in range(1, len(hs)-1):
        Eab = np.zeros((dim, dim))
        for a in range(dim):
            for b in range(a, dim):
                B = np.zeros((dim, dim))
                B[a, b] = 1.0
                B[b, a] = 1.0
                hp = [x.copy() for x in hs]
                hm = [x.copy() for x in hs]
                hp[k] = hp[k] + eps * B
                hm[k] = hm[k] - eps * B
                # preserve SPD check
                if np.min(np.linalg.eigvalsh(hp[k])) <= 1e-10 or np.min(np.linalg.eigvalsh(hm[k])) <= 1e-10:
                    Eab[a, b] = np.nan
                    Eab[b, a] = np.nan
                    continue
                grad = (action(hp, R3s, Ns) - action(hm, R3s, Ns)) / (2 * eps)
                Eab[a, b] = grad
                Eab[b, a] = grad
        responses.append(Eab)
    return responses


def memory_source(hs, eta, seed):
    """Weak-memory spatial source proxy S_ab ~ eta * h_ab trace-normalized."""
    rng = np.random.default_rng(seed + 99)
    sources = []
    for h in hs[1:-1]:
        tr = np.trace(h) + 1e-12
        isotropic = h / tr
        noise = rng.normal(0, 0.05, size=h.shape)
        noise = 0.5 * (noise + noise.T)
        sources.append(eta * (isotropic + noise))
    return sources


def verify(cfg):
    hs, R3s, Ns = make_slices(cfg)
    E = finite_euler_response(hs, R3s, Ns, cfg.eps)
    S1 = memory_source(hs, cfg.eta_mem, cfg.seed)
    S2 = memory_source(hs, cfg.eta_mem * 0.5, cfg.seed)

    e_norms, s_norms, r_norms, s2_norms = [], [], [], []
    for e, s, s2 in zip(E, S1, S2):
        e_norms.append(np.linalg.norm(e))
        s_norms.append(np.linalg.norm(s))
        r_norms.append(np.linalg.norm(e - s))
        s2_norms.append(np.linalg.norm(s2))

    vals = np.asarray(e_norms + s_norms + r_norms + s2_norms, dtype=float)
    finite_fraction = float(np.mean(np.isfinite(vals))) if len(vals) else 0.0

    e_med = float(np.nanmedian(e_norms))
    s_med = float(np.nanmedian(s_norms))
    r_med = float(np.nanmedian(r_norms))
    s2_med = float(np.nanmedian(s2_norms))
    source_to_euler = s_med / (e_med + 1e-12)
    weak_scaling = s2_med / (s_med + 1e-12)

    stable = bool(
        finite_fraction > 0.99
        and np.isfinite(e_med) and e_med > 0
        and np.isfinite(s_med)
        and np.isfinite(r_med)
        and source_to_euler < 1.0
        and 0.35 < weak_scaling < 0.65
    )

    return FieldProxyResult(e_med, s_med, r_med, source_to_euler, weak_scaling, finite_fraction, stable)


def classify(cfg):
    r = verify(cfg)
    if r.finite_fraction < 0.99:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=200, seed=739):
    rng = np.random.default_rng(seed)
    counts = {"PASS":0, "SOFT_FAIL":0, "HARD_FAIL":0}
    vals = {k: [] for k in [
        "euler_norm_median","source_norm_median","residual_norm_median",
        "source_to_euler_ratio","weak_scaling_ratio","finite_fraction"
    ]}
    for _ in range(n_sweeps):
        cfg = FieldProxyConfig(
            n_slices=int(rng.integers(5, 14)),
            dim=3,
            eps=float(10 ** rng.uniform(-6, -3)),
            eta_mem=float(10 ** rng.uniform(-4, -1.5)),
            seed=int(rng.integers(0, 10_000_000)),
        )
        label, r = classify(cfg)
        counts[label] += 1
        if label in {"PASS","SOFT_FAIL"}:
            for k in vals:
                vals[k].append(getattr(r, k))
    out = {k: 100*v/n_sweeps for k,v in counts.items()}
    for k, arr in vals.items():
        if arr:
            out[k + "_median"] = float(np.nanmedian(arr))
    return out


def main():
    print("Causal ADM field equation proxy verifier")
    print("="*50)
    print("Route:")
    print("finite Euler response E_ab^(k) = weak-memory source S_ab^(mem,k)")
    print("This is a discrete proxy, not Einstein's equation.")
    print()
    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
