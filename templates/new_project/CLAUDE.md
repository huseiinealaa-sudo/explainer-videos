# Project: NAME — <topic title> (<N> episodes | single video)

Project-specific rules. The general rules in the root `CLAUDE.md` also apply; where they differ, this file wins for this project.

## Start a project from this template
```bash
name=my_topic                                   # lowercase_with_underscores
cp -r templates/new_project projects/$name
cd projects/$name
for f in $(find . -name '*NAME*'); do mv "$f" "${f//NAME/$name}"; done
grep -rl NAME . | xargs sed -i "s/NAME/$name/g"
```
Then fill in this file, `project.toml` and `sources/<name>_source.md`, and delete `<name>_data.py` if the topic shows no numbers.

## Source
- Primary reference: `projects/NAME/sources/NAME_source.md` (cleaned: no real site, personal or confidential data).
- Research notes per video: `projects/NAME/sources/NAME_<video>.md` (claim → source URL → short note).

## Narration
- Language / voice / speed: see `project.toml` (default: Arabic, ar-SA-HamedNeural, normal speed).
- Foreign terms written in the narration's letters (keep this list up to date):
  | Term | Narration spelling |
  |---|---|
  | Example | إِكْزَامْبِل |

## Videos
| # | Script / output | Topic | Status |
|---|---|---|---|
| 1 | `NAME_ep01_intro` | <topic of episode 1> | draft |

## Terminology and on-screen conventions
- <term> = <meaning>; never use <wrong term>.
- Colours: ACCENT_1 = <role>, ACCENT_2 = <role>, ACCENT_3 = <role>, ACCENT_4 = alarm / error.

## Data (only if the topic shows numbers)
- All numbers come from `projects/NAME/NAME_data.py`, which runs `self_test()` on import.
- Illustrative inputs only; list them here:
  | Item | Value |
  |---|---|
  | <input> | <illustrative value> |

## Owner decisions
- <date>: <decision>.
