"""Exact ordered specification coverage, independently invoked by verifier."""
def verify_identities(records, expected):
    if not isinstance(records,list) or records != expected:
        raise ValueError('canonical case identities')
    return True
