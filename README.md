# skill-finder

A zero-read skill selection discipline for Claude Code. It turns "which skills should I use"
from a reflex into a deliberate two-pass decision, made from information the session already has.

## The problem

At the start of a session, or when a task changes domain, an agent needs to decide which of its
installed skills apply. The reflex is to go read a skill catalog file, or dispatch a subagent to
survey what is installed, before answering. Both are waste: the skill list and its descriptions are
already injected into the system prompt, and the project's own rules are already auto-injected from
`CLAUDE.md` or `AGENTS.md`. Reading a catalog to pick skills re-derives context that is already
sitting in the prompt. Dispatching a subagent to do the same lookup is worse -- it costs tens of
thousands of tokens to read a file that is worth a few thousand, and the subagent starts blind to
the conversation so far. skill-finder replaces both habits with a selection pass that reads nothing
and spawns nothing, run only when it is actually needed: the first substantive request of a session,
or a change of domain.

## Install

```
/plugin marketplace add Bilohit/skill-finder
/plugin install skill-finder
```

## What it does

skill-finder runs a two-pass selection over the skills already visible in the session:

- **Pass 1 -- the four process buckets.** Every non-trivial task gets a pick, or a stated reason it
  does not need one, for planning, thinking, subagent dispatch, and handover.
- **Pass 2 -- route the domain.** A table matches what the task actually touches (UI, a bug, a
  codebase question, a document, harness configuration, and so on) to the class of skill that
  applies, ranking rather than hoarding.

The result is two lines -- a loadout and what was skipped, and why -- followed immediately by work.
No table, no narration of the choosing, and no re-running on every turn: the loadout stays sticky
until the domain changes.

## License

MIT. See `LICENSE`.
