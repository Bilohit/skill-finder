# Contributing

skill-finder is one markdown file and a small standard-library Python test suite -- no dependencies
to install, no build step.

## Running the tests

From the repository root:

```
python -m pytest -q
```

This runs every test in the repository: `test_readme.py`, `test_manifests.py` and `test_skill.py` at
the root. `pytest.ini` already puts the repository root on `pythonpath`, so no extra setup is
needed.

To run only this repository's own documentation checks:

```
python -m pytest test_readme.py -q
```

## What to change and where

- `plugins/skill-finder/skills/skill-finder/SKILL.md` -- the skill itself, and the only file the
  agent ever loads at run time. Everything else in this repository exists to describe it or to keep
  it honest.
- `test_skill.py` -- the guard that keeps the skill general. skill-finder was extracted from one
  project's private rules, so this file asserts that none of that project's vocabulary came with it,
  and that the core discipline (read nothing, spawn nothing, decide from what is already in context)
  survived the extraction. Add a term to `BIRTHPLACE_TERMS` whenever a new one would be a leak.
- `docs/` -- `concepts.md` defines the vocabulary the skill uses; `walkthrough.md` is one worked
  example from install to output. Keep both in sync with `SKILL.md` -- a reference that drifts from
  the thing it describes is worse than no reference at all.
- `assets/`, `README.md`, this file -- the page a stranger decides on.

## Ground rules

- The skill reads no files and spawns no agents. That is the whole point of it, so any change that
  adds a read or a dispatch to the selection pass needs to justify itself against the token cost it
  reintroduces -- the numbers in the README's "See it" section are what it has to beat.
- The two pass tables are the skill's interface. A new row goes in when a real task had nowhere to
  route, never on a hunch, and it names a *class* of skill rather than a specific one -- naming a
  particular vendor's skill would break the skill everywhere that skill is not installed.
- Skills are named generically in `SKILL.md` ("a systematic-debugging skill"), never by a specific
  invocable ID. The one exception is a project's own `CLAUDE.md`, which is allowed to bind those
  generic slots to real IDs, and which outranks this skill on conflict.
- No emoji, no arrow characters, no typographic dashes in anything you write here -- use `->` and
  `--`. Keep the register plain.
- Do not vendor third-party code without an upstream URL and an author credit in `README.md`'s
  Credits section -- see that section for the current status.

## Before opening a pull request

Run `python -m pytest -q` from the repository root and make sure it is clean. If you touched
`README.md`, `assets/`, `docs/`, or this file, also run `python -m pytest test_readme.py -q`
directly, and check the changed files by eye for a stray emoji, arrow, or a leading byte-order
mark -- `test_readme.py` only checks the root documents and the two SVGs for these, not every file
you might touch.
