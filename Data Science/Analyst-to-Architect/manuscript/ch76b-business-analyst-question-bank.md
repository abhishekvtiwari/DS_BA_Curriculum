# Chapter 76B. Business Analyst Question Bank

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will learn to:** answer the requirements-gathering, process-mapping, and documentation questions that come up in BA interviews · tell a BRD, FRD, and SRS apart without hesitating · write a user story with real acceptance criteria, not a vague wish · map a process the way a BA actually would, with decision points and swimlanes · handle "can you just change the number?" and other stakeholder pushback without folding or getting defensive.
>
> **Before you start:** Chapter 24 (all of it: turning an ask into a question, business rules, stakeholders, and pushback) and Chapter 25 (all of it: the business analyst track), which between them teach every technique this bank tests; Chapter 26, section 26.10 (Agile, Scrum, and the backlog); Chapter 3, section 3.2 (order 5001's journey from enquiry to cash, which the worked examples use); and Chapter 69 for the three answer tiers and the twelve extra-point tags. This chapter tests those skills; it doesn't teach them again. When you can't answer a question, its **Learn it in** line sends you to the section that teaches it.
>
> **Time needed:** 2.5–3 hours to read and drill once (about 10 minutes per core question answered aloud, 1–2 minutes per rapid-fire row), plus 4–6 hours for the project: two interviews, a swimlane map, a story, and a requirement.
>
> **How this chapter is built.** Same format as every question bank in Part 8. Every **core question** gives a memory hook ("Remember it as…"), a one-line answer you can recall under pressure, and a tier table: what **passes**, what's **strong**, and the **extra points** (Chapter 69's moves, tagged the same way: **[+Clarify]**, **[+Edge cases]**, **[+Validate]** and so on). Then come the likely follow-ups, the red flag, and where to learn it. Every **rapid-fire section** is a scan table: question, one-line answer, one extra point, level, and where to learn it (a bare number such as 25.8 means that section). This chapter has no code to execute; a requirements document, a process map, and a user story are judged on completeness and clarity, so every worked example here is a full, concrete artifact, not a description of one. The worked examples use Riverstone's order-to-cash process, the same one Chapter 25 maps, with the same steps, requirement numbers, and figures.
>
> **Levels and roles.** Each question carries a level and the roles that usually ask it. **Fresher:** screening calls and first-job interviews. **Mid:** one to three years in the role. **Senior:** lead or specialist rounds. **BA** business analyst · **DA** data analyst · **BI** BI developer. The basic-but-tricky questions come first; if you're aiming at your first BA job, start with section 76B.1 and the Fresher questions, then work through the rest.

---

## 76B.1 Basic-but-tricky BA questions

### Q76B-007 · What's the difference between a BRD, an FRD, and an SRS?

**Level:** Fresher · **Roles:** BA, DA

**Remember it as:** *BRD is for the business, FRD is for the build, SRS is for the engineers, each one more technical and more detailed than the last.*

**Answer in one line:** A **BRD** (Business Requirements Document) captures the business need and goals, written for sponsors, executives, and finance, readable by someone who will never log in; an **FRD** (Functional Requirements Document) translates them into numbered functional requirements, process flows, business rules, and data definitions, written for developers and testers (detailed enough that two developers reading it build the same thing); an **SRS** (Software Requirements Specification) is the most technical of the three, detailed enough for a vendor to build from without talking to you, adding interfaces, non-functional requirements, data models, constraints, and error handling.

| Tier | What to say |
|---|---|
| Passes | Knows all three acronyms exist, can't distinguish their actual audience or level of detail |
| Strong | The audience-and-detail-level distinction above, with a one-line example of the same requirement expressed at each level |
| Extra points | **[+Edge cases]** not every organization uses all three; some combine BRD and FRD into one document, or skip a formal SRS entirely and go straight to user stories (section 76B.3) for agile teams: naming that this varies by organization shows real experience, not just memorized definitions |

**Likely follow-ups:** Which of the three would a project sponsor sign off on? Which would a developer actually build from?
**Red flag:** treating the three as interchangeable synonyms.
**Learn it in:** Chapter 25, section 25.7 (the three documents, and who reads each).

### Q76B-008 · Is a user story the same thing as a requirement?

**Level:** Fresher · **Roles:** BA, DA, BI

**Remember it as:** *A user story is a conversation starter with acceptance criteria attached. A requirement can be a much heavier, more formal document. They're related, not identical.*

**Answer in one line:** Not exactly: a **user story** is a short, deliberately incomplete description of a need from a user's perspective ("As a [role], I want [goal], so that [benefit]"), meant to prompt a conversation and get refined collaboratively with the team; a **requirement** in the traditional sense is meant to be complete and unambiguous on its own, without needing further conversation to be understood.

| Tier | What to say |
|---|---|
| Passes | Treats "user story" and "requirement" as interchangeable words for the same thing |
| Strong | The completeness distinction above: a user story is intentionally a placeholder for a conversation, not a finished specification |
| Extra points | **[+Business]** this is exactly why a user story needs acceptance criteria (Q76B-013) attached before it's actually "done": the criteria are what turn the conversation starter into something testable, closing the gap between the two |

**Likely follow-ups:** In what kind of project would you use formal requirements documents instead of user stories, or both together?
**Red flag:** treating a bare user story ("As a user, I want a better dashboard, so that I can see my data") as if it were already a complete, actionable requirement.
**Learn it in:** Chapter 25, section 25.8 (use cases and user stories).

### Rapid-fire, 76B.1

Roles: BA for every row; DA for Q76B-010 and Q76B-011.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q76B-009 | Use case vs. user story? | A use case describes a full interaction between an actor and a system, including alternate and exception flows, in more formal, structured detail / a user story is a short, single-sentence expression of a need | **[+Business]** use cases suit complex, multi-step system interactions; user stories suit iterative, conversation-driven agile work | Fresher · 25.8 |
| Q76B-010 | What's an assumption, in a requirements document, and why document it explicitly? | Something taken as true without confirmation, stated openly so it can be challenged or validated before it silently becomes a wrong foundation for the whole project | **[+Assume]** Chapter 69's Move 2 (state assumptions), the identical discipline applied to formal documentation instead of a live answer | Fresher · 25.7 (what a BRD holds); 69.3, Move 2 |
| Q76B-011 | What's the difference between "in scope" and "out of scope," and why does an explicit out-of-scope list matter? | In scope is what the project will deliver; out of scope is what it explicitly will not, stated up front to prevent scope creep and manage expectations before, not after, stakeholders assume otherwise | **[+Business]** an unstated out-of-scope item is the single most common source of a stakeholder feeling blindsided at delivery | Fresher · 25.7; 24.1 (question 3) |
| Q76B-012 | What's a stakeholder register? | A structured list of everyone with an interest in the project, their role, their influence, and how and when they need to be communicated with: the power–interest grid written down as a table | **[+Business]** distinguishing high-influence, high-interest stakeholders (manage closely) from low-influence, low-interest ones (monitor only) is the core of practical stakeholder prioritization | Fresher · 24.3 |

---

## 76B.2 Requirements gathering

### Q76B-001 · A stakeholder says "make the report better." How do you turn that into an actual requirement?

**Level:** Fresher · **Roles:** BA, DA, BI

**Remember it as:** *"Better" is a feeling, not a requirement. Your job is to find the specific, checkable thing hiding behind the vague word.*

**Answer in one line:** Ask specifically what problem the current report causes them, day to day, and work backward from that concrete pain point to a testable requirement, rather than guessing at what "better" might mean.

**Worked example**, a real elicitation dialogue:

> **Analyst:** "When you say 'better,' can you walk me through the last time the current report let you down?"
> **Stakeholder:** "Last Tuesday I needed last week's numbers by region, and I had to open it in Excel and build a pivot table myself, it took twenty minutes."
> **Analyst:** "So the requirement isn't 'better,' it's specifically: the report needs a region-level breakdown, viewable without any manual rework, available same-day."

| Tier | What to say |
|---|---|
| Passes | Asks what "better" means, gets "faster, clearer", and writes that down with one follow-up question |
| Strong | Asks for a specific recent example of the pain, then restates it as a testable requirement in the stakeholder's own words |
| Extra points | **[+Business]** the fix here isn't asking more questions in general, it's asking for a *specific instance*, since people are far better at describing one real moment than defining an abstract concept like "better"<br>**[+Validate]** restating the requirement back to the stakeholder in one sentence and getting a "yes, exactly" confirms it was captured correctly before any work starts |

**Likely follow-ups:** What if the stakeholder can't recall a specific example? How would you prioritize this requirement against three other vague asks from different stakeholders?
**Red flag:** documenting "make the report better" as the requirement itself, or guessing at a specific fix with no elicitation at all.
**Learn it in:** Chapter 24, section 24.1 (turning an ask into a question) and Chapter 25, section 25.3 (the five moves from a vague ask to a written requirement).

### Q76B-002 · What's the difference between a business requirement, a functional requirement, and a non-functional requirement?

**Level:** Fresher · **Roles:** BA, DA, BI

**Remember it as:** *Business requirement: why we're doing this. Functional requirement: what the system must do. Non-functional requirement: how well it must do it.*

**Answer in one line:** A **business requirement** states the underlying business goal ("reduce time spent reconciling orders"); a **functional requirement** states what the system must specifically do to support that goal ("the system shall flag any order with a quantity mismatch between the PO and the invoice"); a **non-functional requirement** states a quality constraint on how it does that ("the flag must appear within 2 seconds of the invoice being uploaded").

| Tier | What to say |
|---|---|
| Passes | Can define one of the three, conflates the other two |
| Strong | All three definitions above, with a matched example showing how one business requirement can produce several functional and non-functional requirements underneath it |
| Extra points | **[+Edge cases]** a common real mistake: writing a functional requirement that's actually a design decision in disguise ("the system shall use a dropdown menu" describes a UI choice, not a requirement; "the system shall let a user select from a predefined list of statuses" is the actual requirement, implementation-neutral)<br>**[+Edge cases]** names a data-specific non-functional requirement unprompted: freshness ("no more than two hours old during working hours") or reconciliation ("monthly revenue reconciles to the ERP to the rupee"), the ones that get dropped and then cause an incident |

**Likely follow-ups:** Give a non-functional requirement that isn't about speed. Why does mixing requirement types in one document cause problems later?
**Red flag:** writing an implementation detail (a specific button, a specific dropdown) as if it were the requirement itself.
**Learn it in:** Chapter 25, section 25.5 (the three kinds, and the table of non-functional requirements specific to data).

### Rapid-fire, 76B.2

Roles: BA for every row; DA for Q76B-004 to Q76B-006.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q76B-003 | What's a business rule, and how does it differ from a requirement? | A business rule is a statement of how the business works, independent of any system. Two kinds matter to a BA: constraints ("orders over ₹5 lakh need manager approval") and definitions ("active customer = a non-cancelled order in the trailing 90 days"). A requirement says what a system must do, often to enforce or compute one | **[+Business]** business rules usually outlive any one system; requirements are tied to the specific project building or changing that system | Mid · 24.2; 23.13 (the six-part template) |
| Q76B-004 | What's elicitation, as a formal BA term? | The structured process of drawing out requirements from stakeholders, via interviews, workshops, document analysis, observation, or surveys, rather than requirements simply being handed over complete | **[+Business]** different elicitation techniques suit different situations: a workshop surfaces conflicting stakeholder views fast; direct observation catches things nobody thinks to mention because it's "just how we do it" | Fresher · 25.1 (the four verbs); 25.3 |
| Q76B-005 | Why interview more than one stakeholder for the same process? | Different roles see different parts of the process and often disagree about how it actually works, even for something they'd all claim to understand the same way | **[+Evidence]** a sales rep and a finance controller frequently describe the exact same order-approval process differently, and the gap between their descriptions is itself useful information | Fresher · 24.3; 25.4 ("the room starts talking") |
| Q76B-006 | What's a requirements traceability matrix, in one sentence? | A table linking each requirement back to its business need and forward to the test case that verifies it, so nothing gets built without a reason or shipped without being checked | **[+Business]** it's the tool that answers "why are we building this" and "how do we know it worked" for every single requirement, at once | Mid · 25.7 |

---

## 76B.3 User stories and acceptance criteria

### Q76B-013 · Write a complete user story with acceptance criteria for: "sales reps want to know which of their accounts are at risk of churning"

**Level:** Mid · **Roles:** BA, DA, BI

**Remember it as:** *A user story with no acceptance criteria is a wish. Acceptance criteria are what turn a wish into something a developer can build and a tester can check off.*

**Answer in one line:** The story states the role, the goal, and the benefit in one sentence; the acceptance criteria list the specific, testable conditions that must be true for the story to be considered done, including the actual rule, never a word like "recently" or "the defined threshold".

**Worked example**, the at-risk list Chapter 25 specifies (its FR-01 to FR-03):

> **User story:** As a sales rep, I want to see which of my accounts are at risk of not ordering again, so that I can call them before they go quiet.
>
> **Acceptance criteria:**
> - **AC-1 (scope).** Given I am a logged-in sales rep, when I open the at-risk list, then I see only accounts where I am the assigned rep.
> - **AC-2 (the rule).** Given an account with at least four days of orders whose time since its last order is more than 1.5 times its own average gap between orders, when the list is generated, then that account appears on it with an "At Risk" flag.
> - **AC-3 (edge case).** Given an account with fewer than four days of orders, including one with a single order or none, when the list is generated, then it is not flagged and is counted separately as "too new to judge".
> - **AC-4 (empty state).** Given I have no at-risk accounts, when I open the list, then I see a clear "no accounts currently at risk" message, not an empty or broken-looking screen.
> - **AC-5 (reconciliation).** Given the list is refreshed, when the twelve-month revenue it shows for an account is compared with the ERP's figure for the same months, then the two agree to the rupee.

The rule in AC-2 isn't hypothetical. Run against Riverstone's 24 key accounts as of 31 December 2025, it flags 3 of them, and 7 are too new to judge (Chapter 25, section 25.6). That's why AC-3 exists: seven accounts that no rule is watching is a finding in itself.

| Tier | What to say |
|---|---|
| Passes | A story plus one happy-path criterion, no edge case |
| Strong | The story plus Given/When/Then criteria for the scope, the actual rule, and at least one edge case |
| Extra points | **[+Edge cases]** the empty state (AC-4) is exactly the kind of edge case a strong BA adds unprompted: what happens when there's *nothing* to show is easy to forget and easy for a developer to leave broken if it's never specified<br>**[+Validate]** a reconciliation criterion (AC-5), the fourth kind of criterion for data, and the one people new to data work miss<br>**[+Limits]** ties the list to a real technical constraint: it's only as fresh as its data, which may be up to one working day old (Chapter 25's NFR-01), so a flag doesn't change the instant a customer orders |

**Likely follow-ups:** How would you prioritize this story against three others in a sprint? What would make you split this into two smaller stories instead of one? What changes in AC-2 if the flag comes from a churn model's score instead of a rule?
**Red flag:** acceptance criteria so vague they can't actually be tested ("the dashboard should work well", or "flag accounts above the defined threshold" with no threshold).
**Learn it in:** Chapter 25, section 25.8 (Figure 25.3's story and its criteria, and the reconciliation criterion AC-5) and section 25.6 (the rule, and the query that counts it).

### Rapid-fire, 76B.3

Roles: BA for every row; DA and BI for Q76B-014 and Q76B-016.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q76B-014 | What does "Given/When/Then" mean in acceptance criteria? | Given (the starting context) / When (the action taken) / Then (the expected result), a structured format (called Gherkin) for writing testable criteria | **[+Business]** this structure is what lets a QA engineer write a test case almost directly from the acceptance criteria with no further translation | Fresher · 25.8 |
| Q76B-015 | What's the INVEST mnemonic for a good user story? | Independent, Negotiable, Valuable, Estimable, Small, Testable | **[+Edge cases]** a story that fails "Independent" (it can't be built without another story finishing first) often signals it should be resequenced or the dependency made explicit | Mid · 25.8; 26.10 |
| Q76B-016 | Why should a user story avoid specifying a particular UI element? | The story should describe the need, not the implementation, so the team retains freedom to choose the best actual design; specifying a "dropdown" locks in a decision that isn't the BA's or the story's to make | **[+Signpost]** name the rule behind it: it's Q76B-002's line between a requirement and a design decision, applied to a story | Fresher · 25.8; 25.5 |
| Q76B-017 | What's a spike, in agile terminology? | A time-boxed research or investigation task, done specifically because a story can't be sized or written properly until an open technical question is answered first | **[+Business]** a spike is the honest alternative to guessing at a story's size or acceptance criteria when genuine uncertainty exists | Mid · 26.10; 25.2 |

---

## 76B.4 Process mapping

### Q76B-018 · Map Riverstone's order-to-cash process at a high level, and explain what a swimlane adds that a simple flowchart doesn't

**Level:** Mid · **Roles:** BA, DA

**Remember it as:** *A flowchart shows what happens. A swimlane shows what happens AND whose job it is, which is usually the more useful question in a real business process.*

**Answer in one line:** A basic flowchart shows the sequence of steps; a **swimlane diagram** adds horizontal or vertical lanes, one per role or department, so each step visibly sits inside the lane of whoever's responsible for it, immediately surfacing handoffs between departments, which is usually exactly where a real process breaks down.

**Worked example**, order-to-cash for Riverstone's order 5001, swimlane by role (the numbers are Chapter 3's ten steps):

> **Customer lane:** 1 enquiry
> **Sales lane:** 2 visit and agree terms → 3 quote → 4 order typed into the ERP
> **Warehouse lane:** 5 stock check and reserve → 6 pick, pack, ship → 8 signed proof of delivery scanned
> **Finance lane:** 7 invoice → 9 payment matched to the invoice → 10 monthly sales report

| Tier | What to say |
|---|---|
| Passes | A flowchart with the right steps in order, with a note on who does each, but no lanes and no handoffs called out |
| Strong | The swimlane version above, correctly separating steps by which team owns them |
| Extra points | **[+Business]** the handoff *between* lanes (sales → warehouse, warehouse → finance) is almost always where delays and errors concentrate in a real process, an insight a plain flowchart hides entirely by not distinguishing ownership at all<br>**[+Evidence]** on order 5001, five of the nine transitions cross a lane, and each crossing is where a data-quality problem is born: re-typed product codes at step 4, missing delivery dates at step 8<br>**[+Edge cases]** a real map would also show what happens on an exception path (a rejected order, a payment dispute), not just the clean happy path shown above |

**Likely follow-ups:** Where in this process would you look first for a delay-reduction opportunity, and why? What would a BPMN version of this add beyond a plain swimlane diagram?
**Red flag:** a process map showing only the happy path, with no exception handling at all.
**Learn it in:** Chapter 25, section 25.4 (Figure 25.1, the swimlane of order 5001, and the lane table under it); the ten steps are Chapter 3, section 3.2.

### Rapid-fire, 76B.4

Roles: BA for every row; DA for Q76B-021 and Q76B-022.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q76B-019 | What's a decision point (or gateway) in a process map? | A point where the process branches based on a condition (approved vs. rejected, in-stock vs. backorder), shown as a diamond in most notations | **[+Edge cases]** every decision point needs every branch mapped, including the "unhappy" ones; a map that only shows the approved path is incomplete | Fresher · 25.4 |
| Q76B-020 | What does BPMN stand for, and what does it add over a generic flowchart? | Business Process Model and Notation, a standardized symbol set (specific shapes for events, gateways, tasks, and messages between participants) that makes a process map unambiguous across different tools and readers | **[+Business]** standardization matters most when a process map needs to be handed to an external vendor or IT team who wasn't in the room when it was drawn | Mid · 25.4 |
| Q76B-021 | What's the difference between an "as-is" and a "to-be" process map? | As-is documents the process exactly as it currently, actually works, warts and all; to-be documents the proposed, improved version | **[+Edge cases]** skipping the as-is map and jumping straight to to-be is a common mistake: you can't credibly propose an improvement to a process you never actually documented as it really runs | Fresher · 25.4 |
| Q76B-022 | Why might the as-is process, once actually mapped, surprise the people who work in it every day? | People executing a process day to day often only know their own step; mapping the whole thing end to end frequently reveals workarounds, redundant approvals, or handoffs nobody had the full picture of before | **[+Evidence]** this is one of the most consistently reported "aha" moments in real BA work: the map itself is often the deliverable that creates the most value, before any redesign happens at all | Mid · 25.4 |

---

## 76B.5 SDLC and where a BA fits

### Q76B-023 · Walk through the phases of the SDLC, and say specifically what a BA does in each

**Level:** Mid · **Roles:** BA

**Remember it as:** *A BA's role doesn't stop after requirements are written. It runs the whole length of the SDLC, in a different form at every stage.*

**Answer in one line:** Across the six phases, the BA does all of **Requirements** (elicitation, process mapping, gap analysis, writing and agreeing the requirements), defends the requirement in **Design** when the design quietly drops part of it, stays available in **Build** to answer the questions that would otherwise be guessed at, writes or reviews the UAT plan and prepares the users in **Test**, facilitates UAT in **Deploy** while real users run it, then confirms sign-off and hands over, and in **Maintain** triages whether an issue is a genuine defect or a new requirement in disguise. The phase names vary by company; the sequence doesn't.

| Tier | What to say |
|---|---|
| Passes | Names the SDLC phases correctly, describes the BA's role as "writing requirements" with no involvement in the other phases |
| Strong | The phase-by-phase involvement above, correctly identifying that a BA's role changes shape but doesn't disappear after requirements are handed off |
| Extra points | **[+Business]** the triage role at the maintenance stage (is this a bug, or a new requirement someone's calling a bug) is a genuinely common, underappreciated part of the job, and naming it specifically signals real experience rather than a textbook answer<br>**[+Edge cases]** the BA facilitates UAT but doesn't drive it: if the BA drives the mouse, the test measures the BA, not whether the product meets the users' need |

**Likely follow-ups:** How does a BA's role differ in a Waterfall project versus an Agile one? What happens when a developer's question during the build phase reveals the original requirement was actually ambiguous?
**Red flag:** describing the BA role as ending once requirements are signed off.
**Learn it in:** Chapter 25, section 25.2 (the six phases and the BA's part in each) and section 25.10 (who runs UAT).

### Rapid-fire, 76B.5

Roles: BA for every row; DA and BI for Q76B-024 to Q76B-026.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q76B-024 | Waterfall vs. Agile, from a BA's perspective? | Waterfall: requirements are finalized once, up front, before development starts / Agile: requirements evolve iteratively across sprints, with the BA continuously refining the backlog | **[+Business]** most real organizations run a hybrid, not a pure version of either, worth naming rather than presenting the two as a strict binary | Fresher · 25.2; 26.10 |
| Q76B-025 | What's the difference between the product backlog and the sprint backlog, and who owns each? | The product backlog is everything not yet started, in priority order, owned and ordered by the **Product Owner** (the person accountable for what gets built and in what order); the sprint backlog is what the team pulled into this sprint, plus its plan, owned by the developers who'll do it. The BA feeds the product backlog with refined, testable stories | **[+Edge cases]** a BA and a Product Owner role can overlap significantly or be entirely separate people depending on the organization | Mid · 26.10; 25.2 |
| Q76B-026 | What's a Definition of Done, and why does a team need to agree on one explicitly? | A team-wide, explicit checklist of what "finished" means for any story (code reviewed, tested, documentation updated, and so on), agreed once so it doesn't get silently redefined story by story | **[+Business]** without an explicit Definition of Done, "done" quietly means something different to the developer, the BA, and the stakeholder, and that gap surfaces late, expensively | Mid · 26.10; 25.8 |
| Q76B-027 | What's a change request, and why does even a small one need a formal process? | A formally logged request to modify already-approved scope, requirements, or a signed-off deliverable; a formal process (however lightweight) protects against silent scope creep and keeps a record of who approved what | **[+Business]** the process doesn't need to be heavy for a small change, but skipping it entirely for "just this once" is exactly how scope creep starts | Mid · 25.11 and its Common mistakes ("agreeing a scope change in a corridor"); 63.9 |

---

## 76B.6 Gap analysis and UAT

### Q76B-028 · What's a gap analysis, and walk through one for Riverstone's order-to-cash process

**Level:** Mid · **Roles:** BA, DA

**Remember it as:** *Gap analysis is just "where are we now" minus "where do we need to be," made explicit and specific enough to act on.*

**Answer in one line:** A **gap analysis** compares the current (as-is) state against the desired (to-be) state, identifying the specific differences that need to be closed and the root cause of each, each one becoming a candidate requirement or improvement initiative.

**Worked example**, the delivery step (step 8) of Riverstone's order-to-cash process:

> **As-is:** A driver brings back a paper proof of delivery. Someone at Bhiwandi Main scans it, emails it to finance, and changes the order to *Delivered* by hand, days later or not at all. The ERP holds no delivery date.
> **To-be:** The delivery is recorded in the ERP when the customer signs, with the date and time.
> **Gap:** Nothing records the delivery when it happens; the ERP hears about it later, from a scanned email.
> **Root cause:** Not "the warehouse is slow". The only record of the delivery is a piece of paper at the customer's site: the driver has no device, so the fact travels back on the truck before anyone can type it in.
> **Resulting requirement:** FR-14: the delivery status and date shall be recorded in the ERP within one hour of the proof of delivery being signed. It depends on NFR-09: a delivery recorded where there is no mobile signal shall reach the ERP within one hour of the signal returning, and none shall be lost.

| Tier | What to say |
|---|---|
| Passes | Defines gap analysis correctly in the abstract, can't apply it to a concrete example |
| Strong | The full worked example above: as-is, to-be, the specific gap, its root cause, and the requirement it produces |
| Extra points | **[+Business]** the gap analysis doesn't stop at identifying the difference, it names the *root cause* (no device where the delivery happens, not "people are slow"), which is what actually makes the resulting requirement solve the real problem rather than a symptom of it<br>**[+Validate]** asks "why" once more than feels necessary: telling the warehouse to scan faster would leave the date arriving days late anyway, so FR-14 can't work without NFR-09, the requirement that the recording survive a missing signal |

**Likely follow-ups:** How would you prioritize this gap against several others found in the same analysis? What would you check before assuming a device for every driver is actually the right fix?
**Red flag:** a gap analysis that identifies a difference but never traces it to an actionable, specific requirement, or that names the symptom as the root cause.
**Learn it in:** Chapter 25, section 25.9 (Figure 25.4 is this row, and the ranking table scores it against two other gaps); the step itself is Chapter 3, section 3.2, and section 3.7 lists what goes wrong there.

### Q76B-029 · What's UAT, who does it, and why can't developers or QA alone replace it?

**Level:** Fresher · **Roles:** BA, DA, BI

**Remember it as:** *UAT isn't "does the system work." It's "does the system actually do what the business needed," and only the business can really answer that.*

**Answer in one line:** **User Acceptance Testing** is the final validation stage, done by real business users (not developers or QA), checking whether the delivered system actually meets the original business need, not just whether it's technically functioning correctly, since a system can pass every technical test while still failing to solve the real problem it was built for.

| Tier | What to say |
|---|---|
| Passes | "UAT is when users test the system before launch" (correct, misses *why* it can't be skipped or delegated to QA) |
| Strong | The distinction above: QA verifies the system works as specified; UAT verifies the specification itself was actually right, which only the people with the original business need can judge |
| Extra points | **[+Business]** a system can pass 100% of its QA test cases and still fail UAT, because the test cases were built from a requirement that, it turns out, didn't fully capture what the business actually needed, exactly the kind of gap Q76B-001's elicitation discipline is meant to prevent upstream<br>**[+Validate]** for a data product, UAT has a second job: reconcile at least one complete period against a source the business already trusts (last month's closed figures, the ERP's own report), at more than one level of aggregation, because a total can match while the breakdown doesn't |

**Likely follow-ups:** What would you do if UAT reveals the original requirements were wrong, this late in the project? How would you structure a UAT test plan?
**Red flag:** treating UAT as a redundant, box-checking repeat of QA testing.
**Learn it in:** Chapter 25, section 25.10 (UAT, and the two halves of a data UAT plan).

### Rapid-fire, 76B.6

Roles: BA for every row; DA and BI for Q76B-030.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q76B-030 | What's a UAT test case, and how does it differ from a QA test case? | Written from the business user's real workflow and language, checking business outcomes / QA test cases are written from the technical specification, checking system behavior | **[+Validate]** well-written acceptance criteria (Q76B-013) are already UAT test cases: they can be handed to a user as they stand | Mid · 25.10; 25.8 |
| Q76B-031 | What happens if UAT fails close to a planned go-live date? | The defect gets triaged: is it a genuine bug (fix and retest), a missed requirement (assess impact and possibly delay), or a misunderstanding of scope (clarify and possibly defer to a later phase) | **[+Business]** the temptation to launch anyway and "fix it after" needs to be weighed honestly against the real cost of the specific gap found, not treated as automatically acceptable or automatically a blocker | Senior · 25.10 |
| Q76B-032 | Who signs off on UAT completion? | Typically the business stakeholder or sponsor who owns the requirement, not IT or the project manager, since sign-off is specifically confirming the business need was met | **[+Business]** this sign-off is the formal moment accountability for "does this actually work for the business" transfers, worth taking seriously rather than as a formality | Mid · 25.10 |

---

## 76B.7 Stakeholder management and pushback

### Q76B-033 · A stakeholder says "can you just change the number to make it look better?" How do you respond, live?

**Level:** Mid · **Roles:** BA, DA, BI

**Remember it as:** *Don't refuse and don't comply silently. Ask what's actually driving the request, then respond to that, not to the literal words.*

**Answer in one line:** Ask what's behind the request (are they worried the number looks bad to their own boss, do they suspect the number itself is wrong, is there missing context that would explain it) before either agreeing or refusing, since the literal request is almost never actually what they need.

**Worked example**, talked through live:

> "I'd say: 'I want to understand what's driving that, can you tell me more? If the number's wrong, I'll absolutely fix it, and I'd want to find the root cause. If it's right but looks concerning, I can add context that helps explain it rather than changing the number itself, since changing a correct number isn't something I can do.' Most of the time what they actually want is help explaining a real number, not a fabricated one, and naming that directly usually resolves it without an awkward confrontation."

| Tier | What to say |
|---|---|
| Passes | Explains politely that the number is correct and can't be changed, and offers to double-check it, but doesn't ask what's driving the request or offer an alternative |
| Strong | The diagnostic question above, distinguishing "the number might be wrong" from "the number is right but needs context" before responding either way |
| Extra points | **[+Business]** offering a legitimate alternative (adding context, a footnote, a caveat) gives the stakeholder something real they can use, rather than leaving them with nothing after a flat refusal, which is often what actually causes the request to escalate or repeat |

**Likely follow-ups:** What if the stakeholder insists after you've explained you can't change a correct number? How would you document this exchange, if at all?
**Red flag:** quietly changing a correct number to avoid conflict: altering a correct figure is an integrity failure, not a stakeholder-management choice. A defensive, unhelpful flat refusal with no attempt to solve the real underlying concern is the lesser failure.
**Learn it in:** Chapter 24, section 24.8 (the decision flow for "can you just change the number?", Figure 24.4).

### Rapid-fire, 76B.7

Roles: BA, DA and BI for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q76B-034 | Two stakeholders give you contradicting requirements. What do you do? | Don't silently pick one; bring both stakeholders together (or relay both positions clearly) so the conflict is resolved explicitly, with a documented decision, not quietly absorbed by the BA | **[+Business]** an undocumented, silently-resolved conflict tends to resurface later when the stakeholder who "lost" notices the outcome | Mid · 24.3 (RACI: who is accountable); 24.8; 25.11 |
| Q76B-035 | A powerful stakeholder wants a feature that conflicts with the actual data or user needs. How do you push back? | Lead with evidence, not opinion: show the specific data or user feedback that conflicts with the request, and frame it as a shared problem to solve together, not a personal disagreement | **[+Signpost]** bottom line up front, one message: Chapter 24's storytelling discipline applied to a difficult conversation instead of a report | Senior · 24.4; 24.8 |
| Q76B-036 | What's the risk of only communicating with the most senior stakeholder on a project? | Requirements end up shaped by whoever has the most authority to speak up, not necessarily whoever has the most accurate day-to-day knowledge of the actual process | **[+Edge cases]** the people closest to the work know the exceptions and the workarounds; that's Q76B-005's reason for interviewing more than one person | Mid · 24.3; 25.4 |
| Q76B-037 | How would you communicate a delay to a stakeholder who's expecting on-time delivery? | As early as possible, with the specific reason, the revised timeline, and what's being done about it, not a vague "it's taking longer than expected" with no further detail | **[+Business]** early, specific bad news is almost always received better than late, vague bad news | Fresher · 24.7 |

---

## 76B.8 Full scenarios, talked through live

### Q76B-038 · Full scenario, talked through live: elicit requirements for automating Riverstone's payment matching

**Level:** Senior · **Roles:** BA, DA

**What they're really testing:** whether a full elicitation-to-requirement cycle can be run start to finish, live, not just described as a concept. The process is step 9 of order-to-cash: a finance assistant reads each bank statement line and works out which invoice it pays.

**Talked through live, start to finish:**

> "First, I'd ask finance to walk me through exactly how they match a payment today, step by step, including what they do when a line doesn't match, since the exception path usually matters more than the happy path. Say they tell me: they read each line on the bank statement, look up that customer's open invoices in the ERP, and record the payment against the one it pays; when the amount doesn't equal any open invoice, or the reference is as thin as 'SHARMA HW JAN', they work it out by eye or ask sales. I'd ask about the awkward cases by name: a customer paying one invoice in two instalments, or one transfer covering two invoices. I'd ask how often a line can't be matched cleanly, since if exceptions are rare, automation removes most of the work, and if they're common, it doesn't. Say it's about 15% of lines. At 15% exceptions, automation handles about 85% of lines unattended, which is worth building, as long as the other 15% go to a named person. I'd then ask what 'match' actually means precisely, exact to the paisa, or within some tolerance for rounding, since 'close enough' matching is a very different, harder requirement than exact matching. From there I'd draft a first-pass requirement: 'The system shall compare each imported bank line with the customer's open invoices and record a match when customer and amount agree within ₹1; any other line shall go to [named person] for review; every automatic match shall record the rule and time that produced it,' and take that back to finance to confirm before writing it up formally."

**Extra-points moves demonstrated:** **[+Clarify]** asked about the exception path, not just the happy path, unprompted. **[+Business]** asked for the exception frequency specifically because it changes the case for automating this at all, and said what 15% implies. **[+Scale]** asked for an audit trail and a named exception owner unprompted, the two additions most often forgotten when a person's job is automated. **[+Validate]** ended by proposing to confirm the draft requirement with the stakeholder before treating it as final, rather than writing it up unilaterally.

**Likely follow-ups:** How would you write the acceptance criteria for this requirement? What would change about your approach if this were a brand-new process instead of automating an existing manual one?
**Red flag:** drafting a requirement after asking only about the happy path, with no question about what happens when something doesn't match.
**Learn it in:** Chapter 25, section 25.3 (the five moves, run live here) and section 25.12 (specifying an automation: BR-05, BR-06, FR-15 to FR-17, and the three additions); the step is Chapter 3, section 3.2, step 9.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Documenting a vague ask as the requirement itself | Nobody can tell what "done" actually means | Ask for a specific example of the pain, restate as a testable requirement |
| Treating BRD/FRD/SRS or use case/user story as interchangeable | Wrong document for the audience, confusion downstream | Know the audience and detail level each one is for |
| A user story with no acceptance criteria | The story can't actually be tested or marked done | Always attach Given/When/Then criteria, including edge cases |
| A process map showing only the happy path | Exception handling gets built as an afterthought, or not at all | Map every branch at every decision point, including rejections |
| Assuming the BA's job ends once requirements are signed off | The delivered system quietly drifts from the original need | Stay involved through design, build, and UAT |
| Skipping the as-is map and jumping straight to to-be | A proposed improvement that doesn't actually address the real current process | Always document as-is first, however tempting it is to skip |
| Silently complying with (or flatly refusing) "can you just change the number" | Either damaged data integrity or an unresolved, escalating stakeholder relationship | Diagnose what's actually driving the request before responding |

---

## In the real world: the requirement that was actually three requirements

Farah, now a data analyst whose first project turned out to be requirements work, is asked to gather requirements for "a way to see which customers haven't ordered recently." She resists the urge to write that sentence down as the requirement and instead asks three different stakeholders, separately, what they'd actually do with that information.

Sales wants it to prioritize outreach calls, and only cares about customers likely to still be recoverable. Finance wants it for a different reason entirely: flagging dormant accounts that still have open balances for a bad-debt review, and closing their credit limits, with no interest in whether they're "recoverable." Customer success wants it for a third reason: proactively checking in with accounts before they become a support escalation, regardless of order recency alone.

What looked like one requirement was genuinely three, each needing a different definition of "haven't ordered recently," a different output format, and a different owner. Farah's actual deliverable ends up being three separate, precisely scoped requirements instead of one vague one, and the project's initial one-week estimate for "the recency report" becomes a more honest three-week estimate for three real features. Her manager's note: *"The original ask would have shipped something nobody could actually use well. Three real requirements, properly scoped, took longer to define but were faster to build right the first time."*

---

## Project

**Goal:** run this chapter's full method on a real process, start to finish.

### Tools you'll need

No software specific to this chapter. A whiteboard or a simple diagramming tool (Lucidchart, draw.io, or even PowerPoint) for process maps; a shared document for BRDs, FRDs, and user stories; Chapter 11's spreadsheet skills (the same ones Chapter 25, section 25.7 uses for a traceability matrix) for a requirements traceability matrix in practice.

1. Pick a real, recurring process you're familiar with (at work or elsewhere), and interview at least two people involved in different steps of it.
2. Map it as-is, including at least one exception path, using a swimlane format.
3. Write one user story with full Given/When/Then acceptance criteria for a specific improvement to that process.
4. Draft the requirement, in one sentence, that a gap analysis of the same process would produce.
5. Write the "can you just change the number" response you'd actually give, for a real or hypothetical version of that request in your own context.

---

## Key terms

elicitation · business requirement · functional requirement · non-functional requirement · business rule · requirements traceability matrix · stakeholder register · BRD · FRD · SRS · user story · use case · INVEST · Given/When/Then (Gherkin) · reconciliation criterion · Definition of Done · spike · swimlane diagram · handoff · BPMN · decision point (gateway) · as-is vs. to-be · gap analysis · root cause · SDLC · product backlog vs. sprint backlog · Product Owner · change request · UAT · UAT sign-off

---

## Final-week revision list

Q76B-001, Q76B-002, Q76B-007, Q76B-008, Q76B-013, Q76B-018, Q76B-023, Q76B-028, Q76B-029, Q76B-033, Q76B-038.

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against, especially Move 1 (clarify) throughout sections 76B.2 and 76B.8.
- **Chapter 75, Product Sense, Metrics, Case Studies & Guesstimates,** already covers case-structure and stakeholder reasoning from the diagnostic-case angle; this chapter covers the same discipline from the documentation and process side.
- **Chapters 24 and 25** teach every technique this bank tests, and Chapter 26, section 26.10 the Agile vocabulary; each question's "Learn it in" names the section.
- **Chapter 78, Automation & Integration Question Bank,** takes automation from the requirement (Q76B-038) to the build: choosing the tool, retries, idempotency, and alerting.
