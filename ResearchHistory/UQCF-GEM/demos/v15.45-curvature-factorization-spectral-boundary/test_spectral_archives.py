"""Archive binding and unmodified-formula even-period falsifiers for Task 3.

Even carriers here are explicitly mathematical fixtures, NOT newly admitted
v15.44 archived carriers. The frozen compact/derivative code stays unchanged.
"""
import json
import gzip
import unittest
from collections import deque
from fractions import Fraction as Q
from hashlib import sha1
from pathlib import Path
from types import SimpleNamespace

import evidence
from factorization import compact_operator
from spectral import scalar_operator, spectral_certificate, rational_rank, apply

HERE = Path(__file__).resolve().parent
J = ((Q(0), Q(-1)), (Q(1), Q(0)))
I = ((Q(1), Q(0)), (Q(0), Q(1)))


def pinned(path, expected):
    raw = path.read_bytes()
    actual = sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if actual != expected:
        raise ValueError('task3_pin_drift:'+path.name)
    return raw


def square_fixture(L):
    """Test-only extension of the unchanged square formula, not identification."""
    labels = tuple(range(L*L))
    edges, directions, adjacency, cycles = [], [], [], []
    def at(x,y):
        return (x % L)*L+y % L
    for x in range(L):
        for y in range(L):
            row = []
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                row.append(at(x+dx,y+dy))
                edges.append((at(x,y), row[-1]))
                directions.append((Q(dx), Q(dy)))
            adjacency.append(tuple(row))
            cycles.append((at(x,y),at(x+1,y),at(x+1,y+1),at(x,y+1)))
    c = SimpleNamespace(labels=labels, directed_edges=tuple(edges),
        direction_classes=tuple(directions), adjacency=tuple(adjacency), cycles=tuple(cycles))
    b = SimpleNamespace(flat=True, labels=labels, directed_edges=tuple(edges),
        transports=tuple((edge,I) for edge in edges))
    return SimpleNamespace(complex=c, baseline=b, L=L, scale=Q(1))


def square_chart(carrier):
    """Derive the periodic coordinates from directions; never from label numbers."""
    L = carrier.L
    c = carrier.complex
    outgoing = {label: [] for label in c.labels}
    directions = dict(zip(c.directed_edges,c.direction_classes,strict=True))
    for (a,b),d in directions.items():
        if d not in ((Q(1),Q(0)),(Q(-1),Q(0)),(Q(0),Q(1)),(Q(0),Q(-1))):
            raise ValueError('non_square_direction')
        outgoing[a].append((b,d))
    coords = {c.labels[0]: (0,0)}
    todo = deque((c.labels[0],))
    while todo:
        a = todo.popleft()
        x,y = coords[a]
        for b,d in outgoing[a]:
            new = ((x+int(d[0]))%L,(y+int(d[1]))%L)
            if b in coords and coords[b] != new:
                raise ValueError('inconsistent_square_chart')
            if b not in coords:
                coords[b] = new
                todo.append(b)
    if len(coords) != L*L or len(set(coords.values())) != L*L:
        raise ValueError('nonbijective_square_chart')
    if any(matrix != I for _,matrix in carrier.baseline.transports):
        raise ValueError('task3_requires_inherited_identity_presentation')
    return coords, directions


def full_from_chart(carrier):
    coords, directions = square_chart(carrier)
    L = carrier.L
    S = scalar_operator(L)
    rows = []
    for cycle in carrier.complex.cycles:
        points = {coords[v] for v in cycle}
        anchors = [(x,y) for x,y in points if
            {(x,y),((x+1)%L,y),((x+1)%L,(y+1)%L),(x,(y+1)%L)} == points]
        if len(anchors) != 1:
            raise ValueError('nonunique_face_anchor')
        x,y = anchors[0]
        a,b = directions[(cycle[0],cycle[1])],directions[(cycle[1],cycle[2])]
        sign = a[0]*b[1]-a[1]*b[0]
        if sign not in (Q(-1),Q(1)):
            raise ValueError('non_square_oriented_face')
        field_row = tuple(sign*S[x*L+y][coords[label][0]*L+coords[label][1]]
                          for label in carrier.complex.labels)
        rows.extend(tuple(J[i][j]*v for v in field_row) for i in range(2) for j in range(2))
    return tuple(rows)


class SpectralArchiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pinned(HERE/'factorization.py', '32da787647f886e942b5719115625212601f950e')
        pinned(HERE/'evidence.py', '342ab62116a03ca98bb9f54cdb893d87c7e48ae5')
        evidence.verify_evidence()
        raw = pinned(HERE.parent/'v15.44-intrinsic-curvature-interpretation/docs/RESULTS.json',
                     'f40002f415515832741a21e4885b7b2f9d7f337e')
        ledger = json.loads(raw)
        if ledger['status'] != 'INTRINSIC_CURVATURE_CHARACTERIZED':
            raise ValueError('parent_not_characterized')
        cls.records = ledger['scientific_verdict']['carriers']
        cls.carriers = evidence.actual_carriers()
        keys = [(c.L,str(c.scale)) for c in cls.carriers]
        if keys != [(5,'1'),(5,'7/3'),(7,'1'),(7,'7/3')]:
            raise ValueError('task3_archive_inventory')
        if [(c['L'],c['scale']) for c in cls.records] != keys:
            raise ValueError('task3_certificate_inventory')

    def test_all_archived_coefficients_ranks_and_kernels(self):
        receipts = []
        for c,record in zip(self.carriers,self.records,strict=True):
            with self.subTest(L=c.L,scale=c.scale):
                a = compact_operator(c)
                frozen = evidence.reference_operator(c)
                archived = record['operator']
                self.assertEqual(a, frozen)
                self.assertEqual(a.labels, tuple(archived['labels']))
                self.assertEqual(a.cycles, tuple(tuple(x) for x in archived['cycles']))
                self.assertEqual(a.entries,tuple(tuple(Q(x) for x in row) for row in archived['entries']))
                self.assertEqual(a.entries, full_from_chart(c))
                expected = spectral_certificate(c.L)
                actual_rank = rational_rank(a.entries)
                cert = record['certificate']
                self.assertEqual((actual_rank,len(a.labels)-actual_rank),
                                 (cert['rank'],cert['nullity']))
                self.assertEqual(actual_rank, expected['rank'])
                self.assertEqual(record['centered_kernel_dimension'],expected['centered_nullity'])
                basis = tuple(tuple(Q(row[j]) for row in cert['null_basis'])
                              for j in range(cert['nullity']))
                self.assertEqual(rational_rank(basis),cert['nullity'])
                for v in basis:
                    self.assertEqual(apply(a.entries,v),(Q(0),)*len(a.entries))
                receipts.append({'L':c.L,'scale':str(c.scale),'rank':actual_rank,
                    'nullity':expected['nullity'],'centered_nullity':expected['centered_nullity'],
                    'scalar_entry_comparisons':len(a.entries)*len(a.labels)})
        print('TASK3_ARCHIVE_RECEIPTS '+json.dumps(receipts,sort_keys=True))

    def test_even_fixtures_against_unmodified_compact_and_frozen_derivative(self):
        receipts = []
        for L in (6,8):
            with self.subTest(L=L):
                c = square_fixture(L)
                a = compact_operator(c)
                frozen = evidence.reference_operator(c)
                self.assertEqual(a, frozen)
                self.assertEqual(a.entries,full_from_chart(c))
                cert = spectral_certificate(L)
                self.assertEqual(rational_rank(a.entries),cert['rank'])
                for v in cert['kernel_basis']:
                    self.assertEqual(apply(frozen.entries,v),(Q(0),)*len(frozen.entries))
                receipts.append({'L':L,'carrier':'DECLARED_FORMULA_EXTENSION_FIXTURE',
                    'rank':cert['rank'],'nullity':cert['nullity'],
                    'centered_nullity':cert['centered_nullity'],
                    'scalar_entry_comparisons':len(a.entries)*len(a.labels)})
        print('TASK3_EVEN_RECEIPTS '+json.dumps(receipts,sort_keys=True))

    def test_chart_does_not_assume_numeric_label_coordinates(self):
        c = self.carriers[0]
        from presentations import _relabel_carrier
        changed,_ = _relabel_carrier(c,tuple(reversed(c.complex.labels)))
        self.assertEqual(full_from_chart(changed),compact_operator(changed).entries)

    def test_published_task3_certificate_replay(self):
        raw = gzip.decompress((HERE/'docs/TASK3_SPECTRAL.json.gz').read_bytes())
        expected = {'scope':'TASK3_ONLY_NOT_FULL_V1545_CERTIFICATION',
                    'certificates':[spectral_certificate(L) for L in (5,6,7,8)]}
        encoded = (json.dumps(expected,sort_keys=True,separators=(',',':'))+'\n').encode('ascii')
        self.assertEqual(raw,encoded)


if __name__ == '__main__':
    unittest.main()
