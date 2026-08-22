"""The README is the only thing most visitors read. A prose instruction to 'write a
good README' is unenforceable; these assertions are what 'good' means here."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"


def test_readme_carries_both_install_lines():
    text = README.read_text(encoding="utf-8")
    assert "/plugin marketplace add Bilohit/skill-finder" in text
    assert "/plugin install skill-finder" in text


def test_readme_states_the_problem_and_is_not_a_stub():
    text = README.read_text(encoding="utf-8")
    match = re.search(r"^## The problem\s*\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
    assert match, "no '## The problem' section found"
    assert len(match.group(1).strip()) > 200, "The problem section is a stub"


def test_readme_names_the_license():
    text = README.read_text(encoding="utf-8")
    assert "MIT" in text


def test_readme_has_no_emoji_and_no_bom():
    assert not README.read_bytes().startswith(b"\xef\xbb\xbf")
    for ch in README.read_text(encoding="utf-8"):
        assert ord(ch) < 0x2190, f"emoji or symbol {ch!r} in README.md"
