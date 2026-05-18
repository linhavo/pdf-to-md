Create a comprehensive index file for a markdown document.

## Instructions

The argument `$ARGUMENTS` is the path to a markdown file (e.g. `outputs/somefile.md`). Create an index file named by inserting `_INDEX` before the `.md` extension (e.g. `outputs/somefile_INDEX.md`).

### Step 1 — Extract structure (main agent)

Use `grep -n "^#" <file>` to get all headings with line numbers. Note the total line count with `wc -l`.

### Step 2 — Read key sections (delegate to Haiku sub-agents)

The file may be too large to read at once (> 256 KB). Spawn one or more **Haiku sub-agents** (use the Agent tool with `model: "haiku"`) to read and summarise chunks. Accuracy matters, so instruct each sub-agent to quote exact numbers, dates, and statistics verbatim.

Suggested split — launch these in parallel:
- **Sub-agent A**: first ~200 lines (title, abstract, table of contents)
- **Sub-agent B**: each major chapter's opening ~30 lines — use heading line numbers from step 1 to target the right offsets; ask it to return a one-paragraph summary per chapter plus all numeric findings
- **Sub-agent C**: the final chapter / conclusions (~80 lines before LITERATURA/REFERENCES)

Each sub-agent prompt should end with: *"Return your findings as structured text: chapter summaries, and a flat list of every number, date, threshold, or statistic you found. Do not omit figures."*

### Step 3 — Synthesise and write (main agent)

Collect the sub-agent outputs and write `<filename>_INDEX.md` in the same directory as the source file. The index must contain:

1. **Header block** — document title, author (if found), source file path, total line count
2. **Quick summary** — 2–3 sentence description of what the document is about and its main conclusion
3. **Table of contents with line numbers** — every heading, indented by level, with `(ř. N)` or `(line N)` references
4. **Per-chapter summaries** — one paragraph each, covering the main argument and key data points
5. **Key numbers table** — a markdown table of the most important figures, thresholds, dates, or statistics found in the document
6. **Reading guide** — bullet list mapping common questions/intents to specific line ranges (e.g. "Want the methodology? → lines 1036–1313")

### Conventions

- Write the index in the same language as the source document
- Use `ř.` for line references if the document is Czech, `line` if English
- Keep the index under ~150 lines so it fits comfortably in a single context load (~4k tokens)
- Do not reproduce large verbatim passages — summarise and reference by line number instead
