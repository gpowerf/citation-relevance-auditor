---
name: paper-workflow
description: "Use when the user asks to write, draft, outline, or produce an academic paper or research article. Also use on phrases like 'write a paper', 'research workflow', 'paper writing', 'evidence database', or 'academic writing'. Gate on 'paper', 'article', 'manuscript', 'research' in an academic/writing context. Loads when the user wants end-to-end guidance through the strategist-scout-analyst-drafter-reviewer pipeline."
---

# Research Paper Writing Workflow

This workflow helps you go from a research question to a fully drafted and audited paper section by section using OpenCode agents.

## Prerequisites
- A project folder initialized with `evidence_db.md` (use the template from `EVIDENCE_SCHEMA.md`)
- Access to a capable LLM

## Agents Available

| Agent              | Command                                  | Purpose                                                      |
| ------------------ | ---------------------------------------- | ------------------------------------------------------------ |
| @strategist        | `@strategist Research question: ...`     | Generates a paper outline with `[CLAIM]` statements          |
| @literature-scout  | `@literature-scout Topic: ...`           | Creates search queries and a template for found papers       |
| @analyst           | `@analyst Paper details and text: ...`   | Extracts factual claims from a paper                         |
| @claim-verifier    | `@claim-verifier Paragraph and ref: ...` | Checks if a single citation supports its claim               |
| @drafter           | `@drafter Section info and evidence: ...`| Writes a paper section from outline + evidence               |
| @reviewer          | `@reviewer Draft section: ...`           | Peer-reviews a draft section                                 |

## Suggested Workflow

1. **Strategist** → Generate outline: `@strategist Research question: [your question]`
2. **Literature Scout** → Find papers: `@literature-scout Topic: [your keywords]`
3. **Analyst** → Extract claims per paper: `@analyst Paper: [paper details + text]`
4. **Drafter** → Write a section: `@drafter Section: [section name] Evidence: [evidence block]`
5. **Claim Verifier** → Audit each citation: `@claim-verifier Paragraph: [text with CITATION_HERE]`
6. **Reviewer** → Peer review the draft: `@reviewer Draft: [full section]`
