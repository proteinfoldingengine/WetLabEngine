from pathlib import Path
import unittest

from evidence import git_blob_sha, verify_evidence
from fixtures import periodic_square_input, relabel_input, relabeled_edges
from operational_complex import ConnectionStatus, construct_operational_complex


class EvidenceTests(unittest.TestCase):
    def test_parent_evidence_blobs_are_exact(self):
        self.assertEqual(
            verify_evidence(),
            {
                "v15.41-design": "6d35aae0ccb6c2584d26d5a83d522b3cc7036728",
                "v15.41-erratum": "d40d03d9d2498ce54839b15dad00c1505c1a586a",
                "v15.41-results": "46cae26d91c709fdde4c5cc39cd3cf3908980e97",
                "v15.42-design": "91f2c66bea982b3180a07c61ccc4bef76e9c031d",
            },
        )

    def test_vendored_substrate_matches_certified_blobs(self):
        self.assertEqual(
            git_blob_sha(Path("exact_algebra.py")),
            "c67ea42b61321469f7735ce589f2e729b241666a",
        )
        self.assertEqual(
            git_blob_sha(Path("operational_complex.py")),
            "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
        )

    def test_fixture_constructs_exact_source_blind_carriers(self):
        for L in (5, 7):
            audit = construct_operational_complex(*periodic_square_input(L))
            self.assertEqual(audit.status, ConnectionStatus.IDENTIFIABLE)
            self.assertEqual(len(audit.complex.labels), L * L)
            self.assertEqual(len(audit.complex.cycles), L * L)

    def test_fixture_relabeling_carries_labels_without_changing_work(self):
        original = periodic_square_input(5)
        permutation = tuple(reversed(range(25)))
        changed = relabel_input(original, permutation)
        self.assertEqual(changed[0], permutation)
        self.assertEqual(
            sorted(map(sorted, changed[2])),
            sorted(map(sorted, relabeled_edges(original, permutation))),
        )


if __name__ == "__main__":
    unittest.main()
