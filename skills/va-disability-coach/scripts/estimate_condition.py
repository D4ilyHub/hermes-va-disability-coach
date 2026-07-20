#!/usr/bin/env python3
"""Transparent, provenance-preserving candidate rating-schedule comparison."""
from __future__ import annotations
import argparse, json
from datetime import date, datetime
from pathlib import Path
from typing import Any, Sequence
try: import yaml
except ImportError: yaml=None
VERSION="1.0.0"
STATUSES={"supported":"Supported by supplied documentation","potential":"Potentially supported","insufficient":"Insufficient documentation","conflict":"Conflicting documentation","medical":"Requires medical determination","adjudicative":"Requires adjudicative judgment","not_estimable":"Not estimable","outside":"Outside the current rating snapshot"}

class EstimateInputError(ValueError): pass

def normalize(value:Any)->Any:
    if isinstance(value,(date,datetime)): return value.isoformat()
    if isinstance(value,dict): return {str(k):normalize(v) for k,v in value.items()}
    if isinstance(value,list): return [normalize(v) for v in value]
    return value

def load_structured(path:Path)->Any:
    text=path.read_text(encoding="utf-8")
    if path.suffix.lower()==".json": return normalize(json.loads(text))
    if yaml is None: raise EstimateInputError("PyYAML is required for YAML input")
    return normalize(yaml.safe_load(text))

def compare(actual:Any,op:str,expected:Any)->bool:
    if op=="eq": return actual==expected
    if op==">=": return actual>=expected
    if op=="<=": return actual<=expected
    if op==">": return actual>expected
    if op=="<": return actual<expected
    if op=="in": return actual in expected
    if op=="truthy": return bool(actual)
    raise EstimateInputError(f"unsupported operator {op}")

def fact_view(facts:dict[str,Any],key:str)->tuple[bool,Any,dict[str,Any]|None]:
    if key not in facts:return False,None,None
    raw=facts[key]
    if isinstance(raw,dict) and "value" in raw:return True,raw["value"],raw.get("provenance")
    return True,raw,None

def evaluate_criterion(criterion:dict[str,Any],facts:dict[str,Any])->dict[str,Any]:
    supported=[];missing=[];conflicts=[]
    for req in criterion.get("requirements",[]):
        key=req["fact"];present,value,prov=fact_view(facts,key)
        if not present: missing.append({"fact":key,"requirement":req});continue
        try: ok=compare(value,req.get("operator","eq"),req.get("value"))
        except (TypeError,ValueError): ok=False
        item={"fact":key,"value":value,"requirement":req,"provenance":prov}
        (supported if ok else conflicts).append(item)
    judgment=criterion.get("judgment","none"); manual=bool(criterion.get("manual_review_required"))
    reqs=criterion.get("requirements",[])
    if conflicts:status=STATUSES["conflict"]
    elif not reqs:
        status=STATUSES["adjudicative"] if judgment=="adjudicative" else STATUSES["medical"] if judgment=="medical" or manual else STATUSES["insufficient"]
    elif missing:
        status=STATUSES["potential"] if supported else STATUSES["insufficient"]
    elif judgment=="adjudicative":status=STATUSES["adjudicative"]
    elif judgment=="medical" or manual:status=STATUSES["medical"]
    else:status=STATUSES["supported"]
    return {"percent":criterion.get("percent"),"criteria_text":criterion.get("criteria_text"),"status":status,"supported_findings":supported,"conflicting_findings":conflicts,"missing_findings":missing,"medical_judgment_required":judgment=="medical" or manual,"adjudicative_judgment_required":judgment=="adjudicative","manual_review_required":manual}

def code_map(snapshot:dict[str,Any])->dict[str,dict[str,Any]]:
    return {str(x["diagnostic_code"]):x for x in snapshot["diagnostic_codes"]}

def infer_candidates(record:dict[str,Any],snapshot:dict[str,Any])->list[str]:
    explicit=record.get("candidate_diagnostic_codes") or []
    if explicit:return sorted({str(x) for x in explicit})
    diagnosis=str((record.get("confirmed_diagnosis") or {}).get("name") or "").lower()
    wording=(str(record.get("user_wording") or "")+" "+diagnosis).lower()
    hits=[]
    for code in snapshot["diagnostic_codes"]:
        if any(a.lower() in wording for a in code.get("aliases",[])):hits.append(str(code["diagnostic_code"]))
    return sorted(set(hits))

def overlap_flags(codes:list[str])->list[str]:
    c=set(codes);flags=[]
    if len(c & {"9411","9434","9413"})>1:flags.append("Multiple mental-health diagnostic codes may describe overlapping occupational and social impairment; separate ratings ordinarily require distinct manifestations.")
    if "8045" in c and c & {"9411","9434","9413"}:flags.append("TBI and mental-health manifestations may overlap; use 38 C.F.R. § 4.124a DC 8045 and § 4.14 to avoid duplicate evaluation of the same manifestation.")
    if c & {"5237","5242"} and "8520" in c:flags.append("A spine evaluation and an objective associated neurologic abnormality can be analytically distinct, but duplicate symptoms must not be rated twice.")
    if len(c & {"5237","5242"})>1:flags.append("Multiple spine diagnostic labels may use the same general formula; do not duplicate the same manifestations.")
    return flags

def estimate(record:dict[str,Any],snapshot:dict[str,Any],as_of:date)->dict[str,Any]:
    if not isinstance(record,dict):raise EstimateInputError("input must be an object")
    facts=record.get("facts") or {}
    if not isinstance(facts,dict):raise EstimateInputError("facts must be an object")
    diagnosis=record.get("confirmed_diagnosis") or {}
    diagnosis_exists=bool(diagnosis.get("exists")) and bool(diagnosis.get("name"))
    candidates=infer_candidates(record,snapshot); mapping=code_map(snapshot); results=[]
    for code in candidates:
        if code not in mapping:
            results.append({"diagnostic_code":code,"status":STATUSES["outside"],"criteria":[],"source_ids":[],"warnings":["No criteria for this code are bundled. Consult current official Part 4 text and require manual review."]});continue
        item=mapping[code]
        if not diagnosis_exists:
            results.append({"diagnostic_code":code,"title":item["title"],"status":STATUSES["not_estimable"],"criteria":[],"source_ids":item["source_ids"],"warnings":["No confirmed diagnosis was supplied. The tool will not infer one to produce a percentage."]});continue
        criteria=[evaluate_criterion(x,facts) for x in item.get("criteria",[])]
        status_order={STATUSES["supported"]:6,STATUSES["medical"]:5,STATUSES["adjudicative"]:4,STATUSES["potential"]:3,STATUSES["conflict"]:2,STATUSES["insufficient"]:1}
        overall=max((x["status"] for x in criteria),key=lambda s:status_order.get(s,0),default=STATUSES["not_estimable"])
        supported=[x["percent"] for x in criteria if x["percent"] is not None and x["status"]==STATUSES["supported"]]
        plausible=[x["percent"] for x in criteria if x["percent"] is not None and x["status"] in {STATUSES["supported"],STATUSES["potential"],STATUSES["medical"],STATUSES["adjudicative"]}]
        results.append({"diagnostic_code":code,"title":item["title"],"body_system":item.get("body_system"),"automatable":item.get("automatable"),"overall_status":overall,"candidate_range":{"lowest":min(plausible) if plausible else None,"highest":max(plausible) if plausible else None,"fully_supported_highest":max(supported) if supported else None},"criteria":criteria,"laterality_matters":item.get("laterality_matters"),"notes":item.get("notes",[]),"source_ids":item.get("source_ids",[]),"separate_issue_flags":item.get("separate_issue_flags",[])})
    stale=as_of>datetime.strptime(snapshot["stale_after"],"%Y-%m-%d").date()
    flags=[]
    for key,label in {"unemployability_possible":"TDIU requires separate analysis; it is not added to the basic combined percentage.","recent_surgery_or_cast":"Temporary convalescence may require separate analysis.","recent_hospitalization_over_21_days":"Temporary hospitalization evaluation may require separate analysis.","loss_of_use_possible":"SMC or loss-of-use analysis may be required separately.","protected_evaluation_question":"Reduction/protection rules require separate analysis."}.items():
        if (record.get("flags") or {}).get(key):flags.append(label)
    flags+=overlap_flags(candidates)
    warnings=["Educational candidate comparison only; not an official VA rating or grant prediction.","Severity evidence does not establish service connection, and service-connection evidence does not establish severity.","The snapshot is deliberately partial; codes outside it require current official-source review.","Qualitative terms such as mild, moderate, severe, and occupational or social impairment are not algorithmically determined."]
    if stale:warnings.insert(0,f"STALE DATA WARNING: bundled rating snapshot passed its re-verification date {snapshot['stale_after']}.")
    if not candidates:warnings.append("No candidate diagnostic code was supplied or safely matched; no rating comparison was attempted.")
    return {"estimator_version":VERSION,"as_of":as_of.isoformat(),"snapshot_id":snapshot["snapshot_id"],"snapshot_version":snapshot["snapshot_version"],"snapshot_effective_through":snapshot["effective_through"],"snapshot_stale":stale,"issue_id":record.get("issue_id"),"diagnosis_input":diagnosis,"input_facts":facts,"candidate_diagnostic_codes":candidates,"candidate_results":results,"separate_issue_flags":sorted(set(flags)),"warnings":warnings,"assumptions":["Only supplied facts were evaluated.","No diagnosis, nexus, in-service event, credibility determination, or service connection was inferred."],"source_ids":sorted({sid for r in results for sid in r.get("source_ids",[])})}

def main(argv:Sequence[str]|None=None)->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input",required=True,type=Path);p.add_argument("--snapshot",type=Path,default=Path(__file__).parents[1]/"references"/"data"/"rating_schedule_snapshot.json");p.add_argument("--as-of");p.add_argument("--output",type=Path);a=p.parse_args(argv)
    try:
        record=load_structured(a.input); snapshot=json.loads(a.snapshot.read_text(encoding="utf-8")); asof=datetime.strptime(a.as_of or str(record.get("as_of") or date.today().isoformat()),"%Y-%m-%d").date(); result=estimate(record,snapshot,asof)
    except (OSError,ValueError,EstimateInputError) as e:p.error(str(e))
    text=json.dumps(result,indent=2,sort_keys=True)
    if a.output:a.output.write_text(text+"\n",encoding="utf-8")
    else:print(text)
    return 0
if __name__=="__main__":raise SystemExit(main())
