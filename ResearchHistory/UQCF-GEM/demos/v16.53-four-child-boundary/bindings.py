"""Exact test identity, full function AST and source-byte bindings."""
import ast,hashlib
FORMAT='python311-ast-without-empty-type-params-v1'
def digest(data):return hashlib.sha256(data).hexdigest()
def assertion_dump(node):
    # Python3.12 adds empty type_params to function/class ASTs. Omit only
    # that structural empty field, never text inside a literal or assertion.
    for item in ast.walk(node):
        if 'type_params' in item._fields:
            if item.type_params:raise ValueError('type parameters outside pinned Python3.11 syntax')
            item._fields=tuple(name for name in item._fields if name!='type_params')
    return ast.dump(node,include_attributes=False)
def build(sources):
    tests=[]
    for module,source in sources.items():
        for cls in ast.parse(source).body:
            if isinstance(cls,ast.ClassDef):
                for node in cls.body:
                    if isinstance(node,ast.FunctionDef) and node.name.startswith('test_'):
                        tests.append({'identity':module+'.'+cls.name+'.'+node.name,'expected':'PASS','ast_sha256':digest(assertion_dump(node).encode())})
    return {'format':FORMAT,'count':len(tests),'sources':{m:digest(s.encode()) for m,s in sources.items()},'tests':tests}
def verify(manifest,sources):
    if manifest!=build(sources):raise ValueError('assertion manifest identity/source/hash mismatch')
    return True
