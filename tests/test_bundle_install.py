from pathlib import Path
from validate_skill_bundle import validate

ROOT = Path(__file__).parents[1]


def test_bundle_validator():
    result = validate(ROOT)
    assert result["status"] == "PASS", result["errors"]
    assert result["runtime_files"] >= 60


def test_no_profile_files():
    names = {p.name for p in ROOT.rglob("*")}
    assert not {"SOUL.md", "USER.md", "MEMORY.md", "config.yaml"} & names


def test_frontmatter_and_path():
    text = (ROOT / "skills/va-disability-coach/SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\nname: va-disability-coach\n")


def test_simulated_exact_reference_install(tmp_path):
    """Simulate Hermes' exact-reference bundle copy for a direct URL/GitHub install."""
    import re
    import shutil

    skill = ROOT / "skills/va-disability-coach"
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    supported = ("references/", "templates/", "scripts/", "examples/", "assets/")
    targets = {
        match
        for match in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
        if match.startswith(supported)
    }
    destination = tmp_path / "va-disability-coach"
    destination.mkdir()
    shutil.copy2(skill / "SKILL.md", destination / "SKILL.md")
    for rel in targets:
        source = skill / rel
        assert source.is_file()
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    expected = {
        p.relative_to(skill).as_posix()
        for folder in supported
        for p in (skill / folder.rstrip("/")).rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    }
    installed = {
        p.relative_to(destination).as_posix()
        for p in destination.rglob("*")
        if p.is_file()
    } - {"SKILL.md"}
    assert installed == expected
