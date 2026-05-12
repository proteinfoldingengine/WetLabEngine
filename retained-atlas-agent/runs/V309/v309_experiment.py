import json, os, math, random
from pathlib import Path
from statistics import mean

RUN_DIR = Path('runs/V309')
RUN_DIR.mkdir(parents=True, exist_ok=True)

SEEDS = list(range(20))
N_STEPS = 60
A_C = 0.527
D_C = 0.0388


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def simulate(seed):
    rng = random.Random(seed)
    series = []
    # Toy latent dynamics: smooth decline with occasional shocks and partial recovery.
    a = 1.0
    bad = False
    for t in range(N_STEPS):
        drift = -0.010 - 0.003 * math.sin(0.17 * t + 0.3 * seed)
        shock = 0.0
        if t in (12, 21, 34, 47):
            shock = -0.08 - 0.05 * rng.random()
        if rng.random() < 0.05:
            shock += -0.03 * rng.random()
        recovery = 0.015 if a < 0.6 else 0.006
        a = max(0.0, min(1.2, a + drift + shock + recovery))

        # Componentized reachability factors, all in [0,1.5] roughly.
        rf = max(0.02, 1.05 - 0.55 * (1.0 - a) + 0.03 * math.sin(0.1 * t + seed))
        cw = max(0.02, 1.00 - 0.75 * (1.0 - a) + 0.02 * math.cos(0.2 * t))
        be = max(0.02, 0.95 - 0.60 * (1.0 - a) + 0.02 * rng.random())
        dr = max(0.02, 1.10 - 0.50 * (1.0 - a) + 0.01 * math.sin(0.3 * t))
        rv = max(0.02, 0.98 - 0.65 * (1.0 - a) + 0.02 * rng.random())

        A_full = (rf * cw * be * dr * rv) ** (1.0 / 5.0)
        A_norm = A_full
        D_A = max(0.0, A_C - A_norm)

        # One-component ablations: remove one factor by setting it neutral.
        ablations = {
            'no_rf': (1.0 * cw * be * dr * rv) ** (1.0 / 5.0),
            'no_cw': (rf * 1.0 * be * dr * rv) ** (1.0 / 5.0),
            'no_be': (rf * cw * 1.0 * dr * rv) ** (1.0 / 5.0),
            'no_dr': (rf * cw * be * 1.0 * rv) ** (1.0 / 5.0),
            'no_rv': (rf * cw * be * dr * 1.0) ** (1.0 / 5.0),
        }

        # Toy label: bad if adaptive reachability is too low or latent state has collapsed.
        bad = int((A_norm < A_C) or (a < 0.42))
        series.append({
            't': t,
            'a': a,
            'bad': bad,
            'A_full': A_full,
            'D_A': D_A,
            **ablations,
        })
    return series


def auc_score(y_true, y_score):
    pairs = sorted(zip(y_score, y_true), key=lambda x: x[0])
    n_pos = sum(y_true)
    n_neg = len(y_true) - n_pos
    if n_pos == 0 or n_neg == 0:
        return 0.5
    rank_sum = 0.0
    i = 0
    while i < len(pairs):
        j = i
        while j < len(pairs) and pairs[j][0] == pairs[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        pos_in_group = sum(v for _, v in pairs[i:j])
        rank_sum += pos_in_group * avg_rank
        i = j
    return (rank_sum - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def balanced_accuracy(y_true, y_pred):
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)
    p = sum(y_true)
    n = len(y_true) - p
    tpr = tp / p if p else 0.0
    tnr = tn / n if n else 0.0
    return 0.5 * (tpr + tnr)


def accuracy(y_true, y_pred):
    return sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp) / len(y_true)


def corr(x, y):
    mx = mean(x)
    my = mean(y)
    vx = sum((a - mx) ** 2 for a in x)
    vy = sum((b - my) ** 2 for b in y)
    if vx == 0 or vy == 0:
        return 0.0
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return cov / math.sqrt(vx * vy)


def metrics_from_scores(y_true, scores, threshold):
    y_pred = [1 if s >= threshold else 0 for s in scores]
    return {
        'AUC': auc_score(y_true, scores),
        'balanced_accuracy': balanced_accuracy(y_true, y_pred),
        'accuracy': accuracy(y_true, y_pred),
        'mean_bad': mean([s for s, y in zip(scores, y_true) if y == 1]) if any(y_true) else 0.0,
        'mean_safe': mean([s for s, y in zip(scores, y_true) if y == 0]) if any(1 - y for y in y_true) else 0.0,
        'corr': corr(scores, y_true),
    }


def main():
    all_rows = []
    for seed in SEEDS:
        all_rows.extend(simulate(seed))

    # Hold-out split by seed parity.
    train = [r for r in all_rows if r['t'] < 40 and (r['t'] % 2 == 0)]
    test = [r for r in all_rows if r['t'] >= 40 or (r['t'] % 2 == 1)]

    y_train = [r['bad'] for r in train]
    y_test = [r['bad'] for r in test]

    variants = ['A_full', 'no_rf', 'no_cw', 'no_be', 'no_dr', 'no_rv']
    out = {}

    # Threshold fixed from the current law stack; no tuning.
    threshold = D_C
    for v in variants:
        train_scores = [r['D_A'] if v == 'A_full' else max(0.0, A_C - r[v]) for r in train]
        test_scores = [r['D_A'] if v == 'A_full' else max(0.0, A_C - r[v]) for r in test]
        m = metrics_from_scores(y_test, test_scores, threshold)
        m['train_auc'] = auc_score(y_train, train_scores)
        m['train_balanced_accuracy'] = balanced_accuracy(y_train, [1 if s >= threshold else 0 for s in train_scores])
        m['trigger_rate'] = sum(1 for s in test_scores if s >= threshold) / len(test_scores)
        out[v] = m

    # Compare intervention-like effect by counting positives caught under threshold.
    baseline_bad_rate = sum(y_test) / len(y_test)
    phase_counts = {'bad': sum(y_test), 'safe': len(y_test) - sum(y_test)}
    result = {
        'version': 'V309',
        'title': 'Component ablation of the reachability law',
        'config': {
            'seeds': SEEDS,
            'n_steps': N_STEPS,
            'A_c': A_C,
            'D_c': D_C,
            'train_size': len(train),
            'test_size': len(test),
        },
        'baseline': {
            'bad_rate': baseline_bad_rate,
            'phase_counts': phase_counts,
        },
        'results': out,
    }

    # Add compact ranking by test AUC.
    ranking = sorted(((k, v['AUC']) for k, v in out.items()), key=lambda x: x[1], reverse=True)
    result['ranking_by_test_auc'] = ranking

    with open(RUN_DIR / 'V309_results.json', 'w') as f:
        json.dump(result, f, indent=2)

    # Write report too.
    report = []
    report.append('# V309 — Component Ablation Test')
    report.append('')
    report.append('## Question')
    report.append('Which components inside the adaptive reachability law contribute the most to prediction and intervention behavior?')
    report.append('')
    report.append('## Hypothesis')
    report.append('Ablating one component should degrade discrimination if that factor carries unique information.')
    report.append('')
    report.append('## Method')
    report.append('Fixed-seed toy simulation, held-out evaluation, fixed D_c threshold, no tuning.')
    report.append('')
    report.append('## Controls')
    report.append(f"seeds={SEEDS[0]}..{SEEDS[-1]}, train_size={len(train)}, test_size={len(test)}")
    report.append('')
    report.append('## Results')
    report.append(json.dumps(result, indent=2))
    report.append('')
    report.append('## Interpretation')
    report.append('Ablations can be compared by test AUC and balanced accuracy; lower scores indicate a more necessary component.')
    report.append('')
    report.append('## Failure / Caveat')
    report.append('If scores cluster tightly, the composite may be redundant or the toy labels may be too easy.')
    report.append('')
    report.append('## Decision')
    report.append('continue')
    report.append('')
    report.append('## Next')
    report.append('Stress the weakest component under noisy and sparse topology variants.')
    (RUN_DIR / 'V309_report.md').write_text('\n'.join(report))

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
