"""The manifests are load-bearing: a malformed one makes the plugin uninstallable
and the failure surfaces to a stranger, not to us."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# The skill's description lives in three places serving three renderers: the SKILL.md
# frontmatter (what the model triggers on), plugin.json (the plugin listing) and
# marketplace.json (the marketplace listing). Exact parity would degrade at least one
# of those jobs, so what is asserted instead is the signature claim -- every copy must
# still say the skill reads nothing and spawns nothing, in either phrasing.
DESCRIPTION_SOURCES = (
    ROOT / "plugins" / "skill-finder" / "skills" / "skill-finder" / "SKILL.md",
    ROOT / "plugins" / "skill-finder" / ".claude-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "marketplace.json",
)


def test_marketplace_is_valid_json_and_lists_skill_finder():
    data = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert data["name"] == "skill-finder"
    names = [p["name"] for p in data["plugins"]]
    assert "skill-finder" in names


def test_every_listed_plugin_has_a_manifest_at_its_source():
    data = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    for entry in data["plugins"]:
        manifest = ROOT / entry["source"].lstrip("./") / ".claude-plugin" / "plugin.json"
        assert manifest.is_file(), f"{entry['name']} has no plugin.json at {manifest}"
        assert json.loads(manifest.read_text(encoding="utf-8"))["name"] == entry["name"]


def test_every_description_carries_the_signature_claim():
    """Three near-duplicate descriptions drift silently -- a rewrite of one leaves the
    other two contradicting it with no failure anywhere. Byte parity is the wrong fix
    (each copy serves a different renderer), so the anchor is semantic: the claim the
    whole skill exists to make must survive every rewrite, in every copy."""
    for path in DESCRIPTION_SOURCES:
        text = path.read_text(encoding="utf-8")
        assert re.search(r"reads? no(thing|\s+files)", text, re.I), (
            f"{path.name} lost the 'reads nothing' claim"
        )
        assert re.search(r"spawns? no(thing|\s+agents)", text, re.I), (
            f"{path.name} lost the 'spawns nothing' claim"
        )


def test_no_emoji_in_manifests():
    for path in ROOT.rglob(".claude-plugin/*.json"):
        text = path.read_text(encoding="utf-8")
        assert all(ord(ch) < 0x2190 for ch in text), f"non-ascii symbol in {path}"
