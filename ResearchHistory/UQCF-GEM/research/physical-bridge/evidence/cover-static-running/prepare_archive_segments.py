"""Preserve original large archives as ordered, unmodified byte segments."""
import hashlib, json, pathlib
P = pathlib.Path(__file__).parent
O = P / 'originals'
def sha(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
archives = []
uploads = []
for path in sorted(O.glob('*.zip')):
    data = path.read_bytes()
    if len(data) > 8_000_000:
        parts = []
        for i, start in enumerate(range(0, len(data), 8_000_000), 1):
            part = data[start:start + 8_000_000]
            name = path.name + f'.part{i:03}'
            (O / name).write_bytes(part)
            row = dict(file=name, bytes=len(part), sha256=sha(part), git_blob_sha1=blob(part))
            parts.append(row)
            uploads.append(row)
        archives.append(dict(file=path.name, bytes=len(data), sha256=sha(data), segments=parts))
    else:
        uploads.append(dict(file=path.name, bytes=len(data), sha256=sha(data), git_blob_sha1=blob(data)))
(O / 'archive_segments.json').write_text(json.dumps(dict(format='unaltered ZIP bytes in ordered segments; concatenate in listed order', archives=archives), indent=2)+'\n')
(P / 'binary_upload_plan.json').write_text(json.dumps(uploads, indent=2)+'\n')
print(json.dumps(dict(archives=len(archives), upload_blobs=len(uploads))))
