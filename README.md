# Citation Relevance Auditor → Full Research Paper Agent Framework

**A modular, Markdown‑native multi‑agent system for independent researchers who want to write rigorous, well‑cited papers with the help of LLMs.**

> Use at your own risk! LLMs allucinate and no ammount of guardrails fully protects you. Work with a team of specialized AI agents—strategist, scout, analyst, drafter, reviewer, and citation auditor—following a transparent, human‑in‑the‑loop process.

---

## ✨ What is this?

This repository started as a single, powerful prompt: the **citation relevance auditor** (`SKILL.md`), designed to check whether a citation actually supports the claim it’s attached to.  
It has now evolved into a **full end‑to‑end paper‑writing framework** built entirely in Markdown.

The extended system gives you:
- A **strategist** that turns your research question into a detailed outline with verifiable claims.
- A **literature scout** that generates precise search queries so you can find the right papers manually (no API keys needed).
- An **analyst** that extracts every factual claim from each paper, creating a personal evidence database.
- A **drafter** that writes sections using only the evidence you’ve collected and audited.
- A **peer reviewer** that critiques your draft for logic, flow, and factual support.
- And your original **citation verifier** (now a team player) that audits every single citation.

Everything is **prompt‑based**, **version‑controllable**, and **human‑driven**. You stay in full control—the LLM assists, but you approve every step.

---

## 🧠 The Agent Team

| Agent                | File                   | Role                                                             |
|----------------------|------------------------|------------------------------------------------------------------|
| **Strategist**       | `agents/strategist.md` | Generates a full paper outline with `[CLAIM]` statements.        |
| **Literature Scout** | `agents/literature_scout.md` | Creates search queries and a fill‑in template for found papers. |
| **Analyst**          | `agents/analyst.md`    | Extracts claims from a paper’s text (or abstract).               |
| **Claim Verifier**   | `agents/claim_verifier.md` | Your original auditor, now modular – checks one citation at a time. |
| **Drafter**          | `agents/drafter.md`    | Writes a section using the outline and verified evidence.        |
| **Reviewer**         | `agents/reviewer.md`   | Applies the `PEERREVIEWER.md` criteria to a draft section.       |

The original standalone auditor remains available in `SKILL.md` for quick audits, and the peer‑review prompt in `PEERREVIEWER.md` is unchanged.

---

## 📁 Repository Structure

