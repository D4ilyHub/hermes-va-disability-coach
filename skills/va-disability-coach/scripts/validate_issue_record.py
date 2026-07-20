#!/usr/bin/env python3
"""Validate an issue record against the bundled JSON Schema."""
from __future__ import annotations
import argparse,json
from datetime import date,datetime
from pathlib import Path
try: import yaml
except ImportError: yaml=None
try: import jsonschema
except ImportError: jsonschema=None

def normalize(value):
    if isinstance(value,(date,datetime)): return value.isoformat()
    if isinstance(value,dict): return {str(k):normalize(v) for k,v in value.items()}
    if isinstance(value,list): return [normalize(v) for v in value]
    return value

def load(path:Path):
    text=path.read_text(encoding="utf-8")
    if path.suffix.lower()==".json": return normalize(json.loads(text))
    if yaml is None: raise RuntimeError("PyYAML is required for YAML input; install the validation extra")
    return normalize(yaml.safe_load(text))

def errors(record,schema):
    if jsonschema is None: raise RuntimeError("jsonschema is required; install the validation extra")
    return [f"{'.'.join(map(str,e.absolute_path)) or '<root>'}: {e.message}" for e in sorted(jsonschema.Draft202012Validator(schema).iter_errors(record),key=lambda x:list(x.absolute_path))]

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("record",type=Path);p.add_argument("--schema",type=Path,default=Path(__file__).parents[1]/"templates"/"issue_record.schema.json");a=p.parse_args()
    try: es=errors(load(a.record),json.loads(a.schema.read_text(encoding="utf-8")))
    except (OSError,ValueError,RuntimeError) as e: print(f"ERROR: {e}");return 2
    if es:
        print("INVALID");[print(f"- {x}") for x in es];return 1
    print("VALID");return 0
if __name__=="__main__":raise SystemExit(main())
