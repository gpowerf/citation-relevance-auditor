# Citation Relevance Auditor → Full Research Paper Agent Framework

A modular, Markdown-native multi-agent system for independent researchers who want to write rigorous, well-cited papers with the help of LLMs.

> Use at your own risk! LLMs hallucinate and no amount of guardrails fully protects you. Work with a team of specialized AI agents—strategist, scout, analyst, drafter, reviewer, and citation auditor—following a transparent, human‑in‑the‑loop process.

---

## Table of Contents

- [What is this?](#what-is-this)
- [Repository structure](#repository-structure)
- [Dependencies & setup](#dependencies--setup)
- [Common tasks](#common-tasks)
  - [1. Write a paper from scratch (full workflow)](#1-write-a-paper-from-scratch-full-workflow)
  - [2. Write one section with existing evidence](#2-write-one-section-with-existing-evidence)
  - [3. Audit an existing paper's citations](#3-audit-an-existing-papers-citations)
  - [4. Verify a single citation](#4-verify-a-single-citation)
  - [5. Peer review a draft section](#5-peer-review-a-draft-section)
  - [6. Zotero → evidence_db pipeline](#6-zotero--evidence_db-pipeline)
- [Agent reference](#agent-reference)
- [Skill reference](#skill-reference)

---

## What is this?

| Agent                | File (OpenCode)                          | File (standalone)         | Role                                                             |
|----------------------|------------------------------------------|---------------------------|------------------------------------------------------------------|
| **Strategist**       | `.opencode/agents/strategist.md`         | `agents/strategist.md`    | Generates a full paper outline with `[CLAIM]` statements.        |
| **Literature Scout** | `.opencode/agents/literature-scout.md`   | `agents/literature_scout.md` | Creates search queries and a fill‑in template for found papers. |
| **Analyst**          | `.opencode/agents/analyst.md`            | `agents/analyst.md`       | Extracts claims from a paper's text (or abstract).               |
| **Claim Verifier**   | `.opencode/agents/claim-verifier.md`     | `agents/claim_verifier.md` | Your original auditor, now modular – checks one citation at a time. |
| **Drafter**          | `.opencode/agents/drafter.md`            | `agents/drafter.md`       | Writes a section using the outline and verified evidence.        |
| **Reviewer**         | `.opencode/agents/reviewer.md`           | `agents/reviewer.md`      | Applies the `PEERREVIEWER.md` criteria to a draft section.       |

The original standalone auditor remains available in `SKILL.md` (`audit` skill in `.opencode/skills/citation-auditor/`) for quick audits, and the peer‑review prompt in `PEERREVIEWER.md` is unchanged.

### OpenCode Integration

This repo doubles as an [OpenCode](https://opencode.ai) project. Open the repo in OpenCode and the agents and skills are automatically loaded:

- Use `@strategist`, `@literature-scout`, `@analyst`, `@claim-verifier`, `@drafter`, `@reviewer` to invoke each agent.
- The **citation auditor** skill auto-triggers when you mention citation auditing.
- The **paper workflow** skill guides you through the end-to-end process.
- Configuration lives in `opencode.json`.
=======
This repo provides a team of AI agents (each in a Markdown prompt file) that work together to help you write academic papers. The agents are:

- **Strategist** — turns a research question into a paper outline with `[CLAIM]` statements
- **Literature Scout** — generates search queries and a template for found papers
- **Analyst** — extracts factual claims from a paper's text/abstract
- **Drafter** — writes a section using outline + evidence
- **Claim Verifier** — checks if a specific citation supports its claim
- **Reviewer** — peer-reviews a draft section

Each agent is a self-contained prompt you paste to an LLM chat. You control every step.
>>>>>>> 65ab0af (Rewrite README with task-based examples and add Zotero fetch script with local SQLite mode)

---

## Repository structure

```
.
├── README.md                ← this file
├── SKILL.md                 ← citation-auditor skill (quick audits)
├── PEERREVIEWER.md          ← peer review criteria
├── WORKFLOW.md              ← original end-to-end workflow guide
├── EVIDENCE_SCHEMA.md       ← evidence_db.md YAML format spec
├── agents/
│   ├── strategist.md        ← generates outline with [CLAIM] statements
│   ├── literature-scout.md  ← generates search queries + YAML template
│   ├── analyst.md           ← extracts claims from a paper
│   ├── drafter.md           ← writes a section from outline + evidence
│   ├── claim-verifier.md    ← checks one citation's support
│   └── reviewer.md          ← peer reviews a draft section
├── skills/
│   ├── citation-auditor/
│   │   └── SKILL.md         ← audits a range of references
│   └── paper-workflow/
│       └── SKILL.md         ← orchestrates all 6 agents in sequence
└── scripts/
    ├── zotero_fetch.py      ← fetch references from Zotero
    └── README-Zotero.md     ← Zotero script docs
```

---

## Dependencies & setup

### Minimum requirements
- An LLM chat (DeepSeek, Claude, GPT-4, etc.) with a large context window
- A text editor for `evidence_db.md`

### For Zotero integration (optional)
```bash
pip install pyyaml
```

The `zotero_fetch.py` script can read your local Zotero SQLite database directly (no API key needed). It looks for your database at `~/Zotero/zotero.sqlite` by default.

To use the Zotero API instead of local mode:
```bash
pip install pyzotero
```
Then get an API key from https://www.zotero.org/settings/keys. Your library ID is visible in your Zotero API settings (numeric).

---

## Common tasks

### 1. Write a paper from scratch (full workflow)

This walks through all 6 agents to produce a complete paper.

```
Strategist → Literature Scout → Analyst → Drafter → Claim Verifier → Reviewer
```

**Step 1: Generate outline**
Paste `agents/strategist.md` as the system prompt. Then send:
```
Research question: How does the rise of AI coding assistants affect software quality?
```
The strategist returns an outline with `[CLAIM]` statements. Copy this into the `outline:` field of your `evidence_db.md`.

**Step 2: Find papers**
Paste `agents/literature-scout.md` as the system prompt with the keywords from step 1. The scout gives you 3–5 search queries. Run them manually on arXiv/Semantic Scholar. Fill out the YAML template for each paper you find. Paste the filled entries into the `papers:` section of `evidence_db.md`.

**Step 3: Extract claims from each paper**
For each paper, paste `agents/analyst.md` as the system prompt. Send the paper's metadata block and text:
```
id: "smith2024"
title: "AI Coding Assistants and Code Quality"
authors: "Smith, J.; Jones, K."
year: 2024
abstract: "We studied the impact of GitHub Copilot on bug rates..."
[full text if available]
```
Copy the extracted claims into that paper's `extracted_claims:` field.

**Step 4: Draft a section**
Pick a section from the outline. Gather evidence from papers whose claims support that section's `[CLAIM]` items. Assign reference numbers. Paste `agents/drafter.md` as system prompt, then send:
```
Section: Introduction
Claims to support:
- [CLAIM] AI coding assistants are widely adopted in industry
- [CLAIM] Their impact on code quality remains debated

Evidence:
[1] Smith et al. (2024) — AI Coding Assistants and Code Quality
    Claim: 78% of surveyed developers use Copilot weekly
[2] ...
```
The drafter writes the section. Paste it into `evidence_db.md` under `drafts.introduction:`.

**Step 5: Verify each citation**
For each citation `[n]` in the draft, paste `agents/claim-verifier.md` as system prompt, then send:
```
Paragraph: The widespread adoption of AI coding tools [CITATION_HERE] suggests a shift in developer workflows.

Paper Details:
Title: "AI Coding Assistants and Code Quality"
Abstract: "We studied the impact..."
Claims: 1. 78% of surveyed developers use Copilot weekly
```
The verifier returns a rating: Highly relevant / Somewhat relevant / Not relevant / Contradicts. If the rating is weak, find a better paper or revise the claim.

**Step 6: Peer review the section**
Paste `agents/reviewer.md` as system prompt with the content of `PEERREVIEWER.md`. Send the draft section. Apply suggested revisions.

**Step 7: Assemble**
Repeat steps 4–6 for each section, then compile. Write the Abstract and Bibliography manually.

---

### 2. Write one section with existing evidence

If you already have papers and just want to draft one section:

Paste `agents/drafter.md` as system prompt. Send:
```
Section: Related Work — AI code review tools
Claims:
- [CLAIM] Automated code review tools reduce review time
- [CLAIM] They still miss certain bug types

Evidence:
[1] Author et al. (2023) — "Automated Code Review"
    Claim: Automated reviews were 40% faster than manual
[2] Author et al. (2022) — "Limits of Static Analysis"
    Claim: Static analyzers detect only 30% of logic bugs
```
The drafter returns a complete section with citations in `[1]`, `[2]` format and a reference mapping.

---

### 3. Audit an existing paper's citations

Use the **citation-auditor skill** when you have a complete draft and want to check a range of references.

Paste the content of `skills/citation-auditor/SKILL.md` as the system prompt, then append:
```
Now please review references 3 to 5 from the paper that follows:

[Paste the full paper text including in-text citations and reference list]
```

The auditor examines each reference's in-text citations, extracts the surrounding claims, checks the reference details, and rates relevance on a 4-point scale. For 5+ references it produces a summary table.

---

### 4. Verify a single citation

When you want to check one specific citation without running the full auditor:

Paste `agents/claim-verifier.md` as system prompt. Send:
```
Paragraph: Recent studies have shown that LLMs can generate unit tests that achieve high coverage [CITATION_HERE], though experts caution about test quality.

Paper Details:
Title: "LLM-Generated Unit Tests: Coverage vs Quality"
Abstract: "We compare hand-written and LLM-generated unit tests..."
Claims:
1. LLM-generated tests achieved 92% line coverage
2. Mutation score was 15% lower than hand-written tests
```

The verifier outputs:
```
**Rating:** Somewhat relevant
**Justification:** The paper supports the coverage claim but also notes quality concerns, which aligns with the caution mentioned. However, the citation primarily supports the first half of the claim.
```

---

### 5. Peer review a draft section

Paste `agents/reviewer.md` as system prompt along with the content of `PEERREVIEWER.md`. Send:
```
[Your full draft section in Markdown]
```

The reviewer returns a structured report with:
- **Summary**: 2–3 sentence overview
- **Strengths**: 2–3 key strengths
- **Weaknesses**: 2–3 areas for improvement
- **Detailed Feedback**: section-by-section comments
- **Suggestions for Revision**: actionable recommendations

---

### 6. Zotero → evidence_db pipeline

If you manage references in Zotero, use `scripts/zotero_fetch.py` to pull them into the agent pipeline.

**List your Zotero collections:**
```bash
python scripts/zotero_fetch.py --local --limit 3 --format evidence
```

**Fetch all papers from a specific collection into evidence_db format:**
```bash
python scripts/zotero_fetch.py --local --collection HRX69G3Z --limit 50 --output my_papers.yaml
```

**Fetch into literature-scout template format:**
```bash
python scripts/zotero_fetch.py --local --collection HRX69G3Z --limit 20 --format scout
```

Then paste the YAML output into the `papers:` section of your `evidence_db.md` and proceed with the `@analyst` agent to extract claims.

See `scripts/README-Zotero.md` for full details.

---

## Agent reference

| Agent | File | What you give it | What you get back |
|---|---|---|---|
| **Strategist** | `agents/strategist.md` | Research question | Paper outline with `[CLAIM]` statements + keywords |
| **Literature Scout** | `agents/literature-scout.md` | Keywords/topic | 3–5 search queries + YAML template for found papers |
| **Analyst** | `agents/analyst.md` | Paper metadata + text | Numbered list of extracted claims with section & type |
| **Drafter** | `agents/drafter.md` | Section name + claims + evidence block | Section prose with `[1]`, `[2]` citations + reference mapping |
| **Claim Verifier** | `agents/claim-verifier.md` | Paragraph (with `CITATION_HERE`) + paper details | Rating (Highly / Somewhat / Not relevant / Contradicts) + justification |
| **Reviewer** | `agents/reviewer.md` + `PEERREVIEWER.md` | Draft section | Structured peer review report |

---

## Skill reference

| Skill | File | When to use |
|---|---|---|
| **citation-auditor** | `skills/citation-auditor/SKILL.md` | You have a full draft and want to audit a range of references (e.g., "refs 3–5") |
| **paper-workflow** | `skills/paper-workflow/SKILL.md` | You want end-to-end orchestration guidance through all 6 agents |

---

## Tips

- **Keep an `evidence_db.md`** per paper project. It's your single source of truth for outline, papers, and drafts.
- **Verify with the claim-verifier early** — don't wait until the full draft is done.
- **The agents can hallucinate.** Always check that citations are real and claims match the source.
- **Use `scripts/zotero_fetch.py --local`** to quickly dump your latest Zotero references into the pipeline without API keys.
