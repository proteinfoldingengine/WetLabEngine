"""v15.46 Stage A: pin source evidence without certifying its physical meaning.

Only reads declared files. No imports of source artifacts, matrix logarithms,
geometry execution, selection rule, or inferred native provenance.
"""
from __future__ import annotations
import argparse
from hashlib import sha1
import json
from pathlib import Path
import re
import stat

HERE = Path(__file__).resolve().parent
INVENTORY_BLOB = 'fadf983aee8aae196d2e8a960673901d03c994f3'
INVENTORY_SCHEMA = 'uqcf-v1546-scoped-input-inventory-v1'
INVENTORY_SCOPE = 'DECLARED_PINNED_SOURCE_REVIEW_NOT_EXHAUSTIVE_ARCHIVE_ABSENCE_PROOF'
PACKET_SCHEMA = 'uqcf-v1546-source-interface-submissions-v1'
PACKET_SCOPE = 'SUBMITTED_WITNESSES_ONLY_NOT_EXHAUSTIVE_ARCHIVE_SCAN'
COMPONENTS = ('joint_state', 'overlap_inclusions', 'support_domain',
              'occurrence_link', 'coupling_law', 'linearity_law', 'provenance_derivation')
KINDS = ('native_claim', 'supplied_hypothesis', 'diagnostic_fixture')


def git_blob(raw: bytes) -> str:
    return sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def canonical_bytes(value) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(',', ':'),
                       ensure_ascii=True, allow_nan=False)+'\n').encode('ascii')


def decode(raw: bytes):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate_json_key:'+key)
            result[key] = value
        return result
    def invalid_constant(value):
        raise ValueError('nonfinite_json:'+value)
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=unique,
                          parse_constant=invalid_constant)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError('invalid_json') from exc


def _keys(value, wanted, error):
    if type(value) is not dict or set(value) != set(wanted):
        raise ValueError(error)


def _text(value):
    return type(value) is str and bool(value.strip())


def read_pin(root: Path, pin: dict) -> dict:
    _keys(pin, ('path', 'git_blob_sha'), 'invalid_pin')
    name, expected = pin['path'], pin['git_blob_sha']
    if type(expected) is not str or not re.fullmatch('[0-9a-f]{40}', expected):
        raise ValueError('invalid_pin')
    if (not _text(name) or '\\' in name or '\0' in name or
            any(part in ('', '.', '..') for part in name.split('/'))):
        raise ValueError('unsafe_path')
    root = Path(root).resolve(strict=True)
    path = root
    for component in name.split('/'):
        path = path/component
        if path.is_symlink():
            raise ValueError('symlink_source:'+name)
    if not path.is_file():
        raise ValueError('missing_source:'+name)
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError('nonregular_source:'+name)
    raw = path.read_bytes()
    actual = git_blob(raw)
    if actual != expected:
        raise ValueError('source_blob_mismatch:'+name)
    return {'path': name, 'git_blob_sha': actual, 'bytes': len(raw)}


def verify_sources(root: Path, inventory: dict) -> list[dict]:
    _keys(inventory, ('schema','scope','repository_head','authorship','joint_states_present',
        'native_input_status','coupling_status','physical_source_law_adopted',
        'source_correspondence','Pillar_3','sources'), 'inventory_schema')
    if (inventory['schema'] != INVENTORY_SCHEMA or inventory['scope'] != INVENTORY_SCOPE
            or inventory['authorship'] != 'AUTHOR_REVIEW_NOT_INDEPENDENT_REVIEW'
            or inventory['physical_source_law_adopted'] is not False
            or inventory['source_correspondence'] != 'NOT_EVALUATED'
            or inventory['Pillar_3'] != 'OPEN'
            or type(inventory['joint_states_present']) is not bool
            or type(inventory['repository_head']) is not str
            or not re.fullmatch('[0-9a-f]{40}', inventory['repository_head'])
            or not _text(inventory['native_input_status'])
            or not _text(inventory['coupling_status'])
            or type(inventory['sources']) is not list or not inventory['sources']):
        raise ValueError('inventory_schema')
    keys, paths = set(), set()
    for source in inventory['sources']:
        _keys(source, ('key','path','git_blob_sha','inspection','interpretation'), 'source_schema')
        if any(not _text(source[k]) for k in ('key','path','inspection','interpretation')):
            raise ValueError('source_schema')
        if source['key'] in keys or source['path'] in paths:
            raise ValueError('duplicate_source')
        keys.add(source['key']); paths.add(source['path'])
    receipts = []
    for source in inventory['sources']:
        receipt = read_pin(root, {k:source[k] for k in ('path','git_blob_sha')})
        receipts.append(dict(receipt, key=source['key']))
    return sorted(receipts, key=lambda item: item['key'])


def assess_submission(root: Path, record: dict) -> dict:
    _keys(record, ('record_id','provenance_kind','components'), 'record_schema')
    if (not _text(record['record_id']) or record['provenance_kind'] not in KINDS
            or type(record['components']) is not dict
            or not set(record['components']) <= set(COMPONENTS)):
        raise ValueError('record_schema')
    missing, receipts = [], []
    for component in COMPONENTS:
        pin = record['components'].get(component)
        if pin is None:
            missing.append(component)
        else:
            receipts.append(dict(read_pin(root,pin), component=component))
    # File identity does not establish that a file contains a valid proof,
    # state, overlap inclusion or physical coupling. Do not promote it here.
    return {'record_id':record['record_id'], 'provenance_kind':record['provenance_kind'],
            'missing_components':missing, 'evidence_receipts':receipts,
            'status':('MISSING_REQUIRED_EVIDENCE' if missing else
                      'EVIDENCE_ATTACHED_SEMANTIC_VALIDATION_REQUIRED'),
            'native_provenance_certified':False, 'interface_admitted':False}


def preflight(root: Path, inventory_raw: bytes, packet_raw: bytes, *, inventory_pin: str) -> dict:
    if git_blob(inventory_raw) != inventory_pin:
        raise ValueError('inventory_pin_mismatch')
    inventory = decode(inventory_raw)
    receipts = verify_sources(root,inventory)
    packet = decode(packet_raw)
    _keys(packet, ('schema','scope','submissions'), 'packet_schema')
    if (packet['schema'] != PACKET_SCHEMA or packet['scope'] != PACKET_SCOPE
            or type(packet['submissions']) is not list):
        raise ValueError('packet_schema')
    records, ids = [], set()
    for record in packet['submissions']:
        assessed = assess_submission(root,record)
        if assessed['record_id'] in ids:
            raise ValueError('duplicate_record_id')
        ids.add(assessed['record_id']); records.append(assessed)
    complete = sum(not record['missing_components'] for record in records)
    return {
        'schema':'uqcf-v1546-evidence-preflight-v1',
        'scope':'STAGE_A_EVIDENCE_AND_SUBMISSION_CHECK_NOT_FULL_SOURCE_ADMISSION',
        'status':('EVIDENCE_PINS_VERIFIED_NO_COMPLETE_WITNESS_SUBMITTED' if not complete
                  else 'EVIDENCE_PINS_VERIFIED_SEMANTIC_VALIDATION_PENDING'),
        'inventory_git_blob':git_blob(inventory_raw),
        'submissions_git_blob':git_blob(packet_raw),
        'computed':{'source_files_verified':len(receipts), 'source_receipts':receipts,
                    'submitted_records':len(records), 'complete_reference_packets':complete},
        'submissions':records,
        'first_unmet_stage':('A_NATIVE_INPUT_WITNESS' if not complete else
                             'B_OPERATOR_DOMAIN_AND_PROVENANCE'),
        'required_components':list(COMPONENTS),
        'interface_admitted':False, 'source_value':'NOT_EVALUATED',
        'later_stages':'NOT_EXECUTED',
        'reviewed_claims':{'status':'AUTHORED_INVENTORY_NOT_MACHINE_PROOF',
                           'inventory_scope':inventory['scope'],
                           'native_input_status':inventory['native_input_status'],
                           'coupling_status':inventory['coupling_status'],
                           'joint_states_present':inventory['joint_states_present']},
        'claims':{'source_correspondence':'NOT_EVALUATED','Pillar_3':'OPEN',
                  'physical_source_law_adopted':False,'full_v1546_certification':False,
                  'archive_absence_proved':False, 'physical_gravity':False},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--submissions',type=Path,default=HERE/'docs/SOURCE_INTERFACE_SUBMISSIONS.json')
    output = parser.add_mutually_exclusive_group(required=True)
    output.add_argument('--out',type=Path)
    output.add_argument('--check',type=Path)
    args = parser.parse_args()
    result = preflight(args.root,(HERE/'docs/INPUT_TYPE_INVENTORY.json').read_bytes(),
                       args.submissions.read_bytes(),inventory_pin=INVENTORY_BLOB)
    raw = canonical_bytes(result)
    if args.out is not None:
        args.out.write_bytes(raw)
    elif args.check.read_bytes() != raw:
        raise SystemExit('stage_a_replay_mismatch')
    print(raw.decode('ascii'),end='')


if __name__=='__main__': main()
