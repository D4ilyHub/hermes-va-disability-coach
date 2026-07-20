from pathlib import Path


ROOT = Path(__file__).parents[1]
SKILL = ROOT / "skills" / "va-disability-coach"
STYLE = SKILL / "references" / "COACHING_STYLE.md"


def test_coaching_style_is_routed_and_manifested():
    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    index_text = (SKILL / "references" / "INDEX.md").read_text(encoding="utf-8")

    assert STYLE.is_file()
    assert "](references/COACHING_STYLE.md)" in skill_text
    assert "Apply `COACHING_STYLE.md` in every mode" in index_text


def test_coaching_style_has_calibration_contract():
    text = STYLE.read_text(encoding="utf-8")
    required_sections = {
        "## Collaborative does not mean passive",
        "## Boundary calibration",
        "## Care and documentation can be pursued together",
        "## Rating-aware without target manipulation",
        "## Treatment and prescription conversations",
        "## Context is a question generator, not a verdict",
        "## Correction protocol",
    }

    assert required_sections <= set(text.splitlines())
    assert "Do not merely soften the wording while retaining the rejected assumption." in text
    assert "Disagreement with the coach is not a safety issue." in text
    assert "Do not assume that mentioning treatment is “claim chasing.”" in text


def test_coaching_regression_scenarios_cover_learned_failure_modes():
    scenario_text = (ROOT / "tests" / "coaching_scenarios.jsonl").read_text(encoding="utf-8")

    for scenario_id in range(1, 7):
        assert f'"COACHING-{scenario_id:03d}"' in scenario_text

    for concept in [
        "benefit-aware recommendation",
        "preserve clinician judgment",
        "pattern-to-question-to-user-report-to-record-evidence ladder",
        "re-run the recommendation",
        "bounded help",
        "unsafe component is refused",
    ]:
        assert concept in scenario_text
