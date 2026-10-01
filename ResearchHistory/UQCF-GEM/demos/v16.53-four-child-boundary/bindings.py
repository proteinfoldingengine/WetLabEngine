"""Exact test identity, full function AST and source-byte bindings."""
import ast,hashlib
def digest(data):return hashlib.sha256(data).hexdigest()
def build(sources):
    tests=[]
    for module,source in sources.items():
        for cls in ast.parse(source).body:
            if isinstance(cls,ast.ClassDef):
                for node in cls.body:
                    if isinstance(node,ast.FunctionDef) and node.name.startswith('test_'):
                        tests.append({'identity':module+'.'+cls.name+'.'+node.name,'expected':'PASS','ast_sha256':digest(ast.dump(node,include_attributes=False).encode())})
    return {'count':len(tests),'sources':{m:digest(s.encode()) for m,s in sources.items()},'tests':tests}
def verify(manifest,sources):
    if manifest!=build(sources):raise ValueError('assertion manifest identity/source/hash mismatch')
    return True
