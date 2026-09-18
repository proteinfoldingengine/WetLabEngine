from __future__ import annotations

import csv
import json
import math
import hashlib
from pathlib import Path
from typing import Iterable

import numpy as np

CURRENT_STEPS = (100, 200, 300, 400)
FUTURE_STEP = {100: 200, 200: 300, 300: 400, 400: 499}
ELIGIBLE_MODE = "bridge_patch_v9"
RIDGE_ALPHA = 1.0
PERMUTATION_SEED = 20260918
PERMUTATION_REPLICATES = 2000
EXPECTED_INSTANCE_COUNTS = {"1UAO": 24, "1L2Y": 40}

SOURCE_BLOBS = {
    "1UAO_traces": (
        "Tmp/TOE/uqcf_bridge_final_verification_pack/"
        "uqcf_bridge_patch_v9_1uao_traces.csv",
        "95bf84ad9d19ee84533190787889bb1d1420c330",
    ),
    "1UAO_results": (
        "Tmp/TOE/uqcf_bridge_final_verification_pack/"
        "uqcf_bridge_patch_v9_1uao_results.csv",
        "2768ccbad6c694282a689bba799d14d65c0bb0d7",
    ),
    "1L2Y_traces": (
        "Tmp/TOE/uqcf_bridge_final_verification_pack/"
        "uqcf_bridge_patch_v9_1l2y_confirm_traces.csv",
        "819e8cecda27ba4248b64288de88d672c7b705bc",
    ),
    "1L2Y_results": (
        "Tmp/TOE/uqcf_bridge_final_verification_pack/"
        "uqcf_bridge_patch_v9_1l2y_confirm_results.csv",
        "aa3565a2a597ef93ba81d3d9d078cf452f29edbb",
    ),
}


def _f(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    if value is None or str(value).strip() == "":
        raise ValueError(f"missing required field {key}")
    return float(value)


def _i(row: dict[str, str], key: str) -> int:
    return int(float(row[key]))


def _slope(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    xc = x - x.mean()
    denom = float(np.dot(xc, xc))
    if denom == 0.0:
        return 0.0
    return float(np.dot(xc, y - y.mean()) / denom)


def build_predictor_rows(
    rows: list[dict[str, str]],
    target: str,
) -> list[dict[str, object]]:
    eligible = [
        row
        for row in rows
        if row.get("mode") == ELIGIBLE_MODE
        and _i(row, "step") in (0, *CURRENT_STEPS, 499)
    ]
    by_seed: dict[int, dict[int, dict[str, str]]] = {}
    for row in eligible:
        by_seed.setdefault(_i(row, "seed"), {})[_i(row, "step")] = row

    out: list[dict[str, object]] = []
    for seed in sorted(by_seed):
        points = by_seed[seed]
        for step in CURRENT_STEPS:
            if step not in points or FUTURE_STEP[step] not in points:
                continue
            prior_steps = sorted(s for s in points if s < step)
            if not prior_steps:
                continue
            prev_step = prior_steps[-1]
            current = points[step]
            previous = points[prev_step]
            prior = [points[s] for s in prior_steps]

            step_norm = step / 500.0
            m0 = np.asarray(
                [
                    step_norm,
                    _f(current, "energy"),
                    _f(current, "sigma_bridge"),
                    _f(current, "closure_ready"),
                    _f(current, "rg"),
                ],
                dtype=float,
            )
            m1 = np.concatenate(
                [
                    m0,
                    np.asarray(
                        [
                            _f(current, "energy") - _f(previous, "energy"),
                            _f(current, "rg") - _f(previous, "rg"),
                        ],
                        dtype=float,
                    ),
                ]
            )

            prior_steps_norm = [s / 500.0 for s in prior_steps]
            prior_sigma = [_f(r, "sigma_bridge") for r in prior]
            prior_closure = [_f(r, "closure_ready") for r in prior]
            retained = np.asarray(
                [
                    float(np.mean(prior_sigma)),
                    float(np.mean(prior_closure)),
                    _slope(prior_steps_norm, prior_sigma),
                    _slope(prior_steps_norm, prior_closure),
                ],
                dtype=float,
            )
            m2 = np.concatenate([m1, retained])
            out.append(
                {
                    "key": (target, seed, step),
                    "step": step,
                    "m0": m0,
                    "m1": m1,
                    "m2": m2,
                }
            )
    return out


def attach_labels(
    predictors: list[dict[str, object]],
    rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    rmsd = {
        (_i(row, "seed"), _i(row, "step")): _f(row, "rmsd")
        for row in rows
        if row.get("mode") == ELIGIBLE_MODE
        and str(row.get("rmsd", "")).strip() != ""
    }
    out: list[dict[str, object]] = []
    for row in predictors:
        target, seed, step = row["key"]
        future = FUTURE_STEP[int(step)]
        y = rmsd[(int(seed), future)] - rmsd[(int(seed), int(step))]
        labeled = dict(row)
        labeled["y"] = float(y)
        out.append(labeled)
    return out


def transfer_split(
    rows: list[dict[str, object]],
    train_target: str,
    test_target: str,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    train = [row for row in rows if row["key"][0] == train_target]
    test = [row for row in rows if row["key"][0] == test_target]
    if any(row["key"][0] == test_target for row in train):
        raise AssertionError("target leakage into train split")
    if any(row["key"][0] == train_target for row in test):
        raise AssertionError("target leakage into test split")
    return train, test


def _matrix(rows: list[dict[str, object]], model: str) -> np.ndarray:
    return np.vstack([np.asarray(row[model], dtype=float) for row in rows])


def _labels(rows: list[dict[str, object]]) -> np.ndarray:
    return np.asarray([float(row["y"]) for row in rows], dtype=float)


def ridge_predict(
    train_x: np.ndarray,
    train_y: np.ndarray,
    test_x: np.ndarray,
    alpha: float = RIDGE_ALPHA,
) -> np.ndarray:
    train_x = np.asarray(train_x, dtype=float)
    test_x = np.asarray(test_x, dtype=float)
    train_y = np.asarray(train_y, dtype=float)

    mu = train_x.mean(axis=0)
    sigma = train_x.std(axis=0)
    sigma = np.where(sigma == 0.0, 1.0, sigma)
    x = (train_x - mu) / sigma
    xt = (test_x - mu) / sigma

    y_mean = float(train_y.mean())
    yc = train_y - y_mean
    gram = x.T @ x + float(alpha) * np.eye(x.shape[1], dtype=float)
    beta = np.linalg.solve(gram, x.T @ yc)
    return y_mean + xt @ beta


def rmse(y: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((np.asarray(y) - np.asarray(pred)) ** 2)))


def pearson(y: np.ndarray, pred: np.ndarray) -> float:
    y = np.asarray(y, dtype=float)
    pred = np.asarray(pred, dtype=float)
    if y.size < 2 or np.std(y) == 0.0 or np.std(pred) == 0.0:
        return 0.0
    return float(np.corrcoef(y, pred)[0, 1])


def _score_model(
    train: list[dict[str, object]],
    test: list[dict[str, object]],
    model: str,
) -> dict[str, float]:
    y_train = _labels(train)
    y_test = _labels(test)
    pred = ridge_predict(_matrix(train, model), y_train, _matrix(test, model))
    return {"rmse": rmse(y_test, pred), "corr": pearson(y_test, pred)}


def evaluate_direction(
    train: list[dict[str, object]],
    test: list[dict[str, object]],
    replicates: int = PERMUTATION_REPLICATES,
    seed: int = PERMUTATION_SEED,
) -> dict[str, float]:
    m0 = _score_model(train, test, "m0")
    m1 = _score_model(train, test, "m1")
    m2 = _score_model(train, test, "m2")
    delta = m1["rmse"] - m2["rmse"]

    rng = np.random.default_rng(seed)
    x1_train = _matrix(train, "m1")
    x2_train = _matrix(train, "m2")
    x2_test = _matrix(test, "m2")
    y_train = _labels(train)
    y_test = _labels(test)

    # Retained-coherence columns are the last four M2 columns.
    null_deltas: list[float] = []
    steps = np.asarray([int(row["step"]) for row in train], dtype=int)
    for _ in range(int(replicates)):
        perm = x2_train.copy()
        for current_step in CURRENT_STEPS:
            idx = np.flatnonzero(steps == current_step)
            if idx.size < 2:
                continue
            for col in range(perm.shape[1] - 4, perm.shape[1]):
                source = perm[idx, col].copy()
                perm[idx, col] = source[rng.permutation(idx.size)]
        pred_perm = ridge_predict(perm, y_train, x2_test)
        rmse_perm = rmse(y_test, pred_perm)
        null_deltas.append(m1["rmse"] - rmse_perm)

    exceed = sum(value >= delta for value in null_deltas)
    p_value = (1.0 + exceed) / (1.0 + len(null_deltas))
    return {
        "rmse_m0": m0["rmse"],
        "corr_m0": m0["corr"],
        "rmse_m1": m1["rmse"],
        "corr_m1": m1["corr"],
        "rmse_m2": m2["rmse"],
        "corr_m2": m2["corr"],
        "delta": float(delta),
        "relative_rmse_reduction": (
            float(delta / m1["rmse"]) if m1["rmse"] > 0.0 else 0.0
        ),
        "p_value": float(p_value),
    }


def adjudicate(
    directions: dict[str, dict[str, float]],
    firewall_passed: bool,
    source_and_cardinality_passed: bool = True,
) -> str:
    required = ("1UAO_to_1L2Y", "1L2Y_to_1UAO")
    if not firewall_passed or not source_and_cardinality_passed:
        return "NO_GO_RETAINED_COHERENCE_TRANSFER_SIGNAL"
    if any(name not in directions for name in required):
        return "NO_GO_RETAINED_COHERENCE_TRANSFER_SIGNAL"
    for name in required:
        row = directions[name]
        if not (float(row["rmse_m2"]) <= 0.90 * float(row["rmse_m1"])):
            return "NO_GO_RETAINED_COHERENCE_TRANSFER_SIGNAL"
        if not (float(row["delta"]) > 0.0):
            return "NO_GO_RETAINED_COHERENCE_TRANSFER_SIGNAL"
        if not (float(row["p_value"]) < 0.05):
            return "NO_GO_RETAINED_COHERENCE_TRANSFER_SIGNAL"
        if not (float(row["corr_m2"]) > float(row["corr_m1"])):
            return "NO_GO_RETAINED_COHERENCE_TRANSFER_SIGNAL"
    return "GO_RETAINED_COHERENCE_TRANSFER_SIGNAL"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def source_integrity(repo_root: Path) -> tuple[bool, dict[str, str]]:
    observed: dict[str, str] = {}
    ok = True
    for key, (relative, expected) in SOURCE_BLOBS.items():
        path = repo_root / relative
        if not path.exists():
            observed[key] = "MISSING"
            ok = False
            continue
        digest = git_blob_sha(path)
        observed[key] = digest
        if digest != expected:
            ok = False
    return ok, observed


def _feature_firewall_check(
    trace_rows: dict[str, list[dict[str, str]]],
) -> bool:
    for target, rows in trace_rows.items():
        base = build_predictor_rows(rows, target)
        changed = [dict(row) for row in rows]
        for row in changed:
            if str(row.get("rmsd", "")).strip() != "":
                row["rmsd"] = str(float(row["rmsd"]) * 17.0 + 91.0)
        mutated = build_predictor_rows(changed, target)
        if len(base) != len(mutated):
            return False
        for a, b in zip(base, mutated):
            if a["key"] != b["key"]:
                return False
            for model in ("m0", "m1", "m2"):
                if not np.array_equal(a[model], b[model]):
                    return False
    return True


def run_analysis(repo_root: Path) -> dict[str, object]:
    integrity_ok, observed_blobs = source_integrity(repo_root)

    trace_rows: dict[str, list[dict[str, str]]] = {}
    for target, source_key in (("1UAO", "1UAO_traces"), ("1L2Y", "1L2Y_traces")):
        relative, _ = SOURCE_BLOBS[source_key]
        trace_rows[target] = load_csv(repo_root / relative)

    firewall = _feature_firewall_check(trace_rows)
    all_rows: list[dict[str, object]] = []
    counts: dict[str, int] = {}
    for target in ("1UAO", "1L2Y"):
        predictors = build_predictor_rows(trace_rows[target], target)
        labeled = attach_labels(predictors, trace_rows[target])
        counts[target] = len(labeled)
        all_rows.extend(labeled)

    cardinality_ok = counts == EXPECTED_INSTANCE_COUNTS

    ua_train, lb_test = transfer_split(all_rows, "1UAO", "1L2Y")
    lb_train, ua_test = transfer_split(all_rows, "1L2Y", "1UAO")

    directions = {
        "1UAO_to_1L2Y": evaluate_direction(ua_train, lb_test),
        "1L2Y_to_1UAO": evaluate_direction(lb_train, ua_test),
    }
    source_and_cardinality = bool(integrity_ok and cardinality_ok)
    decision = adjudicate(
        directions,
        firewall_passed=firewall,
        source_and_cardinality_passed=source_and_cardinality,
    )
    return {
        "schema": "protein-p9-retained-coherence-result-v1",
        "decision": decision,
        "source_integrity_passed": bool(integrity_ok),
        "observed_git_blobs": observed_blobs,
        "instance_counts": counts,
        "expected_instance_counts": EXPECTED_INSTANCE_COUNTS,
        "cardinality_passed": bool(cardinality_ok),
        "native_information_firewall_passed": bool(firewall),
        "directions": directions,
        "claim_boundary": (
            "P9A tests only whether frozen retained v9 bridge/coherence history "
            "adds transferable predictive information beyond the preregistered "
            "instantaneous and ordinary-history controls in the archived 1UAO/1L2Y data."
        ),
    }


def main() -> None:
    here = Path(__file__).resolve()
    repo_root = here.parents[4]
    result = run_analysis(repo_root)
    out = here.parent / "p9_result.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
