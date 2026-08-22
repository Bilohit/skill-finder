# Concepts

The vocabulary skill-finder uses, and what each term means in the skill itself
(`plugins/skill-finder/skills/skill-finder/SKILL.md`).

## Loadout

The set of skills chosen for the current domain, plus the stage each one applies at. A loadout is
the skill's entire output: one line naming what was picked, one line naming a notable omission and
why. It is applied, not announced -- a skill named in the loadout and then never used is worse than
one that was never picked, because it reads as discipline that ran when it did not.

## Domain

The kind of work in progress, and the only thing that expires a loadout. Backend to UI, build to
debug, code to planning are domain changes; the next turn of the same task is not. This is what
"sticky" means: the loadout survives every turn until the domain moves, and re-running the selection
pass per turn is an anti-pattern rather than thoroughness.

## Zero-read

The constraint the skill is built around: the selection pass opens no files and dispatches no
subagents. Both inputs it needs are already in the prompt before the first turn -- the injected
skill list with each skill's description, and the project's own auto-injected rules from `CLAUDE.md`
or `AGENTS.md`. Reading a catalog to pick skills re-derives what is already in context; dispatching
an agent to do it costs tens of thousands of tokens for the same answer, from a subagent that starts
blind to the conversation.

## Pass 1 -- the process buckets

Four questions every non-trivial task has to answer: how it will be planned, how it will be thought
through, whether it will be dispatched to subagents, and how it will be handed over. Each bucket
gets a pick or an explicit reason it does not need one. The buckets are about *process*, so they
fire regardless of what the task touches.

## Pass 2 -- the domain routing table

A table from what the task actually touches to the class of skill that applies. One row usually
fires; two is normal on a cross-cutting change. Every row firing is the diagnostic that the ranking
step was skipped -- the table exists to rank, not to accumulate.

## Class of skill, not skill

Every entry in both tables names a category ("a systematic-debugging skill", "a data-visualization
skill"), never a specific invocable ID. Naming a particular skill would break the routing everywhere
that skill is not installed. Binding those slots to real IDs is a project's job, in its own
`CLAUDE.md`, and that binding outranks this skill on conflict.

## Already armed

Skills a `SessionStart` hook or a plugin's own hook loaded before the session's first turn. They are
excluded before either pass begins: naming an already-active skill in a loadout is noise, and
re-picking one implies a choice that was never available.

## Ranking versus hoarding

There is no numeric cap on a loadout. The discipline is relevance, not arithmetic: loading five
design skills because the task contains the word "UI" is hoarding whether or not a limit forbids it,
and a cap low enough to prevent it would also block the legitimately cross-cutting change. Ranking
is the job the skill does; a cap would only disguise skipping it.

## Recon escalation

The one case that justifies a subagent: the applicable skills cannot be determined without reading
the repository first -- an unfamiliar codebase, or "fix whatever is broken" with no named surface.
That is a reconnaissance task, not a skill lookup. A cheap read-only investigator reports what the
code is; the skills are then selected from its answer, in context. Dispatching a general-purpose
agent to read a skill catalog is never the answer -- that was this skill's original design, and it
was wrong.
