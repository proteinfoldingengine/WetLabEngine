import gzip
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

import producer
import independent


class StarCarrier(unittest.TestCase):
    def make(self, directory):
        path = pathlib.Path(directory) / "certificate.json"
        producer.build(path, fixture=True)
        return path

    def test_fixture_reconstructs(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.make(directory)
            self.assertTrue(independent.verify(path, fixture=True)["accepted"])

    def test_frozen_complete_universe_size(self):
        configs = list(producer.configurations())
        self.assertEqual(configs, list(independent.configurations()))
        states = sum((2 ** n) ** m for m, n, _ in configs)
        toggles = sum((2 ** n) ** m * m * n for m, n, _ in configs)
        self.assertEqual(states, 148480)
        self.assertEqual(toggles, 2302976)

    def test_tau_equals_h_for_every_fixture_state(self):
        for code in range(8 ** 3):
            masks = producer.decode(code, 3, 3)
            self.assertEqual(producer.tau_c3(masks, 3), producer.h_star(masks, 3))

    def mutate_row(self, transform):
        with tempfile.TemporaryDirectory() as directory:
            path = self.make(directory)
            stream = pathlib.Path(str(path) + ".identities.jsonl.gz")
            with gzip.open(stream, "rt") as source:
                rows = [json.loads(line) for line in source]
            transform(rows)
            with stream.open("wb") as raw:
                with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as target:
                    for row in rows:
                        target.write((json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n").encode())
            data = json.loads(path.read_text())
            import hashlib
            data["identity_archive_sha256"] = hashlib.sha256(stream.read_bytes()).hexdigest()
            path.write_text(json.dumps(data))
            with self.assertRaises(AssertionError):
                independent.verify(path, fixture=True)

    def test_reject_wrong_h(self):
        self.mutate_row(lambda rows: rows[0].__setitem__("h", 99))

    def test_reject_corrupted_child_order(self):
        def change(rows):
            row = next(r for r in rows if r["kind"] == "state" and len(set(r["masks"])) > 1)
            row["masks"][0], row["masks"][1] = row["masks"][1], row["masks"][0]
        self.mutate_row(change)

    def test_reject_omitted_floor(self):
        def change(rows):
            row = next(r for r in rows if r["kind"] == "state" and not r["floor_ok"])
            row["floor_ok"] = True
        self.mutate_row(change)

    def test_reject_omitted_band(self):
        def change(rows):
            row = next(r for r in rows if r["kind"] == "state" and r["floor_ok"] and r["tau"] < 3)
            row["admitted"] = True
        self.mutate_row(change)

    def test_reject_edge_status_corruption(self):
        def change(rows):
            row = next(r for r in rows if r["kind"] == "transition" and not r["c3"])
            row["c3"] = row["star"] = True
            row["reason"] = "ACCEPTED"
        self.mutate_row(change)

    def test_reject_truncation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.make(directory)
            stream = pathlib.Path(str(path) + ".identities.jsonl.gz")
            stream.write_bytes(stream.read_bytes()[:-20])
            with self.assertRaises(AssertionError):
                independent.verify(path, fixture=True)

    def test_optimized_runtime_rejection(self):
        root = pathlib.Path(__file__).parent
        for module in ("producer", "independent"):
            for flag in ("-O", "-OO"):
                result = subprocess.run(
                    [sys.executable, flag, "-c", "import " + module],
                    cwd=root, capture_output=True, text=True,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("requires assertions", result.stderr)


if __name__ == "__main__":
    unittest.main()
