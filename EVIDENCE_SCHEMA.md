# Evidence Database Format

The file `evidence_db.md` holds the entire project’s knowledge. It must be valid YAML inside a Markdown code block (so it’s both human‑ and machine‑readable).

> ⚠️ **Copyright notice:** This file will contain pasted abstracts and possibly full paper text. Do not commit it to version control or distribute it publicly. It is excluded from git via `.gitignore`.

```yaml
# Project Evidence Database
outline: |
  (paste the strategist’s Markdown outline here, indented)

papers:
  - id: "unique_string_arxiv_id_or_shortname"
    title: "Paper Title"
    authors: "Author1, Author2"
    year: 2023
    abstract: "..."
    pdf_url: "https://..."
    source: "arxiv"  # or "s2"
    why_relevant: "one sentence"
    full_text_available: true/false  # if you copied text from PDF
    extracted_claims:
      - claim: "..."
        section: "..."
        type: "empirical_result"  # empirical_result, theoretical_statement, methodology, background, opinion
      - claim: "..."
        section: "..."
        type: "..."

  - id: "another_paper"
    ...

drafts:
  introduction: |
    (paste the drafted Introduction section)
  related_work: |
    ...
  # one field per section, as you draft them
```