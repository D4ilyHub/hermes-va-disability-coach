from datetime import date
import json
from pathlib import Path
from estimate_condition import estimate,STATUSES
ROOT=Path(__file__).parents[1];SNAP=json.loads((ROOT/'skills/va-disability-coach/references/data/rating_schedule_snapshot.json').read_text())
def rec(code='6260',diagnosis=True,facts=None,as_of='2026-07-16'):
 return {'as_of':as_of,'issue_id':'TEST-001','user_wording':'generic','confirmed_diagnosis':{'exists':diagnosis,'name':'generic diagnosis' if diagnosis else None,'source':'generic'},'candidate_diagnostic_codes':[code],'facts':facts or {},'flags':{}}
def test_tinnitus_supported():
 r=estimate(rec(facts={'tinnitus.recurrent':{'value':True,'provenance':{}}}),SNAP,date(2026,7,16));assert r['candidate_results'][0]['candidate_range']['fully_supported_highest']==10

def test_no_diagnosis():assert estimate(rec(diagnosis=False),SNAP,date(2026,7,16))['candidate_results'][0]['status']==STATUSES['not_estimable']
def test_outside():assert estimate(rec('9999'),SNAP,date(2026,7,16))['candidate_results'][0]['status']==STATUSES['outside']
def test_stale():assert estimate(rec(),SNAP,date(2027,1,1))['snapshot_stale'] is True
def test_input_preserved():
 x=rec();r=estimate(x,SNAP,date(2026,7,16));assert r['diagnosis_input']==x['confirmed_diagnosis']
def test_mental_is_judgment():
 r=estimate(rec('9411'),SNAP,date(2026,7,16));assert any(c['adjudicative_judgment_required'] for c in r['candidate_results'][0]['criteria'])
def test_overlap_flag():
 x=rec('9411');x['candidate_diagnostic_codes']=['9411','9434'];r=estimate(x,SNAP,date(2026,7,16));assert any('mental-health' in f for f in r['separate_issue_flags'])
def test_no_grant_probability_field():
 r=estimate(rec(),SNAP,date(2026,7,16));assert 'grant_probability' not in json.dumps(r)
