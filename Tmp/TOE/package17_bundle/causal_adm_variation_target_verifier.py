
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class VariationConfig:
    n_slices: int = 9
    dim: int = 3
    eps: float = 1e-4
    seed: int = 701

@dataclass(frozen=True)
class VariationResult:
    action0: float
    grad_norm_median: float
    grad_norm_max: float
    finite_fraction: float
    positive_definite_fraction: float
    nontrivial_fraction: float
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
    n = len(hs)
    terms = []
    for k in range(1, n - 1):
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

def is_spd(M):
    try:
        return bool(np.min(np.linalg.eigvalsh(M)) > 1e-10)
    except np.linalg.LinAlgError:
        return False

def verify(cfg):
    hs, R3s, Ns = make_slices(cfg)
    S0 = action(hs, R3s, Ns)
    grads, pd_flags, nontriv = [], [], []
    for k in range(1, cfg.n_slices - 1):
        local = []
        for a in range(cfg.dim):
            for b in range(a, cfg.dim):
                E = np.zeros((cfg.dim, cfg.dim))
                E[a, b] = 1.0
                E[b, a] = 1.0
                hp = [x.copy() for x in hs]
                hm = [x.copy() for x in hs]
                hp[k] = hp[k] + cfg.eps * E
                hm[k] = hm[k] - cfg.eps * E
                pd = is_spd(hp[k]) and is_spd(hm[k])
                pd_flags.append(pd)
                if not pd:
                    local.append(np.nan)
                    continue
                g = (action(hp, R3s, Ns) - action(hm, R3s, Ns)) / (2 * cfg.eps)
                local.append(g)
                nontriv.append(abs(g) > 1e-8)
        local = np.asarray(local, dtype=float)
        finite = local[np.isfinite(local)]
        grads.append(np.linalg.norm(finite) if len(finite) else np.nan)
    grads = np.asarray(grads, dtype=float)
    finite_fraction = float(np.mean(np.isfinite(grads))) if len(grads) else 0.0
    pd_fraction = float(np.mean(pd_flags)) if pd_flags else 0.0
    nontriv_fraction = float(np.mean(nontriv)) if nontriv else 0.0
    grad_med = float(np.nanmedian(grads)) if len(grads) else np.nan
    grad_max = float(np.nanmax(grads)) if len(grads) else np.nan
    stable = bool(np.isfinite(S0) and finite_fraction > 0.99 and pd_fraction > 0.99 and nontriv_fraction > 0.5 and np.isfinite(grad_max) and grad_max < 1e5)
    return VariationResult(S0, grad_med, grad_max, finite_fraction, pd_fraction, nontriv_fraction, stable)

def classify(cfg):
    r = verify(cfg)
    if not np.isfinite(r.action0) or r.finite_fraction < 0.99:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r

def run_sweep(n_sweeps=200, seed=709):
    rng = np.random.default_rng(seed)
    counts = {"PASS":0, "SOFT_FAIL":0, "HARD_FAIL":0}
    vals = {k: [] for k in ["action0","grad_norm_median","grad_norm_max","finite_fraction","positive_definite_fraction","nontrivial_fraction"]}
    for _ in range(n_sweeps):
        cfg = VariationConfig(int(rng.integers(5, 14)), 3, float(10 ** rng.uniform(-6, -3)), int(rng.integers(0, 10_000_000)))
        label, r = classify(cfg)
        counts[label] += 1
        if label in {"PASS","SOFT_FAIL"}:
            for k in vals:
                vals[k].append(getattr(r, k))
    out = {k:100*v/n_sweeps for k,v in counts.items()}
    for k, arr in vals.items():
        if arr:
            out[k + "_median"] = float(np.nanmedian(arr))
    return out

def main():
    print("Causal ADM variation target verifier")
    print("="*50)
    print("Route:")
    print("finite-difference variation of S_proxy^(N,R3) with respect to h_ab slices")
    print("This is proxy variation, not Einstein variation.")
    print()
    for k, v in run_sweep().items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
