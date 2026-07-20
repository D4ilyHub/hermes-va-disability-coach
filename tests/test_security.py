from pathlib import Path
import re

ROOT = Path(__file__).parents[1]
TEXT_SUFFIXES = {".md", ".py", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".txt", ".csv", ".cff"}


def public_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in {".git", "__pycache__", ".pytest_cache"} for part in path.parts):
            continue
        yield path, path.read_text(encoding="utf-8")


def test_no_scheduled_workflows():
    for path in (ROOT / ".github/workflows").glob("*.yml"):
        assert not re.search(r"^\s*schedule\s*:", path.read_text(encoding="utf-8"), re.M)


def test_no_external_action_code():
    scripts = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "skills/va-disability-coach/scripts").glob("*.py")
    )
    assert "requests.post" not in scripts
    assert "subprocess.run" not in scripts
    assert "selenium" not in scripts


def test_updater_not_automatic():
    text = (ROOT / "skills/va-disability-coach/scripts/update_rating_schedule.py").read_text(encoding="utf-8")
    assert "--stage" in text
    assert "active_snapshot_changed" in text


def test_examples_deidentified():
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "skills/va-disability-coach/examples").glob("*")
        if path.suffix in {".md", ".json"}
    )
    assert "SSN" not in text
    assert "@" not in text


def test_repository_has_no_obvious_personal_identifiers_or_home_paths():
    patterns = {
        "macOS home path": re.compile(r"(?<![A-Za-z0-9:/])/[U]sers/[^/\s]+/"),
        "Linux home path": re.compile(r"(?<![A-Za-z0-9:/])/[h]ome/[^/\s]+/"),
        "email address": re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
        "US phone number": re.compile(r"(?<!\d)(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)"),
        "SSN-like value": re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)"),
    }

    for path, text in public_text_files():
        if path.resolve() == Path(__file__).resolve():
            continue
        for label, pattern in patterns.items():
            assert not pattern.search(text), f"possible {label} in {path.relative_to(ROOT)}"


def test_no_profile_control_files_or_os_metadata():
    forbidden = {"SOUL.md", "USER.md", "MEMORY.md", "credentials.json", "secrets.json", ".DS_Store"}
    present = {path.name for path in ROOT.rglob("*") if path.is_file()}
    assert forbidden.isdisjoint(present)


def test_core_scripts_have_no_runtime_dependencies():
    for name in ["combine_ratings.py", "generate_transition_plan.py"]:
        text = (ROOT / "skills/va-disability-coach/scripts" / name).read_text(encoding="utf-8")
        assert "requests" not in text
        assert "pandas" not in text
