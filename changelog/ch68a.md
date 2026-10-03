# 4 October 2026 · New chapter 68A: The Rounds Nobody Prepares For

66 questions, Q68A-001 to 066 (17 core, 49 rapid-fire). Registered as `'68a'` in
`PART_PACKAGES['8']` between 68 and 69; nothing renumbered. Book 4 rebuilt: **702 → 729 pages**,
444 internal links all resolving, 935 bookmarks all landing correctly, no missing glyphs.
`check_bank.py`: range 001–066, no gaps or duplicates, all 17 core questions carry all five house
parts, 0 uneven tables. **Part VIII: 1,160 → 1,226 questions.**

## Why it exists

The owner asked whether the book covers the whole journey "from the screening round to getting
hired". Measured against the chapters, the technical rounds, the CV, LinkedIn, referrals, take-homes,
behavioural questions and the offer conversation were well covered, but these were absent or one
line deep:

| Gap | Before | Now |
|---|---|---|
| The timed online test (HackerRank-style), hidden test cases, output format | nothing | §68A.2, 12 questions |
| Campus drives, fresher hiring, the group discussion | nothing | §68A.3, 12 questions |
| Thinking aloud, being stuck, virtual-round logistics | one line | §68A.4, 12 questions |
| Messaging recruiters, values and bar-raiser rounds, portals | two mentions | §68A.5, 9 questions |
| Follow-up after an interview, being ghosted, rejection | one row | §68A.6, 10 questions |
| Reading the offer letter, acceptance to joining, the first 90 days | two mentions | §68A.7, 11 questions |

## What was checked

- **The one code example was run** (Python 3.12.0) and its output pasted: a second-highest function
  that passes the visible test, returns the wrong answer on ties and crashes on one value or none,
  then the fixed version.
- **Every section pointer** (68 pointer/claim pairs) was checked against the real heading of the
  section it names. One weak fit was replaced (§26.0, the terminal, cited for call setup → §69.5).
- **Every cross-referenced question** was checked to say what this chapter claims: Q81-031 (never
  resign before a written offer), Q81-032 (reneging), Q81-033 (counter-offers), Q81-078 (asking why
  you were rejected), Q76A-070 (first 90 days), Q75-047 and Q72B-022 (the findings used in examples).
- **An error caught in the draft:** the fresher "tell me about yourself" template described
  Chapter 75's December finding backwards, saying most of the drop was the incomplete month. Q75-047
  measured that the incomplete month explains about a tenth; the rest is a real fall in order value.
  Corrected before commit.

## Claims deliberately not made

No salary, placement rate, cut-off, notice-period law or company policy is stated as fact. Where
those vary, the answer says what to ask and who to ask — the college placement cell, HR, the
recruiter, or someone qualified for legal questions such as bonds and non-competes. Aptitude, which
the owner chose to leave out of the book, is mentioned only so candidates are not surprised by it.

## Also in this change

- **Covers** count 68A automatically: 1,226 questions, seventeen banks (now spelled from the data
  rather than typed), 729 pages. The back cover overflowed the bottom margin by 5.6 px with the
  seventeenth row; the cover script's own measurement caught it and the rows were tightened.
- **The topic guide parser** never matched letter-suffixed sections (`## 72B.4`), so 68A, 69A, 72A,
  72B, 76A and 76B had no section lists in *Where-Everything-Is*; it also only read "You will learn
  to:" while the banks say "You will practise:". Both fixed: 840 → 897 sections listed.
