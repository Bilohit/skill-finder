"""The skill was written for one workspace and is being published for everyone.
These tests fail if a reference to its birthplace survives -- that is the whole
substance of the generalization, so it is the thing worth asserting."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "plugins" / "skill-finder" / "skills" / "skill-finder" / "SKILL.md"

# Every term that only means something inside the Second Thought workspace.
BIRTHPLACE_TERMS = (
    "Second Thought",
    "BUILD-STATE",
    "skill-catalog",
    "update_inventory",
    "ledger-wrap",
    "cavecrew",
    "device-qa",
    "cdp-qa",
    "tauri-v2",
    "expo-react-native-typescript",
    "argent",
    "graphify",
    "impeccable",
    "taste-skill",
    "uiux-pro-max",
    "check.py",
)


def test_skill_file_exists_and_is_not_a_stub():
    assert SKILL.is_file(), f"{SKILL} is missing"
    assert len(SKILL.read_text(encoding="utf-8").strip()) > 1500


def test_no_birthplace_terms_survive():
    text = SKILL.read_text(encoding="utf-8")
    for term in BIRTHPLACE_TERMS:
        assert term not in text, f"{term!r} is workspace-specific and must not ship"


def test_frontmatter_name_matches_the_plugin():
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert "\nname: skill-finder\n" in text


def test_core_discipline_survives_the_generalization():
    """Stripping the workspace references must not strip the point. The skill exists
    to say: the list is already in context, so read nothing and spawn nothing."""
    text = SKILL.read_text(encoding="utf-8")
    assert "already in context" in text
    assert "read nothing" in text
    assert "spawn nothing" in text


def test_no_emoji():
    text = SKILL.read_text(encoding="utf-8")
    for ch in text:
        assert ord(ch) < 0x2190, f"emoji or symbol {ch!r} in SKILL.md"


def test_no_bom():
    assert not SKILL.read_bytes().startswith(b"\xef\xbb\xbf")
