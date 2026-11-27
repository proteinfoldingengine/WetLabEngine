"""Verify the downloaded historical publication independently against its checkout."""
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile
import json
import sys

archive = Path(sys.argv[1])
checkout = Path(sys.argv[2])
digest = '3bca38711fc59c27a614536ee28fdc7b690902f0cabe8544d3729a1406e84b78'
assert sha256(archive.read_bytes()).hexdigest() == digest
prefix = 'ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/evidence/'
with ZipFile(archive) as package:
    assert package.testzip() is None
    lines = package.read(prefix+'SHA256SUMS').decode().splitlines()
    for line in lines:
        expected, name = line.split(maxsplit=1)
        assert sha256(package.read(prefix+name)).hexdigest() == expected
    for name in ('COMMANDS.json','EXECUTION.json','WITNESS.json','historical-producer.log'):
        assert package.read(prefix+name) == (checkout/(prefix+name)).read_bytes()
    log = package.read(prefix+'historical-producer.log')
    assert package.read(prefix+'original-green/historical-producer.log') == log
    execution = json.loads(package.read(prefix+'EXECUTION.json'))
    print(json.dumps(dict(run=execution['run'],sha=execution['sha'],entries=len(lines),
                          log_bytes=len(log),log_sha256=sha256(log).hexdigest()),sort_keys=True))
