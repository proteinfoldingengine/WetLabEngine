"""Literal source binding for the narrowly scoped approved PUSH transport."""
import json
import os
from pathlib import Path
import re
import subprocess

BASE="ResearchHistory/UQCF-GEM/demos/v16.55-renewable-guard-repair/"
PREREG="891470cfc817f26d9721f96278b2c0f8652c3fdf"
PARENT="466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f"
REPORTING_EXCLUSIONS=("CAMPAIGN_REQUEST.json","CONTROL_REQUEST.json","MERGE_CONTRACT.json","CLOSEOUT.md","INDEPENDENT_V16_55_WHOLE_REVIEW.md","INDEPENDENT_ACTUAL_MERGE_AUDIT.md")

def scientific_inventory(head):
    listing=subprocess.check_output(["git","ls-tree","-r",head],text=True).splitlines();result={}
    workflows={".github/workflows/v16.55-controls.yml",".github/workflows/v16.55-renewable-guard-validation.yml"}
    for line in listing:
        header,path=line.split("\t",1);wanted=path in workflows
        if path.startswith(BASE):
            relative=path[len(BASE):];parts=relative.split("/")
            wanted=(len(parts)==1 and relative not in REPORTING_EXCLUSIONS and Path(relative).suffix in (".py",".md",".json")) or (len(parts)==2 and parts[0] in ("tests","analytical") and Path(relative).suffix in (".py",".md"))
        if wanted:result[path]=header.split()[2]
    if not result or not workflows<=set(result):raise ValueError("empty/incomplete scientific source inventory")
    return result

def bind_request():
    if os.environ.get("GITHUB_ACTIONS")!="true":raise RuntimeError("GitHub only")
    event=os.environ["GITHUB_SHA"]
    if os.environ["GITHUB_REF"]=="refs/heads/research/v16.34-fiber-component-invariant":
        parents=subprocess.check_output(["git","show","-s","--format=%P",event],text=True).split()
        if len(parents)!=2:raise ValueError("actual-merge replay requires an actual two-parent merge event")
        contract=json.loads(Path(BASE+"MERGE_CONTRACT.json").read_text())
        if parents[0]!=contract["integration_parent"]:raise ValueError("actual merge differs from authorized integration parent")
        subprocess.run(["git","merge-base","--is-ancestor",contract["reviewed_source_parent"],parents[1]],check=True)
        if contract["preregistration_sha"]!=PREREG:raise ValueError("merge preregistration mismatch")
        if contract["reporting_exclusions"]!=list(REPORTING_EXCLUSIONS):raise ValueError("unapproved scientific membership exclusions")
        required=scientific_inventory(contract["reviewed_source_parent"])
        if contract["scientific_git_blobs"]!=required or scientific_inventory(event)!=required:raise ValueError("empty/partial/modified reviewed scientific source inventory")
        for path,blob in contract["scientific_git_blobs"].items():
            if subprocess.check_output(["git","rev-parse",event+":"+path],text=True).strip()!=blob:raise ValueError("actual merge scientific source differs from reviewed source")
        request=dict(mode="actual_merge",contract=contract)
        source=event
    elif os.environ["GITHUB_REF"]=="refs/heads/research/v16.55-renewable-guard-repair":
        request=json.loads(Path(BASE+"CAMPAIGN_REQUEST.json").read_text());source=request["scientific_parent_sha"]
        if request["preregistration_sha"]!=PREREG or request["scope"]!="all" or request["mode"]!="campaign":raise ValueError("unapproved request")
        actual_parent=subprocess.check_output(["git","show","-s","--format=%P",event],text=True).strip()
        if actual_parent!=source:raise ValueError("request must be the sole child of the literal scientific source parent")
        changed=subprocess.check_output(["git","diff","--name-only",source,event],text=True).splitlines()
        if changed!=[BASE+"CAMPAIGN_REQUEST.json"]:raise ValueError("request commit changes other files")
    else:raise ValueError("unapproved transport branch")
    if not re.fullmatch("[0-9a-f]{40}",source):raise ValueError("invalid literal scientific source")
    for ancestor in (PREREG,PARENT):subprocess.run(["git","merge-base","--is-ancestor",ancestor,source],check=True)
    if subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()!=event:raise ValueError("actual scientific checkout must equal event SHA")
    with open(os.environ["GITHUB_ENV"],"a") as stream:
        stream.write("SCIENTIFIC_SHA="+event+"\nPREREGISTRATION_SHA="+PREREG+"\n")
    print(json.dumps(dict(workflow_sha=event,scientific_sha=event,scientific_source_parent=source,request=request),sort_keys=True))

if __name__=="__main__":bind_request()
