#!/usr/bin/env python3
"""Deterministic educational implementation of 38 C.F.R. §§ 4.25 and 4.26."""
from __future__ import annotations
import argparse, itertools, json
from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Iterable, Sequence

VERSION = "1.0.0"
SNAPSHOT_DATE = "2026-07-13"
CITATIONS = ["CFR-4.25", "CFR-4.26", "FR-BILATERAL-2023"]

class RatingInputError(ValueError): pass

@dataclass(frozen=True)
class Evaluation:
    percent: int
    label: str = "evaluation"
    side: str = "none"
    paired_group: str = "none"
    issue_id: str | None = None

    @classmethod
    def from_mapping(cls, raw: dict[str, Any], index: int) -> "Evaluation":
        if not isinstance(raw, dict): raise RatingInputError(f"evaluation {index} must be an object")
        value = raw.get("percent")
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 100:
            raise RatingInputError(f"evaluation {index} percent must be an integer from 0 through 100")
        side = str(raw.get("side", "none")).lower()
        if side not in {"left", "right", "bilateral", "none"}:
            raise RatingInputError(f"evaluation {index} side is invalid")
        return cls(value, str(raw.get("label", f"evaluation {index+1}")), side,
                   str(raw.get("paired_group", "none")) or "none", raw.get("issue_id"))


def round_half_up(value: Decimal) -> int:
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def combine_pair(left: int, right: int) -> tuple[int, dict[str, Any]]:
    if not all(isinstance(x, int) and not isinstance(x, bool) and 0 <= x <= 100 for x in (left, right)):
        raise RatingInputError("pair values must be whole numbers from 0 through 100")
    exact = Decimal(left) + Decimal(100-left) * Decimal(right) / Decimal(100)
    value = round_half_up(exact)
    return value, {"left": left, "right": right, "remaining_efficiency": 100-left,
                   "exact": f"{exact:.4f}", "table_value": value}


def combine_values(values: Iterable[int]) -> tuple[int, list[dict[str, Any]], list[int]]:
    order = sorted([int(v) for v in values if int(v) > 0], reverse=True)
    if not order: return 0, [], []
    current, steps = order[0], []
    for value in order[1:]:
        current, step = combine_pair(current, value); steps.append(step)
    return current, steps, order


def round_final(value: int) -> int:
    if value >= 100: return 100
    return min(100, ((value + 5)//10)*10)


def initial_bilateral(evals: Sequence[Evaluation]) -> list[int]:
    groups: dict[str, dict[str, list[int]]] = {}
    for i, e in enumerate(evals):
        if e.percent > 0 and e.side in {"left", "right"} and e.paired_group != "none":
            groups.setdefault(e.paired_group, {"left":[], "right":[]})[e.side].append(i)
    return sorted(i for sides in groups.values() if sides["left"] and sides["right"]
                  for i in sides["left"] + sides["right"])


def valid_subset(evals: Sequence[Evaluation], subset: frozenset[int]) -> bool:
    if len(subset) < 2: return False
    groups: dict[str, set[str]] = {}
    for i in subset:
        e = evals[i]
        if e.percent <= 0 or e.side not in {"left", "right"} or e.paired_group == "none": return False
        groups.setdefault(e.paired_group, set()).add(e.side)
    return bool(groups) and all(s == {"left", "right"} for s in groups.values())


def candidate_subsets(evals: Sequence[Evaluation]) -> list[frozenset[int]]:
    eligible = initial_bilateral(evals)
    result: set[frozenset[int]] = {frozenset()}
    if len(eligible) <= 16:
        for n in range(2, len(eligible)+1):
            for combo in itertools.combinations(eligible, n):
                sub = frozenset(combo)
                if valid_subset(evals, sub): result.add(sub)
    else:
        grouped: dict[str, list[int]] = {}
        for i in eligible: grouped.setdefault(evals[i].paired_group, []).append(i)
        groups = list(grouped.values())
        for mask in range(1, 1 << len(groups)):
            sub = frozenset(i for bit,g in enumerate(groups) if mask & (1<<bit) for i in g)
            if valid_subset(evals, sub): result.add(sub)
    return sorted(result, key=lambda s:(len(s), tuple(sorted(s))))


def calc_subset(evals: Sequence[Evaluation], subset: frozenset[int]) -> dict[str, Any]:
    components: list[tuple[int,int,str]] = []
    bilateral = None
    if subset:
        base, base_steps, _ = combine_values(evals[i].percent for i in subset)
        addition = Decimal(base) * Decimal("0.10")
        adjusted_exact = Decimal(base) + addition
        adjusted = round_half_up(adjusted_exact)
        bilateral = {"included_indices": sorted(subset),
                     "included_labels": [evals[i].label for i in sorted(subset)],
                     "bilateral_combined_value": base,
                     "bilateral_addition_exact": f"{addition:.4f}",
                     "bilateral_adjusted_exact": f"{adjusted_exact:.4f}",
                     "bilateral_value_used": adjusted,
                     "base_steps": base_steps}
        components.append((adjusted,-1,"bilateral aggregate"))
    for i,e in enumerate(evals):
        if i not in subset and e.percent > 0: components.append((e.percent,i,e.label))
    components.sort(key=lambda x:(-x[0],x[1]))
    raw, steps, _ = combine_values(x[0] for x in components)
    return {"raw":raw,"rounded":round_final(raw),"bilateral":bilateral,"steps":steps,
            "components":[{"percent":v,"source_index":None if i==-1 else i,"label":label} for v,i,label in components]}


def calculate(evals: Sequence[Evaluation]) -> dict[str, Any]:
    if not evals: raise RatingInputError("at least one evaluation is required")
    candidates=[]
    for subset in candidate_subsets(evals):
        calc=calc_subset(evals,subset)
        score=(calc["rounded"],calc["raw"],len(subset),tuple(sorted(subset)))
        candidates.append((score,subset,calc))
    _, chosen, best=max(candidates,key=lambda x:x[0])
    initial=frozenset(initial_bilateral(evals)); warnings=[]
    if any(e.percent==0 for e in evals): warnings.append("Zero-percent evaluations remain listed but do not change combined-rating math.")
    if any(e.percent==100 for e in evals): warnings.append("An existing 100-percent evaluation makes the basic combined result 100 percent; separate SMC review may still matter.")
    if any(e.percent % 10 for e in evals): warnings.append("One or more inputs are not multiples of 10; verify the official evaluation.")
    if initial and chosen != initial:
        omitted=[evals[i].label for i in sorted(initial-chosen)]
        warnings.append("38 C.F.R. § 4.26(d) most-favorable exception applied" + (f"; omitted from bilateral factor: {', '.join(omitted)}." if omitted else "."))
    if any(e.side in {"left","right"} and e.paired_group!="none" for e in evals) and not initial:
        warnings.append("No bilateral factor applied because no compensable left/right pair was supplied in one paired group.")
    warnings += ["The engine does not decide service connection, diagnostic-code selection, pyramiding, staged ratings, TDIU, SMC, temporary totals, or protection rules.",
                 "Educational estimate only; not an official VA rating."]
    return {"calculation_version":VERSION,"rating_schedule_snapshot_date":SNAPSHOT_DATE,
            "input_evaluations":[asdict(e) for e in evals],
            "included_bilateral_groups":sorted({evals[i].paired_group for i in chosen}),
            "bilateral":best["bilateral"],"combination_order":best["components"],
            "intermediate_combined_values":best["steps"],"raw_final_value":best["raw"],
            "rounded_final_evaluation":best["rounded"],"warnings":warnings,
            "regulatory_citations":CITATIONS}


def load(path: Path) -> list[Evaluation]:
    try: raw=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as e: raise RatingInputError(str(e)) from e
    if isinstance(raw,dict): raw=raw.get("evaluations")
    if not isinstance(raw,list): raise RatingInputError("input must be a list or an object with an evaluations list")
    if len(raw)>100: raise RatingInputError("maximum 100 evaluations")
    return [Evaluation.from_mapping(x,i) for i,x in enumerate(raw)]


def human(result: dict[str,Any]) -> str:
    lines=["VA combined-rating calculation (educational)",f"Version: {VERSION}",f"Snapshot: {SNAPSHOT_DATE}","","Inputs:"]
    lines += [f"- {e['label']}: {e['percent']}% (side={e['side']}, group={e['paired_group']})" for e in result["input_evaluations"]]
    b=result["bilateral"]
    if b:
        lines += ["","Bilateral factor:",f"- Included: {', '.join(b['included_labels'])}",f"- Combined value: {b['bilateral_combined_value']}",f"- 10% addition: {b['bilateral_addition_exact']}",f"- Adjusted: {b['bilateral_adjusted_exact']} -> {b['bilateral_value_used']}"]
    lines += ["","Combination order:"]+[f"- {x['label']}: {x['percent']}" for x in result["combination_order"]]
    lines += ["","Steps:"]+[f"- {s['left']} with {s['right']}: {s['exact']} -> {s['table_value']}" for s in result["intermediate_combined_values"]]
    lines += ["",f"Raw final value: {result['raw_final_value']}",f"Rounded final evaluation: {result['rounded_final_evaluation']}%","","Warnings:"]+[f"- {w}" for w in result["warnings"]]
    lines += ["","Source IDs:"]+[f"- {c}" for c in CITATIONS]
    return "\n".join(lines)


def main(argv: Sequence[str]|None=None)->int:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--input",required=True,type=Path); p.add_argument("--json",action="store_true"); a=p.parse_args(argv)
    try: r=calculate(load(a.input))
    except RatingInputError as e: p.error(str(e))
    print(json.dumps(r,indent=2,sort_keys=True) if a.json else human(r)); return 0
if __name__=="__main__": raise SystemExit(main())
