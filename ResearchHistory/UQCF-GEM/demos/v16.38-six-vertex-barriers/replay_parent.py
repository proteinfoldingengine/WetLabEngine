from pathlib import Path
import subprocess,sys,tempfile
parent=Path(__file__).resolve().parent.parent/'v16.37-certified-closure'
with tempfile.TemporaryDirectory() as out:
 subprocess.run([sys.executable,str(parent/'run_campaign.py'),out],check=True)
 for name in ('CERTIFICATE.json.gz','SUMMARY.json','VERIFY.json'):
  if (Path(out)/name).read_bytes()!=(parent/'evidence/science/scientific'/name).read_bytes():raise ValueError('parent scientific bytes differ '+name)
 print('PARENT_SCIENTIFIC_BYTES_IDENTICAL',flush=True)
