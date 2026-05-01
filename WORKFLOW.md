# End‑to‑End Paper Writing Workflow

This workflow uses the agent team to go from a research question to a fully drafted and audited paper section by section. **You remain in control at every stage**—no automation without your approval.

## Prerequisites
- A project folder containing this repository.
- Access to a capable LLM with a large context window (e.g., DeepSeek, Claude, GPT‑4). You will paste prompts and input blocks into the chat.
- A text editor for maintaining the `evidence_db.md` file (following `EVIDENCE_SCHEMA.md`).

## Stage 0: Initialize the Evidence Database
1. Create a new file `evidence_db.md` in your project folder.
2. Paste the empty template from `EVIDENCE_SCHEMA.md` into it.
3. This file will hold all paper metadata and extracted claims, plus the outline and drafts.

## Stage 1: Strategist – Generate Outline
1. Open your LLM chat. Paste the **entire content** of `agents/strategist.md` as the system prompt (or first message).
2. User message: `Research question: [your question]`
3. The LLM replies with an outline. **Review it carefully.** Edit the claims if they don’t capture your argument. Remove or add sections as needed.
4. Copy the final outline into the `outline:` section of `evidence_db.md`.

## Stage 2: Literature Scout – Find Papers
1. Start a new chat (or clear context). System prompt: `agents/literature_scout.md` and the keywords from the strategist’s output.
2. The LLM gives you search instructions. Execute the searches manually in your browser (arXiv, Semantic Scholar).
3. For each paper you deem relevant, fill out the YAML template the scout provided. Paste the filled block into the `papers:` section of `evidence_db.md`.

## Stage 3: Analyst – Extract Claims from Papers
1. For each paper in your `evidence_db.md` that doesn’t yet have extracted claims, do the following:
2. System prompt: `agents/analyst.md`.
3. User message: the paper’s metadata block (from `evidence_db.md`). If you have the full text (e.g., you copied it from the PDF), include it; otherwise, the abstract is enough but note that the output will be less detailed.
4. The LLM outputs the list of extracted claims.
5. Copy those claims into the `extracted_claims:` field of that paper’s entry in `evidence_db.md`.

## Stage 4: Drafting – Write Each Section
The strategist’s outline defines the sections and the claims each must contain.
1. For a given section, gather the relevant evidence. From `evidence_db.md`, pick papers whose extracted claims can support the section’s `[CLAIM]` items. Assign each a reference number (1, 2, ...) and create an “evidence summary” block as shown in the drafter’s input example.
2. System prompt: `agents/drafter.md`.
3. User message: the section info, the claims to include, and the evidence summary block.
4. The LLM drafts the section.
5. **Review and refine** the draft manually. Adjust wording, fix any citation mis‑match.

## Stage 5: Citation Verification (per citation)
Now use your Claim Verifier to ensure every citation genuinely supports its attached claim.
1. For each citation `[n]` in the draft:
   - Extract the paragraph containing that citation. Replace the `[n]` with `CITATION_HERE` (so the verifier knows which one to check).
   - Prepare the cited paper details: its title, abstract, and extracted claims (from `evidence_db.md`).
2. System prompt: `agents/claim_verifier.md`.
3. User message: the paragraph with `CITATION_HERE` and the paper details.
4. The LLM outputs a rating. If `Not relevant` or `Contradicts`, go back to your evidence database and either find better support, revise the claim, or remove the citation.

## Stage 6: Peer Review (optional but recommended)
1. After a full section is drafted and audited, run the Reviewer agent.
2. System prompt: paste the content of `PEERREVIEWER.md` followed by the instruction block from `agents/reviewer.md`.
3. User message: the final draft of the section.
4. Apply the suggested revisions as you see fit.

## Stage 7: Assemble the Full Paper
Repeat Stages 4‑6 for each section. Then compile all sections into one Markdown document. Manually write the Abstract and Bibliography using the reference mapping.

## Stage 8: Final Audit (Full Draft)
Re‑run the citation verifier on the assembled paper, or use the original `SKILL.md` (root folder) to audit the entire document at once, flagging any weak citations for a final check.