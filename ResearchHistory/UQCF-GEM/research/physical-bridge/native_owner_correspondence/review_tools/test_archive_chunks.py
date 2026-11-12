"""Exercise the production reconstruction statement without network access."""
import ast,pathlib,sys,tempfile
tree=ast.parse(pathlib.Path(sys.argv[1]).read_text())
statement=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='rebuilt' for t in n.targets))
with tempfile.TemporaryDirectory() as directory:
    root=pathlib.Path(directory);(root/'a').write_bytes(b'abc');(root/'b').write_bytes(b'\x00def')
    scope={'root':root,'parts':[{'file':'a'},{'file':'b'}]}
    exec(compile(ast.Module(body=[statement],type_ignores=[]),'<production-reconstruction>','exec'),scope)
    assert scope['rebuilt']==b'abc\x00def'
print('Production chunk reconstruction PASS')
