from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(here/'replay_parent.py')],check=True)
for line in (here/'inherited.txt').read_text().splitlines():
 if line.strip():subprocess.run([sys.executable,line],check=True)
