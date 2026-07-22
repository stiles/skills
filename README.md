# Skills

Personal Cursor Agent Skills. This directory is the global skills folder (`~/.cursor/skills`).

## Locations

| Type | Path | Scope |
|------|------|-------|
| Global (personal) | `~/.cursor/skills/skill-name/` | Available across all projects |
| Project | `.cursor/skills/skill-name/` | Shared with anyone using that repository |

Do not put custom skills in `~/.cursor/skills-cursor/`. That directory is reserved for Cursor's built-in skills and is managed by the system.

## Skill layout

Each skill is a directory with a required `SKILL.md`:

```
skill-name/
├── SKILL.md       # Required: frontmatter + instructions
├── reference.md   # Optional: detailed reference
├── examples.md    # Optional: examples
└── scripts/       # Optional: helper scripts
```

`SKILL.md` starts with YAML frontmatter:

```markdown
---
name: skill-name
description: What the skill does and when to use it
---

# Skill name

Instructions for the agent...
```

| Field | Rules |
|-------|-------|
| `name` | Max 64 chars; lowercase letters, numbers and hyphens only |
| `description` | Max 1024 chars; say what it does and when to apply it |

Set `disable-model-invocation: true` when the skill should load only if named explicitly. Omit it when the agent should pick the skill up from context (for example writing style guidance).

## Best practices

- Keep `SKILL.md` under about 500 lines. Put long word lists and edge cases in linked files such as `reference.md`.
- Write the description in third person and include trigger terms so the agent can discover the skill.
- Prefer concise, actionable instructions over background essays. Assume the agent is capable; teach what it would not already know.
- Link supporting files one level deep from `SKILL.md` (no nested reference chains).
- Use specific skill directory names (`ai-writing`, not `helper` or `utils`).
- Match specificity to the task: tight checklists for fragile workflows; looser guidance when judgment matters.
- Prefer project skills when the practice should be shared with a repository; keep personal defaults here.

## Skills in this directory

| Skill | Purpose |
|-------|---------|
| [ai-writing](ai-writing/) | Avoid common LLM writing tells in docs, READMEs, copy and other prose |
| [fecfile](fecfile/) | Analyze FEC campaign finance filings (contributions, disbursements, committees) |
| [gis-datasets](gis-datasets/) | Defaults for stilesdata.com/gis, gis/korea and la-geography layers |
| [graphics-style](graphics-style/) | Chart and map design standards (Roboto charts, chorokit / Barlow maps) |
| [hangarbay](hangarbay/) | Query FAA aircraft registry by N-number, owner or fleet |
| [jupyter-notebook](jupyter-notebook/) | Scaffold JupyterLab notebooks with uv, live fetches and the `_template` layout |
| [stock-market](stock-market/) | Fetch stock prices, indices, commodities, Fear & Greed and economic indicators |
| [streetview-dl](streetview-dl/) | Download Google Street View panoramas from Maps URLs |
| [weather-forecast](weather-forecast/) | Fetch 7-day forecasts from Open-Meteo (coordinates then forecast) |

## Creating a skill

1. Add a directory under this folder (or under `.cursor/skills/` in a project).
2. Write `SKILL.md` with `name`, `description` and clear agent instructions.
3. Add `reference.md` or scripts only when they keep the main file short.
4. Point Cursor at the skill by name when you want it applied on demand.
