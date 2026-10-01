"""Exact identity equality, never coverage inferred from supplied records."""
import json
def verify_identities(actual,expected):
    if json.dumps(actual,separators=(',',':'))!=json.dumps(expected,separators=(',',':')):
        raise ValueError('INCOMPLETE: exact ordered identity coverage')
