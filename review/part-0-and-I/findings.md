# Analyst to Architect — Findings Register: Part 0 and Part I

Status: reviewed 2026-09-25; **awaiting Abhishek's approval**. No fix instructions written yet.
Live review doc: https://claude.ai/code/artifact/43dd9cc0-558e-4053-8e34-413426640130
Source files: `Analyst-to-Architect-Part-0.pdf` (Ch 1–6, 136 pp), `Analyst-to-Architect-Part-I.pdf` (Ch 7–9, 71 pp).

## Review lens (7 tests)

| # | Test | Question |
|---|---|---|
| 1 | First-time reader | Could a total beginner follow this without outside help? Every term defined before use? |
| 2 | Line-by-line code | Is every line of code shown, run and explained like a Jupyter cell: what it does, each parameter, its output? |
| 3 | Flow | Does the chapter depend only on what came before? Are forward references limited to what helps? |
| 4 | Load | Is the amount of new material per section and sitting reasonable for a novice? |
| 5 | Consistency | Do numbers, names, datasets and claims agree across chapters and parts? |
| 6 | Reader-facing polish | Anything left from drafting, editing or the build pipeline that a reader should never see? |
| 7 | Sequence | Does anything (code, formula, term) appear before the chapter that teaches it? Does each idea climb: plain idea → by hand → known tool → new tool one line at a time? |

Severity: **High** = beginner gets stuck, misled, or a wrong number. **Medium** = slows or confuses; resolved later. **Low** = polish, wording, small inconsistency.

Fix dependency: **Independent** = can be fixed now. **Needs map** = depends on the whole-book sequence map (what later chapters teach, where tools move).

## Sequence findings (cross-part, Parts 0 and I)

Code shown before it is taught:

| What the reader sees | First shown | First taught |
|---|---|---|
| Python code and output (`0.1 + 0.2`) | Ch 2 | Ch 17 |
| JSON, XML, HTTP requests and responses | Ch 2 | Ch 18, 20 |
| Spreadsheet formulas (`=RRI`, `=SUMPRODUCT`, ranges) | Ch 4 | Ch 10 |
| Terminal, venv, pip, PowerShell execution policy | Ch 6 | Ch 17, 34 |
| SQL with type casts (`::double precision`, `45E1`) | Ch 6 | Ch 12 |
| Python `round()`, `print()` | Ch 6 | Ch 17 |
| 12-line SQL with LEFT JOIN/HAVING + MySQL version | Ch 7 | Ch 12–13 |
| LEFT JOIN + WHERE trap in help-request example | Ch 9 | Ch 12 §12.10 |

| ID | Where | Issue | Sev | Fix dependency |
|---|---|---|---|---|
| S.1 | Parts 0, I | Code shown before it is taught (table above). "You don't need to read this yet" labels don't fix it. | High | Needs map |
| S.2 | Ch 6 ex. 6 | Tests PostgreSQL double precision / MySQL approximate-value rounding never taught. Typo: part (e) `ROUND(45E1)` = 450, answer treats it as 4.5 (`45E-1`). | High | Typo: Independent; exercise: Needs map |
| S.3 | Ch 6 whole | Setup chapter too early: Python installed Ch 6, first used Ch 17 (~150+ study hours later); Git → Ch 26; Power BI → Ch 16; reader runs terminal/venv/PowerShell policy before knowing what Python is; 3–4 h of installing at the weakest moment; Ch 7–9 use no software. | High | Needs map |
| S.4 | Ch 4, 5, 7 | "Spreadsheet link", "SQL link", "Dialect note" boxes point to unlearned tools. | Medium | Needs map |

**Proposed direction for S.3 (decision pending):** just-in-time setup — each tool installed in the chapter that first uses it, ending in a one-line first run: Spreadsheet Ch 10 (`=ROUND(A1,0)`), PostgreSQL + DBeaver Ch 12 (`SELECT 1;`), Power BI Ch 16 (empty report), Python + Jupyter Ch 17 (first notebook, one cell `print("hello")`, Shift+Enter), Git Ch 26 (`git --version`). Ch 6 becomes a tool-free "how to study this book" chapter (or merges into Ch 9). Appendix B keeps an all-in-one install guide.

## Part 0 — First Principles (Ch 1–6)

Verdict: strong; Ch 1, 3, 5 near-ideal for beginners. Ch 2 too dense; Ch 6 too early (S.3).
Keep: plain-English analogy opening each chapter; single company (Riverstone) with numbers reconciling to the rupee (~40 figures rechecked, all correct); consistent chapter skeleton.

| ID | Where | Issue | Test | Sev | Fix dependency |
|---|---|---|---|---|---|
| 0.1 | Ch 6 §6.8, Fig 6.2 | Plan says Parts 0–II take 6 months at 8 h/week (~208 h); book's own estimates total 319–396 h; Closing says 12–15 months at 6 h/week. Meera's "nine months at 6 h" also wrong. | Consistency | High | Needs map (final hours) |
| 0.2 | Ch 6 §6.3 | WITHDRAWN (see S.3). Was: no first Jupyter notebook in Ch 6. Jupyter belongs in Ch 17. | — | Withdrawn | — |
| 0.3 | Ch 6 §6.3 | SUPERSEDED by S.3. Was: venv/pip/activate/Set-ExecutionPolicy lines not explained. These commands shouldn't be in Part 0. | — | Superseded | — |
| 0.4 | Ch 6 §6.3 step 2 | DB install sends reader forward to Ch 12 §12.3 ("do them now, and come back"). | Flow | Medium | Needs map |
| 0.5 | Ch 2 §2.1, 2.5, 2.8, 2.9 | Results shown without the code that produced them: `0.30000000000000004`, exact-decimal 0.3, pandas reading CSV, curl request, SHA-256 hashes. | Line-by-line | Medium | Needs map (remove vs keep) |
| 0.6 | Ch 2 overall | ~110 key terms in one chapter (bits → Unicode → floating point → formats → Parquet → DNS/HTTPS → IaaS/PaaS/SaaS → APIs → CIA → hashing → 3-2-1). | Load | Medium | Needs map |
| 0.7 | All chapters | Heavy forward references (Ch 12–78) in nearly every section. | Flow | Medium | Needs map |
| 0.8 | Ch 1–6 | Two datasets used without introduction: mini database (Q1 2026, 12 orders) vs one-year database (2025, 173 orders); March = ₹31,800 in one chapter, ₹278,008 in another. | Consistency | Medium | Independent |
| 0.9 | Ch 1–5 | Fast-growing cast (Meera, Anita, Vikram, Neha, Rahul, Farah, Suresh, Imran, Rakesh, Kavya); no cast list or company fact sheet. | First-time reader | Low | Independent |
| 0.10 | Ch 4 §4.4 | Monthly revenues sum to ₹4,335,473, stated total ₹4,335,471 (rounding). | Consistency | Low | Independent |
| 0.11 | Ch 1 §1.6, Fig 1.3 | "Each level allows everything the level above it allows" reads backwards. | First-time reader | Low | Independent |
| 0.12 | Ch 1 §1.6 ex. 2 | Kelvin conversion is unnecessary physics for the point. | Load | Low | Independent |
| 0.13 | Ch 2 §2.2, §2.5 | Fig 2.1 says "see section 2.2" from inside 2.2; §2.5 title "six ways" vs text "five data formats". | Polish | Low | Independent |
| 0.14 | Ch 4 §4.4 | "Eleventh root" / `2.17 ^ (1/11)` with no one-line explanation of a root. | First-time reader | Low | Independent |
| 0.15 | Ch 1–6 answers | "(In the finished book these move to Appendix G.)" production note in every chapter. | Polish | Low | Independent |

Code in Part 0, snippet by snippet:

| Snippet | Code shown? | Output shown? | Each line explained? |
|---|---|---|---|
| Python `0.1 + 0.2` (Ch 2) | No | Yes | No |
| pandas reads CSV (Ch 2) | No | Described | No |
| curl to demo API (Ch 2) | No | Yes | Response only |
| SHA-256 (Ch 2) | No | Yes | No |
| venv/pip (Ch 6) | Yes | Partly | No |
| check_setup.py (Ch 6) | Command only | Yes | Script not shown |
| ROUND in PostgreSQL/MySQL/Python (Ch 6) | Yes | Yes | Via documentation, not line by line |

## Part I — The Map (Ch 7–9)

Verdict: excellent orientation content; drafting notes leak into reader text; SQL shown too early.
Keep: four questions (§7.1); one request through ten roles (§7.6); skills matrix (all counts rechecked correct); salary maths, Farah's 13/28 score and practice log (2,800 min, 46.7 h) all correct.

| ID | Where | Issue | Test | Sev | Fix dependency |
|---|---|---|---|---|---|
| I.1 | Ch 8 §8.1, §8.2; Ch 9 §9.2, §9.7; Ch 8 ans. 1 | Drafting history addressed to reader: "The draft of this book introduced…", "fix for the first edition's tier order", "rules from the first edition still hold", "first edition saved this topic for its closing chapter", "as the first edition did". | Polish | High | Independent |
| I.2 | Ch 8, Ch 9 Tools | Author's build scripts named as reader resources: `checks/ch08_check.py`, `figures/make_figs08.py`, `checks/ch09_check.py`, `figures/make_figs09.py`. | Polish | High | Independent |
| I.3 | Ch 7 §7.6 step 2 | 12-line SQL (LEFT JOIN, GROUP BY, HAVING, NULLS FIRST, date arithmetic) + MySQL dialect version before any SQL is taught. Upgraded to High (see S.1). | Load / Sequence | High | Needs map |
| I.4 | Ch 7 §7.6 steps 5–7 | "Every role depends on the ones before it", but data engineer (step 7) supplies data needed by data scientist and ML engineer (steps 5–6). | Flow | Medium | Independent |
| I.5 | Ch 8 §8.6 | Table labels ₹577,000 PayScale **median** base; text and answer 7 call ₹577,472 the **average** base. | Consistency | Medium | Independent (verify source) |
| I.6 | Ch 8 §8.6 | Long, dated salary section (retrieved Sep 2026) in an orientation chapter; goes stale fastest. | Load | Medium | Independent (decide placement) |
| I.7 | Ch 9 §9.7 + story | Weeks 1–4 and 4–8 both count week 4; "cut her minutes back" not shown in log (weeks 9–12 avg 245 min vs 246 in plateau). | Consistency | Low | Independent |
| I.8 | Ch 6 vs Ch 9 | Optimistic Ch 6 plan comes before Ch 9's honest timeline (same root as 0.1). | Flow | Low | Needs map |
| I.9 | Ch 7–9 answers | "(In the finished book these move to Appendix G.)" repeated. | Polish | Low | Independent |
| I.10 | Ch 8 Fig 8.1 | Roles on the tree ("BI analyst", "Senior analyst", "Reporting / MIS assistant") not among Ch 7's ten roles. | First-time reader | Low | Independent |

## Open decisions for Abhishek

1. Approve Part 0 and Part I findings (or mark disagreements).
2. Approve just-in-time setup direction for Ch 6 (S.3).
3. Approve the next step: whole-book sequence map (first shown vs first taught, every concept/tool/code construct) before fixing "Needs map" items; independent fixes can be drafted in parallel.
4. Part II review granularity: one section (planned) or chapter by chapter.
