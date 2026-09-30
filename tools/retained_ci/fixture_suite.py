"""Run the unchanged v16.36 test file with isolated optional input reuse."""
import importlib.util,sys,time,unittest,json
from pathlib import Path
from core import fixture_cache,dump,sha

def execute(out,reuse):
    start=time.perf_counter();folder=Path('ResearchHistory/UQCF-GEM/demos/v16.36-barrier-law-closure').resolve()
    sys.path.insert(0,str(folder))
    import producer,verifier
    original=producer.produce;verify=verifier.verify_document
    metrics={'fixture_hashes':{},'producer_requests':0,'producer_generations':0,'producer_seconds':0.0,'verifier_calls':0,'verifier_seconds':0.0,'verifier_uncached':True,'tests':[],'reuse':reuse}
    def generate(bound=4):
        tick=time.perf_counter();value=original(bound)
        metrics['producer_seconds']+=time.perf_counter()-tick;metrics['producer_generations']+=1
        digest=sha(json.dumps(value,sort_keys=True,separators=(',',':')).encode())
        prior=metrics['fixture_hashes'].setdefault(str(bound),digest)
        if prior!=digest:raise ValueError('nondeterministic fixture')
        return value
    inputs=fixture_cache(generate) if reuse else generate
    def produce(bound=4):metrics['producer_requests']+=1;return inputs(bound)
    def check(document):
        metrics['verifier_calls']+=1;tick=time.perf_counter()
        try:return verify(document)
        finally:metrics['verifier_seconds']+=time.perf_counter()-tick
    producer.produce=produce;verifier.verify_document=check
    spec=importlib.util.spec_from_file_location('inherited_v1636',folder/'test_gate.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    class Results(unittest.TextTestResult):
        def startTest(self,test):super().startTest(test);self.tick=time.perf_counter()
        def addSuccess(self,test):super().addSuccess(test);metrics['tests'].append({'id':test.id(),'outcome':'success'})
        def addFailure(self,test,err):super().addFailure(test,err);metrics['tests'].append({'id':test.id(),'outcome':'failure'})
        def addError(self,test,err):super().addError(test,err);metrics['tests'].append({'id':test.id(),'outcome':'error'})
    result=unittest.TextTestRunner(verbosity=2,resultclass=Results).run(unittest.defaultTestLoader.loadTestsFromModule(module))
    metrics.update(success=result.wasSuccessful(),seconds=time.perf_counter()-start)
    dump(out,metrics)
    if not result.wasSuccessful() or result.testsRun!=12 or len(metrics['tests'])!=12:raise SystemExit(1)
    if metrics['verifier_calls']!=12:raise ValueError('all independent verifier calls required')
    if reuse and metrics['producer_generations']!=2:raise ValueError('expected two isolated fixtures')

if __name__=='__main__':execute(sys.argv[1],sys.argv[2]=='reuse')
