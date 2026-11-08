"""Read archived outputs only; this does not rerun or reconstruct V1696.6."""
import base64
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
NAME = 'V1696_6_hardened_pair_class_signature_python_test_package.zip'
path = ROOT / 'originals' / NAME
raw = path.read_bytes()
sha256 = lambda b: hashlib.sha256(b).hexdigest()
members = []
tables = {}
with zipfile.ZipFile(path) as z:
    for info in z.infolist():
        data = z.read(info.filename)
        entry = {'name': info.filename, 'bytes': len(data), 'sha256': sha256(data)}
        decoded = data.decode('utf-8')
        if info.filename.endswith('.csv'):
            reader = csv.DictReader(io.StringIO(decoded))
            rows = list(reader)
            tables[info.filename] = rows
            entry.update(columns=reader.fieldnames, rows=len(rows))
        elif info.filename.endswith('.json'):
            json.loads(decoded)
        members.append(entry)
    manifest_equals_summary = z.read('run_manifest.json') == z.read('V1696_6_SUMMARY.json')
audit = tables['hardened_pair_class_audits.csv']
nulls = tables['hardened_pair_class_nulls.csv']
residuals = tables['hardened_pair_class_residuals.csv']
post = (ROOT / 'V1696_7_POSTMORTEM.json').read_bytes()
report = {
    'purpose': 'Original archive inspection, not historical execution or native-bridge certification',
    'archive': {'name': NAME, 'bytes': len(raw), 'sha256': sha256(raw),
        'git_blob_sha1': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),
        'library_file_id': 'libfile_860fb7cb950c8191a0e99818c1a8a15f'},
    'members': members,
    'manifest_equals_summary_bytes': manifest_equals_summary,
    'support_count_frequencies': dict(collections.Counter(x['support_nonzero'] for x in audit)),
    'coarse_class_defined_frequencies': dict(collections.Counter(x['coarse_class_defined'] for x in residuals)),
    'support_shuffle_comparisons': dict(collections.Counter(x['valid_beats_null'] for x in nulls if x['null_family']=='N_support_class_shuffle')),
    'postmortem_transcription': {'name': 'V1696_7_POSTMORTEM.json',
        'library_file_id': 'libfile_e537fcd07ed88191844233ac3cde0ac4',
        'file_id': 'file_00000000c238720ebb3ca3164d1f9c39',
        'reported_original_bytes': 7673, 'preserved_bytes': len(post), 'sha256': sha256(post),
        'basis': 'Complete Library full-text read; not independently compared with original downloadable bytes'}
}
(ROOT / 'ARCHIVE_INSPECTION.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({'archive': report['archive'], 'member_count': len(members),
    'csv_rows': {k: len(v) for k,v in tables.items()},
    'postmortem_bytes': len(post)}, indent=2))
