# Agent Guide for `cs212`

Notes and solutions for Peter Norvig's CS212 (Design of Computer Programs, Udacity). This is a learning project: the point is understanding, not finished code.

## Where things live

- `cs212.org` — canonical notes: one top-level section per topic, with org-fc cards (`:fc:`). Read the relevant section before touching code.
- One module per topic, written as a companion to the notes: `poker.py`, `zebra.py`, `cryptarithmetics.py`.
- No tangle — the Org file holds the reasoning and the module holds the code. Keep the two in sync by hand.

## Working notes

- Code style: Norvig style, `~/git/notes/agents/programming.md`. The modules build incrementally: introduce a concept when needed, define the minimal construct, test early, refactor later.
- Standard library only, Python 3.12 (`ty.toml` points at `/usr/bin/python3`); no venv or dependencies. Run a module directly: `python3 poker.py`.
- Prefer small examples and assertions over explanations of the obvious. The org notes and the code should tell the same story.
- Guide me to the solution rather than handing it over; I'm working through the course.
