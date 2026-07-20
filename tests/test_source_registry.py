import csv,json
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).parents[1];ROWS=list(csv.DictReader(open(ROOT/'SOURCE_REGISTRY.csv',encoding='utf-8')))
def test_counts():assert len(ROWS)>=200;assert sum(r['official_primary']=='Yes' for r in ROWS)>=120;assert sum(r['clinical']=='Yes' for r in ROWS)>=30
def test_domains():assert len({urlparse(r['url_or_locator']).netloc.lower().removeprefix('www.') for r in ROWS if r['url_or_locator'].startswith('http')})>=40
def test_ids_unique():assert len({r['source_id'] for r in ROWS})==len(ROWS)
def test_required_metadata():
 for r in ROWS:
  for k in ['authority_class_label','effective_date','access_date','reliability_assessment','reverification_date']:assert r[k]
def test_runtime_copy_equal():assert (ROOT/'SOURCE_REGISTRY.csv').read_bytes()==(ROOT/'skills/va-disability-coach/references/data/source_registry.csv').read_bytes()
