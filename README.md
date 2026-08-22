<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img src="assets/banner.svg" alt="skill-finder">
</picture>

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Plugin](https://img.shields.io/badge/plugin-skill--finder-informational.svg)
![Dependencies](https://img.shields.io/badge/dependencies-none-blue.svg)

skill-finder turns "which skills should I use" from a reflex into a deliberate two-pass decision,
made entirely from information the session already has. It reads no files and spawns no agents, and
it returns two lines instead of a survey. It runs on the first substantive request of a session and
again when the task changes domain, never on every turn.

## The problem

At the start of a session, or when a task changes domain, an agent needs to decide which of its
installed skills apply. The reflex is to go read a skill catalog file, or dispatch a subagent to
survey what is installed, before answering. Both are waste: the skill list and its descriptions are
already injected into the system prompt, and the project's own rules are already auto-injected from
`CLAUDE.md` or `AGENTS.md`. Reading a catalog to pick skills re-derives context that is already
sitting in the prompt. Dispatching a subagent to do the same lookup is worse -- it costs tens of
thousands of tokens to read a file that is worth a few thousand, and the subagent starts blind to
the conversation so far. skill-finder replaces both habits with a selection pass that reads nothing
and spawns nothing, run only when it is actually needed.

## See it

Before -- the reflex, on a request to restyle a settings panel:

```
Let me check what skills are available for this.
  Read  ~/.claude/skills/catalog.md                       (4,118 tokens)
  Task  general-purpose: "survey installed skills and
        report which apply to a UI restyle"              (31,540 tokens)

Based on the catalog, the relevant skills are: design-review, frontend-design,
visual-direction, motion, a11y-audit, css-architecture, component-patterns.
```

After -- the same request, through skill-finder:

```
Loadout: brainstorming, design-review, react-stack  (+ verification-before-completion at close)
Skipped: visual-direction -- this is a restyle inside an established look, not a new surface.
```

Nothing was read and nothing was dispatched, because the skill list and the project's rules were
already in the prompt. Two of the seven skills the reflex named were the same skill under different
words, and three were loaded on the word "UI" rather than on what the task actually touches -- which
is the difference between ranking and hoarding.

## Install

```
/plugin marketplace add Bilohit/skill-finder
/plugin install skill-finder
```

## When it runs

| | |
|---|---|
| **Run** | the first substantive request of a session; when the task changes domain (backend to UI, build to debug, code to planning); on request |
| **Skip** | conversational turns, one-line answers, mechanical edits -- answer directly |
| **Never** | re-run per turn. The loadout is sticky until the domain changes |

Anything a `SessionStart` hook or a plugin's own hook already armed is excluded before the passes
begin. Naming an already-active skill in a loadout is noise.

## The selection pass

**Pass 1 -- the four process buckets.** On a non-trivial task, each bucket gets a pick, or a stated
reason it does not need one.

| Bucket | Default | Escalate to |
|---|---|---|
| Planning | a brainstorming skill, then a plan-writing skill | a spec skill, for new or large work only |
| Thinking | an in-context deliberation skill: no subagents, near-free | a subagent council, only for a binding go/no-go |
| Subagents | a parallel-dispatch skill | task-by-task execution: same session, or a separate session with review checkpoints |
| Handover | the project's own session-wrap ritual | a mid-session handoff |

**Pass 2 -- route the domain.** Match what the task actually touches. One row usually fires; two is
normal on a cross-cutting change. Every row firing means the ranking step was skipped.

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

There is no hard cap on the total. Rank by relevance and load what the task actually needs -- loading
five design skills because the task says "UI" is hoarding whether or not a number forbids it.

## Rules

- **A loadout is applied, not announced.** Every picked skill stays active for the whole domain. A
  skill named in the output line and then ignored is worse than not loading it: it reads as
  discipline that never ran.
- **Name only skills visible in this session's skill list.** Never invent one.
- **A project rule beats any skill's own guidance.** On conflict the project rule wins, and the
  conflict is said out loud rather than resolved silently.
- **Check what a skill is allowed to do before trusting it in a constrained repo.** A skill with
  write access can create files; where the file set is controlled, hold it to in-context work.
- **A skill the model cannot invoke cannot be auto-loaded.** Suggest its command instead.

## Escalating to a subagent

Rare, and only when the applicable skills cannot be told **without reading the repo first** -- an
unfamiliar codebase, or "fix whatever is broken" with no named surface. That is a recon task, not a
skill lookup: dispatch a cheap read-only investigator to report what the code is, then select the
skills from its answer.

Never dispatch a general-purpose agent to read a skill catalog. That was this skill's original
design, and it was wrong.

## Going deeper

- [docs/walkthrough.md](docs/walkthrough.md) -- one worked example, from install through the first
  substantive request of a session
- [docs/concepts.md](docs/concepts.md) -- the vocabulary skill-finder uses, and what each term
  means in the skill itself

## Requirements

Claude Code, or any agent harness that loads Claude Code plugins. The skill is a single markdown
file -- no runtime, no dependencies, nothing to install beyond the plugin itself. This repository's
own tests need Python 3.10+ and the standard library only.

## Credits

skill-finder bundles no third-party code. The skill, the reference docs and this repository's tests
are all original work, released under the MIT license -- see `LICENSE`.

If that ever changes -- a dependency gets added, a file gets vendored, wording gets lifted from
somewhere else -- it is credited right here with an upstream URL and an author's name, never
included silently.

## Related

skill-finder is one of three sibling plugins, one product per repository, each installable on its
own:

| Repo | What it does |
|---|---|
| [flow-review](https://github.com/Bilohit/flow-review) | drives your product end to end like a first-time user and returns ranked findings plus a design critique |
| skill-finder (this repo) | picks a session's skill loadout deliberately -- reads no files, spawns no agents |
| [build-state](https://github.com/Bilohit/build-state) | imprints a `/boot` you can trust: session continuity from a computed baton, an append-only ledger and a verification ladder |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to run the tests and where things live.

## License

MIT -- see [LICENSE](LICENSE).
