"""Verify archival/integration identity; never rerun the model or scientific code."""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import zipfile

ACCEPTED = '5865e4d0525e5bcf3bc706c7de60f84774ccdb86'
BASE = Path('ResearchHistory/UQCF-GEM/research/physical-bridge/p1_receiver_location_resolution')
ARCHIVES = {'p1-location-integrity-1.zip': 'f03e5b7122592a416d37ea61b57fe04543a9a627e97477b99272fa1af41ad88e', 'p1-location-publication-1.zip': '2a43548eb8c6558c8a7541d5f766b1d7920015a023cd354671a01c73174d8e9d', 'p1-location-review-1.zip': '2ba237d62eabf8ae2d0b7aae855f6365606df0f063da16cbb8440c92c9bb3a82'}
CODE = [
    '.github/scripts/uqcf_p1_location_review.py',
    '.github/scripts/uqcf_p1_location_publication.py',
    '.github/scripts/uqcf_p1_location_tests.py',
    '.github/workflows/uqcf-p1-location-review.yml',
]

def verify_archive(raw, expected, extracted):
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('Original ZIP digest mismatch')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or any(Path(n).name != n for n in names):
            raise ValueError('Invalid or duplicate archive member')
        files = {p.name for p in extracted.iterdir() if p.is_file()} if extracted.is_dir() else set()
        if set(names) != files:
            raise ValueError('Archive and retained extraction differ')
        for name in names:
            if archive.read(name) != (extracted/name).read_bytes():
                raise ValueError('Archive member differs from retained evidence')
        return len(names)

def main():
    out = Path('receiver_archive_audit')
    out.mkdir(exist_ok=True)
    try:
        # The exact accepted commit selects the complete old path set and blobs.
        tree = subprocess.check_output(['git','ls-tree','-r','-z',ACCEPTED,'--',str(BASE),*CODE])
        current_tree = subprocess.check_output(['git','ls-tree','-r','-z','HEAD','--',str(BASE),*CODE])
        current = {entry.split(b'\t',1)[1]:entry.split(b'\t',1)[0]
                   for entry in current_tree.split(b'\0') if entry}
        rows = []
        for record in tree.split(b'\0'):
            if not record:
                continue
            metadata, path = record.split(b'\t',1)
            if current.get(path) != metadata:
                raise ValueError('Accepted checkpoint Git mode/type/blob changed')
            mode, kind, blob = metadata.decode().split()
            path = path.decode('utf-8')
            raw = Path(path).read_bytes()
            actual = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            if mode != '100644' or kind != 'blob' or actual != blob:
                raise ValueError('Accepted checkpoint byte identity changed')
            rows.append({'path':path,'git_blob':actual,'sha256':hashlib.sha256(raw).hexdigest()})
        if len(rows) != 29:
            raise ValueError('Incomplete accepted checkpoint path set')
        archives = []
        for name, digest in ARCHIVES.items():
            raw = (BASE/'evidence'/name).read_bytes()
            count = verify_archive(raw,digest,BASE/'evidence'/name.removeprefix('p1-location-').removesuffix('-1.zip'))
            archives.append({'name':name,'bytes':len(raw),'sha256':digest,'members':count})
        receipt = {
            'status':'PASS','accepted_evidence_sha':ACCEPTED,
            'checkout_sha':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
            'workflow_sha':os.environ.get('UQCF_WORKFLOW_SHA'),
            'run_id':os.environ.get('GITHUB_RUN_ID'),'run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),
            'native_bridge':'NOT_DERIVED','model_called':False,'scientific_execution':False,
            'accepted_files':rows,'original_archives':archives,
        }
        (out/'audit.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
        print('PASS: 29 accepted files unchanged; all 3 original ZIPs and their exact contents verified.')
    except Exception as error:
        (out/'failure.json').write_text(json.dumps({'status':'FAIL','error_type':type(error).__name__})+'\n')
        raise

if __name__=='__main__':main()
