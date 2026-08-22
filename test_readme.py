"""The README is the only thing most visitors read. A prose instruction to 'write a
good README' is unenforceable; these assertions are what 'good' means here."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"

# Every document a stranger reads before or instead of the skill. A scan that covers only
# README.md misses the three files most likely to pick up a leftover from the codebase this
# skill was generalized out of -- nothing else here was ever checked for it.
ROOT_DOCS = (
    ROOT / "README.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "docs" / "concepts.md",
    ROOT / "docs" / "walkthrough.md",
)


def test_readme_carries_both_install_lines():
    text = README.read_text(encoding="utf-8")
    assert "/plugin marketplace add Bilohit/skill-finder" in text
    assert "/plugin install skill-finder" in text


def test_readme_opens_with_the_banner():
    """The banner is the first thing rendered on the repository page. A README that
    stops referencing it does not fail anywhere else -- the image simply vanishes."""
    first = README.read_text(encoding="utf-8").lstrip().splitlines()[0]
    assert first == "![skill-finder](assets/banner.svg)", first


def test_readme_states_the_problem_and_is_not_a_stub():
    text = README.read_text(encoding="utf-8")
    match = re.search(r"^## The problem\s*\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
    assert match, "no '## The problem' section found"
    assert len(match.group(1).strip()) > 200, "The problem section is a stub"


def test_readme_shows_the_output_it_promises():
    """The skill's entire deliverable is a two-line loadout. A README that describes
    that without ever printing one is asking to be taken on trust."""
    text = README.read_text(encoding="utf-8")
    assert "## See it" in text
    assert "Loadout:" in text
    assert "Skipped:" in text


def test_credits_section_is_specific_about_third_party_status():
    """A bare 'Credits' heading would pass a substring check while promising nothing.
    This checks the section says something real: whether third-party code is bundled,
    and points at the license that governs the original work either way."""
    text = README.read_text(encoding="utf-8")
    match = re.search(r"^## Credits\s*\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
    assert match, "no '## Credits' section found"
    section = match.group(1).strip()
    assert len(section) > 80, "Credits section is a stub"
    assert "third-party" in section.lower()
    assert "MIT" in section or "LICENSE" in section


def test_svgs_are_dark_ink_on_an_explicit_white_plate():
    """These marks ship on a white plate, so the ink is a fixed near-black rather than
    currentColor: an inherited ink on a white ground goes invisible the moment the host
    page is dark. Both halves are asserted, because either one alone is the bug."""
    for name in ("mark.svg", "banner.svg"):
        text = (ROOT / "assets" / name).read_text(encoding="utf-8")
        assert "currentColor" not in text, f"{name} inherits its ink onto a white plate"
        assert 'fill="#FFFFFF"' in text, f"{name} has no white plate"
        assert "#141414" in text, f"{name} does not use the fixed ink"


def test_no_emoji_in_any_root_document():
    for path in ROOT_DOCS:
        for ch in path.read_text(encoding="utf-8"):
            assert ord(ch) < 0x2190, f"emoji or symbol {ch!r} in {path}"


def test_no_bom_in_any_root_document():
    for path in ROOT_DOCS:
        assert not path.read_bytes().startswith(b"\xef\xbb\xbf"), f"BOM in {path}"


def test_readme_names_the_license():
    assert "MIT" in README.read_text(encoding="utf-8")


def test_docs_and_contributing_exist_and_are_not_stubs():
    for rel in ("docs/concepts.md", "docs/walkthrough.md", "CONTRIBUTING.md"):
        path = ROOT / rel
        assert path.is_file(), f"{rel} is missing"
        assert len(path.read_text(encoding="utf-8").strip()) > 400, f"{rel} looks like a stub"
