# Chapter 24. Requirements, Storytelling & Stakeholders

*Part II — The Analyst*

> **Chapter at a glance**
>
> **You will learn to:** turn a vague ask into a specific, answerable question · write down a business rule so precisely that two people applying it get the same answer · map stakeholders by power and interest, and adjust how much you involve each one · lead with the answer instead of the journey (bottom-line-up-front, the pyramid principle) · design a slide around one message instead of a table of everything you found · write a one-page analysis memo that survives being forwarded without you in the room · present to executives: structure, pacing, and handling the interruption · respond to "can you just change the number?" without becoming difficult or becoming compliant.
>
> **Before you start:** nothing technical — this chapter is about communication. Chapter 23's KPI diagnosis is used throughout as the worked example, so reading that chapter first (or at least its section 23.11) will make the worked examples click faster; Chapter 15's chart-design rules apply directly to the slides in section 24.6.
>
> **Time needed:** 10–12 hours, spread over a week. The reading is short; the exercises ask you to write, which takes longer than it looks.
>
> **Tools:** nothing beyond a text editor and, for the project, whatever you use to make slides. Every example in this chapter uses real numbers from Chapter 23's December 2025 revenue diagnosis.
>
> **Practice data:** `companion/ch24/`: a bank of clarifying questions, a one-page memo template, a fully worked memo and three-slide story built from Chapter 23's real analysis, all ready to adapt.

---

## Why this matters

You can run the correct query, build the honest chart, and still fail the assignment, because the assignment was never really "find the number." It was "help me decide something," and nobody said so out loud.

Two failures account for most of the wasted analyst-hours in any company. The first is answering the wrong question well: someone asks "can you pull the sales numbers?", you spend two days building a beautiful regional breakdown, and it turns out they wanted last week's total to check against an invoice. The second is answering the right question badly: you have the correct, useful finding, and you deliver it as eleven bullet points in an email that nobody reads past the second line, so the decision gets made without it anyway.

This chapter is about the two skills that sit either side of the analysis itself: figuring out what's actually being asked before you start, and making sure the answer lands once you're done. Neither is optional polish. An analyst who does brilliant work nobody understood, or beautiful work on the wrong question, has produced nothing a business can use — and, fairly or not, gets a reputation for being slow or for missing the point, when the real gap was somewhere else entirely.

---

## In plain English

A junior doctor doesn't start a consultation by ordering every test in the hospital. They ask what's wrong, ask a few sharpening questions, form a hypothesis, run the *relevant* tests, and then explain the result in one sentence a frightened patient can actually take in — not by reading out the lab report line by line.

Requirements gathering is the questions before the tests. Storytelling is the one sentence at the end. Stakeholder mapping is knowing that the patient wants the plain answer, the referring doctor wants the clinical detail, and the insurance company wants a form filled in correctly — three different people, three different versions of the same truth, none of them wrong to want what they want.

Analysts skip the questions because asking feels like admitting you don't already know the answer, and skip the plain sentence because the detailed version feels more rigorous. Both instincts are backwards. Asking a good question before you start is the single fastest thing you can do to avoid wasted work; saying the answer first is the single fastest thing you can do to get it acted on.

---

## 24.1 Turning an ask into a question

Almost every request an analyst receives arrives underspecified, not because the person asking is careless, but because they're thinking in terms of a decision, not a dataset. "Can you check on customer churn?" is a completely reasonable thing for a manager to say and a nearly unanswerable thing for a query to be built from.

**Six questions turn most vague asks into something you can act on:**

1. **What decision will this answer inform?** Knowing whether to cut a budget line needs a different number than knowing whether to congratulate a team.
2. **What should it be compared against?** Last month, last year, a target, a competitor — the same figure means something different against each.
3. **What's the scope, explicitly?** Which branches, segments, time period — and just as importantly, what's *out* of scope.
4. **How will the answer be used?** A one-line Slack reply, a slide in a board deck, and a detailed workbook are three different deliverables, not three formats of the same thing.
5. **When is it needed**, and would an approximate answer today beat an exact one next week?
6. **Has this been looked at before?** Redoing an analysis that already has an agreed answer wastes time and, worse, risks producing a second, different "truth."

| The ask | Left unclarified | Clarified |
|---|---|---|
| "Can you pull the sales numbers?" | You guess a scope, spend a day, guess wrong | "Net revenue by region, Q4 2025 vs Q4 2024 — for the Monday board pack" |
| "Why is revenue down?" | You analyze every possible cause | "Why did December fall from November, and is it one-off or a pattern?" |
| "Can you check if the new pricing worked?" | "Worked" is undefined | "Did average order value rise for orders after 1 March, for the same customers, versus before?" |

Notice what changed in each row: not the topic, but the **comparison**, the **scope**, and the **decision it serves**. Chapter 23's own worked example began exactly this way — "why is revenue down?" is not answerable until it becomes "why did December fall from November, and should we be worried?"

> **Watch out: clarifying questions are not stalling.** A well-aimed question at the start looks, to some stakeholders, like you're pushing back on the work. Frame it as speeding things up: *"So I build the right thing the first time — are we comparing December to November, or to last December?"* takes ten seconds and can save two days.

---

## 24.2 Documenting business rules

A **business rule** is a definition that decides who's in a count and who isn't — "active customer," "on-time delivery," "qualified lead." Chapter 23, section 23.13 gave the six-part template for writing one down; this section is about the conversation that produces it.

Business rules almost always start as a sentence someone says in a meeting, and that sentence is almost always ambiguous in a way nobody notices until two teams get different numbers. "A customer counts as active if they've ordered recently" needs a definition of *recently* before it can be a query. The analyst's job is to surface the ambiguity **before** it becomes two disagreeing reports, not after.

**A short script for pinning down a rule in the room:**

- *"When you say 'recently', do you mean the last 90 days, the calendar year, or something else?"*
- *"Should a cancelled order count, or only a delivered one?"*
- *"If a customer orders once and never again, are they active for the rest of that window, or only on the day they ordered?"*
- *"Is there an existing report that already answers something close to this? What does it use?"*

Write the answer down in the six-part form — name, formula, grain and population, time window, exclusions, owner — and send it back to the room as confirmation: *"To confirm: active customer = placed a non-cancelled order in the trailing 90 days, refreshed daily, owned by Analytics. Shout if that's not what you meant."* That one sentence, sent after the meeting, is worth more than an hour of careful analysis built on a guess.

---

## 24.3 Mapping your stakeholders

Not every stakeholder needs the same attention, and treating them as if they do wastes your time and theirs. The standard tool is a **power–interest grid**: how much influence someone has over the decision, against how much they care about this particular piece of work.

![A two-by-two grid with power on the vertical axis and interest on the horizontal, placing Riverstone people in each quadrant: manage closely (Anita Rao, Vikram Singh), keep satisfied (Finance Controller, Board), keep informed (Regional Sales Managers), monitor (branch staff, IT)](figures/fig24-1-stakeholder-grid.svg)

*Figure 24.1 — Where someone sits on this grid decides how much of your time they get, not how important they are as a person.*

| Quadrant | Who | How to engage |
|---|---|---|
| **Manage closely** (high power, high interest) | The person who asked, and whoever approves the outcome | Involve them in defining the question; show drafts before the final version |
| **Keep satisfied** (high power, low interest) | Finance, the board — they'll act on the conclusion but don't want the process | A short, polished summary; don't ask for their time until you need a decision |
| **Keep informed** (low power, high interest) | Teams affected by the finding, who can't change the outcome but should hear it from you first | Share the finding once it's solid; invite questions |
| **Monitor** (low power, low interest) | Everyone else touched in passing | Nothing proactive; answer if asked |

The mistake to avoid is treating the grid as a ranking of importance. A branch manager in "monitor" isn't unimportant as a person; they simply don't need — and usually don't want — to be looped into every draft of an analysis that doesn't change their day. Over-communicating to low-interest stakeholders is as much a failure of judgment as under-communicating to high-power ones: it trains people to skim everything you send.

**A second, complementary tool** for anyone actually doing work on the analysis (not just receiving it) is **RACI**: for each task, name who is **R**esponsible (does the work), **A**ccountable (answerable for it, usually one person), **C**onsulted (gives input beforehand), and **I**nformed (told afterward). It answers a different question than the power–interest grid — not "how much do I tell them" but "whose sign-off do I actually need" — and the two are worth keeping separate, because a stakeholder can be Accountable without having much day-to-day interest, or Consulted without having much power.

---

## 24.4 Bottom line up front: the pyramid principle

Here is how most analysis actually gets written, in the order it was discovered: background, then data sources, then findings one by one as they emerged, then caveats, and finally, on the last page, the conclusion. It's a completely natural order to *write in* — it's the order you thought in — and it is close to the worst possible order to be *read in*, because most readers form a judgment in the first paragraph and stop paying full attention well before page two.

![Left: how most analysis gets written, background then data then findings then caveats then conclusion buried at the bottom, with a note that the reader gives up around halfway. Right: the pyramid — conclusion first, then the two or three reasons, then supporting detail and appendix](figures/fig24-2-pyramid-principle.svg)

*Figure 24.2 — The pyramid principle, from Barbara Minto's work at McKinsey: state the conclusion, then the two or three reasons that support it, then the detail underneath each reason. Readers who stop after the first sentence still get the point.*

The fix, known widely as **BLUF (bottom line up front)** or the **pyramid principle**, is simple to state and takes practice to do naturally: **say the conclusion first, then the two or three reasons it's true, then the evidence under each reason.** Everything is still there — nothing gets cut — it's only reordered so that a reader who stops after one paragraph has the actual answer, and a reader who continues finds exactly the support they'd expect, in the order they'd expect it.

Compare the two openings of the same finding from Chapter 23:

> **Written bottom-up:** *"We pulled order data for November and December 2025 and computed revenue, order counts, and customer counts for each month. Revenue fell from ₹15.60 crore to ₹8.73 crore. We then decomposed this using a chain-linked method into three factors: customer count, orders per customer, and average order value. We found that average order value accounted for ₹4.55 crore of the ₹6.87 crore fall..."*

> **Written top-down (BLUF):** *"December's revenue fall (44%, to ₹8.73 crore) is the expected post-festive normalisation, not a new problem — average order value drove two-thirds of it, and no other explanation (fewer customers, a mix shift) held up. No action needed; we'll re-check if January doesn't recover."*

The second version is shorter, and a reader who stops after it has everything they need to make a decision. The first version has exactly the same facts, presented in the order the analyst experienced them rather than the order the reader needs them.

**How to build the pyramid**, working backward from your finished analysis:

1. **State the answer in one sentence.** If you can't, the analysis isn't finished — this is often the moment an analyst realizes they've found data, not a conclusion.
2. **List the two or three reasons the answer is true.** Not everything you found — the two or three load-bearing points. Chapter 23's example uses exactly three: AOV drove most of the fall, the mix didn't shift, and the same pattern repeated an earlier month.
3. **Put supporting detail under each reason**, not in a separate, undifferentiated pile.
4. **Move method, caveats, and full data to an appendix** that exists for the reader who wants to check your work, not for the reader who wants the answer.

---

## 24.5 One message per slide

The pyramid principle applies to a whole document; **one message per slide** is the same discipline applied to a single screen. A slide titled "December Sales Review" with a bulleted list of ten findings asks the reader to do the work of deciding what matters. A slide titled with the *finding itself* does that work for them.

![Left, a slide titled "December Sales Review" with ten bullet points of numbers and no clear point, labelled "reader has to find the point." Right, a slide titled "December's dip is seasonal, not a problem," with one headline number, a short waterfall chart, and one recommendation line](figures/fig24-3-one-message-per-slide.svg)

*Figure 24.3 — Same underlying facts. The left slide reports; the right slide tells.*

**The test for a slide title:** it should be a complete sentence stating a finding, not a topic label. "Revenue by Region" is a topic. "West region grew fastest, driven by new customers, not bigger orders" is a finding. If you can't write the title as a sentence, you haven't decided what the slide is *for* yet — and that's a sign to go back to the data, not a sign to write a vague title and hope the chart explains itself.

**What belongs on the slide, and what belongs in your mouth or the appendix:**

- **The slide** carries the headline number, one supporting chart (Chapter 15's rules apply in full: sorted bars, a zero baseline, one highlight color, a title that states the finding), and, where relevant, one recommendation line.
- **Your narration** carries the "why," the context, and the answer to the question you expect. Don't caption every bar with a paragraph; say it out loud, or put it in the appendix.
- **The appendix** carries the method, the full breakdown, and anything a skeptical reader would want to check but the room doesn't need to see.

This is uncomfortable the first few times, because it means deliberately leaving true, relevant, effortfully-produced numbers off the slide. That discomfort is the whole skill: **the goal of a slide is a decision, not a demonstration of how much work you did.**

---

## 24.6 Writing a one-page analysis memo

Not every finding gets a slide deck and a meeting. Most get a memo — an email, a shared doc, a Slack message with structure — read by someone without you in the room to fill the gaps. The memo has to work standing alone.

**A one-page memo has six parts:**

1. **Header:** to, from, date, and the question in one line.
2. **Bottom line:** the answer and the recommendation, in one or two sentences. A reader who stops here should know what happened and what to do about it.
3. **What we found:** the two or three load-bearing findings, each with its number.
4. **Why:** the mechanism, in a short paragraph — not just what happened, but why it happened.
5. **What we recommend:** one clear action, or an explicit "no action needed, and here's why," which is a real recommendation, not an absence of one.
6. **What could change this / appendix:** the assumption most likely to be wrong, and the method for anyone checking the work.

Here is Chapter 23's December revenue finding, written as the memo a reader could act on without ever opening a workbook:

> **To:** Anita Rao, Sales Head **From:** Meera Iyer, Analytics **Re:** Why did December revenue fall from November?
>
> **Bottom line.** December's ₹8.73 crore is 44.1% below November's ₹15.60 crore, but this is the expected post-festive normalisation, not a new problem: order values fell broadly across every segment, with no drop in active customers beyond the usual seasonal pattern. No corrective action is needed.
>
> **What we found.** Revenue fell ₹6.87 crore. Decomposed into its three drivers, customers contributed −₹1.26 crore, orders per customer −₹1.06 crore, and average order value −₹4.55 crore — AOV drove 66% of the fall. Segment mix was essentially unchanged. The same AOV-led pattern repeated the May-to-June dip earlier in the year (−40.4%).
>
> **Why.** Riverstone's festive season pulls forward large bulk and gifting orders; December's order book reverts to routine reordering — smaller per order, not fewer in number. The same mechanism explains both dips this year, which is itself evidence this is structural seasonality rather than a customer or competitive problem.
>
> **What we recommend.** No corrective action for December. For planning: build the FY2026 monthly revenue plan around this seasonal shape rather than a flat run rate.
>
> **What could change this.** If January 2026 also falls well below its typical range, the seasonal explanation would be wrong and this should be reopened.

The full version, with the appendix, is `companion/ch24/example_memo_dec_dip.md`; `memo_template.md` is the blank form.

Notice the memo does something the bulleted-list version wouldn't: it commits to an actual recommendation ("no action needed"), states the one thing that would change the analyst's mind, and gives Finance or the board enough to forward the email as-is, without a follow-up meeting. **A memo that requires a meeting to be understood hasn't finished its job.**

---

## 24.7 Presenting to executives

Executive attention is the scarcest resource in the building, and it behaves differently from a colleague's attention in three specific ways worth planning around.

- **They will interrupt, and the interruption is not a sign you've failed.** A senior stakeholder who asks a question halfway through your first slide is engaging, not derailing. Answer it, briefly, and offer to return to the detail if it matters ("Good question — the short answer is X; I have the full breakdown on slide four if it's useful"). Resisting the interruption to "get through the deck" reads as more concerned with your slides than their question.
- **They decide from the headline and check the detail only if something doesn't add up.** This is BLUF's whole justification in one sentence: build for the reader who stops at slide one, and reward the reader who keeps going.
- **They will ask the question you were hoping nobody would ask.** Usually the honest weak point in the analysis — the smallest sample, the shakiest assumption, the exception that doesn't fit the story. Anticipate it before the meeting and have the honest answer ready. "That's a fair challenge — the sample there is small (n=40), so I'd treat that slice as directional, not conclusive" lands far better than being caught flat-footed by your own data.

**A structure that survives interruption**, because each piece can stand alone if you never reach the next one: headline first, then the two or three reasons (each a complete thought, so being cut off after any one of them still leaves something useful said), then the recommendation, then stop talking and let the room ask questions rather than filling silence with more detail.

**Pacing:** rehearse the version that fits in half the time you've been given. Meetings run over, get bumped up the agenda, or lose ten minutes to the item before yours, and the failure mode is a rushed, unclear ending to the part that mattered — the recommendation and the ask — because the setup ran long. Say the headline in the first thirty seconds; everything after that is elaboration you can cut if you must.

---

## 24.8 Handling pushback: "can you just change the number?"

Every analyst eventually hears some version of: *"Can you re-run that without the outlier?"* — *"Can we use a different comparison period?"* — *"Are you sure that's the right definition?"* Some of these are completely legitimate. Some are an attempt to make an inconvenient number disappear. Telling them apart, calmly, is a core professional skill, not a confrontation to dread.

![A decision flow: a stakeholder asks to change a number; the analyst asks the reason; a genuine error gets fixed and nearby numbers rechecked; a reasonable alternative definition gets shown alongside the original with the choice documented; a request with no methodological reason gets the number held, with an offer to explain it in writing](figures/fig24-4-handling-pushback.svg)

*Figure 24.4 — The same question — why do you want this changed? — sorts almost every pushback into one of three honest responses.*

**The one question that does most of the work:** *"Help me understand why — is there something wrong with how I calculated it, or does the comparison need to change?"* This isn't a challenge; it's a genuine request for information, and the answer usually reveals which of three situations you're in.

1. **They've spotted a real error** — wrong filter, wrong period, a definition that doesn't match what was agreed. **Fix it, thank them for catching it, and check whether the same error affected anything nearby.** This is the most common outcome by far, and treating it as anything other than useful feedback damages your credibility, not theirs.
2. **They're proposing a genuinely reasonable alternative** — a different but defensible comparison period, a different but defensible definition. **Show both versions side by side, let them choose with the trade-off visible, and document which was used and why.** Chapter 23's section 23.13 exists exactly for this: write the definition down once it's settled, so the next person doesn't relitigate it.
3. **There's no methodological reason — the number is simply inconvenient.** **Hold the number.** You can be warm about it: *"I understand this isn't the news anyone wanted. I've checked the calculation twice and I'm confident in it — happy to walk through the method with anyone who wants to see it, or to note a caveat if there's a real one I'm missing."* Offering to explain, in writing, is not the same as offering to change the answer, and saying so explicitly protects both the number and the relationship.

**The test that resolves ambiguous cases:** *would you be comfortable explaining this change, and the reason for it, to the person who first asked for the number?* If the honest explanation is "a reasonable person pointed out a flaw," change it freely. If the honest explanation is "someone didn't like it," don't — and say, kindly, that you can't.

> **Watch out: "just" is doing a lot of work in that sentence.** "Can you *just* change the filter" or "*just* use last year instead" often signals that the requester believes this is a small, cosmetic adjustment. Sometimes it is. Sometimes changing "just" one thing changes the conclusion entirely, which is exactly why it's worth asking the reason before touching anything.

---

## 24.9 Bringing it together

The full arc, using Chapter 23's real diagnosis from start to finish:

1. **The ask arrives vague:** *"Why is revenue down?"*
2. **Clarify it** (section 24.1): down versus what, over what period, for what decision? → *"Why did December fall from November, and should we be worried going into the new year?"*
3. **Map the stakeholders** (section 24.3): Anita Rao (manage closely — she asked, and she'll decide whether to act), the Finance Controller (keep satisfied — cares about the conclusion, not the method), the Regional Sales Managers (keep informed — affected, can't change the outcome).
4. **Do the analysis**, applying Chapter 22's discipline (is the change real?) and Chapter 23's method (decompose it).
5. **Write the memo** (section 24.6), leading with the bottom line.
6. **Build the three-slide story** (section 24.5) for the meeting where it needs to be presented live.
7. **Present it** (section 24.7), expecting the interruption and the hard question.
8. **Handle whatever pushback arrives** (section 24.8) by asking the reason before touching the number.

Every step exists because skipping it has a specific, observable cost: skip step 2 and you analyze the wrong thing; skip step 3 and you either bore the board or blindside the branch managers; skip step 5's ordering and your correct finding gets buried; skip step 8's discipline and you either get steamrolled into a false conclusion or unnecessarily antagonize a legitimate question. None of these steps requires more technical skill than the rest of this book has already given you. They require slowing down at the two ends of the work — before you start, and after you've finished — where the technical skill alone doesn't help.

---
## Common mistakes and how to spot them

| Mistake | Symptom | Fix |
|---|---|---|
| Starting work on a vague ask | Two days spent, wrong scope delivered | Six clarifying questions before the first query |
| Assuming "recently" or "active" is obvious | Two teams report different numbers from the same data | Write the six-part business rule and confirm it in writing |
| Treating every stakeholder the same | Low-interest people skim everything; high-power people feel excluded | Map power and interest; adjust engagement per quadrant |
| Confusing power–interest with RACI | Unclear who actually needs to approve the work | Keep them separate: one is "how much do I tell them," the other is "whose sign-off do I need" |
| Writing in the order you discovered things | The reader gives up before the conclusion | Bottom line first, then reasons, then detail |
| A slide titled with a topic, not a finding | The room has to find the point themselves | Write the title as a complete sentence stating the finding |
| Putting every number on the slide | The headline drowns in supporting detail | Headline number, one chart, one recommendation; the rest is appendix or narration |
| A memo with no explicit recommendation | The reader doesn't know what to do next | State an action, or explicitly state that no action is needed and why |
| Rushing through interruptions in a meeting | Reads as more concerned with your slides than their question | Answer the question, offer to return to the detail, keep going |
| Changing a number because someone's unhappy with it | The analysis quietly loses its credibility | Ask the reason first; hold the number if there's no methodological one |
| Changing a number without documenting why | The next person doesn't know which version is "the" number | Show both versions, note the choice and the date |
| Treating a clarifying question as pushing back | Analysts under-ask to seem competent, then rework everything | Frame the question as speeding delivery up, not slowing it down |

---

## In the real world: the meeting that never needed to happen

Riverstone's January 2026 leadership meeting had one agenda item that had been dreaded all week: "Discuss December's revenue decline." Vikram Singh had asked for it on 3 January, in a message that read, in full: *"December numbers look bad, can someone explain?"*

Meera had the analysis finished by the 8th — Chapter 23's decomposition, done properly, with the mix check that ruled out a segment shift. What she almost sent was the analysis itself: four paragraphs of method, a table of the three effects, a comparison with June, and the conclusion in the last line. She stopped, reread it as if she'd never seen the data before, and rewrote the opening line before sending anything.

The message that actually went to Vikram, two days before the meeting, opened: *"Short answer: December's fall is the expected seasonal pattern, not a new problem — no action needed. Full breakdown below if useful, happy to present at Monday's meeting if you'd still like to discuss it."*

Vikram's reply came back within the hour: *"Thanks — that's exactly what I needed. Let's pull the item, save the slot for the Q1 pipeline instead."*

The meeting that had been dreaded all week never happened, because the answer had already arrived in a form that let Vikram make his own decision about whether a meeting was still necessary. Two things had changed from the analysis Meera almost sent:

1. **The bottom line came first**, not last, so a busy person reading on a phone got the entire useful content in one sentence.
2. **It answered "should we be worried" explicitly**, rather than presenting facts and leaving the worry-or-not judgment to the reader.

At the Monday meeting — now freed of an agenda item — Anita Rao asked, almost as an aside, whether this meant the FY2026 monthly targets should be reshaped around the seasonal pattern rather than a flat run rate. That question, not the one originally asked, turned into the actually useful outcome of the week: Finance agreed to rebuild the monthly plan with December and June built in as expected troughs, which meant no manager would spend February explaining a "miss" against a target that was unrealistic from the day it was set.

What made the difference:

- **She wrote the conclusion first**, and let the length of the response match how much the reader actually needed, not how much work had gone into producing it.
- **She answered the anxiety behind the question**, not just the literal words of it — "should we be worried" was the real ask inside "can someone explain."
- **She offered the meeting rather than assuming it was needed**, which let the recipient decide whether more of his time was actually required.
- **The real value came from a question the analysis prompted**, not the one it was asked to answer — which only happened because the original answer was clear enough to think past.

---

## Tools

- No new software this chapter. Every principle applies equally to an email, a shared document, a slide deck, or a chat message.
- **Companion files (`companion/ch24/`):**
  - `clarifying_questions_bank.md`: the six-question framework and worked examples from section 24.1.
  - `memo_template.md`: the blank one-page memo structure from section 24.6.
  - `example_memo_dec_dip.md`: the fully worked December memo, with its appendix.
  - `three_slide_story.md`: the same finding as a three-slide outline, ready to build in any slide tool.
- **Worth reading further:** Barbara Minto's *The Pyramid Principle* (the origin of the structure in section 24.4) and any of the standard stakeholder-management frameworks referenced in project management literature — the power–interest grid in this chapter is the common core of most of them.

---

## The project: turn one analysis into a memo and a three-slide story

**Goal:** take a finding you already have — from this book's earlier projects, or from your own work — and deliver it twice, in the two formats this chapter teaches.

**Option A: your own analysis.** Any finding you've produced that hasn't yet been formally written up or presented.

**Option B: Riverstone.** Use Chapter 23's December revenue diagnosis, or Chapter 21's Kolkata delivery-time finding, or Chapter 22's transporter comparison.

**Steps**

1. **Write the ask as it likely arrived**, vaguely, in one sentence.
2. **Write the six clarifying questions** you'd ask, and the specific, answerable question they produce.
3. **Map three stakeholders** for this finding using the power–interest grid, and say how each would be engaged differently.
4. **Write the one-page memo**, using the six-part template. Lead with the bottom line. State an actual recommendation.
5. **Build the three-slide story**: one headline slide, one "why" slide with a single supporting chart, one "what we'll do" slide.
6. **Write the title of each slide as a complete sentence** stating its finding, not a topic label.
7. **Anticipate one hard question** a skeptical executive would ask, and write the honest answer you'd give.
8. **Write one plausible piece of pushback** on the finding, decide which of section 24.8's three categories it falls into, and write your response.

**What good looks like:** the memo's bottom line is understandable with nothing else read; every slide title is a sentence, not a topic; the recommendation is explicit (including "no action needed" if that's the honest answer); the anticipated hard question has a real, honest answer rather than a deflection.

**Stretch goals**

- Time yourself presenting the three slides out loud in ninety seconds. If you can't, the slides are still carrying too much.
- Ask a colleague who doesn't know the underlying data to read only your memo's bottom line and tell you what they think should happen next. If their answer doesn't match your recommendation, the memo isn't finished.
- Rewrite the same finding for a fourth audience not covered by your three stakeholders (a new employee with no context, say), and note what changes.

---

## You've got it when…

- [ ] You turn a vague request into a specific question before starting any analysis.
- [ ] You can write a business rule with a name, formula, population, time window, exclusions, and owner — and you confirm it in writing after the meeting where it was agreed.
- [ ] You place stakeholders on a power–interest grid and engage each quadrant differently, rather than treating every stakeholder identically.
- [ ] You state your conclusion in the first sentence of anything you write, not the last.
- [ ] Every slide title in your decks is a complete sentence stating a finding.
- [ ] Your memos include an explicit recommendation, even when that recommendation is "no action needed."
- [ ] You expect interruptions in executive presentations and treat them as engagement, not derailment.
- [ ] When someone asks you to change a number, you ask why before you touch anything, and you know which of the three honest responses applies.
- [ ] You can tell the difference between a stakeholder's literal question and the real concern behind it, and you answer the real one.

---

## Recap

- **Requirements gathering** turns "can you check X?" into an answerable question, using six clarifying questions about decision, comparison, scope, format, timing, and prior work.
- **Business rules** need to be written down precisely — name, formula, population, time window, exclusions, owner — and confirmed back to the room, because the ambiguity in a spoken definition becomes two disagreeing reports if it isn't caught early.
- **Stakeholder mapping** by power and interest decides how much of your time and detail each person gets; RACI answers the separate question of whose sign-off you actually need.
- **The pyramid principle (BLUF)** puts the conclusion first, the two or three supporting reasons next, and the detail underneath — the opposite of the order most analysis is written in, and much closer to the order it should be read in.
- **One message per slide** means the title states the finding as a sentence, the slide carries one headline and one chart, and everything else moves to narration or an appendix.
- **A one-page memo** has six parts — header, bottom line, findings, why, recommendation, appendix — and must work for a reader who never talks to you directly.
- **Presenting to executives** means expecting interruption, building a structure that survives being cut short, and having an honest answer ready for the hardest question in the room.
- **"Can you just change the number?"** sorts into three honest responses: fix a real error, show both versions of a reasonable alternative, or hold the number when there's no methodological reason to move it — decided by asking why before touching anything.

---

## Practice exercises

### Warm-up

1. Turn each vague ask into a specific, answerable question using the six clarifying questions: (a) "Can you look at our top customers?" (b) "How's the new product doing?" (c) "Can you check the delivery times?"
2. Write a six-part business rule for "on-time delivery" at Riverstone, using Chapter 21's data as your source.
3. Place these three people on a power–interest grid for a finding about a single branch's delivery delays: the branch manager, the Sales Head, a customer service representative. Justify each placement in one sentence.
4. Rewrite this opening in bottom-line-up-front order: *"We collected data from three sources, cleaned it according to the process in Chapter 14, and after reconciling several discrepancies found that Kolkata's on-time rate is 68.1%, well below the other branches, which we believe is linked to route length."*
5. Which of these slide titles states a finding, and which is a topic label? Rewrite the topic labels as findings: (a) "Regional Performance", (b) "West grew fastest, driven by new customers, not bigger orders", (c) "Q4 Marketing Spend."
6. A colleague asks you to "just use last year's numbers instead" for a comparison. What's the one question you ask before doing it?

### Core

7. Write the six clarifying questions and the resulting specific question for: "Can you tell me if our customers are happy?"
8. Draft a full six-part business rule for "qualified lead," using Chapter 23's real leads data as your source, and note one place where the definition could reasonably go two ways.
9. Build a power–interest grid for the December revenue finding (section 24.9), placing at least five stakeholders, including at least one in each quadrant.
10. Take any three findings from Chapter 21 (delivery times) and write them as three slide titles, each a complete sentence stating the finding.
11. Write the one-page memo for Chapter 21's Kolkata delivery-time finding, using the six-part template.
12. Write the three-slide outline for the same finding: one headline slide, one "why" slide, one "what we'll do" slide.
13. Write the hardest question an executive could ask about the December revenue memo, and write the honest answer.
14. A regional manager asks you to exclude "an unusual one-off order" from a monthly total because it makes their number look inflated. Using section 24.8, decide which of the three categories this falls into and write your response.
15. Rewrite this slide's content to carry one message: a slide currently titled "Marketing Metrics" with nine bullet points covering spend, leads, CAC, ROAS, and conversion by month.
16. Write the "what could change this" section of a memo for any finding in this book, stating the single assumption most likely to be wrong.

### Stretch

17. Take a real request you've received at work (or invent a plausible one) and write the full arc from section 24.9: ask, clarifying questions, stakeholder map, memo, three slides, anticipated hard question, and a piece of pushback with your response.
18. Interview a colleague (or role-play with a friend) who plays a stakeholder pushing back on a finding for no methodological reason. Practice the response from section 24.8 out loud, and note what felt hardest to say.
19. Take a memo you or a colleague has written in the past and rewrite its opening in BLUF order without changing any of the facts. Compare the two versions for length and clarity.

### Think about it

20. A stakeholder consistently asks for "just a quick number" and then acts on it as if it were a fully vetted analysis. What's the risk, and how would you address it without refusing to help?
21. You're asked to present a finding you believe is correct but that will be unwelcome to a powerful stakeholder in the room. What do you do to prepare, beyond getting the analysis right?
22. Is it ever appropriate to give a stakeholder the detailed, bottom-up version of an analysis rather than the BLUF version? When?

---

## Key terms

requirements gathering · clarifying question · business rule · stakeholder mapping · power–interest grid · RACI (Responsible, Accountable, Consulted, Informed) · bottom line up front (BLUF) · pyramid principle · one message per slide · slide title as a finding · one-page analysis memo · executive presentation · pushback · Goodhart's law (Chapter 23)

*(All terms are defined in the Glossary, Appendix A.)*

---

## Where this leads

- **Chapter 25, The Business Analyst Track:** requirements gathering formalized further, with process mapping, user stories, and the documents (BRD, FRD, SRS) that a full BA role produces.
- **Chapter 23, Business Acumen, KPIs & Metrics:** the diagnosis method this chapter's worked example leans on throughout.
- **Chapter 15, Data Visualization Principles:** the chart-design rules that make the "why" slide in section 24.5 honest and readable.
- **Chapter 26, The Professional Toolkit:** documentation habits that make a business rule or a memo findable months later.
- **Interview preparation:** the Business Analyst bank (Chapter 76) and the Behavioral & Case Interview bank (Chapter 75) both draw directly on this chapter — "tell me about a time a stakeholder pushed back on your analysis" is one of the most common behavioral questions an analyst will face.

---

## Answers to practice exercises

*(In the finished book these move to Appendix G.)*

**1.** (a) "Top customers by what measure — revenue, order count, or longest relationship — over what period, and for which decision (a loyalty program, a sales call list, a board slide)?" (b) "Doing well by what measure — units sold, revenue, repeat purchase rate — since launch or in a specific recent period, compared against what target or prior product?" (c) "Delivery times for which branch or period, compared against the promised times or against another branch, and is this for an operational fix or a customer-facing promise?"

**2.** Name: On-time delivery, 2025. Formula: `delivery_days <= promised_days` per order. Population: delivered orders only (excludes cancelled). Time window: calendar year 2025. Exclusions: cancelled orders, and orders with no recorded delivery date. Owner: Operations analytics, reviewed quarterly.

**3.** Branch manager: high power (controls the branch's operations), high interest (directly affected) — manage closely. Sales Head: high power (sets targets and promises), moderate-to-high interest (one branch among several) — likely manage closely or keep informed, depending on how material this branch is to the whole. Customer service representative: low power (can't change delivery operations), high interest (fields the complaints) — keep informed.

**4.** *"Kolkata's on-time delivery rate (68.1%) is well below Riverstone's other branches, and we believe it's linked to route length. We reconciled several data discrepancies across three sources to reach this figure; details below."*

**5.** (b) states a finding. (a) and (c) are topic labels. Rewritten: (a) → "West region grew fastest this quarter" (or whatever the actual finding is); (c) → "Q4 marketing spend rose 18% while CAC stayed flat" (or the actual finding).

**6.** "Help me understand why — is there something about how the current comparison was calculated that's wrong, or is last year genuinely a better comparison for what we're deciding?"

**7.** Six questions: what decision (retention strategy? product changes?), compared against what (last survey, an industry benchmark), which customers (all, or a segment), how it'll be used (a slide, an ongoing tracker), when it's needed, and whether a satisfaction measure already exists. Resulting question, for example: "What's our Net Promoter Score this quarter compared to last quarter, and which segment is driving any change?"

**8.** Name: Qualified lead, 2025. Formula: a lead that has reached at least the "Quoted" stage. Population: all 43 leads in the CRM. Time window: calendar year 2025. Exclusions: leads still at "New" with no contact recorded. Owner: Sales operations. The reasonable ambiguity: should "Contacted" count as qualified, or only "Quoted" and beyond? Both are defensible, and the choice changes the qualified count from 14 to 22.

**9.** For example: Anita Rao (manage closely — asked, decides on action), Vikram Singh (manage closely — owns the sales relationship), Finance Controller (keep satisfied — cares about the conclusion for planning, not the method), Regional Sales Managers (keep informed — affected by any resulting FY2026 plan change), branch-level staff (monitor — not directly affected by this particular finding).

**10.** For example: "Kolkata's delivery times are both the slowest and the least predictable of any branch," "The company promise of 5–7 days is met for 82% of orders, but only 68% in Kolkata," "The festive season adds 1–2 days to delivery times across every branch."

**11.** Bottom line: Kolkata's median delivery time (5.7 days) and on-time rate (68.1%) are both the worst of Riverstone's four branches, and the gap is driven by inconsistency, not just slowness — its interquartile range is 2.5 times Mumbai HO's. What we found: [the section 21's branch comparison numbers]. Why: [route length / logistics explanation]. Recommend: investigate the Kolkata route structure; consider a longer, honest promise for that branch in the interim. What could change this: if a specific operational cause is found and fixed, revisit the promise.

**12.** Slide 1: "Kolkata is Riverstone's slowest and least predictable branch" (headline numbers). Slide 2: "The gap is inconsistency, not just speed" (box plot comparison, IQR called out). Slide 3: "Investigate the route structure; consider an honest interim promise" (recommendation, timeline).

**13.** Hard question: "How do we know this isn't just bad luck in one year — have we checked whether this pattern holds over multiple years?" Honest answer: "We've only got one full year of comparable data, so this is the best evidence available; if it's a real concern, tracking it through the next seasonal cycle would confirm whether it's a stable branch effect or a one-off."

**14.** This is category 3 (or possibly 2, depending on the reason given) — ask first: is there a data error in how the order was recorded, or is it simply that the order makes the number look worse than the manager would like? If it's a genuinely miscategorized transaction (say, a data-entry duplicate), fix it. If it's a real, correctly recorded order that the manager just doesn't like seeing counted, hold the number and offer to show both the with- and without-outlier views side by side, clearly labelled, so nothing is hidden.

**15.** One message, for example: "CAC held steady at ₹8,194 while lead volume grew 15% — marketing efficiency is improving." One headline number, one supporting chart (CAC by month), one line on what that means; the other eight numbers move to an appendix or get mentioned verbally if asked.

**16.** For example, for Chapter 23's December memo: "This conclusion assumes December 2026 will follow the same seasonal pattern as 2025; if a genuine change in customer behaviour (not just seasonality) is driving the fall, this assumption would be wrong and the recommendation should be revisited."

**17–19.** These are personal exercises with no single correct answer; check your work against the chapter's criteria: does the memo's bottom line stand alone, does every slide title state a finding, and is the pushback response honest rather than either capitulating or refusing to engage?

**20.** The risk is that a "quick number" gets treated with the confidence of a fully checked analysis, and a caveat or limitation that should have travelled with it gets lost. Address it by attaching one line of context even to a fast answer — "quick estimate, not reconciled against the full data" — so speed and confidence aren't accidentally conflated.

**21.** Check the analysis itself extra carefully (a wrong number delivered to an unhappy audience is much worse than one delivered to a receptive one), anticipate the specific objections that stakeholder is likely to raise and prepare honest answers, consider briefing them privately before the group meeting so the reaction happens in a lower-stakes setting, and make sure the tone of the delivery is neutral and fact-led rather than appearing to take a side.

**22.** Yes — when the audience is technical peers reviewing your method (not deciding on an action), when you're explicitly asked to show your work step by step (a code review, an audit), or when the "reasons" themselves are the point of the conversation, such as teaching someone the method. BLUF is for decisions; bottom-up is for verification and learning.
