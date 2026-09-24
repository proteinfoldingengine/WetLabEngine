"""v15.51 Task 4: strict-subpackage minimality."""
def minimal_packages(contract,origin_results):
 success=sorted(p for p,r in origin_results.items() if r["status"]!="INSUFFICIENT")
 mins=[]
 for p in success:
  if not any(q in success for q in contract["strict_subpackages"][p]): mins.append(p)
 return {"schema":"uqcf-v1551-minimality-v1","successful_packages":success,
         "minimal_successful_packages":mins,
         "insufficient_packages":sorted(p for p,r in origin_results.items() if r["status"]=="INSUFFICIENT")}
