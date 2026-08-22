---
name: skill-finder
description: Pick the session's skill loadout deliberately instead of by reflex. A zero-read selection discipline - the skill list and the project rules are already in context, so this reads no files and spawns no agents. Use before acting on the first substantive request of a session, and again when the task changes domain (backend to UI, build to debug, code to planning). Also triggers on "what skills should I use", "pick skills", "skill loadout", "/skill-finder".
---

# Skill Finder

Choosing skills is a decision, not a lookup. Everything needed to decide is **already in context**:

- **Skill names and descriptions** -- injected into every session's system prompt.
- **Project rules and defaults** -- `CLAUDE.md` or `AGENTS.md`, auto-injected every session.

So: **read nothing, spawn nothing.** Reading a skill catalog in order to pick skills re-derives
context you already have, and dispatching a subagent to do it costs tens of thousands of tokens to
read a file worth a few thousand. Both are pure waste.

## When to run

**Run:** the first substantive request of a session; when the task changes domain; on request.

**Skip:** conversational turns, one-line answers, mechanical edits. Answer directly.

**Never re-run per turn.** The loadout is sticky until the domain changes.

## The selection pass

**Already armed before you run -- never re-pick these:** anything a `SessionStart` hook or a
plugin's own hook loads for you. Naming an already-active skill in a loadout is noise.

**Pass 1 -- the four process buckets.** On a non-trivial task, each bucket gets a pick or a stated
reason it does not.

| Bucket | Default | Escalate to |
|---|---|---|
| Planning | a brainstorming skill, then a plan-writing skill | a spec skill, for new or large work only |
| Thinking | an in-context deliberation skill: no subagents, near-free | a subagent council, only for a binding go/no-go |
| Subagents | a parallel-dispatch skill | task-by-task execution: same session, or a separate session with review checkpoints |
| Handover | the project's own session-wrap ritual | a mid-session handoff |

**Pass 2 -- route the domain.** Match what the task actually touches. One row usually fires; two is
normal on a cross-cutting change. Every row firing means you skipped the ranking step.

| The task is about | Load |
|---|---|
| a UI surface | the project's design skills; a motion skill only if motion is in scope |
| a chart, gauge, dashboard | a data-visualization skill, before the first line of chart code |
| a new surface with no established look | a visual-direction skill as a third lens -- never on an audit or a fix |
| accessibility as the deliverable | an a11y tooling skill. For an a11y review, a design-review skill already carries the lens |
| framework mechanics | the matching stack skill, and at most one |
| driving a device or the running app | the project's device or browser automation skills and agents |
| a bug, a test failure, unexpected behaviour | a systematic-debugging skill first. It replaces brainstorming; it does not join it |
| new non-trivial logic | a test-driven-development skill, then a verification-before-completion skill |
| finding defects in a diff | three different verbs, three different skills: find bugs, cut over-engineering, check security |
| a codebase question | a code-graph or search skill first, before any manual exploration |
| a document deliverable | that file format's skill |
| harness configuration | a settings skill. An automation recommender proposes only; diff before applying |
| authoring a skill | a skill-writing skill. A skill-evaluation skill only for evals and benchmarking |
| context bloat | a context-audit skill |

**No hard cap on the total.** Rank by relevance and load what the task actually needs. Ranking is
still the job. Loading five design skills because the task says "UI" is hoarding, whether or not a
number forbids it.

## Rules

- **A loadout is applied, not announced.** Every picked skill stays active for the whole domain. A
  skill named in the output line and then ignored is worse than not loading it -- it reads as
  discipline that never ran.
- **Name only skills you can see in this session's skill list.** Never invent one.
- **A project rule beats any skill's own guidance.** On conflict the project rule wins, and you say
  so out loud rather than resolving it silently.
- **Check what a skill is allowed to do before trusting it in a constrained repo.** A skill with
  write access can create files; in a repo where the file set is controlled, hold it to in-context
  work.
- **A skill marked non-invocable by the model cannot be auto-loaded.** Suggest its command; the user
  runs it.

## Escalating to a subagent (rare)

Only when you cannot tell which skills apply **without reading the repo first** -- an unfamiliar
codebase, or "fix whatever is broken" with no named surface. That is a recon task, not a skill
lookup: dispatch a cheap read-only investigator to report what the code is, then select skills
yourself from its answer.

Never dispatch a general-purpose agent to read a skill catalog. That was the original design of this
skill and it was wrong.

## Output

Two lines, then work. No table, no narration of the choosing.

```
Loadout: <skill>, <skill>, <skill>  (+ <skill> at <stage>)
Skipped: <notable skill> -- <reason>
```

## Anti-patterns

- Reading a catalog to pick skills. It is reference; the live list is already in context.
- Spawning an agent for a lookup.
- Running the finder, then ignoring the loadout.
- Re-running every turn.
