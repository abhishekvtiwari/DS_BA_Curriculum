# Chapter 68A. The Rounds Nobody Prepares For

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will practise:** clearing the timed online test that screens most applicants before any human sees them, including the hidden test cases that fail correct-looking code · getting through a campus drive and a group discussion as a fresher · thinking aloud in a live-coding round, and recovering when you are stuck · running a virtual interview that survives a dropped connection · writing to a recruiter so that you get a reply · following up after an interview, and handling silence and rejection without burning the bridge · reading an offer letter before you sign it, and getting from acceptance to a good first 90 days.
>
> **Before you start:** Chapter 68 (the hiring process, gate by gate) and Chapter 69 (the three answer tiers and the twelve extra-point moves). The technical rounds themselves are tested in Chapters 70–80 and the HR and offer conversation in Chapter 81; this chapter covers everything around them that the banks do not.
>
> **Time needed:** 3–4 hours to read and answer every question aloud. Section 68A.2 is worth doing on a laptop with a timer running, because the online test is a skill of pace as much as knowledge.
>
> **How this chapter is built.** Same format as every question bank in Part 8: a memory hook ("Remember it as…"), a one-line answer, a tier table (**passes**, **strong**, **extra points**, tagged with Chapter 69's moves), then follow-ups, the red flag, and where to learn it. Rapid-fire sections are scan tables. The one code example was run on Python 3.12.0 and its output is real. **Nothing here states a salary, a placement rate, a law or a company's policy as fact**: where those vary, the answer says what to ask and who to ask, because a confident wrong rule is worse than an honest "check this".

---

## 68A.1 Why these rounds sink prepared candidates

Chapters 70 to 81 prepare you for the rounds where someone asks you a question. This chapter is about the rounds where nobody does: the timed test you take alone, the group discussion where twelve people talk at once, the video call that freezes halfway through your best answer, and the week of silence after a final round.

They have one thing in common. **They are filters, and a filter does not care how much you know.** A strong SQL candidate who runs out of time on an online test never reaches the SQL interview. A fresher who knows every answer but says nothing in a group discussion is cut before the technical round. A candidate who gives an excellent final interview and then sends nothing, hears nothing, and assumes rejection has sometimes simply been forgotten in a busy recruiter's queue.

These rounds are also the least prepared-for, because they feel like logistics rather than skill. They are skills, they can be practised, and the questions below are the ones that come up.

**Levels and roles.** Each question carries a level — **Fresher**, **Mid** or **Senior** — and the roles that face it: **DA** data analyst · **DS** data scientist · **DE** data engineer · **AE** analytics engineer · **BA** business analyst.

---

## 68A.2 The online assessment

For many companies, and most large ones hiring freshers in India, the first real filter is a timed online test on a platform such as HackerRank, HackerEarth, Codility or Mercer Mettl. It is scored by software. It usually arrives as an emailed link with a deadline, and it often decides whether a human ever reads your CV properly.

### Q68A-001 · You have a 90-minute online test with three SQL and two Python problems. How do you approach it?

**Level:** Fresher · **Roles:** DA, DS, DE, AE, BA

**Remember it as:** *Read everything first, bank the easy points, and never leave a problem blank. The test rewards points, not elegance.*

**Answer in one line:** Spend the first few minutes reading every problem and the rules, solve the problems you are surest of first, submit something that passes the visible tests for every problem before polishing any of them, and keep a few minutes at the end to resubmit and check — because scoring is per test case, and a partial solution scores where a blank does not.

**The plan, in order:**

| | What you do | Why |
|---|---|---|
| **1. Read the rules screen** | Webcam, tab switching, allowed languages, whether you may use your own notes | Many tests flag tab switches or record the webcam. Breaking a rule you did not read can void the whole attempt |
| **2. Read every problem** | Before writing any code | So you can order them by how sure you are, not by the order they were given |
| **3. Easiest first** | Bank the points you are confident of | Confidence costs least time; it also settles your nerves |
| **4. Something for everything** | A working answer that passes the visible tests, for every problem | Most platforms score each hidden test case separately, so partial credit is real |
| **5. Then improve** | Edge cases, efficiency | Q68A-002 is why this matters |
| **6. Last few minutes** | Resubmit, check nothing is half-typed | An unsubmitted answer scores zero |

**The one sentence an interviewer will want to hear if they ask how you prepared:** that you practised under the same timer, on the same kind of platform, rather than only solving problems untimed. Pace is the skill the online test measures that no other round does.

| Tier | What to say |
|---|---|
| Passes | "Do the easy ones first and watch the time" |
| Strong | The ordered plan: read the rules, read everything, easiest first, something for everything, then improve, then resubmit — with the reason that scoring is per test case |
| Extra points | + **[+Edge cases]** read the rules screen; a broken proctoring rule can cost more than a wrong answer + **[+Validate]** test your own code against the cases the problem does not show you (Q68A-002) + **[+Trade-offs]** a correct brute-force answer submitted beats an optimal answer unfinished, unless the problem states a time limit the brute force will fail |

**Likely follow-ups:** How would you practise for one? What would you do if the platform crashed mid-test?
**Red flag:** solving the first problem perfectly and leaving the last two blank.
**Learn it in:** Chapter 68, §68.1 (the gates) and §68.7 (preparing in 30, 60 or 90 days); Chapter 71's and Chapter 72's banks for the problems themselves.

### Q68A-002 · Your answer passed the sample test but scored 2 out of 10. What happened?

**Level:** Fresher · **Roles:** DA, DS, DE, AE

**Remember it as:** *The sample test is the easy case. The hidden tests are the edge cases you did not think of: ties, one row, no rows.*

**Answer in one line:** The platform ran your code against hidden test cases — usually ties, duplicates, a single value, an empty input or a very large input — and your code was only right for the normal case it was shown, so the fix is to test those edges yourself before you submit.

**Run, on Python 3.12.0.** A typical online-test problem: return the second-highest amount in a list. The obvious first answer:

```python
def second_highest(amounts):
    """First attempt: sort descending and take position 1."""
    return sorted(amounts, reverse=True)[1]


print('visible test :', second_highest([430, 1400, 620, 115]))

for name, case in [('ties at the top', [1400, 1400, 620]),
                   ('one value only', [430]),
                   ('empty input', [])]:
    try:
        print(f'{name:<15}:', second_highest(case))
    except Exception as e:
        print(f'{name:<15}: {type(e).__name__}: {e}')
```

```
visible test : 620
ties at the top: 1400
one value only : IndexError: list index out of range
empty input    : IndexError: list index out of range
```

It passes the visible test and fails all three hidden ones. With a tie at the top it returns 1400 — the highest value again, not the second-highest — and with fewer than two values it crashes. Each failure is a lost test case, which is how a correct-looking answer scores 2 out of 10.

The fix is to say what "second-highest" means when values repeat, and what to return when there is no answer:

```python
def second_highest_fixed(amounts):
    """Second-highest DISTINCT value, or None when there is no such value."""
    distinct = sorted(set(amounts), reverse=True)
    return distinct[1] if len(distinct) > 1 else None


print()
for name, case in [('visible test', [430, 1400, 620, 115]), ('ties at the top', [1400, 1400, 620]),
                   ('one value only', [430]), ('empty input', [])]:
    print(f'{name:<15}:', second_highest_fixed(case))
```

```

visible test   : 620
ties at the top: 620
one value only : None
empty input    : None
```

**The habit, which is the actual answer.** Before submitting any online-test problem, run it yourself on four inputs the problem did not give you: a tie, a single value, an empty input, and one very large input. That takes two minutes and is where most of the hidden test cases live. SQL problems have the same traps — duplicate values at a rank boundary, `NULL`s, a group with no rows — which is why Chapter 71's `RANK` against `DENSE_RANK` questions exist.

| Tier | What to say |
|---|---|
| Passes | "There were hidden test cases I didn't handle" |
| Strong | Names the usual hidden cases — ties, duplicates, one value, empty, very large — and the habit of testing them before submitting |
| Extra points | + **[+Clarify]** when the problem is silent on ties or empty input, state your assumption in a comment, because some reviewers read the code later + **[+Edge cases]** the SQL versions: duplicates at a rank boundary, `NULL` in a comparison, a group with no rows + **[+Validate]** a large input tests speed as well as correctness; an O(n²) answer can time out on the last hidden case |

**Likely follow-ups:** What would you return for an empty input, and why? How is this the same problem in SQL?
**Red flag:** submitting the moment the sample test passes.
**Learn it in:** Chapter 72A, §72A.1 (why data roles get DSA questions); Chapter 71's ranking questions; Chapter 17, §17.10 (errors and tracebacks).

### Q68A-003 · An online SQL problem says "return the result ordered by customer, then date". Your query is correct but fails. Why?

**Level:** Fresher · **Roles:** DA, DS, AE, BA

**Remember it as:** *The checker compares output, not intent. Column names, column order, row order and rounding are all part of the answer.*

**Answer in one line:** Automated checkers compare your output to the expected output exactly, so a correct query with columns in a different order, a different column alias, unrounded decimals or a missing `ORDER BY` is marked wrong — read the expected output format as carefully as the question.

**The five things that fail correct SQL in an online test:**

| | Fails because | Check |
|---|---|---|
| **Row order** | No `ORDER BY`, or ordered on the wrong column | Rows from a database have no guaranteed order unless you ask for one |
| **Column order** | `name, total` where the expected output is `total, name` | Match the sample output column by column |
| **Column names** | `sum(amount)` where the expected header is `total_amount` | Alias every computed column |
| **Rounding** | `3.333333` against an expected `3.33` | Use the rounding the problem states |
| **Dialect** | A MySQL function on a PostgreSQL checker | Check which database the platform runs; Chapter 71, §71.8 covers the differences |

**The deeper point, worth one sentence.** This is not pedantry from the platform. In a real job, a report consumed by another system breaks in exactly the same ways — a renamed column, a reordered extract — which is why Chapter 77 talks about data contracts. The online test is checking the same discipline.

| Tier | What to say |
|---|---|
| Passes | "Maybe the output format didn't match" |
| Strong | Names row order, column order, aliases, rounding and dialect, and checks each against the sample output |
| Extra points | + **[+Edge cases]** rows have no order without `ORDER BY`, so a query that "worked" in testing can fail on the checker + **[+Business]** the same mismatches break real downstream systems, which is why the discipline matters beyond the test + **[+Clarify]** if the expected output shows a tie-breaking order, it is part of the specification even when the wording does not mention it |

**Likely follow-ups:** How would you find which part of your output differs? What does `ORDER BY` do with `NULL`s?
**Red flag:** relying on the order rows happened to come back in.
**Learn it in:** Chapter 12, §12.5 (ORDER BY and LIMIT) and §12.16 (the same SQL in MySQL); Chapter 71, §71.8.

### Rapid-fire, 68A.2

Roles: DA, DS, DE, AE and BA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q68A-004 | How do you practise for an online test? | On the same kind of platform, under the same timer, in the language you will use — untimed practice builds knowledge but not the pace the test actually measures | **[+Validate]** keep a log of which problem types cost you most time; that is the study plan | Fresher · 68.7 |
| Q68A-005 | The test includes an aptitude section. What should you know? | That it is common in online tests and campus drives, that it is scored separately, and that this book does not teach it — practise it from a dedicated source rather than being surprised on the day | **[+Clarify]** check the test invitation; it usually lists the sections and their timing | Fresher · 68.1 |
| Q68A-006 | Can you use Google or ChatGPT during an online test? | Only if the rules screen says so, and usually it does not; many platforms detect tab switches and paste events, and a flagged attempt can be discarded entirely | **[+Edge cases]** "open book" tests exist, so read the rules rather than assuming either way | Fresher · 68.1 |
| Q68A-007 | What if your internet drops mid-test? | Reconnect at once, take a screenshot or note of the time, and email the recruiter or the address on the invitation the same day with what happened — most platforms save submitted work, so submit often | **[+Business]** a prompt, factual email is often enough to get a retake; silence is not | Fresher · 68.1 |
| Q68A-008 | One problem is clearly beyond you. What now? | Write the simplest version you can — handle the basic case, even with brute force — and submit it for partial credit, then move on rather than sinking the rest of the time | **[+Trade-offs]** ten minutes on a partial answer usually beats forty on a perfect one | Fresher · 72A.1 |
| Q68A-009 | Should you add comments in an online test? | A short one where you made an assumption — ties, empty input, rounding — because some companies have a person read the code after the score | **[+Clarify]** the assumption comment is what turns a "wrong" answer into a defensible one | Fresher · 69.3 |
| Q68A-010 | You finished early. What do you do with the time? | Re-run every solution on the edge cases from Q68A-002, check output formats against Q68A-003, then resubmit; do not leave early with points still on the table | **[+Validate]** the last ten minutes are the cheapest marks in the test | Fresher · 69.3 |
| Q68A-011 | A take-home arrives instead of a timed test. How is it different? | It is judged by a person on quality, clarity and judgement rather than by a checker on output, so the write-up and the reasoning matter as much as the code | **[+Signpost]** Chapter 82 covers take-homes in full, including whether one is fair to accept | Mid · 82.0 |
| Q68A-012 | You failed an online test. Can you try again? | Often after a cooling-off period the company sets; ask the recruiter what it is, and use the gap to fix the specific problem type that cost you | **[+Business]** asking politely signals interest; reapplying immediately to the same test signals nothing changed | Fresher · 68.8 |

---

## 68A.3 Campus drives, fresher hiring and the group discussion

Campus hiring in India runs on its own rhythm: a pre-placement talk, an eligibility filter, an online test, often a group discussion, then technical and HR interviews, sometimes all on one day. Placement rules — how many offers a student may take, what happens after the first accepted offer — **vary from college to college**, so the first thing to do is read your own placement cell's policy.

### Q68A-013 · A company is coming to campus next month. How do you prepare?

**Level:** Fresher · **Roles:** DA, DS, DE, AE, BA

**Remember it as:** *Know the company, know the role, know the rounds, and have one project you can talk about for two minutes.*

**Answer in one line:** Find out the role and the rounds from the placement cell and seniors, read the job description the way Chapter 8 teaches, practise the online test format under a timer, prepare a two-minute account of one real project, and read your college's placement policy before you accept anything.

**The month, in four weeks:**

| Week | Focus |
|---|---|
| **1** | The role and the rounds. Ask the placement cell and seniors who went through the same company last year; decode the job description (Chapter 8, §8.5) |
| **2** | The online test format, timed (section 68A.2), plus the question bank for the role's core skill — usually SQL (Chapter 71) |
| **3** | One project, told in two minutes and in ten (Chapter 27, §27.10); the group discussion (Q68A-014) with friends |
| **4** | Behavioural and HR basics (Chapter 81, §81.4), questions to ask (§81.5), and the placement policy |

**The thing seniors know and the job description does not say:** what the rounds actually were last year. That information is usually one conversation away, and it is the highest-value hour of the month.

| Tier | What to say |
|---|---|
| Passes | Revise the technical topics and practise interview questions |
| Strong | A plan by week covering the rounds, the timed test, one project story, behavioural basics, and the placement policy |
| Extra points | + **[+Clarify]** ask seniors what the rounds were last year; it is the cheapest, most accurate preparation available + **[+Business]** read the placement policy before the drive, because accepting one offer can end your placement season at some colleges + **[+Signpost]** one project told well beats five listed, which is Chapter 27's whole argument |

**Likely follow-ups:** What if you have no project? How would you prepare for two companies on the same day?
**Red flag:** discovering the placement policy after accepting an offer.
**Learn it in:** Chapter 8, §8.5 (decoding a job description) and §8.8 (entry routes); Chapter 27, §27.10; Chapter 68, §68.7.

### Q68A-014 · How do you do well in a group discussion without dominating it?

**Level:** Fresher · **Roles:** DA, DS, DE, AE, BA

**Remember it as:** *Evaluators score what you add to the group, not how long you talk. One structured point, one built on someone else's, and a fair summary beat ten minutes of volume.*

**Answer in one line:** Make one clear, structured contribution early, build visibly on other people's points, bring in someone who has not spoken, and offer a short balanced summary near the end — because a group discussion is scored on content, listening and how you work with the group, and talking over people loses on two of the three.

**What evaluators usually watch, and what to do about each:**

| They watch | What earns it | What loses it |
|---|---|---|
| **Content** | One specific point with a reason or a number | Generalities everyone else also said |
| **Structure** | "There are two sides here: X and Y" | Jumping between ideas |
| **Listening** | "Building on what she said about cost…" | Repeating a point already made |
| **Working with others** | Inviting a quiet member in; disagreeing politely | Interrupting, raising your voice |
| **Summary** | A fair one-minute close that includes views you disagreed with | Summarising only your own points |

**For a data role, the move that stands out.** Bring evidence. In a discussion on, say, whether India should adopt a four-day work week, the candidate who says "the question is what we would measure to know whether it worked — output per hour, attrition, sick days" is doing exactly what the job is. Structuring a vague question is Chapter 5's skill, and in a group discussion it is visible to everyone at once.

| Tier | What to say |
|---|---|
| Passes | Speak early and clearly, and do not interrupt |
| Strong | One structured point, visible listening, bringing others in, and a balanced summary — with the reason that the group, not airtime, is being scored |
| Extra points | + **[+Business]** for a data role, frame the topic as "what would we measure", which shows the job's core skill + **[+Edge cases]** if the group turns into a shouting match, a calm "can we hear from the people who haven't spoken" is often the most noticed thing anyone says + **[+Signpost]** structuring the question is Chapter 5, §5.4's issue tree, done out loud |

**Likely follow-ups:** What if you know nothing about the topic? What if someone keeps interrupting you?
**Red flag:** treating it as a debate to win.
**Learn it in:** Chapter 5, §5.2 (from a vague request to a precise question) and §5.4 (issue trees); Chapter 24, §24.4 (bottom line up front).

### Q68A-015 · "Tell me about yourself." You are a fresher with no work experience. What do you say?

**Level:** Fresher · **Roles:** DA, DS, DE, AE, BA

**Remember it as:** *Present, past, future in ninety seconds: what you are doing now, the one thing that proves you can do this job, and why this role is the next step.*

**Answer in one line:** In about ninety seconds: who you are now (degree, the data skills you have actually used), the one project or piece of work that shows you can do this job and what it found, and why this role is the logical next step — no life story, and nothing you cannot talk about for five more minutes.

**A worked shape, as a template rather than a script:**

> I'm in my final year of a B.Com, and over the last year I've taught myself SQL and Python for analysis. The piece of work I'm proudest of is an analysis of a public sales dataset where revenue appeared to halve in one month. Only about a tenth of that drop was the month being incomplete; the rest was a real fall in order value, while the number of orders fell much less. I'd like to start as a data analyst because that is exactly the work I've enjoyed most, and this role is in a team that does it for real customers.

Notice what it does: one concrete finding, with a number-shaped insight, said in plain words. The finding in that example is real — it is Chapter 75's Q75-047, on this book's own data — and any project you have done can be told the same way.

| Tier | What to say |
|---|---|
| Passes | A clear summary of education and skills |
| Strong | Present, past, future in ninety seconds, with one specific piece of work and what it found |
| Extra points | + **[+Business]** the finding, not the tools, is what an interviewer remembers + **[+Signpost]** anything you mention becomes the next question, so mention only what you can expand on + **[+Clarify]** tailor the last sentence to this role and this company, which shows you read the job description |

**Likely follow-ups:** Tell me more about that project. Why data and not something else?
**Red flag:** reciting the CV, or starting from school.
**Learn it in:** Chapter 27, §27.10 (telling the story in two minutes and in ten); Chapter 81, §81.4.

### Rapid-fire, 68A.3

Roles: DA, DS, DE, AE and BA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q68A-016 | What is a pre-placement talk for, from your side? | Information: what the role is, what the rounds are, and what the team actually does — and one good question asked there gets you remembered | **[+Clarify]** ask what a new joiner works on in the first three months | Fresher · 8.5 |
| Q68A-017 | Your CGPA is below a company's cut-off. What can you do? | Usually nothing for that drive, since campus cut-offs are applied as a filter; apply off-campus or through a referral instead, where a portfolio can carry more weight | **[+Business]** off-campus routes are slower but not filtered the same way | Fresher · 68.5 |
| Q68A-018 | What is a pool campus drive? | One company hiring from several colleges at a single venue or online event, which means more candidates per opening and a stronger filter at the first round | **[+Edge cases]** travel and timing are your problem; confirm the venue and reporting time a day ahead | Fresher · 68.1 |
| Q68A-019 | How do you answer "Why should we hire you?" as a fresher? | Match two or three requirements from the job description to specific evidence — a project, a result, a skill you have used — rather than listing qualities | **[+Business]** evidence beats adjectives; "hard-working" proves nothing | Fresher · 81.4 |
| Q68A-020 | How do you answer "What are your weaknesses?" honestly? | Name a real, job-relevant weakness, say what you are doing about it, and show progress — never a disguised strength like "I work too hard" | **[+Signpost]** Chapter 81 works this in full | Fresher · 81.4 |
| Q68A-021 | You have two offers on campus on the same day. What do you check? | Your placement cell's policy first — some colleges treat the first acceptance as final — then role, team, learning, location and the CTC breakup, not the headline number | **[+Business]** the role you will learn most in is usually worth more than a small difference in CTC | Fresher · 81.6, 81.9 |
| Q68A-022 | What is a group-discussion "case" format? | A business problem given to the group to solve together in the time, rather than an opinion topic — scored on structure and collaboration as much as on the answer | **[+Signpost]** it is a case interview done as a team; Chapter 75's framework applies | Fresher · 75.1 |
| Q68A-023 | Should a fresher apply for jobs asking for one to two years' experience? | Often yes, if you can show the skills through real projects; "years required" is frequently softer than it looks, and the cost of applying is low | **[+Clarify]** read which requirements are must-haves and which are wish-list (Chapter 8, §8.5) | Fresher · 8.5, 8.8 |
| Q68A-024 | How do you get a data internship with no experience? | A portfolio of one or two real projects, applications through referrals and direct messages as well as job portals, and a willingness to start in a narrower role | **[+Signpost]** an internship is the shortest route to "experience" on a fresher's CV | Fresher · 8.8, 27.11 |

---

## 68A.4 Live coding and virtual rounds

### Q68A-025 · The interviewer says "think aloud while you solve this". What does that actually mean?

**Level:** Fresher · **Roles:** DA, DS, DE, AE

**Remember it as:** *Narrate decisions, not keystrokes. Say what you are about to do and why, not what you are typing.*

**Answer in one line:** Restate the problem and your assumptions, say your plan before writing code, narrate each decision as you make it ("I'll group by customer first because…"), and say when you are checking something — because the interviewer is scoring your reasoning, and silence gives them nothing to score.

**The pattern, out loud:**

| Stage | What you say |
|---|---|
| **Restate** | "So I need each customer's second-highest order — distinct values, or can repeats count?" |
| **Plan** | "I'll rank orders within each customer, then filter to rank two." |
| **Build** | "Using `DENSE_RANK` rather than `RANK`, so ties don't skip a position." |
| **Check** | "Let me test a customer with only one order — that should give no row." |
| **Close** | "This works; for very large data I'd check it uses the index on customer." |

**What not to narrate:** "Now I'm typing SELECT. Now FROM." That is noise. The skill is narrating the decisions, which is where your judgement is visible — and it is exactly the shape of Chapter 69's strong answer, done live.

| Tier | What to say |
|---|---|
| Passes | Explain what the code is doing while writing it |
| Strong | Restate, plan, narrate decisions, check, close — with the point that decisions, not keystrokes, are what to say aloud |
| Extra points | + **[+Clarify]** the restatement often surfaces an assumption the interviewer then confirms, which is a point scored before writing anything + **[+Validate]** saying "let me test the edge case" out loud shows the habit even if time runs out + **[+Signpost]** this is Chapter 69's answer shape applied to a live round |

**Likely follow-ups:** What do you do if you go quiet because you are thinking hard? How do you think aloud in a language that is not your first?
**Red flag:** long silence, then a finished answer with no explanation.
**Learn it in:** Chapter 69, §69.2 (the shape of a strong answer) and §69.5 (the same moves under different rounds); Chapter 68, §68.3.

### Q68A-026 · You are stuck in a live coding round. What do you do?

**Level:** Fresher · **Roles:** DA, DS, DE, AE

**Remember it as:** *Say you are stuck, say where, and offer the simplest working version. Interviewers help candidates who show their thinking.*

**Answer in one line:** Say plainly where you are stuck, describe the simplest approach that would work even if inefficient, get that working, and ask a specific question if you need a hint — because most interviewers want to see how you recover, and many will help a candidate who is visibly reasoning.

**The recovery sequence:**

1. **Name it.** "I'm not sure how to handle customers with no orders here."
2. **Shrink it.** Solve a smaller version — one customer, three rows — by hand, out loud.
3. **Brute force first.** "The simple way is a loop over every customer; it's slow but correct. Let me get that working and then improve it."
4. **Ask a specific question.** "Is it acceptable to return zero for those customers, or should they be excluded?" A specific question is a clarification. "I don't know what to do" is a request to be rescued.

**Why this works.** A live round is partly a simulation of working with you. A colleague who says "I'm stuck on this part, here's what I've tried" is someone people want on their team; one who goes silent for ten minutes is not, however clever the eventual answer.

| Tier | What to say |
|---|---|
| Passes | Ask the interviewer for a hint |
| Strong | Name where you are stuck, shrink the problem, get a brute-force version working, then ask a specific question |
| Extra points | + **[+Business]** recovery is part of what is being assessed, because it predicts how you work on real problems + **[+Trade-offs]** a working slow answer, improved if time allows, beats an elegant unfinished one + **[+Clarify]** a specific question often turns out to be the assumption the problem intended you to ask about |

**Likely follow-ups:** What if the interviewer gives no hints? Have you ever been stuck in a real project — what did you do?
**Red flag:** going silent, or abandoning the problem.
**Learn it in:** Chapter 69, §69.3 (the twelve moves) and §69.6 (what not to do); Chapter 72A's walk-throughs.

### Q68A-027 · Your video interview freezes in the middle of your best answer. What do you do — and what should you have done before?

**Level:** Fresher · **Roles:** DA, DS, DE, AE, BA

**Remember it as:** *Prepare like the call will fail, so that when it does, recovery takes thirty seconds and costs nothing.*

**Answer in one line:** Before the call, test the link, camera, microphone and screen sharing, keep a phone hotspot ready and the recruiter's number to hand; when it freezes, rejoin at once, say briefly where you were, and summarise the answer in one sentence rather than restarting it.

**Before, the checklist:**

| | |
|---|---|
| **The link** | Open it fifteen minutes early; install whatever it needs |
| **Sound and camera** | Test both; use earphones to avoid echo |
| **Screen sharing** | Practise sharing the right window, not your whole desktop with notifications on |
| **A shared editor** | If the round uses one, open the practice version beforehand |
| **Backup** | Phone hotspot ready, phone charged, recruiter's number or email to hand |
| **The room** | Quiet, lit from the front, nothing on screen you would not want shared |

**After a drop:** rejoin immediately; if you cannot within a minute or two, message the recruiter or the interviewer by the contact you were given. On rejoining: "Sorry, I lost the connection. I was explaining why I'd use a left join here — in short, it keeps customers with no orders. Shall I continue from there?" One sentence, then carry on. Dropped connections are routine; how calmly you handle them is what is remembered.

| Tier | What to say |
|---|---|
| Passes | Rejoin quickly and apologise |
| Strong | The before-checklist plus the one-sentence recovery on rejoining |
| Extra points | + **[+Edge cases]** share a single window, not the whole screen, so a private notification never appears mid-interview + **[+Business]** a calm recovery is itself evidence of how you handle problems at work + **[+Validate]** a practice call with a friend on the same platform finds most problems before they matter |

**Likely follow-ups:** What if it happens during a timed coding task? What would you do if you could not rejoin at all?
**Red flag:** restarting the whole answer from the beginning, or vanishing without a message.
**Learn it in:** Chapter 68, §68.3 (what each round tests); Chapter 69, §69.5 (the same moves, under different rounds).

### Rapid-fire, 68A.4

Roles: DA, DS, DE, AE and BA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q68A-028 | The interviewer is silent and gives no reactions. What does it mean? | Usually nothing — many interviewers stay neutral on purpose, or are taking notes; keep narrating and checking in occasionally with "does that approach make sense?" | **[+Clarify]** a short check-in invites a hint without asking for one | Fresher · 69.5 |
| Q68A-029 | Can you look things up during a live round? | Ask first; many interviewers allow documentation for syntax, and asking is far better than being seen searching silently | **[+Business]** "I'd normally check the exact syntax — is that okay?" is honest and common | Fresher · 69.6 |
| Q68A-030 | You realise your earlier answer was wrong. Do you say so? | Yes, at once: "I said X earlier — I think that's wrong, it should be Y because…" Correcting yourself is a strong signal, not a weak one | **[+Validate]** self-correction shows the checking habit interviewers want | Mid · 69.3 |
| Q68A-031 | How long should an answer in a technical round be? | Two or three minutes for most questions: the answer first, then the reasoning, then stop and let them ask — long answers lose the interviewer and use up the round | **[+Signpost]** answer-first is the pyramid principle of Chapter 24 | Fresher · 24.4, 69.2 |
| Q68A-032 | What do you do if you do not understand the question? | Restate what you think it means and ask if that is right; it costs ten seconds and prevents ten minutes on the wrong problem | **[+Clarify]** this is Chapter 69's first move, and interviewers score it | Fresher · 69.3 |
| Q68A-033 | Should you keep your camera on in a virtual interview? | Yes unless told otherwise; it is expected, and turning it off without explanation reads as disengaged | **[+Edge cases]** if bandwidth forces it off, say so and offer to switch back on | Fresher · 68.3 |
| Q68A-034 | How do you handle an interviewer who interrupts constantly? | Stop, answer the interruption, then briefly return: "To finish the earlier point —" — interruptions are often deliberate, to see how you handle pressure | **[+Signpost]** Chapter 81 §81.7 covers hostile follow-ups | Mid · 81.7 |
| Q68A-035 | How do you show nerves are not hurting you? | Slow down deliberately, pause before answering, and restate the question — calm pacing reads as confidence whatever you feel | **[+Business]** a pause before a good answer is never penalised; a rushed wrong one is | Fresher · 81.10 |
| Q68A-036 | The round ends and you had no time for your questions. What do you do? | Ask one, briefly, if the interviewer offers, otherwise send it to the recruiter afterwards — and keep two ready for every round | **[+Signpost]** Chapter 81 §81.5 lists questions worth asking | Fresher · 81.5 |

---

## 68A.5 Getting found, and the rounds in between

### Q68A-037 · Write a message to a recruiter or hiring manager on LinkedIn that gets a reply.

**Level:** Fresher · **Roles:** DA, DS, DE, AE, BA

**Remember it as:** *Short, specific, and easy to say yes to: who you are, why this role, one piece of evidence, one clear ask.*

**Answer in one line:** Four or five sentences: name the specific role, give one piece of evidence that you fit it, make one small, clear request — usually whether they would consider your application or a short call — and attach or link nothing they did not ask for beyond a portfolio link.

**A worked example:**

> Hi Priya — I saw the Data Analyst opening on your team (job ID 4521). I've been doing exactly this kind of work on my own projects: most recently an analysis of a 25,000-row sales export where I found two-thirds of the dates were being silently lost in parsing. Would you be open to considering my application? My portfolio is here: [link]. Thank you for your time.

**Why it works:** it names the role, so it can be routed; it shows one concrete thing, so it is memorable; and it asks for something small, so saying yes costs little. The evidence in that example is, again, a real finding from this book's own data (Chapter 72B, Q72B-022) — use your own.

**What to avoid:** "Please refer me" to a stranger; a message that is only a CV attachment; asking for "any opening"; and following up more than once or twice.

| Tier | What to say |
|---|---|
| Passes | A polite message asking about openings |
| Strong | Specific role, one piece of evidence, one small request, a portfolio link, under 100 words |
| Extra points | + **[+Business]** a request that is easy to say yes to gets more yeses than one that asks a stranger to vouch for you + **[+Clarify]** quoting the job ID lets them route it in seconds + **[+Signpost]** Chapter 68, §68.5 covers referrals, which are a different, warmer request |

**Likely follow-ups:** How many people should you message? When is it acceptable to follow up?
**Red flag:** asking a stranger for a referral in the first message.
**Learn it in:** Chapter 68, §68.4 (LinkedIn hiring) and §68.5 (referrals).

### Q68A-038 · What is a "values" or "culture" round, and how do you prepare for it?

**Level:** Mid · **Roles:** DA, DS, DE, AE, BA

**Remember it as:** *They are testing whether your past behaviour matches what they say they value. Read their values, then find your stories that show each one.*

**Answer in one line:** A round, sometimes run by someone from outside the hiring team, that tests whether your past behaviour fits the company's stated values — so read those values, map one true story from your story bank to each, and answer in STAR form with specifics rather than agreeing with the values in general terms.

**How to prepare in an hour:**

| Step | Do this |
|---|---|
| **1** | Find the company's stated values — careers page, annual report, founder letters |
| **2** | For each value, pick one true story from your story bank (Chapter 81, §81.2) |
| **3** | Rehearse each in STAR form, with a specific result |
| **4** | Prepare one honest story about a time you fell short of a value, and what you changed |

**The trap:** answering "do you value ownership?" with "yes, very much". Every candidate says that. The round is scored on evidence: a specific time you owned something, what you did, and what happened.

| Tier | What to say |
|---|---|
| Passes | Research the company's values and show enthusiasm for them |
| Strong | Map a true story to each stated value and tell it in STAR form, including one about falling short |
| Extra points | + **[+Business]** a story about falling short and changing is often the most credible answer in the round + **[+Signpost]** this is Chapter 81's story bank used against a specific list + **[+Edge cases]** these rounds can be run by someone outside the team who can block a hire, so treat them as seriously as the technical ones |

**Likely follow-ups:** Tell me about a time you disagreed with your manager. Which of our values do you find hardest?
**Red flag:** agreeing with every value without a single example.
**Learn it in:** Chapter 81, §81.1 (STAR) and §81.2 (the story bank).

### Rapid-fire, 68A.5

Roles: DA, DS, DE, AE and BA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q68A-039 | Do you need a cover letter for data roles in India? | Rarely required, and often not read; a short, specific note in the application form or message does the job when one is asked for | **[+Business]** time is better spent on the CV and one strong project | Fresher · 68.2 |
| Q68A-040 | Which job portals should you use? | The ones your target companies actually post on — commonly LinkedIn, Naukri and company careers pages — plus referrals, which usually convert better than any portal | **[+Validate]** track where your interview calls actually come from and spend time there | Fresher · 68.4, 68.5 |
| Q68A-041 | How many applications should you send a week? | Fewer, better-targeted ones: a tailored CV for ten roles you fit beats an untouched CV sent to a hundred | **[+Signpost]** Chapter 68 §68.9 shows four CVs matched to their job descriptions | Fresher · 68.9 |
| Q68A-042 | A recruiter calls unexpectedly. What do you do? | If you cannot talk properly, ask to call back at a fixed time; if you can, have your notice period, current and expected CTC as ranges, and why you are looking ready | **[+Signpost]** the recruiter call is Chapter 68's gate 3 | Fresher · 68.1, 81.9 |
| Q68A-043 | What is a "bar raiser" interviewer? | At some companies, an interviewer from outside the team whose job is to keep the hiring standard high, often with a strong say in the decision | **[+Clarify]** ask the recruiter who is on the panel and what each round covers | Mid · 68.3 |
| Q68A-044 | Should you accept an interview for a role you are not sure about? | Usually yes: it is practice under real conditions and you learn about the role; just be honest if you decide it is not for you | **[+Business]** practice interviews before your target company are some of the best preparation there is | Fresher · 68.7 |
| Q68A-045 | How do you keep track of many applications at once? | A simple sheet: company, role, date applied, contact, stage, next step and date — the analyst's own pipeline, measured | **[+Validate]** the conversion rate at each stage tells you which part of your process to fix | Fresher · 68.7 |

---

## 68A.6 After the interview

### Q68A-046 · The final round ended an hour ago. What do you send, and when?

**Level:** Fresher · **Roles:** DA, DS, DE, AE, BA

**Remember it as:** *A short thank-you the same day, one specific detail from the conversation, and nothing that sounds like pressure.*

**Answer in one line:** A brief thank-you to the recruiter (or the interviewers, if you have their contact) within a day, mentioning one specific thing from the conversation and, if relevant, a short addition to an answer you wish you had given better — then wait for the timeline they gave.

**An example:**

> Thank you for the time today. I enjoyed the discussion about how the team defines active customers — it's a problem I'd like to work on. On the cohort question, I should have mentioned I'd also check that the definition is applied consistently across months. I look forward to hearing about next steps.

**Why the addition works:** it shows you kept thinking about the problem, which is exactly what an analyst does — and it is the only legitimate way to improve an answer after the round.

**What it cannot do:** change a decision already made. A thank-you is courtesy and a small signal, not a second interview. Keep it short.

| Tier | What to say |
|---|---|
| Passes | Send a thank-you email |
| Strong | Within a day, short, with one specific detail and optionally a brief improvement to one answer |
| Extra points | + **[+Business]** the improved answer shows the reflective habit the role needs + **[+Clarify]** note the timeline they gave you, so you know when a follow-up is reasonable + **[+Edge cases]** do not send a long essay; length reads as anxiety |

**Likely follow-ups:** Who should you send it to? What if you do not have the interviewers' emails?
**Red flag:** a long message re-arguing the interview.
**Learn it in:** Chapter 81, §81.5 (questions to ask interviewers); Chapter 24, §24.6 (writing short).

### Q68A-047 · It has been two weeks since your final round and you have heard nothing. What do you do?

**Level:** Fresher · **Roles:** DA, DS, DE, AE, BA

**Remember it as:** *One polite follow-up after the timeline passes, one more a week later, then keep going with your other applications. Silence is not an answer either way.*

**Answer in one line:** If the timeline they gave has passed, send one short, polite message asking whether there is an update, follow up once more about a week later if nothing comes, and keep every other application moving — because delays are common and usually have nothing to do with you, but waiting on one company is the most expensive mistake a job-seeker makes.

**The follow-up:**

> Hi Rahul — I wanted to check in on the Data Analyst role I interviewed for on the 12th. I'm still very interested and would be glad to hear about any update. Thank you.

**Why delays happen, which is worth knowing so you do not over-read them:** other candidates still being interviewed, a hiring manager on leave, a budget approval, a re-scoped role. None of them means rejection, and none of them is information about you.

**What not to do:** message every day, contact interviewers on personal channels, or put your search on hold. Treat the role as "in progress", and keep the pipeline full until you have a written offer.

| Tier | What to say |
|---|---|
| Passes | Send a follow-up email asking for an update |
| Strong | Follow up after the stated timeline, once more a week later, and keep all other applications moving |
| Extra points | + **[+Business]** a full pipeline protects you from the cost of waiting on one decision + **[+Edge cases]** a verbal "we'll make you an offer" is not an offer; keep going until it is written + **[+Clarify]** if they gave no timeline, asking for one at the end of the round avoids this situation entirely |

**Likely follow-ups:** When would you stop following up? What if you get another offer while waiting?
**Red flag:** pausing every other application while you wait.
**Learn it in:** Chapter 68, §68.1 (the gates); Chapter 81, §81.6 (handling offers).

### Q68A-048 · You were rejected after the final round. What do you do next?

**Level:** Fresher · **Roles:** DA, DS, DE, AE, BA

**Remember it as:** *Thank them, ask once for one thing to improve, write down what you would change, and keep the door open. A final-round rejection is close to an offer, not far from one.*

**Answer in one line:** Reply graciously, ask once for one specific thing to work on, write down for yourself what went worst while it is fresh, and stay in touch professionally — because reaching a final round means you were close, and companies often come back to strong runners-up for the next opening.

**The reply:**

> Thank you for letting me know, and for the time your team spent with me. If you're able to share one thing I could improve, I'd value it. I'd be glad to be considered for future roles.

**What you do privately, within a day:** list each round, what went well, what went badly, and the one change that would have helped most. That list is your study plan for the next interview, and it is far more specific than any general preparation.

**Reapplying.** Many companies have a cooling-off period before you can apply to the same role again; ask, or check their careers page. Chapter 68's Example 8 works through reapproaching a company for a different role after a rejection.

| Tier | What to say |
|---|---|
| Passes | Accept it politely and move on |
| Strong | Reply graciously, ask once for one improvement, do a private round-by-round review, and keep the door open |
| Extra points | + **[+Business]** runners-up are often contacted for the next opening, so the tone of your reply matters + **[+Validate]** the private review turns a rejection into the most specific study plan you will ever have + **[+Edge cases]** many companies give no feedback as a policy; do not read that as anything personal |

**Likely follow-ups:** What would you do if the feedback seemed unfair? When would you reapply?
**Red flag:** arguing with the decision, or disappearing without a reply.
**Learn it in:** Chapter 68, §68.8 (Example 8: re-approaching after a rejection); Chapter 81, §81.10 (hard moments).

### Rapid-fire, 68A.6

Roles: DA, DS, DE, AE and BA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q68A-049 | Should you connect with your interviewers on LinkedIn? | It is usually fine after the process ends, with a short note; doing it during the process can look like pressure | **[+Business]** a connection after a rejection, made graciously, keeps the door open | Fresher · 68.4 |
| Q68A-050 | A recruiter says "you'll hear by Friday" and you don't. Is it a no? | Not necessarily; timelines slip routinely. Follow up once on Monday, as in Q68A-047 | **[+Edge cases]** a no usually arrives as a no; silence is more often delay | Fresher · 68.1 |
| Q68A-051 | You think you did badly in one round. Do you mention it in a follow-up? | Only to add something useful — a better approach to one problem — not to apologise; the thank-you note is the place for one brief improvement, not a confession | **[+Signpost]** Q68A-046 shows the one-line version | Fresher · 69.6 |
| Q68A-052 | How do you stay motivated through many rejections? | Treat the search as a pipeline with conversion rates rather than a series of verdicts: measure each stage, fix the weakest, and expect most applications to end in no | **[+Validate]** if most rejections are at one stage, that stage is the problem to work on | Fresher · 83.8 |
| Q68A-053 | Should you ask why you were rejected? | Once, politely, asking for one thing to improve; some companies will tell you, many have a policy not to, and either is fine | **[+Signpost]** Chapter 81's Q81-078 | Fresher · 81.10 |
| Q68A-054 | You get an offer from your second choice while waiting on your first. What do you do? | Tell your first choice, politely, that you have an offer with a deadline and ask whether they can share their timeline — never invent an offer to create pressure | **[+Business]** honest urgency is common and usually respected; a bluff discovered is fatal | Mid · 81.6 |
| Q68A-055 | How do you decline an offer without burning the bridge? | Promptly, by email or a call, with thanks and a brief honest reason, and an expressed wish to stay in touch | **[+Business]** the recruiter you decline today may be hiring for your next role | Fresher · 81.6 |

---

## 68A.7 From offer to joining, and the first 90 days

### Q68A-056 · You have a written offer. What do you check before you sign it?

**Level:** Fresher · **Roles:** DA, DS, DE, AE, BA

**Remember it as:** *The headline number is the least informative line in the letter. Read the breakup, the dates, the conditions and anything that costs you money if you leave.*

**Answer in one line:** Read the role and level, the CTC breakup (what is fixed, what is variable, what is in-hand), the joining date and location, the probation terms and notice period, and any clause that costs you money if you leave early — a bond, a joining-bonus clawback, a training-cost recovery — and ask HR to explain anything unclear before you sign.

**The checklist:**

| Check | Why |
|---|---|
| **Role, level, reporting manager** | That it matches what you were interviewed for |
| **CTC breakup** | Fixed against variable, and the monthly in-hand — Chapter 81, §81.9 works the arithmetic |
| **Variable pay** | What it depends on and how it has actually paid out, which you can ask about |
| **Joining date and location** | That they match your notice period and your plans |
| **Probation** | How long, and what the notice period is during it |
| **Notice period** | After confirmation, and whether it is longer than you expected |
| **Bonds and clawbacks** | Any service bond, training-cost recovery, or joining-bonus repayment if you leave early |
| **Background verification** | What documents they will need, so you can gather them now |

**Clauses you are unsure about.** If a clause worries you — a long bond, a broad non-compete — ask HR to explain it in writing, and if it matters to you, take advice from someone qualified. Whether a particular clause is enforceable is a legal question, and this book does not answer legal questions.

| Tier | What to say |
|---|---|
| Passes | Check the salary and joining date |
| Strong | The full checklist, with the CTC breakup, probation and notice terms, and money-on-leaving clauses read before signing |
| Extra points | + **[+Business]** the money-on-leaving clauses are what most new joiners discover too late + **[+Clarify]** ask how variable pay has actually paid out in past years, which is a fair and common question + **[+Edge cases]** if something verbal is not in the letter, ask for it in writing before you sign |

**Likely follow-ups:** What would you do if the letter differs from what was agreed on the call? How do you ask for a later joining date?
**Red flag:** signing on the strength of the headline CTC.
**Learn it in:** Chapter 81, §81.6 (handling offers) and §81.9 (the Indian hiring conversation); Chapter 8, §8.6 (how to read salary figures).

### Q68A-057 · You have accepted the offer and resigned. What happens between now and joining?

**Level:** Fresher · **Roles:** DA, DS, DE, AE, BA

**Remember it as:** *Serve the notice well, leave cleanly, get your papers, and stay in touch with the new team. How you leave is part of your reputation.*

**Answer in one line:** Serve your notice professionally and hand over properly, collect your relieving and experience letters, have your background-verification documents ready, stay lightly in touch with your new recruiter or manager, and do not accept a counter-offer you have no intention of keeping — because both companies will remember how this period went.

**The period, in order:**

| | |
|---|---|
| **Resign in writing**, after the new offer is signed — never before | Chapter 81, Q81-031 makes this point |
| **Hand over properly** | Document what you own, who takes it over, and where things live |
| **Collect your papers** | Relieving letter, experience letter, final salary slips |
| **Background verification** | Respond promptly; delays here can delay your joining |
| **Stay in touch** | A short message to the new manager or recruiter every couple of weeks; ask if there is anything to read before day one |
| **A counter-offer** | Decide on the merits, once, and do not use it to renegotiate the new offer you already accepted (Chapter 81, Q81-033) |

**Reneging.** Accepting an offer and then backing out is sometimes unavoidable, but it costs the company real effort and is remembered. If you must, tell them as early as possible, honestly. Chapter 81's Q81-032 covers it.

| Tier | What to say |
|---|---|
| Passes | Serve the notice period and join on the date |
| Strong | Resign only after signing, hand over properly, collect the papers, keep verification moving, and stay in touch |
| Extra points | + **[+Business]** a clean handover is the last thing your old team remembers about you, and references come from it + **[+Edge cases]** resigning before the new offer is signed is the most expensive mistake in this period + **[+Clarify]** asking the new manager what to read before day one makes the first week easier and is noticed |

**Likely follow-ups:** What would you do if your current employer refused to release you early? How would you handle a counter-offer?
**Red flag:** resigning on a verbal offer.
**Learn it in:** Chapter 81, §81.9 (notice periods, buy-outs, counter-offers, relieving letters).

### Q68A-058 · You have joined as a data analyst. What do you do in the first 90 days?

**Level:** Fresher · **Roles:** DA, DS, AE, BA

**Remember it as:** *Learn the data and its definitions first, deliver one small useful thing early, and find one quietly broken thing to fix. Do not redesign anything in the first month.*

**Answer in one line:** In the first month learn the business, the data and how key numbers are defined; in the second deliver one small, useful piece of work and find one thing that is quietly wrong; in the third take ownership of something recurring — and resist redesigning anything until you understand why it is the way it is.

**The three months:**

| Month | Focus | What it produces |
|---|---|---|
| **1 · Learn** | The business, the main tables, how "revenue" and "active customer" are defined here, who owns what | A short glossary of definitions — which nearly always reveals that two teams define something differently |
| **2 · Deliver** | One small, useful piece of work, done fully, plus one data-quality problem found and reported | Trust, and a reputation for checking |
| **3 · Own** | A recurring report, a dashboard, or a process that becomes yours | A reason people come to you |

**Why the glossary matters most.** Chapter 76B's ambiguity drill showed that "revenue" on one quarter of data has four defensible values spanning ₹6.25 crore. In a new job, learning which one this company means — and finding where two teams mean different ones — is often the most valuable thing a new analyst does in their first month.

| Tier | What to say |
|---|---|
| Passes | Learn the tools and the data, and ask questions |
| Strong | Learn, deliver, own — with the definitions glossary in month one and one quietly broken thing found in month two |
| Extra points | + **[+Business]** finding a definition mismatch early is often worth more than any analysis + **[+Validate]** reconcile one important number to its source in the first month; it teaches the data faster than reading about it + **[+Edge cases]** redesigning a report before understanding its users is the most common way new analysts lose goodwill |

**Likely follow-ups:** What if nobody has time to onboard you? How would you know if the 90 days went well?
**Red flag:** a plan that starts with rebuilding the team's dashboards.
**Learn it in:** Chapter 76A, Q76A-070 (the first 90 days); Chapter 76B, §76B.11 (the ambiguity drill); Chapter 23, §23.13 (defining a metric).

### Rapid-fire, 68A.7

Roles: DA, DS, DE, AE and BA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q68A-059 | Can you negotiate an offer after it is written? | Often yes, before you sign: thank them, state what you are asking for and why, and be ready for either answer — negotiation after signing is far harder | **[+Signpost]** Chapter 81, §81.6 covers how | Fresher · 81.6 |
| Q68A-060 | Can you ask for a later joining date? | Yes, with a reason — usually your notice period — and as early as possible; most companies plan around notice periods routinely | **[+Business]** asking early is a request; asking late is a problem | Fresher · 81.9 |
| Q68A-061 | What documents does background verification usually need? | Typically identity, education certificates, past employment proof such as relieving letters and payslips, and sometimes address proof — the exact list comes from the company or its verification agency | **[+Clarify]** gather them during your notice period, not after joining | Fresher · 81.9 |
| Q68A-062 | What is probation, and what changes at the end of it? | A trial period after joining, after which you are confirmed; notice periods, some benefits and sometimes leave rules can differ before and after, as your letter states | **[+Validate]** know your probation goals in writing, so confirmation is not a surprise | Fresher · 81.9 |
| Q68A-063 | What should you do in your first week? | Meet the people you will work with, get access to the data and tools, read existing documentation and past reports, and write down every term you do not understand | **[+Signpost]** the list of unknown terms becomes your month-one glossary (Q68A-058) | Fresher · 3.2, 25.4 |
| Q68A-064 | How do you ask questions without seeming to know nothing? | Batch them, show what you tried first, and write down the answers so you never ask twice — new joiners are expected to ask; repeating questions is what is noticed | **[+Business]** a shared notes page of answers often becomes the team's onboarding document | Fresher · 83.7 |
| Q68A-065 | Your first assigned analysis has a vague brief. What do you do? | Exactly what Chapter 76B's drill teaches: ask the two or three questions that change the answer before building anything | **[+Signpost]** this is where the interview skill becomes the job | Fresher · 76B.11 |
| Q68A-066 | When should you start thinking about your next move? | Not in the first year: learn deeply, build a record of work you can describe, and let the next step come from evidence of what you did here | **[+Signpost]** Chapter 83 is the long game | Fresher · 83.4 |

---

## Common mistakes

- **Treating the online test as a knowledge test.** It is also a pace test and an edge-case test. Practise under a timer and test the hidden cases yourself.
- **Saying nothing in a group discussion, or saying too much.** Both lose. One structured point, visible listening and a fair summary win.
- **Narrating keystrokes instead of decisions** in a live round.
- **Pausing the whole search** while waiting on one company.
- **Resigning on a verbal offer.** Only a signed written offer is an offer.
- **Signing on the headline CTC** without reading the breakup, the notice and probation terms, and the clauses that cost money on leaving.
- **Redesigning things in the first month** of a new job.

## Final-week revision list

- Q68A-001, Q68A-002 and Q68A-003: the online test, the hidden cases and the output format.
- Q68A-014 and Q68A-015: the group discussion and "tell me about yourself".
- Q68A-025, Q68A-026 and Q68A-027: thinking aloud, being stuck, and the virtual round.
- Q68A-046 to Q68A-048: after the interview.
- Q68A-056 and Q68A-058: the offer letter and the first 90 days.

## Where this leads

Chapter 69 is the method for every answer in this part: the three tiers and the twelve extra-point moves. The question banks from Chapter 69A to Chapter 81 then cover each round's content, Chapter 82 runs take-homes and full mock interviews end to end, and Chapter 83 is the long game after you are hired.
