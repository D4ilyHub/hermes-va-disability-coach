#!/usr/bin/env python3
"""Generate a source-backed date-relative separation plan."""
from __future__ import annotations
import argparse,json
from datetime import date,datetime,timedelta
from pathlib import Path
from typing import Sequence
VERSION="1.0.0"
class PlannerInputError(ValueError): pass

def parse_date(v:str)->date:
    try:return datetime.strptime(v,"%Y-%m-%d").date()
    except ValueError as e: raise PlannerInputError(f"invalid date {v!r}; use YYYY-MM-DD") from e

def generate_plan(separation_date:date,as_of:date,retirement:bool=False,bdd_intended:bool=True,unexpected_separation:bool=False)->dict:
    remaining=(separation_date-as_of).days
    items=[]
    items.append((-730 if retirement else -540,"recommended planning milestone","Begin transition planning; identify care gaps and unresolved health concerns.","DOD-TAP-EVENTS","DoD recommends early planning; this is not a VA claim deadline."))
    items += [
    (-365,"official deadline / requirement","Begin the normal TAP process, Initial Counseling, and pre-separation counseling.","DOD-TAP-EVENTS; DODI-1332.35","When separation is unanticipated or fewer than 365 days remain, begin promptly and use service guidance."),
    (-330,"recommended planning milestone","Create a body-system-neutral health issue inventory and seek medically appropriate evaluation.","VA-EVIDENCE; CLIN-PATIENT-AGENDA","Care first; do not delay care to build a claim."),
    (-300,"recommended planning milestone","Request and reconcile service, civilian, behavioral health, dental, hearing, vision, sleep, surgical, medication, exposure, personnel, and line-of-duty records.","VA-EVIDENCE; DOD-SHA","Track requested, received, missing, and contradictory records."),
    (-240,"recommended planning milestone","Prepare concise symptom-and-function agendas for routine and specialty appointments, including sensitive topics.","CLIN-PATIENT-AGENDA; CLIN-MILITARY-CULTURE","Do not request unsupported diagnoses or nexus language."),
    (-180,"official eligibility-window opening","Ordinary BDD filing window opens for otherwise eligible full-time service members.","VA-BDD","Verify known separation date, exam availability, exclusions, and current requirements; SHA Part A is required."),
    (-150,"optional best practice","If using BDD, filing earlier in the window can preserve examination and response margin.","VA-BDD","Planning recommendation, not a separate deadline."),
    (-90,"official eligibility-window closing","Ordinary BDD window closes; fewer than 90 days generally uses another applicable claim path.","VA-BDD","Verify current VA instructions and special handling."),
    (-90,"official deadline / requirement","Complete TAP Capstone under the normal timeline.","DOD-TAP-EVENTS","Service-specific exceptions may apply."),
    (-75,"recommended planning milestone","Confirm whether VA or DoD will conduct the Separation Health Assessment.","VA-SHA; DOD-SHA","VA generally schedules SHA for BDD/IDES; DoD generally conducts it outside BDD/IDES or with fewer than 90 days."),
    (-60,"recommended planning milestone","Obtain personal copies of records and arrange continuity of prescriptions, equipment, and specialty care.","VA-EVIDENCE","Do not assume continued access to service systems."),
    (-30,"recommended planning milestone","Confirm C&P logistics and prepare factual issue-by-issue notes describing typical and flare/worst functional periods.","VA-C&P","Do not rehearse target criteria or exaggerate."),
    (0,"separation event","Preserve separation documents and confirm post-service contact information and care.","VA-EVIDENCE","No decision or payment date is guaranteed."),
    (30,"recommended post-separation follow-up","Review correspondence, attend exams, continue care, and preserve new records.","VA-C&P; VA-STATUS","Follow deadlines in actual notices."),
    (90,"recommended post-separation follow-up","Review claim status, evidence gaps, and whether accredited help is appropriate.","VA-REP; VA-OGC-ACCREDITATION","Verify accreditation."),
    (365,"matter requiring professional advice","Review effective-date consequences and one-year post-separation provisions if relevant.","CFR-3.400; USC-5110","Effective dates are fact-specific; seek accredited advice for material issues.")]
    milestones=[]
    for offset,classification,action,authority,notes in items:
        on=separation_date+timedelta(days=offset)
        milestones.append({"date":on.isoformat(),"days_relative_to_separation":offset,"classification":classification,"action":action,"authority":authority,"notes":notes,"status":"past" if on<as_of else "today" if on==as_of else "upcoming"})
    milestones.sort(key=lambda x:(x["date"],x["classification"],x["action"]))
    alerts=[]
    if remaining<0: alerts.append("The separation date has passed; use post-separation claim and continuity-of-care pathways.")
    elif remaining<90: alerts.append("Fewer than 90 days remain. The ordinary BDD window is closed; review another applicable claim path and complete separation-health steps promptly.")
    elif remaining<=180: alerts.append("The date is within the ordinary 180-to-90-day BDD window. Verify eligibility before relying on BDD.")
    else: alerts.append("More than 180 days remain. Use the time for care, records, inventory, and transition preparation.")
    if unexpected_separation and remaining<365: alerts.append("Because separation is unanticipated, normal 365-day TAP actions should begin as soon as possible.")
    if not bdd_intended: alerts.append("BDD was not selected; BDD dates remain for awareness only.")
    return {"planner_version":VERSION,"generated_as_of":as_of.isoformat(),"separation_date":separation_date.isoformat(),"days_remaining":remaining,"assumptions":{"retirement":retirement,"bdd_intended":bdd_intended,"unexpected_separation":unexpected_separation},"alerts":alerts,"milestones":milestones,"disclaimer":"Educational planning aid. Verify current requirements and personal eligibility with official sources or an accredited representative. Recommended milestones are not legal deadlines."}

def markdown(p:dict)->str:
    lines=["# Date-relative separation plan","",f"- **As of:** {p['generated_as_of']}",f"- **Proposed separation:** {p['separation_date']}",f"- **Days remaining:** {p['days_remaining']}","","## Alerts",""]+[f"- {x}" for x in p["alerts"]]+["","## Milestones","","| Date | Relative day | Classification | Action | Authority | Status |","|---|---:|---|---|---|---|"]
    for m in p["milestones"]:
        action=m["action"].replace("|","\\|")
        lines.append(f"| {m['date']} | {m['days_relative_to_separation']} | {m['classification']} | {action} | {m['authority']} | {m['status']} |")
    return "\n".join(lines+["",f"> {p['disclaimer']}",""])

def main(argv:Sequence[str]|None=None)->int:
    q=argparse.ArgumentParser(description=__doc__);q.add_argument("--separation-date",required=True);q.add_argument("--as-of",default=date.today().isoformat());q.add_argument("--retirement",action="store_true");q.add_argument("--no-bdd",action="store_true");q.add_argument("--unexpected-separation",action="store_true");q.add_argument("--format",choices=["json","markdown"],default="markdown");q.add_argument("--output",type=Path);a=q.parse_args(argv)
    try:p=generate_plan(parse_date(a.separation_date),parse_date(a.as_of),a.retirement,not a.no_bdd,a.unexpected_separation)
    except PlannerInputError as e:q.error(str(e))
    out=json.dumps(p,indent=2,sort_keys=True) if a.format=="json" else markdown(p)
    if a.output:a.output.write_text(out+"\n",encoding="utf-8")
    else:print(out)
    return 0
if __name__=="__main__":raise SystemExit(main())
