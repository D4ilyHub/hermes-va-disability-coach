#!/usr/bin/env python3
"""Validate repository structure, Hermes references, source metadata, and safe defaults."""
from __future__ import annotations
import argparse,csv,hashlib,json,re,sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse
try: import yaml
except ImportError: yaml=None

FORBIDDEN_NAMES={"SOUL.md","USER.md","MEMORY.md","config.yaml","credentials.json","secrets.json"}
RUNTIME_DIRS=("references","templates","scripts","examples","assets")
REQUIRED_SOURCE_FIELDS={"source_id","title","publisher","url_or_locator","effective_date","access_date","authority_class","authority_class_label","binding_status","reliability_assessment","superseded_status","reverification_date"}

class Validation:
 def __init__(self):self.errors=[];self.warnings=[];self.checks=0
 def ok(self,condition,msg):
  self.checks+=1
  if not condition:self.errors.append(msg)

def frontmatter(text:str):
 if not text.startswith("---\n"):raise ValueError("SKILL.md lacks YAML frontmatter")
 end=text.find("\n---\n",4)
 if end<0:raise ValueError("SKILL.md frontmatter is not closed")
 raw=text[4:end]
 if yaml is None:raise RuntimeError("PyYAML is required")
 return yaml.safe_load(raw),text[end+5:]

def local_links(path:Path,text:str):
 for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)",text):
  target=target.strip().split()[0].strip("<>")
  if target.startswith(("http://","https://","mailto:","#")):continue
  clean=target.split("#",1)[0]
  if clean:yield (path.parent/clean).resolve(),target

def validate(root:Path)->dict:
 v=Validation();skill=root/'skills'/'va-disability-coach';sm=skill/'SKILL.md'
 v.ok(root.name=='hermes-va-disability-coach',"repository directory must be hermes-va-disability-coach")
 v.ok(sm.is_file(),"missing skills/va-disability-coach/SKILL.md")
 for p in root.rglob('*'):
  if p.name in FORBIDDEN_NAMES:v.errors.append(f"forbidden profile/credential file: {p.relative_to(root)}")
 text=sm.read_text(encoding='utf-8') if sm.exists() else ''
 try:
  fm,_=frontmatter(text);v.ok(fm.get('name')=='va-disability-coach',"frontmatter name mismatch");v.ok(fm.get('version')=='1.0.0',"frontmatter version mismatch");v.ok(bool(fm.get('description')),"frontmatter description missing")
 except Exception as e:v.errors.append(str(e));fm={}
 runtime=[p for d in RUNTIME_DIRS for p in (skill/d).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
 for p in runtime:
  rel=p.relative_to(skill).as_posix();v.ok(f"]({rel})" in text,f"runtime file is not explicitly referenced in SKILL.md: {rel}")
 for p in list(root.rglob('*.md')):
  t=p.read_text(encoding='utf-8')
  for resolved,target in local_links(p,t):v.ok(resolved.exists(),f"broken local link in {p.relative_to(root)}: {target}")
 # structured files
 for p in root.rglob('*.json'):
  if any(x in p.parts for x in ('.git','__pycache__')):continue
  try:json.loads(p.read_text(encoding='utf-8'));v.checks+=1
  except Exception as e:v.errors.append(f"invalid JSON {p.relative_to(root)}: {e}")
 if yaml:
  for p in [*root.rglob('*.yaml'),*root.rglob('*.yml')]:
   if p.name=='SKILL.md':continue
   try:yaml.safe_load(p.read_text(encoding='utf-8'));v.checks+=1
   except Exception as e:v.errors.append(f"invalid YAML {p.relative_to(root)}: {e}")
 for p in root.rglob('*.csv'):
  try:
   with p.open(encoding='utf-8',newline='') as f:
    r=csv.reader(f);rows=list(r);v.ok(bool(rows) and bool(rows[0]),f"empty CSV {p.relative_to(root)}")
  except Exception as e:v.errors.append(f"invalid CSV {p.relative_to(root)}: {e}")
 # source registry
 reg=skill/'references'/'data'/'source_registry.csv'
 try:
  with reg.open(encoding='utf-8',newline='') as f:src=list(csv.DictReader(f))
  v.ok(REQUIRED_SOURCE_FIELDS.issubset(src[0]),"source registry missing required columns")
  ids=[r['source_id'] for r in src];v.ok(len(ids)==len(set(ids)),"duplicate source IDs")
  v.ok(len(src)>=200,"fewer than 200 substantive source rows")
  normalized={urlparse(r['url_or_locator']).netloc.lower().removeprefix('www.') for r in src if r['url_or_locator'].startswith('http')};v.ok(len(normalized)>=40,"fewer than 40 unique domains")
  v.ok(sum(r.get('official_primary')=='Yes' for r in src)>=120,"fewer than 120 official/primary sources")
  v.ok(sum(r.get('clinical')=='Yes' for r in src)>=30,"fewer than 30 clinical sources")
  for r in src:
   v.ok(all((r.get(f) or '').strip() for f in REQUIRED_SOURCE_FIELDS),f"source {r.get('source_id')} has blank required metadata")
  root_hash=hashlib.sha256((root/'SOURCE_REGISTRY.csv').read_bytes()).hexdigest();skill_hash=hashlib.sha256(reg.read_bytes()).hexdigest();v.ok(root_hash==skill_hash,"root and runtime source registries differ")
 except Exception as e:v.errors.append(f"source registry validation failed: {e}");src=[];ids=[]
 # snapshot
 try:
  snap=json.loads((skill/'references'/'data'/'rating_schedule_snapshot.json').read_text(encoding='utf-8'))
  v.ok(snap.get('coverage_status')=='partial',"rating snapshot must declare partial coverage")
  codes=[str(x['diagnostic_code']) for x in snap['diagnostic_codes']];v.ok(len(codes)==len(set(codes)),"duplicate diagnostic codes")
  for code in snap['diagnostic_codes']:
   v.ok(bool(code.get('source_ids')),f"code {code.get('diagnostic_code')} lacks source IDs")
   for sid in code.get('source_ids',[]):v.ok(sid in ids,f"snapshot source ID missing from registry: {sid}")
 except Exception as e:v.errors.append(f"snapshot validation failed: {e}")
 # workflows and Python
 for p in (root/'.github'/'workflows').glob('*.yml'):
  v.ok(not re.search(r'^\s*schedule\s*:',p.read_text(encoding='utf-8'),re.M),f"active scheduled workflow found: {p.name}")
 import py_compile
 for p in (skill/'scripts').glob('*.py'):
  try:py_compile.compile(str(p),doraise=True);v.checks+=1
  except Exception as e:v.errors.append(f"Python syntax error {p.name}: {e}")
 # sensitive patterns: flag actual assignment-like secrets, not explanatory words
 secret_re=re.compile(r'(?im)^\s*(?:api[_-]?key|token|password|secret)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{16,}')
 for p in root.rglob('*'):
  if p.is_file() and p.suffix.lower() in {'.md','.py','.json','.yaml','.yml','.toml','.txt','.csv','.cff'}:
   try:v.ok(not secret_re.search(p.read_text(encoding='utf-8')),f"possible embedded secret in {p.relative_to(root)}")
   except UnicodeDecodeError:pass
 return {"status":"PASS" if not v.errors else "FAIL","checks":v.checks,"errors":v.errors,"warnings":v.warnings,"runtime_files":len(runtime),"source_rows":len(src)}

def main()->int:
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo-root',type=Path,default=Path(__file__).parents[3]);p.add_argument('--json',action='store_true');a=p.parse_args();r=validate(a.repo_root.resolve());print(json.dumps(r,indent=2,sort_keys=True) if a.json else f"{r['status']}: {r['checks']} checks, {len(r['errors'])} errors\n"+'\n'.join(f"- {x}" for x in r['errors']));return 0 if r['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
