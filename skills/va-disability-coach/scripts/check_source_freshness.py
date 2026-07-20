#!/usr/bin/env python3
"""Check source-registry and rating-snapshot re-verification dates; no network use."""
from __future__ import annotations
import argparse,csv,json
from datetime import date,datetime
from pathlib import Path

def parse(v:str):return datetime.strptime(v,"%Y-%m-%d").date()
def check(registry:Path,snapshot:Path,as_of:date)->dict:
    rows=list(csv.DictReader(registry.open(encoding="utf-8",newline="")))
    stale=[];invalid=[]
    for r in rows:
        try:
            if parse(r["reverification_date"])<as_of:stale.append(r["source_id"])
        except Exception:invalid.append(r.get("source_id","<missing>"))
    s=json.loads(snapshot.read_text(encoding="utf-8"));snapshot_stale=parse(s["stale_after"])<as_of
    return {"as_of":as_of.isoformat(),"source_count":len(rows),"stale_source_count":len(stale),"stale_source_ids":stale,"invalid_reverification_dates":invalid,"snapshot_stale":snapshot_stale,"snapshot_stale_after":s["stale_after"],"status":"STALE" if stale or invalid or snapshot_stale else "CURRENT"}
def main()->int:
    root=Path(__file__).parents[1];p=argparse.ArgumentParser(description=__doc__);p.add_argument("--registry",type=Path,default=root/"references"/"data"/"source_registry.csv");p.add_argument("--snapshot",type=Path,default=root/"references"/"data"/"rating_schedule_snapshot.json");p.add_argument("--as-of",default=date.today().isoformat());p.add_argument("--json",action="store_true");a=p.parse_args();r=check(a.registry,a.snapshot,parse(a.as_of));print(json.dumps(r,indent=2,sort_keys=True) if a.json else f"{r['status']}: {r['stale_source_count']} stale sources; snapshot stale={r['snapshot_stale']}");return 1 if r["status"]=="STALE" else 0
if __name__=="__main__":raise SystemExit(main())
