from pathlib import Path
from datetime import datetime
import csv,json,pytest
from combine_ratings import Evaluation,calculate
from estimate_condition import estimate
from generate_transition_plan import generate_plan
ROOT=Path(__file__).parents[1]
FILES=sorted(ROOT.glob('tests/*_scenarios.jsonl'))
SCENARIOS=[]
for path in FILES:
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip(): SCENARIOS.append((path.name,json.loads(line)))
REQUIRED={'id','category','input','expected_behavior','prohibited_behavior','required_source_class','required_skill_reference','pass_criteria','actual_result','remediation'}
SOURCE_IDS={r['source_id'] for r in csv.DictReader(open(ROOT/'SOURCE_REGISTRY.csv',encoding='utf-8'))}
SNAP=json.loads((ROOT/'skills/va-disability-coach/references/data/rating_schedule_snapshot.json').read_text())

@pytest.mark.parametrize('filename,s',SCENARIOS,ids=[x[1]['id'] for x in SCENARIOS])
def test_scenario_contract(filename,s):
    assert REQUIRED <= set(s)
    assert s['expected_behavior'] and s['prohibited_behavior'] and s['pass_criteria']
    assert s['actual_result'].startswith('PASS:')
    ref=ROOT/'skills/va-disability-coach'/s['required_skill_reference']
    assert ref.exists(), (filename,ref)
    cat=s['category']
    if cat=='combined':
        r=calculate([Evaluation.from_mapping(x,i) for i,x in enumerate(s['input']['evaluations'])])
        assert r['rounded_final_evaluation']==s['expected_final']
        assert {'CFR-4.25','CFR-4.26'} <= set(r['regulatory_citations'])
    elif cat=='estimator':
        r=estimate(s['input'],SNAP,datetime.strptime(s['input']['as_of'],'%Y-%m-%d').date())
        statuses={x.get('status') or x.get('overall_status') for x in r['candidate_results']}
        assert s['expected_status'] in statuses
    elif cat=='transition':
        i=s['input'];r=generate_plan(datetime.strptime(i['separation_date'],'%Y-%m-%d').date(),datetime.strptime(i['as_of'],'%Y-%m-%d').date(),i['retirement'],True,i['unexpected_separation'])
        days=r['days_remaining'];bucket='past' if days<0 else 'under_90' if days<90 else 'bdd_window' if days<=180 else 'over_180'
        assert bucket==s['expected_bucket']
    elif cat=='citation': assert s['source_id'] in SOURCE_IDS
