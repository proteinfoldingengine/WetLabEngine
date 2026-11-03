"""Independent C2 check: matrix-unit channel composition, Choi SVD, full-unitary trace."""
import json
import sys
import numpy as np

def require(ok, message):
    if not ok:
        raise ValueError(message)

PROVENANCE = {'scope': 'SUPPLIED_CHANNEL', 'native_bridge': 'NOT_DERIVED',
              'original_head': '23543a5b8c5f8938fe0d25c42be975296c8055fb'}

def verify(c):
    require(set(c) == {'schema', 'provenance', 'choi_rank', 'nonzero_choi_spectrum', 'cases'}, 'certificate fields')
    require(c['schema'] == 'thermal-C2-v1' and c['provenance'] == PROVENANCE, 'provenance')
    # Build the target as a composition of two erasures, independently of the producer's Kraus list.
    def erase(x, removed, owner):
        y = x.copy()
        y[removed, :] = 0
        y[:, removed] = 0
        y[owner, owner] += x[removed, removed]
        return y
    actions = []
    J = np.zeros((36, 36))
    for i in range(6):
        for j in range(6):
            x = np.zeros((6, 6)); x[i, j] = 1
            y = erase(erase(x, 2, 1), 4, 3)
            actions.append([[a, b, int(y[a, b])] for a, b in zip(*np.nonzero(y))])
            J[i*6:(i+1)*6, j*6:(j+1)*6] = y
    sv = np.linalg.svd(J, compute_uv=False)
    rank = int(np.count_nonzero(sv > 1e-10))
    require(type(c['choi_rank']) is int and c['choi_rank'] == rank == 3, 'Choi rank')
    require(c['nonzero_choi_spectrum'] == [4, 1, 1] and np.allclose(sv[:rank], c['nonzero_choi_spectrum'], rtol=0, atol=1e-12), 'Choi spectrum')
    require(isinstance(c['cases'], list) and len(c['cases']) == 2, 'case count')
    require([x['id'] for x in c['cases']] == ['A-pure-E2', 'A-pure-E3'], 'case identity/order')
    for row, d in zip(c['cases'], (2, 3)):
        require(set(row) == {'id', 'dE', 'rank_tau', 'fan_in', 'local_bound_satisfied', 'pure_kraus_capacity', 'realizable_R_untouched', 'witness'}, 'case fields')
        require(type(row['dE']) is int and row['dE'] == d and row['rank_tau'] == 1 and row['fan_in'] == [2, 2], 'case premises')
        require(row['local_bound_satisfied'] is True and 2 <= d, 'local rank bound')
        require(row['pure_kraus_capacity'] == d, 'pure bath capacity')
        require(row['realizable_R_untouched'] is (rank <= d), 'global realization claim')
        if d == 2:
            require(row['witness'] is None, 'E2 has no witness')
            continue
        w = row['witness']
        require(isinstance(w, dict) and set(w) == {'permutation', 'matrix_unit_actions'}, 'witness fields')
        perm = w['permutation']
        require(all(type(x) is int for x in perm) and sorted(perm) == list(range(18)), 'full permutation')
        expected = list(range(18))
        for a, b in ((6, 4), (12, 11)):
            expected[a], expected[b] = expected[b], expected[a]
        require(perm == expected, 'frozen witness slots')
        U = np.eye(18)[:, perm]
        require(np.array_equal(U.T @ U, np.eye(18)), 'full-space unitarity')
        require(w['matrix_unit_actions'] == actions, 'all 36 target actions')
        blank = np.diag([1, 0, 0])
        for i in range(6):
            for j in range(6):
                x = np.zeros((6, 6)); x[i, j] = 1
                evolved = U @ np.kron(x, blank) @ U.T
                reduced = np.trace(evolved.reshape(6, 3, 6, 3), axis1=1, axis2=3)
                require(np.array_equal(reduced, J[i*6:(i+1)*6, j*6:(j+1)*6]), 'unitary channel action')
    return {'status': 'PASS', 'method': 'composed-matrix-units/Choi-SVD/full-unitary-partial-trace',
            'cases': 2, 'matrix_units_checked': 36, 'choi_rank': rank,
            'native_bridge': 'NOT_DERIVED'}

if __name__ == '__main__':
    print(json.dumps(verify(json.load(open(sys.argv[1]))), indent=2, sort_keys=True))
