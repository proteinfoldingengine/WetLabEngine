import mpmath as mp

from uqcf_codazzi_verification import (
    codazzi,
    det2,
    response_tensor,
    susceptibility,
)


def test_reported_audit_point():
    mp.mp.dps = 60
    M = response_tensor(mp.mpf("0.2"), mp.mpf("-0.15"), mp.mpf("0.7"))
    I = codazzi(mp.mpf("0.2"), mp.mpf("-0.15"), mp.mpf("0.7"))

    assert abs(M[0][0] - mp.mpf("1.38129946619327500003604689263")) < mp.mpf("1e-28")
    assert abs(M[0][1] - mp.mpf("1.35748327515301168689699113769")) < mp.mpf("1e-28")
    assert abs(M[1][1] - mp.mpf("1.39073195464899875795712611409")) < mp.mpf("1e-28")
    assert abs(I[0] - mp.mpf("-0.345896392762439037790290015984")) < mp.mpf("1e-28")
    assert abs(I[1] - mp.mpf("-0.320972490518245982182853398245")) < mp.mpf("1e-28")


def test_unbiased_point_is_codazzi_zero():
    mp.mp.dps = 60
    for J in ("0", "0.01", "0.1", "0.7"):
        I = codazzi(mp.mpf("0"), mp.mpf("0"), mp.mpf(J))
        assert max(abs(I[0]), abs(I[1])) < mp.mpf("1e-42")


def test_weak_coupling_susceptibility_is_full_rank():
    mp.mp.dps = 60
    J = mp.mpf("0.001")
    Xi = susceptibility(J)
    assert abs(det2(Xi)) > mp.mpf("1e-30")


def test_susceptibility_approaches_quarter_turn():
    mp.mp.dps = 60
    J = mp.mpf("0.001")
    Xi = susceptibility(J)
    scaled = [[Xi[i][j]/J**2 for j in range(2)] for i in range(2)]
    target = ((0, 1), (-1, 0))
    assert max(abs(scaled[i][j]-target[i][j]) for i in range(2) for j in range(2)) < mp.mpf("0.006")
