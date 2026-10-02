"""Prospective aggregate/reproduction rejection contracts."""
import copy
import sys
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from publication import check_partition,check_required_diagnostics,compare_reproduction

class Publication(unittest.TestCase):
    def shards(self):
        return [{'shard':i,'shards':8,'start':i*2,'stop':i*2+2,'total':16,'whole_universe_sha256':'a'*64,'identity_sha256':str(i)*64,'scope':'all'} for i in range(8)]

    def test_complete_partition(self):
        self.assertEqual(check_partition(self.shards()),[])

    def test_missing_shard_rejected(self):
        self.assertTrue(check_partition(self.shards()[:-1]))

    def test_duplicate_shard_rejected(self):
        s=self.shards();s[-1]=s[-2]
        self.assertTrue(check_partition(s))

    def test_overlapping_interval_rejected(self):
        s=self.shards();s[3]['start']-=1
        self.assertTrue(check_partition(s))

    def test_mismatched_universe_rejected(self):
        s=self.shards();s[3]['whole_universe_sha256']='b'*64
        self.assertTrue(check_partition(s))

    def test_empty_mechanism_category_rejected(self):
        self.assertTrue(check_required_diagnostics({}))

    def test_equal_scientific_reproduction(self):
        self.assertEqual(compare_reproduction({'a':'a'*64},{'a':'a'*64}),[])

    def test_scientific_byte_change_rejected(self):
        self.assertTrue(compare_reproduction({'a':'a'*64},{'a':'b'*64}))

    def test_missing_reproduction_file_rejected(self):
        self.assertTrue(compare_reproduction({'a':'a'*64},{}))
