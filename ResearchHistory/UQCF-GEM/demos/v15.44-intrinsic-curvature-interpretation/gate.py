"""Ordered fail-closed exact audit with canonical, reproducible ledger bytes."""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path

# -I removes the script directory from sys.path; pin this actual file's sibling
# modules without admitting cwd or environment-controlled import paths.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from operator_types import canonical_bytes, _unique
from worker import parse, wire, INVENTORY, HERE, ROOT

STAGES = ('evidence','projection_carriers','operator_derivation_equality',
          'kernel_image_certificates','controls','all_archived_field_comparisons','ledger')
SCHEMA = 'uqcf-v1544-intrinsic-curvature-characterization-v1'
CLAIMS = {'source_correspondence':'NOT_EVALUATED','Pillar_3':'OPEN',
          'physical_metric':False,'physical_curvature':False,'stress_energy':False,
          'einstein_equations':False,'continuum_limit':False,'spacetime':False,
          'physical_gravity':False,'foundational_uniqueness':False,'scientific_breakthrough':False,
          'inherited_axiom_dependence':True,'isotropic_scalar_lift_dependence':True,
          'fundamental_time_introduced':False,'dark_matter_primitive_introduced':False}


def result_bytes(value):
    """Deterministic compact JSON keeps the complete ledger publishable as one blob."""
    return (json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode('ascii')


def _decode_worker(raw, stage):
    result=parse(raw)
    if type(result) is not dict or set(result)!={'stage','result'} or result['stage']!=stage:
        raise ValueError('worker envelope')
    value=result['result']
    expected={'evidence':{'pins'},'projection_carriers':{'geometries'},
              'operator_derivation_equality':{'operators','operator_hashes'},
              'kernel_image_certificates':{'certificates','certificate_hashes'},
              'controls':{'control','index'},'all_archived_field_comparisons':{'comparison'}}
    if stage not in expected or type(value) is not dict or set(value)!=expected[stage]:
        raise ValueError('worker result schema')
    return value


def _worker_process(stage, data, timeout, *, index=None, progress=None, _test_command=None):
    with tempfile.TemporaryDirectory(prefix='uqcf-v1544-worker-') as tmp:
        directory=Path(tmp); inp=directory/'input.json'; out=directory/'output.json'
        log=directory/'stderr.log'; marker=directory/'progress.txt'
        inp.write_bytes(canonical_bytes(wire(data)))
        if _test_command:
            script={'timeout':'import time; time.sleep(5)',
                    'nonzero':'import sys; sys.exit(3)',
                    'malformed':'from pathlib import Path; import sys; Path(sys.argv[1]).write_bytes(b"{")'}[_test_command]
            command=[sys.executable,'-I','-B','-c',script,str(out)]
        else:
            command=[sys.executable,'-I','-B',str(HERE/'worker.py'),'--stage',stage,
                     '--input',str(inp),'--output',str(out),'--progress',str(marker)]
            if index is not None: command.extend(['--index',str(index)])
        with log.open('wb') as err, (directory/'stdout.log').open('wb') as stdout:
            try: completed=subprocess.run(command,cwd=ROOT,stdin=subprocess.DEVNULL,
                                          stdout=stdout,stderr=err,timeout=timeout,check=False)
            except subprocess.TimeoutExpired as exc:
                if progress is not None: _read_progress(marker,progress)
                raise ValueError('worker_timeout: '+stage) from exc
        if progress is not None: _read_progress(marker,progress)
        if completed.returncode:
            raise ValueError('worker_nonzero: '+stage+': '+log.read_text(errors='replace')[-3000:])
        if not out.is_file(): raise ValueError('worker_missing_output: '+stage)
        return _decode_worker(out.read_bytes(),stage)


def _read_progress(path, progress):
    if not path.exists(): return
    for line in path.read_text(encoding='ascii').splitlines():
        if line not in progress: raise ValueError('worker_progress_schema')
        progress[line].append(True)


def _controls(data, progress):
    # Concurrent subprocesses have independent mutable inherited core globals.
    # A single deadline bounds the whole four-carrier control stage.
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures=[pool.submit(_worker_process,'controls',data,7200,index=i) for i in range(4)]
        deadline=time.monotonic()+7200
        results=[]
        for i,future in enumerate(futures):
            remaining=max(0,deadline-time.monotonic())
            try: result=future.result(timeout=remaining)
            except TimeoutError as exc: raise ValueError('controls overall timeout') from exc
            if result['index']!=i: raise ValueError('control order')
            results.append(result['control']); progress['controls'].append(True)
    return {'controls':results}


def _stage(name, context, progress):
    if name=='ledger': return _ledger(context,progress)
    if name=='controls': return _controls({key:context[key] for key in ('geometries','operators',
                                  'certificates','operator_hashes','certificate_hashes')},progress)
    needed={'evidence':(), 'projection_carriers':('pins',),
            'operator_derivation_equality':('geometries',),
            'kernel_image_certificates':('geometries','operators','operator_hashes'),
            'all_archived_field_comparisons':('geometries','operators','certificates',
                                              'operator_hashes','certificate_hashes')}
    return _worker_process(name,{key:context[key] for key in needed[name]},
             60 if name=='evidence' else 7200 if name=='projection_carriers' else 1800,
             progress=progress if name=='all_archived_field_comparisons' else None)


def _ledger(context,progress):
    from worker import operator_from_wire, certificate_from_wire
    from kernel import verify_kernel
    from operator_types import load_geometry
    gs=tuple(load_geometry(canonical_bytes(g)) for g in context['geometries'])
    ops=tuple(operator_from_wire(v) for v in context['operators'])
    certs=tuple(certificate_from_wire(v,o) for v,o in zip(context['certificates'],ops,strict=True))
    for i,(o,c) in enumerate(zip(ops,certs,strict=True)):
        if sha256(canonical_bytes(wire(o))).hexdigest()!=context['operator_hashes'][i]:
            raise ValueError('ledger operator seal')
        if sha256(canonical_bytes(wire(c))).hexdigest()!=context['certificate_hashes'][i]:
            raise ValueError('ledger certificate seal')
        verify_kernel(o,c)
    comparison=context['comparison']
    if len(comparison['cases'])!=len(progress['cases']) or len(comparison['pairs'])!=len(progress['pairs']) or len(comparison['scale_pairs'])!=len(progress['scale_pairs']):
        raise ValueError('ledger incomplete progress')
    if comparison['counts']['cases']!=740 or comparison['counts']['pairs']!=592 or comparison['counts']['scale_pairs']!=370:
        raise ValueError('ledger coverage')
    controls=context['controls']
    if len(controls)!=4 or len(progress['controls'])!=4: raise ValueError('ledger controls')
    carriers=[]
    for i,(g,o,c,control) in enumerate(zip(gs,ops,certs,controls,strict=True)):
        if (control['L']!=g.L or control['scale']!=str(g.scale) or
            control['rank']!=c.rank or control['nullity']!=c.nullity or control['exact'] is not True):
            raise ValueError('ledger carrier control')
        carriers.append({'L':g.L,'scale':str(g.scale),'labels':wire(o.labels),'cycles':wire(o.cycles),
            'operator':wire(o),'operator_sha256':context['operator_hashes'][i],
            'certificate':wire(c),'certificate_sha256':context['certificate_hashes'][i],
            'control':control,'constant_field_annihilated':
                all(sum(row)==0 for row in o.entries),'centered_kernel_dimension':len(c.centered_basis[0])})
        if carriers[-1]['constant_field_annihilated'] is not True: raise ValueError('constant field')
    return {'schema':SCHEMA,'pins':context['pins'],
        'theorems':{'linearity':'PROVED_FROM_EXACT_EDGE_COEFFICIENTS_AND_FOUR_FACTOR_PRODUCT',
                    'basis_equality':'CERTIFIED_ALL_COLUMNS_ON_FOUR_FROZEN_CARRIERS',
                    'kernel_rank':'CERTIFIED_BY_REPLAYED_RATIONAL_ROW_OPERATIONS',
                    'projector':'CERTIFIED_SYMMETRIC_IDEMPOTENT_AND_KERNEL_IMAGE'},
        'carriers':carriers,'cases':comparison['cases'],'pairs':comparison['pairs'],
        'scale_pairs':comparison['scale_pairs'],'coverage':comparison['counts'],
        'claims':CLAIMS,'interpretation':'EXACT_FINITE_FOUR_CARRIER_CHARACTERIZATION_ONLY'}


def _audit(executors=None):
    execute=_stage if executors is None else executors
    progress={'cases':[],'pairs':[],'scale_pairs':[],'controls':[]}
    context={}; completed=[]
    for stage in STAGES:
        try:
            value=execute(stage,context,progress)
            if type(value) is not dict: raise ValueError('stage result')
            if stage=='ledger':
                if set(value)!={'schema','pins','theorems','carriers','cases','pairs',
                                'scale_pairs','coverage','claims','interpretation'}:
                    raise ValueError('ledger schema')
                context['scientific_verdict']=value
            else: context.update(value)
            completed.append(stage)
            if executors is None:
                print('completed stage '+stage+' accepted='+str({k:len(v) for k,v in progress.items()}),
                      file=sys.stderr,flush=True)
        except Exception as error:
            return {'status':'INTRINSIC_CURVATURE_INTERPRETATION_INVALID',
                    'first_failed_stage':stage,'failure':type(error).__name__+': '+str(error),
                    'completed_stages':completed,
                    'completed_counts':{key:len(items) for key,items in progress.items()},
                    'scientific_verdict':None}
    return {'status':'INTRINSIC_CURVATURE_CHARACTERIZED','first_failed_stage':None,
            'failure':None,'completed_stages':completed,
            'completed_counts':{key:len(items) for key,items in progress.items()},
            'scientific_verdict':context['scientific_verdict']}


def audit(): return _audit()


def main():
    parser=argparse.ArgumentParser()
    choice=parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--out',type=Path); choice.add_argument('--check',type=Path)
    args=parser.parse_args()
    result=audit(); raw=result_bytes(result)
    if result['status']!='INTRINSIC_CURVATURE_CHARACTERIZED':
        print(result['first_failed_stage']+': '+result['failure'],file=sys.stderr)
        raise SystemExit(1)
    if args.out:
        args.out.write_bytes(raw)
    elif args.check.read_bytes()!=raw:
        raise SystemExit('canonical replay mismatch')
    print(result['status']+' cases='+str(result['completed_counts']['cases'])+
          ' pairs='+str(result['completed_counts']['pairs'])+
          ' sha256='+sha256(raw).hexdigest())


if __name__=='__main__': main()
