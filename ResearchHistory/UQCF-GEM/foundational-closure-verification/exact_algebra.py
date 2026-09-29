"""Pinned inherited Fraction algebra, used by producer only."""
from pathlib import Path
from fractions import Fraction as F
import hashlib, importlib.util
PATH = Path(__file__).resolve().parents[1]/'demos/v15.56-response-selector-obstruction/pruning_consistency_audit.py'
raw=PATH.read_bytes()
if hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() != '94d946dfc5fb5aa150834a807eb35c29b3133604':
    raise ValueError('inherited exact source blob changed')
spec=importlib.util.spec_from_file_location('fcv_pinned_exact_parent', PATH)
pc=importlib.util.module_from_spec(spec);spec.loader.exec_module(pc)
zeros,eye,add,sub,mul,rank=pc.zeros,pc.eye,pc.add,pc.sub,pc.mul,pc.rank

def transpose(a):
    return [list(x) for x in zip(*a)]

def encode(a): return [[str(x) for x in row] for row in a]
def vector(a): return [str(row[0]) for row in a]
def col(a,i): return [[row[i]] for row in a]
def zero_col(n): return zeros(n,1)
