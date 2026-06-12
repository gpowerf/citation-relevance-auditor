# Citation Relevance Auditor → Full Research Paper Agent Framework

**A multi-agent LLM pipeline that plans, researches, writes, verifies, and peer-reviews academic papers — with human oversight at every step.**

> ⚠️ LLMs hallucinate. This system helps you write faster, but you are responsible for verifying every fact and citation.

---

## What is this?

Six specialized LLM agents that work together to produce rigorous, well-cited papers:

| Agent | What it does |
|---|---|
| **Strategist** | Takes a research question, returns a full outline with `[CLAIM]` statements |
| **Literature Scout** | Generates search queries + YAML templates for finding papers |
| **Analyst** | Extracts factual claims from a paper's text |
| **Drafter** | Writes a section from an outline + verified evidence |
| **Claim Verifier** | Checks if a single citation actually supports the claim it's attached to |
| **Reviewer** | Applies PEERREVIEWER.md criteria to a draft section |

**Quick demo** — audit a single citation using a real paper:

```
You:
Paragraph: A 2025 study by Xu et al. found that while tools like
GitHub Copilot increase productivity, they do so at the cost of
sustainability and maintainability [CITATION_HERE].

Paper Details:
Title: "GenAI as a coding partner: Productivity gains at the cost
of sustainability and maintenance"
Abstract: "We analyze developer activity in OSS projects following
Copilot's introduction. Productivity increases, but code requires
more rework. The added burden falls on core developers, who review
6.5% more code, leading to a 19% drop in their original code
productivity."
Claims:
1. Copilot increases productivity, primarily for peripheral devs
2. Code written after AI adoption requires more rework
3. Core developers bear the maintenance burden

Agent: Rating: Highly relevant
       Justification: The paper directly supports the claim that
       productivity gains come at the cost of sustainability. The
       increased rework and burden on core developers are the exact
       mechanisms behind the maintainability cost described.
```

---

## Quick start

1. **Generate outline** — paste `agents/strategist.md` as system prompt, then your research question
2. **Find papers** — paste `agents/literature-scout.md` with keywords from step 1
3. **Extract claims** — paste `agents/analyst.md` with each paper's metadata + text
4. **Draft sections** — paste `agents/drafter.md` with section name + claims + evidence
5. **Verify citations** — paste `agents/claim-verifier.md` with paragraph + paper details
6. **Peer review** — paste `agents/reviewer.md` + `PEERREVIEWER.md` with your draft

Or use the **citation auditor** skill (`SKILL.md`) to audit a range of references at once.

---

## Requirements

- Any LLM chat (DeepSeek, Claude, GPT-4) with a large context window
- Text editor for `evidence_db.md`

Optional: `pip install pyyaml` (for Zotero integration)

---

## Project structure

```
├── README.md
├── SKILL.md                 ← citation-auditor skill (quick audits)
├── PEERREVIEWER.md          ← peer review rubric
├── WORKFLOW.md              ← end-to-end workflow guide
├── EVIDENCE_SCHEMA.md       ← evidence_db.md YAML format
├── LICENSE
├── opencode.json            ← OpenCode configuration
├── agents/                  ← Agent prompts (one per role)
│   ├── strategist.md
│   ├── literature-scout.md
│   ├── analyst.md
│   ├── drafter.md
│   ├── claim-verifier.md
│   └── reviewer.md
├── .opencode/
│   ├── agents/              ← Same prompts, mirrored for OpenCode users
│   └── skills/
│       ├── citation-auditor/
│       └── paper-workflow/
└── scripts/
    └── zotero_fetch.py      ← Pull references from Zotero
```

> Agents exist in both `agents/` (standalone use) and `.opencode/agents/` (auto-loads when opened in [OpenCode](https://opencode.ai)). Same content, two locations.

---

## Tips

- Keep one `evidence_db.md` per project — it's your single source of truth
- Verify early (don't wait until the full draft is done)
- Agents can hallucinate — always check that citations are real

---

## License

MIT
