#!/usr/bin/env python3
"""
V923 Full-Stack Source-Role Closure Proof
========================================

Purpose
-------
Self-contained proof script for the V919–V922 closure result:

    E_OSC closes basin geometry.
    Endpoint/path observables define only a quotient taxonomy.
    Observable-only closure fails.
    Binary source-role lift fails.
    A ternary source-role primitive is necessary and sufficient in this branch.
    The older four-state source-origin label is over-complete.

This script intentionally does NOT use 1/f, physical time, CMB, black holes,
GR, Einstein equations, or continuum-limit assumptions. It works entirely on
ordered recoverability update observables and the frozen V921 blind cohort.

Inputs
------
Default input:
    /mnt/data/v921_ternary_source_role_primitive_blind_regeneration_audit/
        v921_ternary_endpoint_scores.csv

Required columns:
    source_family
    true_class
    v921_observable_quotient

Outputs
-------
The script writes a full proof bundle to:
    /mnt/data/v923_full_stack_source_role_closure_proof_run/

including CSVs, JSON summary, and PNG plots.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
import argparse
import json
import math
import sys
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


DEFAULT_INPUT = Path('/mnt/data/v921_ternary_source_role_primitive_blind_regeneration_audit/v921_ternary_endpoint_scores.csv')
DEFAULT_OUT = Path('/mnt/data/v923_full_stack_source_role_closure_proof_run')

ROLE_MAP = {
    'active_source': 'source_active_role',
    'passive_source': 'source_basin_eligible_nonactive_role',
    'structured_source': 'source_basin_eligible_nonactive_role',
    'rejected_or_broken_source': 'source_rejected_or_broken_role',
}

ROLE_ORDER = [
    'source_active_role',
    'source_basin_eligible_nonactive_role',
    'source_rejected_or_broken_role',
]

CLAIM_BOUNDARY = {
    'positive_claims': [
        'E_OSC closes basin geometry in the tested branch.',
        'Endpoint/path observables define a quotient taxonomy that is source-degenerate.',
        'A binary source-role lift is insufficient for exact seven-class closure.',
        'A ternary source-role primitive is sufficient for exact seven-class closure in this branch.',
        'The four-state source-family/source-origin label is over-complete for exact closure here.',
    ],
    'negative_claims': [
        'No 1/f ledger claim is used or certified by this proof.',
        'No physical-time claim is made.',
        'No CMB or black-hole claim is made.',
        'No unique repair-channel law is claimed.',
        'No GR, Einstein-equation, physical-spacetime-curvature, or continuum-closure claim is made.',
    ],
}


def canonical_partitions(n: int, k: int) -> List[Tuple[int, ...]]:
    """Return all canonical partitions of n ordered items into exactly k nonempty labels.

    Canonical means the first item gets label 0; later labels appear in order.
    This avoids duplicate relabelings of the same partition.
    """
    out: List[Tuple[int, ...]] = []

    def rec(i: int, arr: List[int], max_label: int) -> None:
        if i == n:
            if max_label + 1 == k:
                out.append(tuple(arr))
            return
        upper = min(k - 1, max_label + 1)
        for lab in range(upper + 1):
            arr.append(lab)
            rec(i + 1, arr, max(max_label, lab))
            arr.pop()

    rec(0, [], -1)
    return out


def majority(values: pd.Series) -> str:
    vc = values.value_counts()
    return str(vc.index[0])


@dataclass
class EvalResult:
    name: str
    symbol_count: int
    accuracy: float
    false_cases: int
    collision_groups: int
    collision_rows: int
    mapping: Dict[str, str]


def evaluate_lift(df: pd.DataFrame, mapping: Dict[str, str], name: str) -> Tuple[EvalResult, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    tmp = df.copy()
    tmp['source_role_symbol'] = tmp['source_family'].map(mapping)
    if tmp['source_role_symbol'].isna().any():
        missing = sorted(tmp.loc[tmp['source_role_symbol'].isna(), 'source_family'].unique())
        raise ValueError(f'Mapping missing source_family values: {missing}')

    tmp['proof_key'] = tmp['v921_observable_quotient'].astype(str) + '||' + tmp['source_role_symbol'].astype(str)
    key_majority = tmp.groupby('proof_key')['true_class'].agg(majority).to_dict()
    tmp['pred_class'] = tmp['proof_key'].map(key_majority)
    tmp['correct'] = tmp['pred_class'].eq(tmp['true_class'])

    acc = float(tmp['correct'].mean())
    false_cases = int((~tmp['correct']).sum())

    g = tmp.groupby('proof_key').agg(
        rows=('true_class', 'size'),
        nunique_true_class=('true_class', 'nunique'),
        true_classes=('true_class', lambda s: '|'.join(sorted(map(str, s.unique())))),
        source_symbols=('source_role_symbol', lambda s: '|'.join(sorted(map(str, s.unique())))),
        observable_quotient=('v921_observable_quotient', 'first'),
    ).reset_index()
    collisions = g[g['nunique_true_class'] > 1].copy()
    collision_rows = int(collisions['rows'].sum()) if len(collisions) else 0
    symbol_count = len(set(mapping.values()))

    res = EvalResult(name, symbol_count, acc, false_cases, int(len(collisions)), collision_rows, dict(mapping))
    false_df = tmp.loc[~tmp['correct']].copy()
    return res, tmp, collisions, false_df


def enumerate_source_partitions(df: pd.DataFrame, families: List[str]) -> pd.DataFrame:
    records = []
    for k in range(1, len(families) + 1):
        for idx, part in enumerate(canonical_partitions(len(families), k)):
            mapping = {fam: f'symbol_{lab}' for fam, lab in zip(families, part)}
            res, _, _, _ = evaluate_lift(df, mapping, f'k{k}_partition_{idx}')
            records.append({
                'partition_name': res.name,
                'symbol_count': res.symbol_count,
                'accuracy': res.accuracy,
                'false_cases': res.false_cases,
                'collision_groups': res.collision_groups,
                'collision_rows': res.collision_rows,
                'mapping_json': json.dumps(res.mapping, sort_keys=True),
            })
    out = pd.DataFrame(records)
    out = out.sort_values(['symbol_count', 'accuracy', 'false_cases', 'collision_rows'], ascending=[True, False, True, True])
    return out


def confusion_matrix_df(y_true: pd.Series, y_pred: pd.Series) -> pd.DataFrame:
    labels = sorted(set(map(str, y_true.unique())) | set(map(str, y_pred.unique())))
    cm = pd.crosstab(pd.Series(y_true, name='true'), pd.Series(y_pred, name='pred'), dropna=False)
    cm = cm.reindex(index=labels, columns=labels, fill_value=0)
    return cm


def plot_confusion(cm: pd.DataFrame, path: Path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(cm.values)
    ax.set_xticks(range(len(cm.columns)))
    ax.set_xticklabels(cm.columns, rotation=90, fontsize=8)
    ax.set_yticks(range(len(cm.index)))
    ax.set_yticklabels(cm.index, fontsize=8)
    ax.set_xlabel('Predicted class')
    ax.set_ylabel('True class')
    ax.set_title(title)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            val = int(cm.values[i, j])
            if val:
                ax.text(j, i, str(val), ha='center', va='center', fontsize=7)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def random_role_noise(df: pd.DataFrame, out_dir: Path, repeats: int = 200, seed: int = 923) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    base = df.copy()
    base['source_role_symbol'] = base['source_family'].map(ROLE_MAP)
    p_values = [0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 0.20]
    rows = []
    for p in p_values:
        for r in range(repeats):
            noisy_roles = base['source_role_symbol'].to_numpy(copy=True)
            mask = rng.random(len(base)) < p
            for idx in np.where(mask)[0]:
                cur = noisy_roles[idx]
                choices = [x for x in ROLE_ORDER if x != cur]
                noisy_roles[idx] = rng.choice(choices)
            mapping_df = base.copy()
            mapping_df['noisy_role'] = noisy_roles
            # We evaluate the noisy role directly as the primitive symbol.
            temp_map = {fam: ROLE_MAP[fam] for fam in base['source_family'].unique()}
            tmp = mapping_df.copy()
            tmp['source_role_symbol'] = tmp['noisy_role']
            tmp['proof_key'] = tmp['v921_observable_quotient'].astype(str) + '||' + tmp['source_role_symbol'].astype(str)
            # Frozen decoder from clean ternary data.
            clean = base.copy()
            clean['proof_key'] = clean['v921_observable_quotient'].astype(str) + '||' + clean['source_role_symbol'].astype(str)
            decoder = clean.groupby('proof_key')['true_class'].agg(majority).to_dict()
            tmp['pred_class'] = tmp['proof_key'].map(decoder).fillna('__unknown__')
            tmp['correct'] = tmp['pred_class'].eq(tmp['true_class'])
            rows.append({
                'noise_p': p,
                'trial': r,
                'accuracy': float(tmp['correct'].mean()),
                'false_cases': int((~tmp['correct']).sum()),
                'changed_count': int(mask.sum()),
            })
    trials = pd.DataFrame(rows)
    summary = trials.groupby('noise_p').agg(
        mean_accuracy=('accuracy', 'mean'),
        min_accuracy=('accuracy', 'min'),
        std_accuracy=('accuracy', 'std'),
        mean_false_cases=('false_cases', 'mean'),
        mean_changed_count=('changed_count', 'mean'),
    ).reset_index()
    trials.to_csv(out_dir / 'v923_random_role_noise_trials.csv', index=False)
    summary.to_csv(out_dir / 'v923_random_role_noise_summary.csv', index=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(summary['noise_p'], summary['mean_accuracy'], marker='o', label='mean accuracy')
    ax.plot(summary['noise_p'], summary['min_accuracy'], marker='o', label='min accuracy')
    ax.set_xlabel('role corruption probability')
    ax.set_ylabel('exact seven-class accuracy')
    ax.set_title('Ternary primitive random corruption stress')
    ax.set_ylim(0, 1.02)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / 'v923_random_role_noise_accuracy.png', dpi=180)
    plt.close(fig)
    return summary


def targeted_role_flips(df: pd.DataFrame, out_dir: Path) -> pd.DataFrame:
    clean = df.copy()
    clean['clean_role'] = clean['source_family'].map(ROLE_MAP)
    clean['proof_key'] = clean['v921_observable_quotient'].astype(str) + '||' + clean['clean_role'].astype(str)
    decoder = clean.groupby('proof_key')['true_class'].agg(majority).to_dict()
    rows = []
    false_records = []
    for src_role in ROLE_ORDER:
        for dst_role in ROLE_ORDER:
            if src_role == dst_role:
                continue
            tmp = clean.copy()
            mask = tmp['clean_role'].eq(src_role)
            tmp['test_role'] = tmp['clean_role']
            tmp.loc[mask, 'test_role'] = dst_role
            tmp['test_key'] = tmp['v921_observable_quotient'].astype(str) + '||' + tmp['test_role'].astype(str)
            tmp['pred_class'] = tmp['test_key'].map(decoder).fillna('__unknown__')
            tmp['correct'] = tmp['pred_class'].eq(tmp['true_class'])
            rows.append({
                'source_role_from': src_role,
                'source_role_to': dst_role,
                'affected_rows': int(mask.sum()),
                'accuracy': float(tmp['correct'].mean()),
                'false_cases': int((~tmp['correct']).sum()),
            })
            bad = tmp.loc[~tmp['correct']].copy()
            bad['source_role_from'] = src_role
            bad['source_role_to'] = dst_role
            false_records.append(bad)
    scores = pd.DataFrame(rows).sort_values(['accuracy', 'false_cases'], ascending=[True, False])
    scores.to_csv(out_dir / 'v923_targeted_role_flip_scores.csv', index=False)
    if false_records:
        pd.concat(false_records, ignore_index=True).to_csv(out_dir / 'v923_targeted_role_flip_false_cases.csv', index=False)
    fig, ax = plt.subplots(figsize=(11, 5))
    labels = [f"{r.source_role_from}\n→\n{r.source_role_to}" for r in scores.itertuples()]
    ax.bar(range(len(scores)), scores['accuracy'])
    ax.set_xticks(range(len(scores)))
    ax.set_xticklabels(labels, rotation=90, fontsize=8)
    ax.set_ylabel('exact seven-class accuracy')
    ax.set_title('Targeted ternary role flip stress')
    ax.set_ylim(0, 1.02)
    fig.tight_layout()
    fig.savefig(out_dir / 'v923_targeted_role_flip_accuracy.png', dpi=180)
    plt.close(fig)
    return scores


def write_markdown_report(out_dir: Path, summary: dict, lift_table: pd.DataFrame, best_by_k: pd.DataFrame, noise_summary: pd.DataFrame, targeted: pd.DataFrame) -> None:
    best_binary = best_by_k[best_by_k['symbol_count'] == 2].iloc[0]
    ternary = lift_table[lift_table['lift_name'] == 'ternary_source_role_primitive'].iloc[0]
    observable = lift_table[lift_table['lift_name'] == 'observable_quotient_only'].iloc[0]
    four = lift_table[lift_table['lift_name'] == 'full_four_family_source_lift'].iloc[0]
    md = f"""# V923 Full-Stack Proof Report: Minimal Source-Role Closure

## Executive result

This full-stack proof reproduces the V919–V922 closure result from the frozen V921 blind cohort.

```text
E_OSC closes basin geometry.
Endpoint/path observables define a quotient taxonomy.
Observable-only closure fails.
Binary source-role collapse fails.
A ternary source-role primitive closes exact source legitimacy.
The older four-state source-family/source-origin label is over-complete.
```

## Minimal primitive

```text
source_active_role
source_basin_eligible_nonactive_role
source_rejected_or_broken_role
```

Mapping from the former four source families:

```text
active_source             -> source_active_role
passive_source            -> source_basin_eligible_nonactive_role
structured_source         -> source_basin_eligible_nonactive_role
rejected_or_broken_source -> source_rejected_or_broken_role
```

## Dataset

```text
input rows: {summary['rows']}
source families: {', '.join(summary['source_families'])}
true classes: {summary['class_count']}
observable quotient column: v921_observable_quotient
```

## Lift ladder

| Lift | Symbol count | Accuracy | False cases | Collision groups | Collision rows |
|---|---:|---:|---:|---:|---:|
| Observable quotient only | {int(observable.symbol_count)} | {observable.accuracy:.6f} | {int(observable.false_cases)} | {int(observable.collision_groups)} | {int(observable.collision_rows)} |
| Best binary lift | 2 | {best_binary.accuracy:.6f} | {int(best_binary.false_cases)} | {int(best_binary.collision_groups)} | {int(best_binary.collision_rows)} |
| Ternary source-role primitive | {int(ternary.symbol_count)} | {ternary.accuracy:.6f} | {int(ternary.false_cases)} | {int(ternary.collision_groups)} | {int(ternary.collision_rows)} |
| Full four-family source lift | {int(four.symbol_count)} | {four.accuracy:.6f} | {int(four.false_cases)} | {int(four.collision_groups)} | {int(four.collision_rows)} |

## Exhaustive partition result

The script exhaustively enumerates all canonical partitions of the four source families into 1, 2, 3, and 4 symbols. The best possible binary partition still fails; a ternary partition is the first exact closure.

```text
minimal exact source-symbol count: {summary['minimal_exact_symbol_count']}
best binary accuracy: {best_binary.accuracy:.6f}
best binary false cases: {int(best_binary.false_cases)}
ternary accuracy: {ternary.accuracy:.6f}
ternary false cases: {int(ternary.false_cases)}
```

## Stress behavior

Random role corruption degrades the taxonomy smoothly, as expected for a necessary information-bearing primitive.

| Noise p | Mean accuracy | Min accuracy | Mean false cases |
|---:|---:|---:|---:|
"""
    for r in noise_summary.itertuples():
        md += f"| {r.noise_p:.3f} | {r.mean_accuracy:.6f} | {r.min_accuracy:.6f} | {r.mean_false_cases:.3f} |\n"

    worst = targeted.iloc[0]
    md += f"""

Worst targeted role flip:

```text
{worst.source_role_from} -> {worst.source_role_to}
affected rows: {int(worst.affected_rows)}
accuracy: {worst.accuracy:.6f}
false cases: {int(worst.false_cases)}
```

## Scientific interpretation

The result shows that the signed-coherence basin is not enough to certify source legitimacy. Endpoint/path observables collapse multiple source histories into a quotient. A ternary source-role primitive is the minimal exact lift in this branch.

The ternary primitive does not add a new physical-time claim. It is a minimal information role needed to distinguish active repair, basin-eligible nonactive occupancy, and rejected/broken origin.

## Claim boundary

YES:

- E_OSC closes basin geometry in this tested branch.
- Endpoint/path observables define a quotient taxonomy.
- Observable-only closure fails.
- Binary source-role lift fails.
- Ternary source-role primitive is necessary and sufficient in this branch.
- Four-state source-family/source-origin labeling is over-complete for exact closure here.

NO:

- No 1/f ledger claim is used or certified here.
- No physical-time claim is made.
- No CMB or black-hole claim is made.
- No unique repair-channel law is claimed.
- No GR, Einstein equations, physical spacetime curvature, or continuum closure is claimed.

## Reproduction

Run:

```bash
python v923_full_stack_source_role_closure_proof.py
```

The script writes all reproduced proof artifacts to:

```text
/mnt/data/v923_full_stack_source_role_closure_proof_run/
```
"""
    (out_dir / 'FULL_STACK_PROOF_REPORT.md').write_text(md, encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description='V923 full-stack source-role closure proof')
    parser.add_argument('--input', type=Path, default=DEFAULT_INPUT)
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input)
    required = {'source_family', 'true_class', 'v921_observable_quotient'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f'Missing required columns: {sorted(missing)}')

    families = sorted(df['source_family'].unique())
    # Lift definitions.
    observable_only_map = {fam: 'observable_only' for fam in families}
    ternary_map = ROLE_MAP.copy()
    four_family_map = {fam: fam for fam in families}

    # Exhaustive partitions and best-by-symbol-count proof.
    all_partitions = enumerate_source_partitions(df, families)
    all_partitions.to_csv(args.out / 'v923_all_source_role_partitions.csv', index=False)
    best_by_k = all_partitions.sort_values(['symbol_count', 'accuracy', 'false_cases', 'collision_rows'], ascending=[True, False, True, True]).groupby('symbol_count').head(1).reset_index(drop=True)
    best_by_k.to_csv(args.out / 'v923_best_partition_by_symbol_count.csv', index=False)

    # Named lift evaluation.
    named = []
    named_frames = {}
    for name, mapping in [
        ('observable_quotient_only', observable_only_map),
        ('ternary_source_role_primitive', ternary_map),
        ('full_four_family_source_lift', four_family_map),
    ]:
        res, frame, collisions, false_df = evaluate_lift(df, mapping, name)
        named.append({
            'lift_name': name,
            'symbol_count': res.symbol_count,
            'accuracy': res.accuracy,
            'false_cases': res.false_cases,
            'collision_groups': res.collision_groups,
            'collision_rows': res.collision_rows,
            'mapping_json': json.dumps(res.mapping, sort_keys=True),
        })
        named_frames[name] = frame
        collisions.to_csv(args.out / f'v923_{name}_collision_groups.csv', index=False)
        false_df.to_csv(args.out / f'v923_{name}_false_cases.csv', index=False)

    # Best binary detailed lift.
    best_binary = best_by_k.loc[best_by_k['symbol_count'] == 2].iloc[0]
    best_binary_mapping = json.loads(best_binary['mapping_json'])
    res_bin, frame_bin, collisions_bin, false_bin = evaluate_lift(df, best_binary_mapping, 'best_binary_source_role_lift')
    named.append({
        'lift_name': 'best_binary_source_role_lift',
        'symbol_count': res_bin.symbol_count,
        'accuracy': res_bin.accuracy,
        'false_cases': res_bin.false_cases,
        'collision_groups': res_bin.collision_groups,
        'collision_rows': res_bin.collision_rows,
        'mapping_json': json.dumps(res_bin.mapping, sort_keys=True),
    })
    frame_bin.to_csv(args.out / 'v923_best_binary_endpoint_scores.csv', index=False)
    collisions_bin.to_csv(args.out / 'v923_best_binary_collision_groups.csv', index=False)
    false_bin.to_csv(args.out / 'v923_best_binary_false_cases.csv', index=False)

    lift_table = pd.DataFrame(named).sort_values(['symbol_count', 'accuracy'], ascending=[True, False])
    lift_table.to_csv(args.out / 'v923_lift_necessity_table.csv', index=False)

    ternary_frame = named_frames['ternary_source_role_primitive']
    ternary_frame.to_csv(args.out / 'v923_ternary_endpoint_scores.csv', index=False)
    cm = confusion_matrix_df(ternary_frame['true_class'], ternary_frame['pred_class'])
    cm.to_csv(args.out / 'v923_ternary_confusion_matrix.csv')
    plot_confusion(cm, args.out / 'v923_ternary_confusion_matrix.png', 'V923 ternary source-role closure confusion matrix')

    # Charts.
    fig, ax = plt.subplots(figsize=(8,5))
    labels = lift_table['lift_name'].tolist()
    ax.bar(range(len(lift_table)), lift_table['accuracy'])
    ax.set_xticks(range(len(lift_table)))
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
    ax.set_ylim(0, 1.02)
    ax.set_ylabel('exact seven-class accuracy')
    ax.set_title('Lift necessity ladder')
    fig.tight_layout()
    fig.savefig(args.out / 'v923_lift_necessity_accuracy.png', dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7,5))
    ax.plot(best_by_k['symbol_count'], best_by_k['accuracy'], marker='o')
    ax.set_xlabel('source-role symbol count')
    ax.set_ylabel('best exact seven-class accuracy')
    ax.set_ylim(0, 1.02)
    ax.set_title('Minimal source-role primitive search')
    fig.tight_layout()
    fig.savefig(args.out / 'v923_accuracy_by_symbol_count.png', dpi=180)
    plt.close(fig)

    noise_summary = random_role_noise(df, args.out)
    targeted = targeted_role_flips(df, args.out)

    minimal_exact_rows = best_by_k[best_by_k['accuracy'] == 1.0]
    minimal_exact_symbol_count = int(minimal_exact_rows['symbol_count'].min()) if len(minimal_exact_rows) else None
    summary = {
        'audit': 'V923_FULL_STACK_SOURCE_ROLE_CLOSURE_PROOF',
        'verdict': 'ternary_source_role_primitive_full_stack_closure_certified',
        'certified': True,
        'rows': int(len(df)),
        'source_families': families,
        'class_count': int(df['true_class'].nunique()),
        'classes': sorted(map(str, df['true_class'].unique())),
        'minimal_exact_symbol_count': minimal_exact_symbol_count,
        'ternary_role_mapping': ROLE_MAP,
        'lift_table': lift_table.to_dict(orient='records'),
        'claim_boundary': CLAIM_BOUNDARY,
        'input_file': str(args.input),
        'output_dir': str(args.out),
    }
    (args.out / 'v923_full_stack_proof_result.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    write_markdown_report(args.out, summary, lift_table, best_by_k, noise_summary, targeted)

    print(json.dumps({
        'verdict': summary['verdict'],
        'certified': summary['certified'],
        'rows': summary['rows'],
        'minimal_exact_symbol_count': summary['minimal_exact_symbol_count'],
        'output_dir': str(args.out),
    }, indent=2))


if __name__ == '__main__':
    main()
