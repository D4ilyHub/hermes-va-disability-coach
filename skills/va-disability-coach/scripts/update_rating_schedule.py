#!/usr/bin/env python3
"""User-initiated eCFR change check and staging tool; never silently replaces the active snapshot."""
from __future__ import annotations
import argparse,hashlib,json,urllib.request
from datetime import date
from pathlib import Path
URL="https://www.ecfr.gov/api/versioner/v1/full/{date}/title-38.xml?part=4"
UA="hermes-va-disability-coach/1.0 (+public open-source maintenance check)"
def fetch(day:str)->bytes:
    req=urllib.request.Request(URL.format(date=day),headers={"User-Agent":UA,"Accept":"application/xml"})
    with urllib.request.urlopen(req,timeout=30) as r:return r.read()
def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--date",default=date.today().isoformat());p.add_argument("--stage",action="store_true",help="write raw official XML to a candidate file for manual review");p.add_argument("--reviewed-by",help="maintainer name required with --stage");p.add_argument("--output-dir",type=Path,default=Path.cwd()/"rating-update-candidates");a=p.parse_args()
    if a.stage and not a.reviewed_by:p.error("--reviewed-by is required with --stage")
    try:data=fetch(a.date)
    except Exception as e:print(f"FETCH FAILED: {e}");return 2
    digest=hashlib.sha256(data).hexdigest();result={"source_url":URL.format(date=a.date),"retrieval_date":date.today().isoformat(),"source_effective_date":a.date,"bytes":len(data),"sha256":digest,"active_snapshot_changed":False,"manual_review_required":True}
    if a.stage:
        a.output_dir.mkdir(parents=True,exist_ok=True);xml=a.output_dir/f"title-38-part-4-{a.date}.xml";meta=a.output_dir/f"title-38-part-4-{a.date}.json";xml.write_bytes(data);result["staged_xml"]=str(xml);result["reviewed_by_requester"]=a.reviewed_by;meta.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8");result["metadata_file"]=str(meta)
    print(json.dumps(result,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
