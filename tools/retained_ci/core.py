"""Initial baseline behavior, before infrastructure regression fixes."""
from pathlib import Path
import shutil,subprocess

def fixture_cache(fn):
    return fn

def replace_directory(source,target):
    shutil.copytree(source,target,dirs_exist_ok=True)

def run_commands(commands,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    for name,argv in commands.items():
        with (out/(name+'.log')).open('w') as log:
            result=subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT)
        if result.returncode:raise RuntimeError(name+' failed')
