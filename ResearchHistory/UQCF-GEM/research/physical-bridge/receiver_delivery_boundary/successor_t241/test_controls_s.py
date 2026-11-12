"""Successor rejecting controls C1-C8 (CORRECTION_T241 section 4, CORRECTION_T242 section 4).
Each mutation must make verify_s.py return RED. Usage (from this directory): test_controls_s.py certificate.json produce_s.py"""
import copy, io, json, os, sys, tempfile, contextlib
import verify_s as vs


def run(cert, prod, patch=None):
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
        json.dump(cert, f)
        path = f.name
    saved = {k: getattr(vs, k) for k in ('F5', 'FY')}
    if patch:
        patch()
    sys.argv = ['verify_s.py', path, prod]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            vs.main()
        code = 0
    except SystemExit as e:
        code = e.code
    except Exception as e:
        code = 'exception:' + type(e).__name__
    finally:
        for k, v in saved.items():
            setattr(vs, k, v)
        os.unlink(path)
    return code


def main():
    cert = json.load(open(sys.argv[1]))
    prod = sys.argv[2]
    res = {'baseline_accepts': run(cert, prod) == 0}

    def mut(name, fn=lambda c: None, patch=None):
        c = copy.deepcopy(cert)
        fn(c)
        res[name] = run(c, prod, patch) != 0

    # C1: the withdrawn "C" claim (W_E contrast equal to W_R's 1/5 on the psi interface)
    mut('C1_withdrawn_constant_contrast', lambda c: c['V1']['Delta'].__setitem__('W_E', '1/5'))
    # C2: withdrawn RD-5 pre-event S-blindness for z'_+-
    mut('C2_pre_event_blindness', lambda c: c['V3']['pre_pi_p'].__setitem__('plus', '1/5'))
    # C3: withdrawn section-5 sentence (equal W_R/W_E statistics for the fixed full-K effect)
    mut('C3_fixed_effect_invariance', lambda c: c['V4'].__setitem__('W_R', '0'))
    # C4: one Y-block perturbed off scalar by a fixed rank-one term, certificate still claiming invariance
    orig_F5 = vs.F5
    def perturbed(a, b):
        x = orig_F5(a, b)
        if a == b == ('p', (0, 1)):
            x = x + vs.Q2(vs.Fr(1, 6))
        return x
    mut('C4_nonscalar_Y_block_claimed_invariant', patch=lambda: setattr(vs, 'F5', perturbed))
    # C5: corrupted producer output (one altered rational)
    mut('C5_corrupted_rational', lambda c: c['V2']['psi']['Delta'].__setitem__('4/5', '43/501'))
    # C6: W_R and W_E labels swapped in V4
    def swap(c):
        c['V4']['W_R'], c['V4']['W_E'] = c['V4']['W_E'], c['V4']['W_R']
    mut('C6_swapped_V4_labels', swap)
    # C7: Dot's F asserted to lie in B(H_S) (x) 1_K / A meets B(H_S)(x)1_K nontrivially
    mut('C7a_F_in_product', lambda c: c['V6'].__setitem__('in_BHS_tensor_1K', True))
    mut('C7b_nontrivial_intersection', lambda c: c['V6'].__setitem__('b_nonzero_solution_exists', True))
    # C8: nonscalar Y-block for Dot's F, or a pair contrast other than 1/20 on a listed realization
    mut('C8a_nonscalar_Y_block', lambda c: c['V6']['diag_blocks'].__setitem__(1, 'nonscalar'))
    mut('C8b_wrong_pair_contrast', lambda c: c['V6']['pair_contrast'].__setitem__('W_R', '1/5'))
    # integrity
    mut('false_producer_hash', lambda c: c.__setitem__('producer_sha256', '0' * 64))
    mut('dropped_section', lambda c: c.pop('V7'))
    res['all_controls_rejected'] = all(res.values())
    print(json.dumps(res, indent=1, sort_keys=True))
    sys.exit(0 if res['all_controls_rejected'] else 1)


if __name__ == '__main__':
    main()
