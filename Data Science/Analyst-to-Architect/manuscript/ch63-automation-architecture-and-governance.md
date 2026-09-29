# Chapter 63. Automation Architecture & Governance

*Part 7 — Architecture, Governance & Leadership*

> **Chapter at a glance**
>
> **You will learn to:** design the flow from source to delivered result as one architecture instead of a pile of independent scripts · discover and prioritize automation opportunities by value, risk, and effort, with a real worked ROI comparison · choose the right tool for a given job from a full decision matrix — macro, scheduled script, BI subscription, low-code flow, orchestrated pipeline, integration platform, RPA, or an AI agent · apply a reference architecture that every automation in this book turns out to be a specialization of · decide between scheduled and event-driven designs · build the shared services every automation needs rather than reinventing them each time · assign ownership, write runbooks, and support what you've automated · find and control shadow IT before it becomes an unowned, business-critical liability · apply the controls — approvals, segregation of duties, audit trails, change management — that keep automation trustworthy at scale · retire an automation safely.
>
> **Before you start:** this chapter governs automations built earlier in this book: Chapter 19 (VBA and Apps Script macros), Chapter 20 (the Daily Sales Flash), Chapter 46 (Dagster orchestration, Part 5), Chapter 51 (the CRM reverse-ETL sync, Part 5), and Chapter 58 (the PO-intake pipeline, Part 6). You don't need to reread any of them — each is reintroduced with the one fact this chapter needs from it.
>
> **Time needed:** 13–15 hours, spread over a week and a half.
>
> **Tools:** nothing new — this chapter organizes and governs automations already built with the tools earlier chapters taught.
>
> **Practice data:** `companion/ch63/`: the full Riverstone automation inventory (24 automations, scored for value, risk, and effort), a center-of-excellence charter template, and a runbook template.

---

## Why this matters

By this point in the book, Riverstone has a lot of automation: a handful of VBA macros holding branch reporting together, a daily email that replaced a manager's morning routine, an orchestrated data pipeline moving real volume, a model reading purchase-order emails, a sync keeping the CRM current. Each one, in its own chapter, was the right answer to the problem in front of it.

Look at all of them together, for the first time, and a different picture appears — the one Chapter 60 first surfaced when Meera drew the whole platform as a diagram and found it "genuinely alarming." Some of these automations have an owner who can explain them in one sentence. Some don't. Some were built once and never touched again. At least one, per Chapter 19's own story, had run for nine years, with no owner since its author left in 2020, before anyone checked it. Multiply Riverstone's six well-documented automations by every branch's own macro, every analyst's personal script, every one-off Apps Script project built to solve a Tuesday-afternoon problem and never revisited — and the real number of things quietly running the business is far larger than any diagram anyone has drawn.

**This chapter is about that larger number.** Not building new automations — Parts 2, 5, and 6 already taught that — but governing the ones that exist: knowing they exist, knowing who owns them, knowing what happens when they break, and having a disciplined way to decide what gets built next and what gets shut down. It's the difference between a company that has automated some things and a company that has an automation *capability* — one that scales, survives people leaving, and doesn't quietly cost more than it saves.

---

## In plain English

Imagine a house where, over ten years, every resident who ever lived there wired in their own convenience: a timer for the porch light, a smart plug for the kettle, a motion sensor in the hallway, a second thermostat someone installed and forgot to register with the first. Each one, on the day it was installed, solved a real problem.

Nobody who lives there now has a full list of what's wired into the walls. Some of it still works perfectly. Some of it fights with something else — the two thermostats arguing over the same room. Some of it is a fire risk nobody's checked in years. And when the power flickers at 2 a.m., the person awake has no idea which of the fifteen anonymous little boxes behind the walls is actually responsible.

**Automation architecture and governance is the electrician's audit of that house** — not ripping everything out and rewiring from scratch, but finding out what's actually there, who's responsible for each thing, which wiring standard new work has to follow, and which of the old boxes are safe to leave alone versus which need to come out before they start a fire. A company that automates without ever doing this audit ends up with exactly the same problem, at a scale that makes it much more expensive to discover during an actual outage than during a calm Tuesday review.

---

## 63.1 One architecture, not a pile of scripts

The starting failure this chapter addresses isn't any single bad automation — it's the *accumulation* of good, reasonable, individually-justified automations into something nobody designed as a whole. By the time Meera draws Chapter 60's diagram, Riverstone's real inventory already spans:

- **Chapter 19's branch consolidation macro** and its Apps Script sibling, the enquiries digest — spreadsheet-bound, built by an analyst, living inside one workbook.
- **Chapter 20's Daily Sales Flash** — a scheduled Python script with its own logging and its own failure alert.
- **Chapter 46's Dagster pipeline** (Part 5) — a properly orchestrated system with dependencies, retries, and a real run history.
- **Chapter 51's CRM reverse-ETL sync** (Part 5) — a scheduled write-back with its own idempotency and reconciliation logic.
- **Chapter 58's PO-intake pipeline** (Part 6) — an AI-assisted extraction system that drafts orders from emails and writes each one into the ERP once a person has confirmed it.

Each was designed well, in its own chapter, against its own requirements. **None of them was designed with the others in mind**, because at the time each was built, "the others" mostly didn't exist yet. That's not a criticism of any individual chapter's work — it's the normal, expected way automation accumulates in any real company, and it's exactly why a dedicated architectural pass, done deliberately rather than accidentally, matters.

**Treating this as one architecture rather than five unrelated projects means asking, for every automation:** what shape does it share with the others? Section 63.4's reference architecture answers that question directly — every one of the five above, and every macro built by every branch since, turns out to be a specialization of the same six-layer shape, just with some layers compressed, skipped, or done by hand.

---

## 63.2 Process discovery and prioritization

Before building anything new, an architect needs an honest answer to a harder question than "what should we automate next?" — namely, **"of everything that could be automated, what's actually worth it, and what's actually risky?"**

**Three factors, scored for every candidate** on a scale of 1 to 5, so that candidates can be compared:

- **Value** — time saved, errors prevented, revenue protected or enabled. Chapter 20's own habit (time before, time after, multiplied by frequency, section 20.14) is exactly this, done for one automation; this section does it across many, so they can be compared. Where a rupee figure exists, use it; where the value is accuracy, or other work the automation makes possible, say so rather than inventing a number. A 1 is a personal convenience; a 5 is something the whole company's numbers depend on.
- **Effort** — what it costs to build and, just as importantly, to *operate* afterward. A script that takes a day to write and needs no ongoing attention is cheap; a pipeline that takes a week to write and needs a person watching it every day is not, regardless of the build cost alone. A 1 takes days; a 3, weeks; a 5, months.
- **Risk** — what happens when it's wrong, not just when it's down. This is the factor most process-discovery exercises skip, and it's the one that changes the answer most dramatically. A 1 means a wrong result is stopped by the automation's own checks before anyone uses it; a 3, that a wrong result reaches people or another system but is caught within a day or two; a 5, that wrong results reach customers or money and nobody sees them.

Here are six of Riverstone's automations, scored. The first five come from the inventory file in `companion/ch63/`, `automation-inventory.csv`. Straight-through PO intake was never switched on, so it isn't in the inventory; its scores are the ones Chapter 58's pilot would have earned. Its value is 5 because, on paper, it saves the most labour of anything on the list.

| Automation | Value | Effort | Risk |
|---|---:|---:|---:|
| Daily Sales Flash (Ch 20) | 4 | 1 | 1 |
| Branch consolidation macro (Ch 19) | 3 | 1 | 1 |
| PO intake, assisted (Ch 58) | 4 | 3 | 3 |
| PO intake, straight through (Ch 58, rejected) | 5 | 3 | 5 |
| Dagster ingestion pipeline (Ch 46) | 5 | 5 | 3 |
| CRM reverse-ETL syncs (Ch 51) | 3 | 3 | 3 |

![A value-against-effort chart on 1-to-5 scales with risk shown as bubble size and as a number in each bubble. Daily Sales Flash (value 4, effort 1, risk 1) and the branch macro (value 3, effort 1, risk 1) sit at the left as quick wins. PO intake in assisted mode (value 4, effort 3, risk 3) and the CRM reverse-ETL syncs (value 3, effort 3, risk 3) sit in the middle. PO intake straight through sits at the top middle (value 5, effort 3) as the largest bubble, risk 5, with a dashed outline. The Dagster pipeline (value 5, effort 5, risk 3) sits at the top right as a big bet.](figures/fig63-1-prioritization.svg)

*Figure 63.1 — Ranked on value and effort alone, straight-through PO intake sits at the top of the chart: the most value on paper, for moderate effort. Its risk score, from Chapter 58's real 19% silent-error finding, is what ruled it out.*

### The worked ROI comparison, with real numbers

The value column below is in rupees a year wherever a rupee figure exists: 250 working days, the same year Chapter 20 used, at Riverstone's loaded cost of ₹300 an hour (Chapter 20, section 20.14; Chapter 58 uses the same rate). The PO-intake rows use Chapter 58's prices for one day of 40 emails (section 58.7): typing them all costs ₹600 of a coordinator's time; assisted mode costs ₹197 of review and queue time, and straight through ₹47 of queue time, before anything is counted for the wrong orders each one lets through.

| Automation | Value in ₹ a year | Effort to build | Risk if wrong |
|---|---|---|---|
| Daily Sales Flash (Ch 20) | ₹97,500: 325 hours saved × ₹300 (Ch 20, section 20.14) | Low (days) | Low: its four checks stop a wrong number before it's sent |
| Branch consolidation macro (Ch 19) | About ₹77 of time: 4 min → 9 s, four runs a year, about 15 minutes. The real value is accuracy: its checks stopped a ₹1.88 crore double count and a silent cut-off at row 5,000 (Ch 19) | Low (days) | Low: the `source_file` column and three checks stop a bad consolidation |
| PO intake, assisted (Ch 58) | +₹1,00,750 in labour ((₹600 − ₹197) × 250); −₹2,32,500 once the wrong orders a reviewer misses are counted, at an assumed 90% catch rate ((₹600 − ₹1,530) × 250) | Medium (weeks) | Medium: a reviewer who misses a wrong draft lets it through, about 0.67 orders a day at a 90% catch rate |
| PO intake, straight through (Ch 58, rejected) | −₹31,95,000: only ₹47 a day of labour, but ₹13,333 a day of wrong orders ((₹600 − ₹13,380) × 250) | Medium (weeks) | High: 19% of unattended orders silently wrong, about ₹2,000 each, found only after the fact |
| Dagster ingestion pipeline (Ch 46) | Not priced: every report downstream depends on it | High (months) | Medium: well tested, but a platform-wide dependency |
| CRM reverse-ETL syncs (Ch 51) | Not priced: keeps sales data in the CRM current without anyone re-typing it | Medium (weeks) | Medium: lag is harmless (Ch 61), but a wrong write overwrites what a person typed (Ch 51's story); controlled by `PATCH`, one system of record per field, and reconciliation |

**Expected value: putting risk into rupees.** Chapter 21 (section 21.5) defined the **expected value** of something uncertain as its long-run average. For an automation, the daily version is:

> expected value a day = labour saved − wrong orders a day × cost of a wrong order

Work it for straight through first. In Chapter 58's 60 test emails, 53 loaded without a person and 10 of those were wrong: 10 wrong orders for every 60 emails. At 40 emails a day, that's 40 × 10 ÷ 60 = 6.67 wrong orders a day, and at ₹2,000 each, ₹13,333. (A quick 40 × 19% × ₹2,000 gives ₹15,200, which is too high: the 19% applies only to the 88% of emails that load without a person.) Labour saved is ₹600 − ₹47 = ₹553. So:

- **Straight through:** ₹553 − ₹13,333 = **−₹12,780 a day.**
- **Assisted, if the reviewer catches 90% of wrong drafts:** 6.67 × 10% = 0.67 missed a day, ₹1,333. Labour saved is ₹600 − ₹197 = ₹403. So ₹403 − ₹1,333 = **−₹930 a day.** At a 99% catch rate the same sum gives +₹270; it breaks even at about 97%, which is Chapter 58's result.

**The finding the table makes obvious, that a value-and-effort-only view would miss entirely:** PO intake's straight-through mode has *better* labour economics than its assisted alternative — ₹47 a day against ₹197 — and that's precisely why the pilot was tempting. Its risk column is what actually decided the question, and Chapter 58's own conclusion (assisted, not straight-through) is this exact prioritization framework, run for real, landing on the answer its raw labour number argued against. **The assisted row carries a second lesson:** its value depends on a number nobody has measured yet, the reviewer's catch rate, which is why Chapter 58 starts it in shadow mode, to measure that number before relying on it. An honest ROI table says which of its numbers are measurements and which are assumptions.

**A simple, usable prioritization rule:** score every candidate on all three factors, plot value against effort (Figure 63.1), and **let the risk bubble's size override a merely-attractive position on the other two axes.** A small, low-risk win (the branch macro) deserves building before a large, high-risk one (straight-through intake) — not because it's more valuable in isolation, but because the *expected* value, once risk is priced in honestly, is genuinely higher: the macro can't lose money, and straight through loses about ₹12,780 a day.

---

## 63.3 Choosing the right tool for the job

Every automation in this book used one of eight tool categories, and Riverstone has a real example of six of them — which makes the decision matrix concrete rather than a list of vendor names.

| Tool category | Best for | Riverstone's real example | Cost when misused |
|---|---|---|---|
| **Spreadsheet macro / script** | One workbook, one owner, low volume | Chapter 19's branch consolidation macro | Becomes Chapter 19's nine-year-old unowned single point of failure |
| **Scheduled script** | Regular, self-contained jobs with clear inputs and outputs | Chapter 20's Daily Sales Flash | No orchestration, dependency tracking, or shared monitoring at scale |
| **BI subscription / alert** | Delivering an existing report or dashboard on a schedule | Chapter 16's Power BI subscriptions (section 16.9) | Can't transform data — only delivers what already exists |
| **Low-code / integration flow** | Connecting SaaS tools, business-owned, no dedicated engineer | The CRM-to-WhatsApp Power Automate flow the audit found (section 63.8); the tools are Chapter 20's (section 20.10) | A forty-step flow with no version control, effectively unmaintainable |
| **Orchestrated pipeline** | Multi-step, dependency-aware, production data workloads | Chapter 46's Dagster ingestion (Part 5) | Overkill — and a real operational burden — for a single weekly report |
| **Integration platform (iPaaS)** | Many system-to-system syncs, vendor-supported | *Not used at Riverstone*: Chapter 51's hand-built sync is what an iPaaS would replace at higher volume | Licensing cost that dwarfs a simpler script for low volume |
| **RPA (robotic process automation)** | A system with no API and no export, only a screen | *Not yet used at Riverstone* — the gap below | Fragile: breaks on every UI change, expensive to maintain |
| **AI agent / LLM pipeline** | Unstructured input (email, documents), judgment-shaped tasks | Chapter 58's PO-intake extraction, Chapter 55's RAG assistant | Confident, wrong answers if not paired with human confirmation and refusal logic |

**iPaaS** (integration platform as a service, Chapter 51, section 51.8) is a hosted hub with ready-made connectors, retries, and monitoring, which you rent rather than build: MuleSoft or Boomi at the enterprise end, Zapier or n8n at the light end (Chapter 51, section 51.9).

**Two honest gaps in Riverstone's toolkit are RPA and iPaaS.** Riverstone doesn't need an iPaaS yet: it has a handful of systems, and hand-built syncs that the platform team can maintain (Chapter 51 called this hub-and-spoke, with the warehouse as the hub). Naming where RPA *would* fit is more useful than pretending it's irrelevant. Riverstone's two transporters (the two Chapter 22 compared) show delivery status only on their own websites: a login page, one consignment at a time, with no API and no export. Today someone in operations checks late consignments by hand, because there are few enough of them. The moment that volume grows, RPA becomes the right tool, rather than trying to force the problem into a script that has nothing to call — and knowing that in advance is what a decision matrix is for. Chapter 58 introduced RPA as a bridge, not a destination (section 58.1), so an RPA bot here would come with an expiry date: the day either transporter offers an API or a daily file.

**The choice, in practice, comes down to three questions, asked in order:**

1. **Does the source system have an API, or at least a file export?** If not, and screen automation is the only option, that's RPA's specific niche — not a reason to avoid automating, but a reason to pick the tool built for exactly that constraint.
2. **Is the logic mostly structured transformation, or does it require judgment on unstructured input?** Structured favors a script or pipeline; judgment on emails, documents, or images favors an AI-agent pattern, paired with human confirmation exactly as Chapter 58 settled on.
3. **Who owns it, and what's their skill set?** A flow a business team can maintain themselves (low-code) beats a beautifully engineered pipeline nobody on that team can touch — Chapter 60's fit-over-fashion principle, applied to tooling rather than architecture.

---

## 63.4 A reference architecture for automation

Every automation examined so far, however different they look, turns out to share one underlying shape: data comes from somewhere, gets moved and cleaned, gets organized around business meaning, gets delivered or acted on, and someone finds out whether it worked.

![Six numbered layers in two rows of three, joined by arrows: sources, ingestion, warehouse, then semantic layer, delivery and activation, and monitoring. Each box says what does that job on Riverstone's platform, with chapter numbers, and what does it inside a macro: the branch files it opens, Workbooks.Open, the Master sheet it rebuilds, the one formula its author chose for revenue, the PDF it emails, and its checks since Chapter 19. A note underneath says a single macro does all six jobs inside one workbook, while Chapter 46's pipeline does each in its own named piece.](figures/fig63-2-reference-architecture.svg)

*Figure 63.2 — Every automation in this book is a specialization of this one shape. Recognizing the layer something sits in is the first step to governing it properly.*

- **Sources:** the ERP, the CRM, plant sensors, inbound email, a spreadsheet someone maintains by hand.
- **Ingestion:** getting data out of a source and into somewhere it can be worked with — Chapter 46's Dagster jobs, or a macro's `Workbooks.Open` call doing the same job at a smaller scale.
- **Warehouse:** where it lands and is organized for reuse — the raw, staging, and mart tables Chapter 45's pipeline builds, plus Chapter 49's Delta Lake sensor archive, or, for a macro, the `Master` worksheet it builds each run.
- **Semantic layer:** one agreed meaning per metric — Chapter 32's semantic layer (section 32.13), built on the metric definitions of Chapter 23, or, for a small automation, simply the one formula the macro's author decided "revenue" means.
- **Delivery and activation:** where the result actually reaches someone or does something — the Flash email, a dashboard, the CRM write, the ERP order.
- **Monitoring:** how anyone finds out whether it worked — Chapter 20's checks and failure alerts, or, for an ungoverned macro, nothing at all, which is precisely the gap section 63.8 addresses.

**Why naming the layers matters more than it first appears:** a macro that compresses all six layers into one Excel workbook isn't doing something fundamentally different from Chapter 46's full pipeline — it's doing the same six jobs, just informally, invisibly, and without any of the shared services (section 63.6) a properly governed automation gets for free. Recognizing "this macro is quietly doing ingestion, warehousing, and delivery all in one VBA module" is the first step toward deciding whether that's still the right shape for it, or whether it's outgrown the workbook it lives in.

---

## 63.5 Scheduled versus event-driven design

Two fundamentally different rhythms govern when an automation runs. The reasoning has the same shape as Chapter 61's PACELC — you pay for freshness — but here the price is complexity, not consistency.

**Scheduled** automations run at a fixed time — Chapter 46's pipeline at 06:30 every morning, with the Flash in inboxes by 07:30 (Chapter 20). They're simple to reason about, easy to debug (the run either happened at the expected time or it didn't), and they accept a bounded staleness: whatever happened between runs isn't reflected until the next one fires.

**Polling** is a scheduled design that can look event-driven: the automation checks the source on a timer ("any new emails?") and works on whatever it finds (Chapter 51, section 51.6). Chapter 58's PO-intake pipeline polls: its 06:00 weekday run reads the emails that arrived since the last run (Chapter 60, section 60.5). With a short timer, polling feels almost instant; it's still a schedule.

**Event-driven** automations run because the source tells them something happened — a webhook firing the moment a CRM record changes (Chapter 51, section 51.6), or the defect model answering each camera image as it arrives (Chapter 56). They're more responsive, and they're genuinely more complex to build correctly: they need to handle bursts (many events at once), gaps (an event that never arrives), and duplicates (the same event delivered twice) — exactly what Chapter 51's webhook receiver had to cope with (respond fast, de-duplicate, keep a scheduled reconciliation sync as a backstop), and what Chapter 61's reliability toolkit exists for.

**The choice is a trade of freshness against complexity:**

| Choose scheduled when… | Choose event-driven when… |
|---|---|
| A daily or weekly cadence genuinely matches how the business uses the result | Being minutes late has a real, specific cost (a line alert, a time-sensitive order) |
| Batching many records together is more efficient than handling them one at a time | Each event is naturally independent and small |
| The team's operational maturity favors the simpler failure mode | The team has (or is building) the infrastructure to handle bursts, gaps, and duplicates safely |

Riverstone's own platform uses both deliberately: the Flash is scheduled because a sales manager checking revenue once a day is a completely adequate cadence; the defect model is event-driven because its answer is only useful while the part is still in front of the camera. PO intake sits in between: it could have been event-driven, but a coordinator confirming the morning's orders in one sitting is the rhythm the business actually works to, so it polls once each weekday morning. **Defaulting to event-driven everywhere because it sounds more sophisticated is a real, common mistake** — most business reporting genuinely doesn't need sub-second freshness, and the added complexity of an event-driven design, paid for that occasion, buys nothing anyone asked for.

---

## 63.6 Shared services

Every automation needs to send a notification, keep a credential somewhere, log what it did, and alert someone when it fails. Building these four things once, well, and sharing them across every automation is one of the highest-leverage investments an automation platform can make.

![A hub-and-spoke diagram. In the middle, a box labelled Every automation lists the Daily Sales Flash, the Dagster pipeline, the CRM syncs, PO intake, the support assistant, the defect model, the branch macros, and all 24 in the inventory. Four boxes around it, each with an arrow running level into the middle box's edge: notification service (one function sends email or chat for everyone), credential vault (no password in any script; rotate without editing code), run logs (every run's start, end, outcome and key numbers in one place), and alerting (a failure pages the owner the same way every time). A note says Chapter 20 built the minimum version of each for one script: its own mail code, environment variables in a .env file instead of a vault, a log file, and a failure email.](figures/fig63-3-shared-services.svg)

*Figure 63.3 — Build these four once. Chapter 20 built the minimum version of each for one script: environment variables instead of a vault, a log file, a failure email. This section makes them shared, platform-wide.*

- **Notification service:** one place that knows how to send an email, a Slack message, an SMS — so every automation calls the same function, instead of each one embedding its own mail settings, all of which break the same way when the mail server's settings change.
- **Credential vault:** no automation stores a password, API key, or connection string in its own code. Chapter 20's environment-variable discipline is the minimum version of this; a real vault (a managed secrets service) is the version that scales past a handful of scripts and lets credentials be rotated without editing code anywhere.
- **Run logs:** every automation's every run — start time, end time, outcome, key numbers — written to one place, not scattered across a different log file, in a different format, for every automation. This is what makes section 63.8's audit possible at all: you cannot inventory what never left a trace.
- **Alerting:** one shared mechanism for "something needs a human," so failures page the right person consistently, rather than each automation inventing its own notion of who to tell and how urgently.

**The payoff compounds with every automation added.** The fifth automation built on top of these four shared services costs a fraction of what the first one cost to build safely, because logging, alerting, and credential handling are already solved problems by then — exactly the leverage a platform is supposed to provide, and exactly what a pile of independent scripts never gets.

---

## 63.7 Ownership, runbooks, and support

An automation without a named owner is not really automated — it's a piece of infrastructure the company depends on that nobody is accountable for, which is precisely Chapter 19's `MASTER_FINAL_v7_USE_THIS.xlsm` and precisely the situation section 63.8's audit exists to find and fix.

**Ownership means one person (or one team) can answer, without research, three questions:** what does this do, why does it do it that way, and what happens if it breaks? Chapter 20's one-page handover note (section 20.13) is the minimum viable version of this, and it scales: the same seven headings — what it does, when it runs, inputs, outputs, checks, failure playbook, owner and deputy — work whether the automation is a five-line script or a company-wide pipeline.

**You met runbooks in Chapter 46** (section 46.10), where every known failure had one and every alert linked to it. Here's how they fit with Chapter 20's handover note: **a runbook** goes one step further than the note's failure playbook. It's the specific, step-by-step instructions for the three or four most likely failures, written so that someone who is *not* the original builder can follow them at 2 a.m. without improvising. "Refresh failed: the ERP load ran late. Rerun after 07:30 with `python daily_flash.py <date> --send`" (Chapter 20's own example) is a runbook entry in miniature — concrete, copy-pasteable, and written before the failure happens, not reconstructed from memory during it.

**Support doesn't end at handover.** Every automation needs, at minimum: a named deputy who has actually run it once (not just read about it), a review date on the handover note so it doesn't silently go stale, and an honest answer to "what happens if the owner is unreachable and it fails right now?" An automation that fails that last question isn't ready to be relied on, however well it was built.

---

## 63.8 Controlling sprawl and shadow IT

**Shadow IT** is any automation running the business that the people responsible for the company's systems don't know exists. It isn't the work of careless people — Chapter 19's story is the honest, sympathetic version: an analyst, years ago, solved a real Tuesday-afternoon problem with a macro, it worked, it kept working, and by the time anyone thought to ask "who owns this and does it still work correctly," the person who wrote it had left the company.

**The first step is not a policy — it's an inventory.** You cannot govern what you haven't found.

![A table of what Riverstone's first automation audit found, 24 automations in five categories, each with a count, an action in words, and examples. Documented, owned, monitored: 6, keep, the model to copy (the Flash, the Dagster pipeline, the CRM syncs, the support assistant, the defect model, PO intake). Working but no owner on record: 11, urgent, name an owner. Duplicated logic, disagreeing outputs: 4, merge each pair (Delhi and Kolkata consolidation macros; Bengaluru and Mumbai HO stock-report reformatters). Business-critical single point of failure: 1, confirm the fix held (MASTER_FINAL_v7 from Chapter 19, rewritten and owned since then). Actively broken, nobody had noticed: 2, fix now. A total row says 24, and that 17 had no owner, no monitoring and no written failure plan.](figures/fig63-4-audit-findings.svg)

*Figure 63.4 — Twenty-four automations found, once someone actually looked for them. Seventeen of them had no owner, no monitoring, and no written failure plan.*

**Running an inventory, in practice:** ask every team what spreadsheet, script, or flow they rely on, weekly or at month- or quarter-end. Check every branch's shared drive for `.xlsm` files. Check the company's low-code tools (Power Automate flows, Apps Script projects) for anything created more than a year ago. Check for scheduled tasks and cron entries on any machine the data team can access. None of this is exotic detective work — it's simply the first time anyone has asked the question company-wide rather than team-by-team.

**What Riverstone's own first audit found**, and what each category demands:

- **Documented, owned, monitored (6):** the automations this book has already governed properly — leave them alone, they're the model to replicate.
- **Working, but no owner on record (11):** the largest category, and the most urgent — not because they're broken, but because nobody would notice if they became broken. Each needs an owner assigned this quarter, using the handover-note template from section 63.7.
- **Duplicated logic, disagreeing outputs (4):** two pairs of duplicates. Delhi and Kolkata had each built their own version of Chapter 19's consolidation macro, and Bengaluru and Mumbai HO had each built a macro to reformat the Bhiwandi warehouse's weekly stock report. Each pair had different bugs, producing different numbers for what should be the same calculation — precisely Chapter 62's "two domains, two definitions" failure mode (section 62.5), discovered here in spreadsheet form rather than warehouse form.
- **Business-critical, single point of failure (1):** Chapter 19's macro itself, which by the time of this audit had already been through its own rewrite and had an owner — the audit's job here is confirming the fix held, not repeating it. It stays in this category because the quarterly branch report still depends on one workbook, and no deputy has run it yet.
- **Actively broken, nobody had noticed (2):** the most sobering finding. A stale Apps Script trigger had silently stopped firing five months before anyone checked, and a macro was still saving its weekly list to a shared folder that IT had moved, where nobody looked. Nothing downstream had noticed either absence — which says as much about the downstream consumers' own lack of freshness monitoring (Chapter 47) as it does about the broken automations themselves.

**Standards, established once the inventory exists:** every new automation gets a named owner before it goes live, not after; every new automation uses the shared services from section 63.6 rather than reinventing them; every automation above a stated risk threshold (section 63.2's scoring) goes through the controls in section 63.9 before deployment.

**A center of excellence** is the ongoing home for these standards — not a gatekeeper that approves every macro anyone wants to write, but a small group (often just the platform team, formalized) that maintains the inventory, publishes the standards, offers the shared services as something easy to adopt rather than a mandate to fight, and runs this audit again on a schedule rather than once and never again. The center of excellence succeeds when building the *right* way is the *easy* way — when a new analyst reaches for the shared logging function because it's less work than writing their own, not because a policy document told them to.

---

## 63.9 Controls: approvals, segregation of duties, audit trails, change management

Not every automation needs every control in this section — a personal script that reformats a spreadsheet needs none of them. **An automation that moves money, changes a customer record, or makes a decision on someone's behalf needs all of them**, and the judgment of which category something falls into is itself part of the architect's job.

- **Approvals:** a defined threshold above which an automation needs a human sign-off before it acts. Chapter 58's PO-intake pipeline uses exactly this: a named person confirms every order before it's written to the ERP, and any order above Riverstone's ₹1,00,000 limit also needs finance's approval, however confident the model is.
- **Segregation of duties:** the person who builds an automation shouldn't be the only person who can approve its changes going live, particularly for anything touching money or customer data. This isn't distrust of the builder — it's the same principle behind a second pair of eyes on any consequential decision, and it's what catches a mistake the builder is too close to their own work to see.
- **Audit trails:** a record of what an automation did, when, and — for anything that writes to another system — on whose authority. Chapter 51's idempotency keys serve double duty here: they prevent duplicate writes *and* provide exactly the trail an auditor would ask for.
- **Change management:** a real process, however lightweight, before a production automation's logic changes — at minimum, someone other than the author looking at the change, and a way to roll it back if it goes wrong. Chapter 60's ADRs are change management for architectural decisions; a code review is the equivalent for an automation's day-to-day logic.

**The right amount of control scales with the risk, not with the size of the automation.** A five-line script that writes financial transactions needs real controls despite its size; a thousand-line report generator that only reads data and emails a PDF needs almost none, despite its length. Applying uniform, heavy process to everything is how governance earns a reputation for slowing teams down for no benefit — and how people quietly route around it, recreating exactly the shadow IT problem section 63.8 exists to fix.

---

## 63.10 Retiring automations safely

Every automation eventually outlives its usefulness — the report it produces stops being read, the process it supports gets redesigned, a better system replaces it. **Retiring one safely is not simply deleting a file**, and skipping this step is how "nobody knows if it's safe to turn off" becomes a permanent reason never to turn anything off.

**A safe retirement checklist:**

1. **Confirm nothing downstream depends on it.** Check the run logs (section 63.6) for who's actually consuming the output, not who was originally meant to.
2. **Announce a sunset date**, publicly, with enough lead time for anyone quietly depending on it to speak up.
3. **Turn it off in stages where possible** — stop the schedule but leave the code and its last output in place for a defined period, rather than deleting everything the same day.
4. **Archive, don't delete**, the code and its documentation for a reasonable retention period — the next audit (section 63.8) should be able to find a retired automation's history, not just its absence.
5. **Update the inventory** the same day, so the center of excellence's record of what's running stays accurate.

The alternative — automations that nobody dares to turn off because nobody's sure what depends on them — is its own form of sprawl, arguably a more expensive one than an unowned macro, because it actively consumes maintenance effort for a benefit nobody can name. **A platform that can retire things safely is what makes it safe to build new things aggressively**: teams experiment more freely when they trust that yesterday's experiment can be cleanly removed if it doesn't pan out.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Building automations with no shared shape in mind | Two dozen scripts, each reinventing logging, alerting, and credential handling | Recognize the six-layer reference architecture in every new automation |
| Prioritizing by value and effort alone | A risky automation looks like the best investment on paper | Score risk honestly, and let a large risk bubble override an attractive position on the other two axes |
| Choosing a tool by familiarity rather than fit | An orchestrated pipeline built for a single weekly report; a fragile RPA script forced onto a system with a perfectly good API | Work through the decision matrix's three questions before picking a tool |
| Defaulting to event-driven because it sounds more sophisticated | Real complexity paid for a freshness requirement nobody asked for | Default to scheduled; justify event-driven with a specific, named cost of delay |
| No shared services | Every automation stores its own credentials, logs its own way, alerts nobody | Build notification, vault, logging, and alerting once, and make them the easy default |
| No named owner | Nobody can explain what an automation does or what happens if it breaks | Ownership assigned before anything goes live, using a real handover note |
| A handover note nobody's tested | The deputy has read about the process but never run it | Have the deputy actually run it once before calling the handover complete |
| Governing only what's already known about | Shadow IT accumulates invisibly for years | Run a real, company-wide inventory — ask every team, check every drive |
| Uniform, heavy controls on everything | Low-risk automations slowed down for no benefit; people route around governance entirely | Scale controls to risk, not to an automation's size or visibility |
| Never retiring anything | Maintenance effort spent on automations nobody uses, "just in case" | A defined, staged retirement process, with the inventory updated the same day |
| Treating the center of excellence as a gatekeeper | Teams avoid it, and shadow IT returns | Make the governed way the easy way — shared services people want to use |
| Confusing a policy document with actual governance | Standards exist on paper; nothing in production actually follows them | An inventory that's checked, not just a document that's written |

---

## In the real world: the first automation audit

That April, three months into her role as Head of Data Platform (Chapter 60), Meera Iyer did something Riverstone had never formally done: she asked every team, in writing, one question — *"What spreadsheet, script, or automated flow does your work depend on, weekly or at month- or quarter-end?"*

She expected her own team's six systems and a handful of others. She got twenty-four.

Eleven of them were automations nobody on her team had ever heard of: a Kolkata macro that built the day's ERP upload spreadsheet, a personal Apps Script project one analyst had built to auto-file expense receipts, a Power Automate flow connecting the CRM to a WhatsApp group that three people depended on and nobody could name the original author of. Four were duplicates, in two pairs: Delhi and Kolkata had each, independently, built their own version of Chapter 19's consolidation macro, and Bengaluru and Mumbai HO had each built a macro to reformat the Bhiwandi warehouse's weekly stock report. Each pair had subtly different bugs, and neither branch knew the other's existed. Two were actively broken — most strikingly, an Apps Script trigger that had silently stopped firing five months earlier, discovered only because the audit asked "when did you last check that this actually ran?" and nobody could answer.

The genuinely uncomfortable finding wasn't any single broken thing. It was the shape of the whole list: **seventeen of the twenty-four automations Riverstone depended on had no owner, no monitoring, and no written failure plan.** The company's real automation footprint was three times the eight systems on Meera's own container diagram.

Her response wasn't to shut anything down. Every one of the twenty-four was, by definition, solving a real problem someone depended on — the alternative to a slightly risky automation is not "no automation," it's "back to the manual process that was slow enough to justify building the automation in the first place." Instead, over the following quarter:

1. **Every automation got a named owner**, using the section 63.7 handover template — including the ones nobody had built, where "owner" meant whoever currently depended on it most, formally accepting that responsibility going forward.
2. **The two pairs of duplicates were each consolidated into one**, owned by the platform team, replacing all four branch versions — Chapter 19's original rewrite, done a second time, at company scale.
3. **The two broken automations were fixed**, and — more importantly — both were migrated onto the shared monitoring service (section 63.6), so the *next* silent failure would page someone within hours, not go unnoticed for months.
4. **A standing inventory review was scheduled quarterly**, not as a one-time project but as an ongoing habit — the center of excellence's actual, ongoing job, rather than a document written once and never revisited.

At the third quarterly review, nine months after the first audit, the count had grown to twenty-nine automations — genuine growth, not sprawl, because every new one arrived with an owner and a handover note from day one, the direct result of the standards section 63.8 describes.

What made the difference:

- **She asked the question company-wide, not team-by-team**, which is the only way to find automation nobody thought to mention because it had quietly become invisible.
- **She treated every finding as a gap to close, not a mistake to punish** — which is why teams kept answering honestly in the next round, rather than learning to hide what they'd built.
- **She fixed the structural problem (no shared monitoring, no ownership standard), not just the two symptoms** she happened to find — the difference between governance and firefighting.
- **The audit became a habit, not a project** — the only way an inventory stays true is if someone keeps asking the question.

---

## Project: a design document for Riverstone's reporting and automation platform

**Goal:** bring the 24 automations in the inventory under one governed platform, and plan for the manual reports still waiting to be automated — a design document in Chapter 60's format, applied to automation specifically.

### Tools you'll need

- No new software this chapter — every tool named in section 63.3's decision matrix was introduced earlier in this book.
- **Companion files (`companion/ch63/`):**
  - `automation-inventory.csv`: the full 24-automation inventory behind Figure 63.4, with each automation's tool category, owner, audit category, value/effort/risk scores, and the layers it covers.
  - `center-of-excellence-charter.md`: a template for the standing group and its responsibilities, from section 63.8.
  - `runbook-template.md`: a blank runbook, expanding Chapter 20's handover note with the step-by-step failure playbook section 63.7 describes.

**Option A: your own workplace.** Run the section 63.8 inventory exercise for real: ask every team what they depend on, weekly or at month- or quarter-end, that isn't a known, owned system.

**Option B: Riverstone.** Use `companion/ch63/automation-inventory.csv` as your starting inventory.

**Steps**

1. **Score every automation in your inventory** for value, effort, and risk (section 63.2), and plot them the way Figure 63.1 does.
2. **Classify each one against the reference architecture** (section 63.4): which layers does it cover, and which does it skip or do informally?
3. **For the five highest-risk, lowest-governance automations**, propose the right tool (section 63.3) if it were rebuilt today, and say whether it should be rebuilt at all or simply given an owner and left alone.
4. **Design the shared services** (section 63.6) your platform needs, and identify which existing automations could adopt them with the least effort — the quick wins that prove the platform's value early.
5. **Write one real handover note and one real runbook** (section 63.7) for your single most business-critical, least-documented automation.
6. **Propose the controls** (section 63.9) appropriate to your three highest-risk automations specifically — not a blanket policy for everything.
7. **Write the center-of-excellence charter** (section 63.8): who's in it, what it owns, how often the inventory gets re-run.
8. **State what gets retired**, if anything, using section 63.10's checklist, and what specifically would need to be true before it's safe to do so.

**What good looks like:** the inventory has at least one honestly uncomfortable finding (an unowned, business-critical automation, or a duplicated one); the risk scoring changes at least one prioritization decision from what value-and-effort alone would suggest; the handover note and runbook are specific enough that someone who didn't build the automation could actually use them.

**Stretch goals**

- Run the section 63.8 inventory question for real, on your own team or organization, and compare what you find against Riverstone's 24-automation result.
- Design the specific migration path for one shadow-IT automation into the governed platform, following Chapter 60's evolve-under-constraints pattern (migrate the lowest-risk piece first, run old and new in parallel).
- Calculate the total hours-saved-per-year across your full inventory, the way Chapter 20's section 20.14 did for one automation, and use it to make the business case for the platform investment this project proposes.

---

## Recap

- **Automation accumulates into an architecture whether anyone designs it that way or not** — Riverstone's real inventory spans macros, scheduled scripts, orchestrated pipelines, and AI-assisted systems, each built well individually and never designed together.
- **Prioritize by value, effort, and risk together** — Chapter 58's real PO-intake numbers show the option with the best labour saving (straight through) losing about ₹12,780 a day once its wrong orders are priced in, and an honest ROI table says which of its numbers (such as a reviewer's catch rate) are still assumptions.
- **Choose the tool from a real decision matrix**: macro, scheduled script, BI subscription, low-code flow, orchestrated pipeline, integration platform, RPA, or an AI agent — with a genuine Riverstone example wherever one exists, and two honest gaps (RPA and iPaaS, not yet needed).
- **Every automation is a specialization of one reference architecture**: sources, ingestion, warehouse, semantic layer, delivery and activation, monitoring — recognizing which layers an automation covers, and which it skips, is the first governance step.
- **Choose scheduled by default; justify event-driven with a specific cost of delay** — a trade of freshness against complexity, the same shape as Chapter 61's PACELC but a different price. Polling on a timer is still a schedule.
- **Shared services — notification, credential vault, run logs, alerting — built once, save every automation built afterward from reinventing them.**
- **Ownership, a handover note, and a tested runbook** are what separate an automation from a liability with no name attached.
- **Shadow IT is found, not assumed away**: a real, company-wide inventory at Riverstone found seventeen of twenty-four automations with no owner, no monitoring, and no written failure plan.
- **Controls scale with risk, not size**: approvals, segregation of duties, audit trails, and change management matter enormously for anything moving money or changing customer data, and barely at all for a read-only report.
- **Retirement is a process, not a deletion** — confirm nothing depends on it, announce a sunset, stage the shutdown, archive rather than delete, and update the inventory the same day.

---

## Key terms

automation architecture · process discovery · value/risk/effort prioritization · expected value · tool decision matrix · iPaaS (integration platform as a service) · RPA (robotic process automation) · reference architecture · sources / ingestion / warehouse / semantic layer / delivery and activation / monitoring · scheduled automation · polling · event-driven automation · shared services · notification service · credential vault · run log · alerting · ownership · handover note · runbook · shadow IT · automation inventory · center of excellence · approvals · segregation of duties · audit trail · change management · safe retirement

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can look at any automation and place it on the six-layer reference architecture, even if it compresses several layers into one.
- [ ] You score value, effort, and risk separately, and let a large risk finding override an otherwise-attractive prioritization.
- [ ] You choose a tool from the full decision matrix based on fit — API availability, structured versus judgment-based logic, who has to maintain it — not familiarity.
- [ ] You default to scheduled automation and can name the specific cost of delay that would justify event-driven instead.
- [ ] You build shared services once rather than letting every automation reinvent logging, alerting, and credential handling.
- [ ] Every automation you're responsible for has a named owner, a handover note, and a runbook for its most likely failures.
- [ ] You've run, or would know how to run, a real company-wide automation inventory — not just a review of what your own team built.
- [ ] You scale controls (approvals, segregation of duties, audit trails, change management) to risk, not to visibility or size.
- [ ] You can retire an automation safely, with a real checklist, rather than either never touching it again or deleting it blind.

---

## Exercises

### Warm-up

1. Name the six layers of the reference architecture, in order, and give a one-sentence example of each from your own experience (work or personal).
2. Why does risk deserve its own axis in prioritization, separate from value and effort? Give an example where ignoring it would produce the wrong decision.
3. What's the difference between a handover note and a runbook?
4. Name three of the eight tool categories from the decision matrix, and a situation where each is clearly the right choice.
5. Why is "we'll delete it if it turns out nobody needs it" not a safe way to retire an automation?

### Core

6. Using Chapter 58's real numbers (section 63.2), explain in your own words why straight-through PO-intake looked attractive on value and effort alone, and what specifically the risk score changed about the decision.
7. Classify Chapter 20's Daily Sales Flash against the six-layer reference architecture: which layers does it cover explicitly, and how?
8. A stakeholder asks for a new automation to sync data between two internal tools with good APIs, judged as high-risk because it touches customer records. Walk through the three tool-selection questions (section 63.3) and the controls (section 63.9) it would need.
9. Design the four shared services (section 63.6) for a team of your own: what would the notification service, credential vault, run logs, and alerting actually look like at your current scale?
10. Write a one-page handover note (Chapter 20's seven-heading template) for an automation you personally rely on, even an informal one.
11. Riverstone's audit found two pairs of duplicated macros. Using Chapter 62's data-contract reasoning (section 62.5), explain why "each branch owns its own macro" without a shared definition produced this exact failure.
12. An automation candidate scores high value, low effort, and low risk. Another scores high value, low effort, and high risk. Using Figure 63.1's method, explain how you'd sequence building them.

### Stretch

13. Design the full migration plan for consolidating Riverstone's two pairs of duplicated branch macros into one governed automation each, following Chapter 60's evolve-under-constraints pattern from section 60.6.
14. Propose Riverstone's RPA use case (reading delivery status from the transporters' websites, section 63.3) as a real project: what would trigger building it, and what would the decision matrix say about the tool choice once that trigger arrives?
15. Using the section 63.9 controls, design the approval and audit-trail requirements for a hypothetical automation that adjusts customer credit limits automatically based on payment history.

### Think about it

16. Is there a size of company below which formal automation governance (an inventory, a center of excellence, standing controls) is genuinely not worth the overhead? Where's that line, and what would move it?
17. A team resists adopting the shared services (section 63.6) because their own ad-hoc version "already works fine." How do you make the case for migrating, without simply mandating it?

---

## Answers

**1.** Sources (the ERP, a spreadsheet you maintain by hand); ingestion (a script that pulls data out of that source); warehouse (wherever it's organized for reuse — a database table, or just a cleaned-up worksheet); semantic layer (the one agreed meaning of a term you use, even informally); delivery and activation (an email, a chart, a written-back record); monitoring (how you'd find out if it stopped working — even if today the honest answer is "I'd notice eventually").

**2.** Value and effort together only tell you whether something is attractive to build; risk tells you what happens when it's wrong. Chapter 58's straight-through PO-intake example is exactly this: it scores well on value and effort, and ignoring risk would mean shipping something with a 19% silent error rate, each error costing roughly ₹2,000 to unwind — a mistake the value/effort view alone would never catch.

**3.** A handover note is the general orientation document — what an automation does, when it runs, its inputs and outputs, and who owns it. A runbook is narrower and more operational: specific, step-by-step instructions for the most likely failures, written so someone who isn't the original builder can follow them under pressure.

**4.** For example: a scheduled script for a self-contained daily report with no complex dependencies; an orchestrated pipeline for a multi-step production data workload with real dependency chains; RPA for a system with no API and no export, only a screen to automate against.

**5.** Because "nobody needs it" is often only true until the one time a year someone does — a month-end process, an annual report, an edge case that only occurs during a specific season. Deleting without confirming, announcing, and staging risks losing something whose only visible dependency shows up rarely, exactly when it would be most disruptive to discover the loss.

**6.** Straight-through PO-intake looked attractive because it removes the ~45 seconds of human review per order, cutting the day's labour from ₹600 (typing) to ₹47 (only the queue) — real value, for moderate effort once the extraction pipeline already exists. The risk score changed the decision by pricing in what value/effort ignored. Follow the chain: 40 emails a day × 88% loaded unattended = 35.3 orders; × 19% silently wrong = 6.67 wrong orders a day; × ₹2,000 = ₹13,333 a day. Plus ₹47 of labour, that's ₹13,380 a day, against ₹600 for typing: an expected loss of about ₹12,780 a day, far more than the labour it was meant to save. (Multiplying 40 × 19% × ₹2,000 skips the 88% step and overstates it at ₹15,200.)

**7.** Sources: the ERP's order data. Ingestion and warehouse: the SQL query pulling the day's and trend data directly (a lightweight version, not a full staged warehouse load). Semantic layer: the headline calculations (revenue, orders, AOV) computed consistently. Delivery and activation: the HTML email itself. Monitoring: the four checks that can stop the send, plus the failure alert — Chapter 20's Flash is unusually complete against this framework precisely because it was built with exactly these concerns in mind from the start.

**8.** Tool selection: (1) both tools have good APIs, so this favors an integration platform or a well-built scheduled script over RPA; (2) the logic is structured (moving records between two systems), favoring a script or integration platform over an AI-agent pattern; (3) who maintains it decides between a low-code flow (if the business team should own it) and an engineered pipeline (if the data platform team should). Controls: because it touches customer records, it needs an audit trail at minimum, and likely approval thresholds and segregation of duties given the risk classification stated in the request.

**9.** Personal exercise; check that all four services are addressed concretely (not "we'll figure it out") and sized to the team's actual current scale rather than an aspirational one.

**10.** Personal exercise; check the note follows the seven Chapter 20 headings and could genuinely be understood by someone who didn't build the automation.

**11.** Without a shared, agreed definition of what the consolidation macro should produce (Chapter 62's data contract, applied here to a spreadsheet rather than a warehouse table), each branch's analyst made their own reasonable, locally-consistent choices about how to build it — and those choices diverged, exactly as two domains publishing their own definition of "active_customer" diverged in Chapter 62's example. The same happened with the two stock-report reformatters. The fix is the same in every case: one agreed, shared, owned version, not two independently-maintained ones.

**12.** Build the high-value/low-effort/low-risk one first — it's a clear win on every axis with nothing to override the obvious call. Build the high-value/low-effort/high-risk one second, but only after either reducing the risk (a smaller pilot, added human confirmation) or explicitly accepting it with the right controls (section 63.9) in place — the same reasoning Chapter 58 applied when it chose assisted mode over straight-through rather than abandoning automation on that risky candidate entirely.

**13.** Following section 60.6, for each pair: (1) pick the lower-risk of the two existing macros as the baseline rather than starting from scratch; (2) run the consolidated version alongside both existing macros for one full reporting cycle, comparing outputs; (3) migrate one branch first, keeping the other branch's existing macro live as a fallback until the new one has proven itself; (4) write the ADR recording the decision, what was rejected (keeping both branch versions, building a third new one from scratch), and why; (5) retire both original macros only once the consolidated version has run cleanly through a full cycle. Do the lower-risk pair first (the stock-report reformatters), to learn the cost of the change before touching the consolidation macros.

**14.** The trigger would be the number of consignments to check crossing the point where looking them up by hand becomes a real bottleneck or a real source of missed late deliveries — not a fixed date, but an observed cost, the same kind of concrete trigger Chapter 62's mesh-readiness discussion used. Once that trigger arrives, the decision matrix's first question (does the source have an API, or a file export?) answers itself — no — which points directly at RPA as the right tool, rather than trying to force a script to call an API that doesn't exist. Following Chapter 58, the bot gets an expiry date: ask each transporter for an API or a daily status file, and retire the bot the day one arrives.

**15.** Approval: any credit-limit increase above a defined threshold routes to a person before taking effect, mirroring Chapter 58's ₹1,00,000 rule; smaller adjustments within a conservative band might auto-apply. Audit trail: every adjustment logged with the customer, the old and new limit, the payment-history data that drove the decision, and a timestamp — auditable both for a customer dispute and for confirming the automation itself is behaving as intended. Segregation of duties: the person who built the credit-scoring logic shouldn't be the sole approver of changes to its thresholds going forward.

**16.** There's no fixed headcount threshold — the right trigger is the same one Chapter 62 used for data mesh readiness: when the number of automations, or the cost of one going wrong, grows past what one or two people can hold in their heads without a formal inventory. A two-person team with three scripts genuinely doesn't need a center of excellence; the same two-person team with thirty scripts, several touching money, does — the governance investment should track the actual risk and scale, not a company's headcount alone.

**17.** Show, don't mandate: build the shared service well enough that adopting it is genuinely less work than maintaining their own version — easier logging, alerting that actually pages someone reliably, credential handling that survives a password rotation without editing code. Migrate one of their existing automations onto it as a demonstration, with their cooperation, rather than requiring migration of everything at once; a team that sees their own ad-hoc pain solved by the shared version adopts the rest voluntarily, which is a far more durable outcome than a mandate that gets quietly worked around.

---

## Where this leads

- **Chapters 19 and 20:** the specific automations this chapter governs, revisited from a company-wide rather than single-automation view.
- **Chapter 60, Designing Whole Systems:** the container diagram and shared-services band this chapter's reference architecture directly extends.
- **Chapter 61, Distributed Systems & Trade-offs:** the scheduled-versus-event-driven choice has the same shape as PACELC, trading freshness for complexity rather than consistency; the reliability toolkit underlies section 63.6's shared services.
- **Chapter 62, Data Architecture Patterns:** the duplicated-macro finding in this chapter's story is section 62.5's "no contract, no shared definition" failure mode, found in spreadsheets rather than warehouse tables.
- **Chapter 64, Security, Privacy, Governance & Responsible AI:** the controls in section 63.9 (approvals, audit trails) are this chapter's entry point into a much fuller governance and compliance treatment.
- **Interview preparation:** the Architecture & Leadership Question Bank (Chapter 80, Q80-023) asks directly about automation governance and shadow IT — "your team's biggest automation just failed silently for a week" is this chapter's method, asked as an interview question.
