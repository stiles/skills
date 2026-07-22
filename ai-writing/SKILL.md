---
name: ai-writing
description: >-
  Avoid common LLM writing tells when drafting or editing prose. Use when
  writing or rewriting documentation, READMEs, blog posts, essays, commit
  messages, PR descriptions, user-facing copy, analyses, or any text that
  should read as human; when the user asks to make writing sound less like AI,
  remove AI tone, or follow Wikipedia Signs of AI writing guidance.
---

# Avoid AI writing tells

Write like a careful human editor. Prefer specific facts over broad significance, plain wording over elevated vocabulary and short direct sentences over balanced rhetoric.

Source patterns: [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). That page is descriptive (how to detect AI text). This skill is prescriptive (how to avoid those patterns).

## Before you ship prose

1. Cut significance padding (legacy, broader trends, "pivotal moment").
2. Replace AI vocabulary with plain words.
3. Prefer "is/are/has" over "serves as / stands as / boasts".
4. Delete throat-clearing and chatbot assents.
5. Check formatting: no title case headings, emoji bullets, bold-label lists or decorative em dashes.

Full word lists and examples: [reference.md](reference.md).

## Content habits to avoid

### Significance and legacy inflation

Do not inflate the subject with generic importance claims.

Avoid:
- "stands as / serves as a testament"
- "marks a pivotal moment" / "key turning point"
- "underscores its importance" / "highlights the significance"
- "reflects broader trends" / "part of a broader movement"
- "continues to shape" / "leaving an indelible mark"
- "nestled in the heart of" plus heritage/tourism filler

Prefer concrete facts: what it is, what happened, who did what, when and what the evidence says.

### Superficial -ing analyses

Do not tack on present-participle commentary that sounds like insight but adds no fact:

- "highlighting the importance of..."
- "ensuring that..."
- "reflecting a commitment to..."
- "fostering innovation..."
- "contributing to the broader landscape..."

End sentences when the fact ends.

### Promotional tone

Avoid brochure voice: "boasts", "vibrant", "rich tapestry", "seamless", "cutting-edge", "renowned", "diverse array", "groundbreaking", "commitment to excellence".

State capabilities and history without sales adjectives.

### Vague attribution

Avoid "experts say", "observers note", "industry reports suggest", "critics argue" unless you name the source. Do not pluralize one source into a consensus.

### Challenges / future outlook outlines

Avoid formula sections:

- "Despite its X, [subject] faces several challenges..."
- "Looking ahead..." / "Future prospects..."
- "As [field] continues to evolve..."

If challenges matter, state them specifically. Do not force a balanced closing paragraph.

### Notability-by-assertion

Do not prove importance by listing outlet types ("featured in leading publications such as..."). Mention coverage only when the content of that coverage is material and cited.

## Language habits to avoid

### AI vocabulary

High-signal overused words (replace or delete):

additionally, align with, boasts, bolster, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), groundbreaking, interplay, intricate, key (as vague adjective), landscape (abstract), meticulous, nuanced, pivotal, robust, seamless, showcase, tapestry, testament, underscore, invaluable, vibrant, utilize

Prefer plain substitutes: "also", "matches", "has", "strengthen", "important", "look into", "lasting", "improve", "build", "get", "show", "detailed", "setting", "careful", "important", "strong", "show", "proof", "stress", "useful", "use".

### Copula avoidance

Do not replace "is/are/has" with:

- "serves as" / "stands as" / "functions as" / "represents a"
- "boasts" / "features" / "offers" / "maintains" (when "has" is meant)

OK: "Harian Metro is a Malay-language newspaper."
Not: "Harian Metro serves as a vital platform serving communities..."

### Negative parallelisms

Avoid fake refinement:

- "not only X but also Y"
- "It's not just X — it's Y"
- "No X, no Y, just Z"

State the claim once.

### Rule of three

Do not pad lists into rhetorical triples ("tiles, metals, and plastics"; "clarity, reliability, and trust"). Use real items only.

### Elegant variation

Do not cycle synonyms for the same referent ("the initiative… the effort… the program… the endeavor"). Repeat the noun or use a pronoun.

## Style habits to avoid

| Habit | Prefer |
|-------|--------|
| Title-Case Headings For Every Section | Sentence case headings |
| **Bold labels** at the start of every bullet | Plain bullets or prose |
| Emoji as bullet markers or section icons | No decorative emoji |
| Em dashes for drama — like this — everywhere | Commas, periods, colons or parentheses |
| Curly quotes “like this” | Straight quotes "like this" in plain text/code |
| Horizontal rules between every section | Ordinary headings |
| Chatbot assents ("Certainly!", "Great question!", "I'd be happy to help") | Start with the answer |
| "I hope this helps!" / "Let me know if you'd like..." | Just stop when done |
| "As an AI language model..." | Never |
| Knowledge-cutoff hedges ("as of my last update", "based on available sources") | State facts or say what you could not verify |
| Placeholder leftovers (`[Your Name]`, `INSERT_URL`, `2025-XX-XX`) | Real values or omit |

## Positive defaults

- Lead with the fact, not the framing.
- Use "is/are/has/does" freely.
- Keep sentences short; vary length only when useful.
- Name sources and people; avoid anonymous authority.
- One idea per sentence is fine.
- Specific numbers, dates, names and constraints beat adjectives.
- For technical docs: follow the user's README/style rules when present (plain verbs, present tense, no buzzwords).

## Quick self-edit checklist

Before delivering prose, confirm:

- [ ] No legacy/significance/broader-trend sentences
- [ ] No AI vocabulary cluster (2+ tells in one paragraph)
- [ ] No "serves as" / "stands as" / "boasts" where "is" / "has" works
- [ ] No "not only / not just" parallelisms
- [ ] No challenges-and-future-outlook filler section
- [ ] No chatbot openers/closers
- [ ] Headings are sentence case; bullets are not bold-label glossaries
- [ ] Claims have sources or are clearly the user's opinion

## When editing user drafts

Remove tells; do not merely swap synonyms for AI words while keeping the inflated structure. If a paragraph only asserts importance, delete it or replace it with a sourced fact.
