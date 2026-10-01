"""Prospective supplied-only baseline; exact-universe rejection is not implemented."""
def verify_identities(records, expected):
    for identity in records:
        if identity not in expected:
            raise ValueError('unknown identity')
    return True
