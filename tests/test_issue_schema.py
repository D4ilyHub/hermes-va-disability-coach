import json
from pathlib import Path
import yaml,jsonschema
from validate_issue_record import normalize
ROOT=Path(__file__).parents[1];SK=ROOT/'skills/va-disability-coach';SCHEMA=json.loads((SK/'templates/issue_record.schema.json').read_text())
def test_example_valid():jsonschema.Draft202012Validator(SCHEMA).validate(normalize(yaml.safe_load((SK/'templates/issue_record.yaml').read_text())))
def test_missing_required_invalid():
 errors=list(jsonschema.Draft202012Validator(SCHEMA).iter_errors({'issue_id':'ABC'}));assert errors
def test_provenance_required():assert 'source_provenance' in SCHEMA['required']
