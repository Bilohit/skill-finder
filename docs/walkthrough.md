# Walkthrough

One worked example: from installing the plugin, through the first substantive request of a session,
to a domain change that re-runs the selection pass. The project used here -- a React front end with
a Python service behind it -- is a stand-in for whatever you point skill-finder at; the passes
described are the real ones in `SKILL.md`, not invented ones.

## 1. Install

Inside your own project, in Claude Code:

```
/plugin marketplace add Bilohit/skill-finder
/plugin install skill-finder
```

## 2. The first substantive request

The session opens. A `SessionStart` hook has already armed two skills of its own, and the project's
`CLAUDE.md` has been auto-injected. Then the first real request arrives:

```
The settings panel looks wrong since the token refactor. Make it match the rest of the app.
```

skill-finder runs -- once, here, because this is the first substantive request.

**Excluded first.** The two skills the `SessionStart` hook armed are dropped from consideration
before either pass begins. They are already active; naming them would be noise.

**Pass 1, the process buckets.** This is a bounded restyle inside an established look, so three of
the four buckets resolve to a stated reason rather than a pick:

| Bucket | Result |
|---|---|
| Planning | a brainstorming skill -- the "match the rest of the app" target needs pinning before any CSS moves |
| Thinking | none: no decision is contested, so an in-context deliberation skill has nothing to deliberate |
| Subagents | none: one surface, one file group, no parallelism to buy |
| Handover | a verification skill at close -- the change has to be proven against the running app |

**Pass 2, the domain routing.** Two rows fire. "A UI surface" loads the project's design skills.
"Framework mechanics" loads the React stack skill, and at most that one. The motion row does not
fire, because nothing in the request is about motion. The visual-direction row does not fire either,
and that is the interesting one: the surface has an established look, and that row is explicitly for
a *new* surface with none. It is a restyle, not a direction.

## 3. The output

Two lines, then work:

```
Loadout: brainstorming, design-review, react-stack  (+ verification-before-completion at close)
Skipped: visual-direction -- this is a restyle inside an established look, not a new surface.
```

No table, no narration of the choosing, and no summary of what the passes considered. The reasoning
above happened; printing it would cost more than the decision saved.

## 4. Every turn after -- nothing happens

The next several turns are the actual work: reading the token file, editing the panel, checking it
against a sibling screen. skill-finder does not run on any of them. The loadout is sticky, and the
domain has not moved -- re-running the selection pass per turn is an anti-pattern, not diligence.

## 5. The domain changes

Later in the same session:

```
The service is returning 500s on the settings save endpoint. Find out why.
```

That is a domain change: UI to a bug. skill-finder runs a second time, and the routing lands
somewhere else entirely. The "a bug, a test failure, unexpected behaviour" row fires, and it
replaces the planning bucket rather than joining it -- a debugging discipline and a brainstorming
one are two answers to the same question, and running both means neither is in charge.

```
Loadout: systematic-debugging, python-stack
Skipped: brainstorming -- systematic-debugging replaces it on a failure; this is a bug, not a design.
```

The design skills from the first loadout are gone, because their domain is gone. That is the whole
mechanism: a loadout is scoped to a domain, expires with it, and costs nothing to recompute because
recomputing it reads nothing and spawns nothing.
