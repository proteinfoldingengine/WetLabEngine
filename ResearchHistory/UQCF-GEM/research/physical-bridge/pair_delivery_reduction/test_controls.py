#!/usr/bin/env python3
"""T-235 rejecting controls: each tampered certificate must be REJECTED by verify.verify.
Usage: test_controls.py CERT.json PRODUCER.py ; exit 0 iff the honest cert passes and every tamper fails."""
import copy
import json
import sys
import verify as V

def tampers(c):
    t = {}
    x = copy.deepcopy(c); x['P_cases'].pop(); t['missing_P_case'] = x
    x = copy.deepcopy(c); x['O_cases'].pop(0); t['missing_O_case'] = x
    x = copy.deepcopy(c); x['P_cases'].append(copy.deepcopy(x['P_cases'][0])); t['duplicated_P_case'] = x
    x = copy.deepcopy(c); x['O_cases'].append(copy.deepcopy(x['O_cases'][3])); t['duplicated_O_case'] = x
    x = copy.deepcopy(c); x['P_cases'][5]['key'] = x['P_cases'][6]['key']; t['substituted_key'] = x
    x = copy.deepcopy(c); r = x['P_cases'][-1]; r['v'], r['u'] = r['u'], r['p']; t['invalid_fork_state'] = x
    x = copy.deepcopy(c); r = x['P_cases'][-1]; r['vertices'] = r['vertices'][:1] + [[9, 9]] + r['vertices'][2:]; t['non_prefix_carrier'] = x
    x = copy.deepcopy(c); x['P_cases'][2]['basis'][0]['post'][0] = '7/5'; t['wrong_post_value'] = x
    x = copy.deepcopy(c); b = x['P_cases'][2]['basis'][0]; b['c'] = '1/3' if b['c'] != '1/3' else '1/7'; t['wrong_c'] = x
    x = copy.deepcopy(c); x['P_cases'][4]['dim'] += 1; t['wrong_P_dim'] = x
    x = copy.deepcopy(c); x['O_cases'][9]['dim'] += 1; t['wrong_O_dim'] = x
    x = copy.deepcopy(c); x['P_cases'][1]['witness']['tot']['kappa'] = '0'; t['wrong_kappa'] = x
    x = copy.deepcopy(c); x['P_cases'][1]['cone_total_control']['C_p']['post'] = '1/5'; t['wrong_control_value'] = x
    x = copy.deepcopy(c); x['tree_counts']['7'] = 47; t['false_coverage_count'] = x
    x = copy.deepcopy(c); x['producer_sha256'] = '0' * 64; t['false_provenance'] = x
    x = copy.deepcopy(c); x['O_cases'][9]['carriers'] -= 1; t['false_carrier_coverage'] = x
    return t

def main():
    cert = json.load(open(sys.argv[1]))
    prod = open(sys.argv[2], 'rb').read()
    out = {}
    try:
        V.verify(cert, prod); out['honest'] = 'ACCEPTED'
    except V.Reject as e:
        out['honest'] = 'REJECTED: ' + str(e)
    for name, bad in sorted(tampers(cert).items()):
        try:
            V.verify(bad, prod); out[name] = 'ACCEPTED'
        except (V.Reject, KeyError, IndexError, ValueError, ZeroDivisionError) as e:
            out[name] = 'REJECTED: ' + type(e).__name__ + ': ' + str(e)
    ok = out['honest'] == 'ACCEPTED' and all(v.startswith('REJECTED') for k, v in out.items() if k != 'honest')
    out['controls_total'] = len(out) - 1
    out['status'] = 'GREEN' if ok else 'RED'
    sys.stdout.write(json.dumps(out, sort_keys=True, indent=1) + '\n')
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
