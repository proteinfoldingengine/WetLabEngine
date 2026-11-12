"""Verify archival/integration identity; never rerun the model or scientific code."""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import zipfile

ACCEPTED = 'f7a42c259f7978b50c2af3b9173c9881443f8cb5'
BASE = Path('ResearchHistory/UQCF-GEM/research/physical-bridge/event_source_correspondence_review')
ARCHIVES = {
    'integrity.zip': '09f90a33b362f673d3ef2c7e3d5f4257b1580439699e860556229cc2e61ca164',
    'review.zip': '872794aebe579c834379937c81a17a34389e387973386888d8ffb075ad1b5ee7',
    'publication.zip': '8d9c8e5b29591b6906c923596d34baaf2de80165c5635886c2b12ecd7bf1cc45',
}
CODE = [
    '.github/scripts/uqcf_event_correspondence_review.py',
    '.github/scripts/uqcf_event_correspondence_publication.py',
    '.github/scripts/uqcf_event_correspondence_tests.py',
    '.github/workflows/uqcf-event-correspondence-review.yml',
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
    out = Path('event_archive_audit')
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
        if len(rows) != 27:
            raise ValueError('Incomplete accepted checkpoint path set')
        archives = []
        for name, digest in ARCHIVES.items():
            raw = (BASE/'evidence/archives'/name).read_bytes()
            count = verify_archive(raw,digest,BASE/'evidence'/name.removesuffix('.zip'))
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
        print('PASS: 27 accepted files unchanged; all 3 original ZIPs and their exact contents verified.')
    except Exception as error:
        (out/'failure.json').write_text(json.dumps({'status':'FAIL','error_type':type(error).__name__})+'\n')
        raise

if __name__=='__main__':main()
