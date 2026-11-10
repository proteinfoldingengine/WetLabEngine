"""One-call wrapper preserving failed transport bodies; no retries or fallback."""
import json,urllib.request,urllib.error
from uqcf_preparability_review import call_model as inherited_call_model

def call_model(out,key,prompt,opener=urllib.request.urlopen):
 def failure(stage,exc,http=False):
  record=dict(stage=stage,error_type=type(exc).__name__,outcome='FAILED_HTTP' if http else ('UNCERTAIN' if stage=='response' else 'FAILED_METADATA'),retry=False)
  if http:
   record['http_status']=exc.code
   try:(out/(stage+'.json')).write_bytes(exc.read())
   except Exception as read_exc:
    partial=getattr(read_exc,'partial',None)
    if isinstance(partial,bytes):(out/(stage+'.partial')).write_bytes(partial)
  else:
   partial=getattr(exc,'partial',None)
   if isinstance(partial,bytes):(out/(stage+'.partial')).write_bytes(partial)
  (out/'transport_failure.json').write_text(json.dumps(record)+'\n')
 class CapturedResponse:
  def __init__(self,response,stage):self.response=response;self.stage=stage
  def __enter__(self):self.entered=self.response.__enter__();return self
  def __exit__(self,*args):return self.response.__exit__(*args)
  def read(self,*args):
   try:return self.entered.read(*args)
   except Exception as exc:failure(self.stage,exc);raise
 def preserve(req,timeout):
  stage='response' if req.get_method()=='POST' else 'model_metadata'
  try:return CapturedResponse(opener(req,timeout=timeout),stage)
  except urllib.error.HTTPError as exc:failure(stage,exc,http=True);raise
  except Exception as exc:failure(stage,exc);raise
 return inherited_call_model(out,key,prompt,opener=preserve)
