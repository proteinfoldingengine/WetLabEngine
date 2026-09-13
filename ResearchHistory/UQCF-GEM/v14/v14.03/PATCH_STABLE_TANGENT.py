#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).with_name("source_ray_audit.py")
text = path.read_text()
text = text.replace("from scipy.linalg import expm\n", "from scipy.linalg import expm, expm_frechet\n")
old = '''def pgrl_tangent(X0: np.ndarray, P: np.ndarray) -> np.ndarray:\n    X0 = _herm(np.asarray(X0, dtype=complex))\n    P = _herm(np.asarray(P, dtype=complex))\n    p, U = np.linalg.eigh(X0)\n    if p[0] <= 0:\n        raise ArithmeticError("PGRL tangent requires faithful X0")\n    Phat = U.conj().T @ P @ U\n    lm = _log_mean_matrix(p)\n    raw = lm * Phat\n    mean = float(np.real(np.trace(X0 @ P)))\n    idx = np.diag_indices(len(p))\n    raw[idx] -= p * mean\n    dotX = _herm(U @ raw @ U.conj().T)\n    return dotX\n'''
new = '''def pgrl_tangent(X0: np.ndarray, P: np.ndarray) -> np.ndarray:\n    """Exact PGRL tangent via a numerically stable exponential Frechet derivative.\n\n    This is analytically equivalent to the logarithmic-mean spectral formula.\n    The Frechet form avoids divided-difference loss of covariance when faithful\n    X0 has repeated or near-repeated eigenvalues.\n    """\n    X0 = _herm(np.asarray(X0, dtype=complex))\n    P = _herm(np.asarray(P, dtype=complex))\n    p, U = np.linalg.eigh(X0)\n    if p[0] <= 0:\n        raise ArithmeticError("PGRL tangent requires faithful X0")\n    logX0 = _herm(U @ np.diag(np.log(p)) @ U.conj().T)\n    raw = expm_frechet(logX0, P, compute_expm=False)\n    mean = float(np.real(np.trace(X0 @ P)))\n    return _herm(raw - X0 * mean)\n'''
if old in text:
    text = text.replace(old, new)
elif new not in text:
    raise SystemExit("expected pgrl_tangent block not found")
path.write_text(text)
