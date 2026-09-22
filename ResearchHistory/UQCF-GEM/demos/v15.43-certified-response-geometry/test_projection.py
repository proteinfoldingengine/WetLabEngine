from __future__ import annotations

import json
import tempfile
import unittest
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


FAMILIES = (
    "GLOBAL_BALANCE_COMPLETION",
    "DIRECT_INHERITANCE",
    "ONE_INCIDENCE_TRANSPORT",
    "MATCHED_DIAGONAL_BALANCE",
    "MATCHED_STEP2_BALANCE",
)
PARENT = "0f426fa28d22871ce042e39bf9704695ede8b336"


def _dependencies():
    manifest = json.loads(Path("dependencies.json").read_text())
    return tuple(sorted((item["path"], item["blob"]) for item in manifest["acquisition"].values()))


def _payload_wire(payload):
    return {
        "L": payload.L,
        "scale": str(payload.scale),
        "labels": list(payload.labels),
        "work": [[str(value) for value in row] for row in payload.work],
        "neighbors": [list(edge) for edge in payload.neighbors],
        "fields": [{"family": field.family, "response_index": field.response_index,
                    "values": [str(value) for value in field.values]} for field in payload.fields],
    }


def valid_projection_bytes():
    from projection import Field, Payload, Projection, canonical_bytes, encode_projection
    payloads = []
    for L, scale in ((5, Fraction(1)), (5, Fraction(7, 3)),
                     (7, Fraction(1)), (7, Fraction(7, 3))):
        count = L * L
        payloads.append(Payload(
            L, scale, tuple(range(count)),
            tuple(tuple(Fraction(i != j) for j in range(count)) for i in range(count)),
            tuple(sorted((i, (i + 1) % count) if i < (i + 1) % count
                         else ((i + 1) % count, i) for i in range(count))),
            tuple(Field(family, response, (Fraction(0),) * count)
                  for family in FAMILIES for response in range(count)),
        ))
    hashes = tuple(sha256(canonical_bytes(_payload_wire(payload))).hexdigest() for payload in payloads)
    return encode_projection(Projection(PARENT, _dependencies(), tuple(payloads), hashes))


def _mutate(change):
    wire = json.loads(valid_projection_bytes())
    change(wire)
    return json.dumps(wire).encode()


class ProjectionCodecTests(unittest.TestCase):
    def test_round_trip_is_canonical_and_immutable(self):
        from projection import decode_projection, encode_projection
        raw = valid_projection_bytes()
        value = decode_projection(raw)
        self.assertEqual(encode_projection(value), raw)
        self.assertIsInstance(value.payloads, tuple)

    def test_valid_but_noncanonical_json_rejected(self):
        from projection import decode_projection
        raw = json.dumps(json.loads(valid_projection_bytes())).encode()
        with self.assertRaisesRegex(ValueError, "noncanonical_json"):
            decode_projection(raw)

    def test_encode_revalidates_dataclass_contents(self):
        from dataclasses import replace
        from projection import encode_projection, decode_projection
        value = decode_projection(valid_projection_bytes())
        bad_payload = replace(value.payloads[0], labels=(1,) + value.payloads[0].labels[1:])
        with self.assertRaisesRegex(ValueError, "duplicate_labels"):
            encode_projection(replace(value, payloads=(bad_payload,) + value.payloads[1:]))

    def test_encode_rejects_list_backed_projection_payloads(self):
        from dataclasses import replace
        from projection import decode_projection, encode_projection
        value = decode_projection(valid_projection_bytes())
        with self.assertRaisesRegex(ValueError, "tuple_backing"):
            encode_projection(replace(value, payloads=list(value.payloads)))

    def test_duplicate_json_key_rejected(self):
        from projection import decode_projection
        raw = valid_projection_bytes().replace(b'"schema": ', b'"schema": "wrong",\n  "schema": ', 1)
        with self.assertRaisesRegex(ValueError, "duplicate_key"):
            decode_projection(raw)

    def test_injected_source_rejected(self):
        from projection import decode_projection
        with self.assertRaisesRegex(ValueError, "unknown_field"):
            decode_projection(_mutate(lambda w: w["payloads"][0].update(sources=[])))

    def test_missing_case_rejected_before_hashes(self):
        from projection import decode_projection
        with self.assertRaisesRegex(ValueError, "incomplete_cases"):
            decode_projection(_mutate(lambda w: w["payloads"].pop()))

    def test_duplicate_case_rejected_before_hashes(self):
        from projection import decode_projection
        with self.assertRaisesRegex(ValueError, "duplicate_case"):
            decode_projection(_mutate(lambda w: w["payloads"].__setitem__(1, w["payloads"][0])))

    def test_swapped_field_order_rejected_before_hashes(self):
        from projection import decode_projection
        def swap(w):
            w["payloads"][0]["fields"][0], w["payloads"][0]["fields"][1] = w["payloads"][0]["fields"][1], w["payloads"][0]["fields"][0]
        with self.assertRaisesRegex(ValueError, "wrong_field_order"):
            decode_projection(_mutate(swap))

    def test_float_rejected_before_hashes(self):
        from projection import decode_projection
        with self.assertRaisesRegex(ValueError, "invalid_type"):
            decode_projection(_mutate(lambda w: w["payloads"][0].__setitem__("L", 5.0)))

    def test_bool_rejected_before_hashes(self):
        from projection import decode_projection
        with self.assertRaisesRegex(ValueError, "invalid_type"):
            decode_projection(_mutate(lambda w: w["payloads"][0]["labels"].__setitem__(0, True)))

    def test_malformed_fraction_rejected(self):
        from projection import decode_projection
        with self.assertRaisesRegex(ValueError, "malformed_fraction"):
            decode_projection(_mutate(lambda w: w["payloads"][0]["fields"][0]["values"].__setitem__(0, "x/y")))

    def test_noncanonical_fraction_rejected(self):
        from projection import decode_projection
        with self.assertRaisesRegex(ValueError, "noncanonical_fraction"):
            decode_projection(_mutate(lambda w: w["payloads"][0]["fields"][0]["values"].__setitem__(0, "0/2")))

    def test_bad_payload_hash_rejected(self):
        from projection import decode_projection
        with self.assertRaisesRegex(ValueError, "payload_hash"):
            decode_projection(_mutate(lambda w: w["payload_hashes"].__setitem__(0, "0" * 64)))

    def test_wrong_dependency_list_rejected(self):
        from projection import decode_projection
        with self.assertRaisesRegex(ValueError, "dependency_list"):
            decode_projection(_mutate(lambda w: w.__setitem__("dependencies", [])))

    def test_duplicate_labels_rejected_before_hashes(self):
        from projection import decode_projection
        with self.assertRaisesRegex(ValueError, "duplicate_labels"):
            decode_projection(_mutate(lambda w: w["payloads"][0]["labels"].__setitem__(1, 0)))

    def test_nonzero_field_sum_rejected_before_hashes(self):
        from projection import decode_projection
        with self.assertRaisesRegex(ValueError, "nonzero_field_sum"):
            decode_projection(_mutate(lambda w: w["payloads"][0]["fields"][0]["values"].__setitem__(0, "1")))


class AcquisitionTests(unittest.TestCase):
    @staticmethod
    def modules(source_marker):
        def family(L, key, amplitude):
            count = L * L
            return SimpleNamespace(labels=tuple(range(count)), sources=(source_marker,) * count,
                                   responses=tuple((Fraction(0),) * count for _ in range(count)))
        generation = SimpleNamespace(FAMILY_KEYS=FAMILIES, response_family=family)
        def geometry(labels, sources, responses):
            count = len(labels)
            return SimpleNamespace(labels=labels,
                work=tuple(tuple(Fraction(i != j) for j in range(count)) for i in range(count)),
                neighbors=frozenset(frozenset((i, (i + 1) % count)) for i in range(count)))
        return generation, SimpleNamespace(construct_response_geometry=geometry)

    def test_source_only_metadata_is_excluded(self):
        import acquire
        left = acquire._project_modules(*self.modules("left"), PARENT, _dependencies())
        right = acquire._project_modules(*self.modules("right"), PARENT, _dependencies())
        self.assertEqual(left, right)
        self.assertNotIn(b"sources", left)

    def test_acquisition_uses_only_pinned_calls(self):
        import acquire
        generation, geometry = self.modules("source")
        generation.audit = lambda *args: (_ for _ in ()).throw(AssertionError("prohibited audit"))
        geometry.metric_passes = lambda *args: (_ for _ in ()).throw(AssertionError("prohibited audit"))
        with patch.object(acquire, "_verified_modules", return_value=(generation, geometry, PARENT, _dependencies())), \
             patch.object(acquire, "_verify_loaded_closure", return_value={}):
            projection = acquire.acquire_projection()
        self.assertEqual(len(projection.payloads), 4)

    def test_atomic_writer_leaves_complete_canonical_file(self):
        import acquire
        generation, geometry = self.modules("source")
        with tempfile.TemporaryDirectory() as directory, patch.object(
                acquire, "_verified_modules", return_value=(generation, geometry, PARENT, _dependencies())), \
             patch.object(acquire, "_verify_loaded_closure", return_value={}):
            target = Path(directory) / "inputs.json"
            acquire.write_projection(target)
            from projection import decode_projection, encode_projection
            self.assertEqual(encode_projection(decode_projection(target.read_bytes())), target.read_bytes())


if __name__ == "__main__":
    unittest.main()
