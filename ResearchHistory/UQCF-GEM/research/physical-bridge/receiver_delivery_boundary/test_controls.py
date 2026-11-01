"""T-240 rejecting controls: each mutation must make verify.py return RED (exit 1).
Usage: test_controls.py certificate.json produce.py   (run from this directory)"""
import copy, io, json, os, sys, tempfile, contextlib
import verify


def run(cert, prod, fam=None):
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
        json.dump(cert, f)
        path = f.name
    saved = verify.FAM
    if fam is not None:
        verify.FAM = fam
    sys.argv = ['verify.py', path, prod]
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            verify.main()
        code = 0
    except SystemExit as e:
        code = e.code
    except Exception as e:  # out-of-scope or malformed input also counts as rejection
        code = 'exception:' + type(e).__name__
    finally:
        verify.FAM = saved
        os.unlink(path)
    return code


def main():
    cert = json.load(open(sys.argv[1]))
    prod = sys.argv[2]
    results = {'baseline_accepts': run(cert, prod) == 0}
    def mut(name, fn, fam=None, prod_path=None):
        c = copy.deepcopy(cert)
        fn(c)
        results[name] = run(c, prod_path or prod, fam) != 0
    mut('wrong_contrast_value', lambda c: c['records'][0]['contrast']['W_R'].__setitem__('TR', '1/7'))
    mut('missing_record', lambda c: c['records'].pop(3))
    mut('duplicated_record', lambda c: c['records'].append(copy.deepcopy(c['records'][5])))
    def subst(c):
        a = next(i for i, r in enumerate(c['records']) if r['pair'] == 'canonical' and r['partition'] == 'o|p|uv')
        b = next(r for r in c['records'] if r['pair'] == 'removed_summand' and r['partition'] == 'o|p|uv')
        c['records'][a] = dict(copy.deepcopy(b), pair='canonical')
    mut('substituted_pair', subst)
    fam_bad = dict(verify.FAM); fam_bad['W_E'] = (verify.vec([(1, 1)]), verify.vec([(1, 2)]))
    mut('non_implementing_realization', lambda c: None, fam=fam_bad)
    fam_noniso = dict(verify.FAM); fam_noniso['W_M'] = (verify.vec([(1, 0)]), verify.vec([(1, 0)]))
    mut('non_isometric_realization', lambda c: None, fam=fam_noniso)
    def blindflip(c):
        r = next(r for r in c['records'] if r['pair'] == 'canonical' and r['partition'] == 'o|p|uv')
        r['initially_blind'] = False
    mut('false_blindness_flag', blindflip)
    mut('false_producer_hash', lambda c: c.__setitem__('producer_sha256', '0' * 64))
    mut('dropped_partition', lambda c: c.__setitem__('records', [r for r in c['records'] if r['partition'] != 'op|uv']))
    mut('non_orthogonal_U', lambda c: c['membership']['W_M']['U'][1].__setitem__(1, '-4/5'))
    results['all_controls_rejected'] = all(v for k, v in results.items())
    print(json.dumps(results, indent=1, sort_keys=True))
    sys.exit(0 if results['all_controls_rejected'] else 1)


if __name__ == '__main__':
    main()
