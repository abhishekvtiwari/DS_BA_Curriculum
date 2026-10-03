# Chapter 80. Architecture & Leadership Question Bank

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will learn to:** reason about distributed-systems trade-offs the way a senior interview actually probes them · make and defend a build-vs-buy or architecture decision with real trade-offs stated, not a confident guess · answer governance, security, and cost questions at the level an architect owns them · handle leadership scenarios (influencing without authority, saying no, presenting to a board) live · walk through a full architecture design case end to end · run a blameless postmortem whose finding is the detection gap rather than the bug · ask for an RPO and an RTO as numbers before designing any disaster recovery · cut a live system over incrementally, with an automated output comparison doing the real work · and diagnose a bottlenecked platform team as a structure problem rather than a headcount one.
>
> **Before you start:** Part 7 (Chapters 60–67), which teaches almost every idea in this bank; Chapter 20, section 20.14 and Chapter 23, section 23.9 for the time-saving and payback arithmetic in Q80-016; Chapter 24, sections 24.7 and 24.8 for presenting to executives and handling pushback; and Chapter 69 for the three answer tiers and the twelve extra-point tags. This chapter tests those skills; it doesn't teach them again. When you can't answer a question, its **Learn it in** line sends you to the section that teaches it.
>
> **Time needed:** 3–4 hours to read and drill once (about 10 minutes per core question answered aloud, 1–2 minutes per rapid-fire row, and 15 minutes to run Q80-016's cells yourself), plus 2–3 hours for the project: an ADR, an ROI, a pushback, and a roadmap. Section 80.7 adds about an hour and is whiteboard arithmetic — do it with a pen, not by reading. Sections 80.8 to 80.10 add about 90 minutes and are the operational and people half of the role: running a live system, changing it without breaking it, and leading the architecture. Three terms in them come from the site-reliability tradition rather than from this book — RPO, RTO and the error budget — and each is marked **Beyond the book** with a one-line primer, as are feature flags in section 80.9.
>
> **A scope note.** This chapter is for senior IC and architect-level interviews specifically (an **IC**, individual contributor, is a senior engineer or scientist who leads work without managing people), distinct from the Data Analyst/Data Scientist/Data Engineer focus of most of this part. Readers targeting DA/DS/DE roles can treat this chapter as optional, forward-looking material for a later career stage.
>
> **How this chapter is built.** Same format as every question bank in Part 8. Every **core question** gives a memory hook ("Remember it as…"), a one-line answer you can recall under pressure, and a tier table: what **passes**, what's **strong**, and the **extra points** (Chapter 69's moves, tagged the same way: **[+Clarify]**, **[+Edge cases]**, **[+Validate]** and so on). Then come the likely follow-ups, the red flag, and where to learn it. Every **rapid-fire section** is a scan table: question, one-line answer, one extra point, level, and where to learn it (a bare number such as 61.4 means that section). Most of this chapter is judgment and trade-off reasoning rather than executable code; where a claim is computable (the ROI in Q80-016), it's actually run and shown with real numbers.
>
> **Levels and roles.** Each question carries a level and the roles that usually ask it. **Mid:** one to three years in the role. **Senior:** lead or specialist rounds. There are no Fresher questions: this bank is for a later stage of a career. **DE** senior data engineer · **DS** senior data scientist or ML engineer · **ARC** data or solutions architect · **LEAD** head of data, or an engineering or analytics manager. A question asked of DE or DS comes up in senior IC rounds; one asked only of ARC or LEAD belongs to architect and lead rounds.

---

## 80.1 Distributed systems trade-offs

### Q80-001 · Explain the CAP theorem, and give a real example of a system choosing each side of the trade-off

**Level:** Mid · **Roles:** DE, ARC

**Remember it as:** *You can't have all three of Consistency, Availability, and Partition tolerance at once during an actual network partition. Partition tolerance isn't optional in a real distributed system, so the real choice is between Consistency and Availability.*

**Answer in one line:** The CAP theorem states that during a network partition, a distributed system must choose between **Consistency** (every read sees the latest write, or an error) and **Availability** (every request gets a response, even if it might be stale); since partitions are a fact of real networked systems, not an edge case to design away, the practical choice most systems actually face is CP vs. AP.

| Tier | What to say |
|---|---|
| Passes | Recites the three letters without explaining that partition tolerance is effectively mandatory, not a genuine third option |
| Strong | Correctly frames the real trade-off as CP vs. AP, with one concrete example of each: a banking system favoring consistency (reject a transaction rather than risk showing a stale balance) versus a social media feed favoring availability (show slightly stale content rather than an error) |
| Extra points | **[+Business]** the right choice is a business decision tied to what's actually worse for that specific system: a stale bank balance is a real, serious problem; a slightly stale "like count" is not, and the architecture should reflect that difference deliberately, not by accident<br>**[+Edge cases]** even banks choose AP in places: an ATM that can't reach the bank may still allow a capped withdrawal and reconcile it later. The business sets a *limit* on the risk of acting on stale data rather than demanding CP everywhere |

**Likely follow-ups:** What's eventual consistency, and where does it fit relative to strict CP or AP? How would you explain this trade-off to a non-technical executive asking "why can't we just have both"?
**Red flag:** claiming a real system can be fully consistent, available, and partition-tolerant simultaneously, with no trade-off at all.
**Learn it in:** Chapter 61, section 61.2 (the CAP theorem, and Riverstone's CP order writes and AP dashboard reads).

### Rapid-fire, 80.1

Roles: DE and ARC for every row; LEAD for Q80-003.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q80-002 | What's eventual consistency? | A guarantee that, given no new writes, all replicas of a piece of data will *eventually* converge to the same value, without promising exactly when | **[+Business]** acceptable for use cases where a brief window of staleness is genuinely harmless (a view count), not for ones where it isn't (an account balance) | Mid · 61.4 (the consistency spectrum) |
| Q80-003 | What's a single point of failure, architecturally? | Any component whose failure alone brings down the whole system, with no redundancy or fallback | **[+Evidence]** name one you found: Chapter 61's container-by-container failure analysis found Riverstone's warehouse to be the platform's one true single point of failure | Mid · 61.7; drilled at pipeline level in Q77-021 |
| Q80-004 | What's the difference between horizontal and vertical scaling? | Vertical (scaling up): making one machine bigger (more CPU/RAM); horizontal (scaling out): adding more machines and distributing load across them | **[+Trade-offs]** vertical scaling is simpler but has a hard ceiling; horizontal scaling has no such ceiling but adds real distributed-systems complexity | Mid · 61.5 ("Scaling up and scaling out") |
| Q80-005 | What's a leader-follower (primary-replica) architecture, and what's its main trade-off? | One node accepts writes and propagates them to read-only replicas; simplifies write consistency but makes the leader a potential bottleneck and single point of failure unless failover is handled carefully, and reads from followers can be stale (replication lag: the eventual consistency of section 61.4) | **[+Edge cases]** automatic failover needs the surviving copies to agree on one new leader (consensus, leader election); two leaders both accepting writes is the failure to design against | Senior · 61.4; 61.5 (replication; "Who is in charge? Quorum and consensus"); 61.7 |

---

## 80.2 Basic-but-tricky architecture questions

### Q80-024 · The warehouse is backed up every night. Is it still a single point of failure?

**Level:** Mid · **Roles:** DE, ARC

**Remember it as:** *A backup protects the data. It doesn't keep the system running. Durability and availability are different promises.*

**Answer in one line:** Yes: a backup means the data survives a failure (**durability**), not that the service keeps answering (**availability**); while the one warehouse is down, and until a restore finishes, everything that reads from it stops, so it's still a single point of failure, and only a second copy that can take over removes that.

| Tier | What to say |
|---|---|
| Passes | "No, we have backups", or a bare "yes" with no reason |
| Strong | Separates durability (backups, versioned copies: the data survives) from availability (a second copy that can take over: the service survives), and says what stops while a restore runs |
| Extra points | **[+Evidence]** Chapter 61's failure analysis found exactly this at Riverstone: the warehouse is the platform's one true single point of failure, and in Chapter 52 a network fault, not lost data, was enough to stop the dashboard and the Flash<br>**[+Trade-offs]** a standby copy with automatic failover costs money and needs the copies to agree which one is in charge (consensus); for a small team, a restore that has actually been tested and timed may be the right first step. Say which you'd pick, and why<br>**[+Validate]** a backup nobody has ever restored is a hope, not a plan: restore it on a schedule and time how long it takes |

**Likely follow-ups:** How long would a restore take, and who decides whether that's acceptable? What would a second copy cost, and what new failure would it add?
**Red flag:** treating "we have backups" as the answer to an availability question.
**Learn it in:** Chapter 61, sections 61.5 (replication, for availability and durability; quorum and consensus) and 61.7 (the warehouse as the platform's one true single point of failure).

### Rapid-fire, 80.2

Roles: DE and ARC for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q80-025 | Is eventual consistency a bug? | No: it's a deliberate trade (faster, more available reads, in exchange for a window where copies disagree), but only if something actually makes the copies converge | **[+Edge cases]** "it'll converge eventually" is only true if a sync, a retry or a reconciliation check makes it happen; Riverstone's CRM syncs are reconciled after every run (Chapter 51, section 51.7) | Mid · 61.4 (and its "Watch out") |
| Q80-026 | What does PACELC add to CAP? Give an example with no partition. | Even with a healthy network, a system trades latency against consistency: waiting for the very latest write costs time on every request | **[+Evidence]** Riverstone's semantic layer is recomputed on a schedule, not on every write: it chooses low latency, and its numbers can lag the latest order | Senior · 61.3 |
| Q80-027 | Is partitioning the same as sharding? | No: partitioning splits one table into pieces by a key, still stored in one place and read by one engine; sharding puts those pieces on different servers, each storing and answering for only its share | **[+Evidence]** Riverstone's sensor archive is partitioned by month, not sharded; it would become sharding if Bhiwandi Main's and Chakan Pune's readings were served by two separate databases | Mid · 61.5 |
| Q80-029 | Does a second copy of a service always make it more available? | Not always: a copy that keeps no data of its own is easy to add, but some pieces must stay single, and copies of data bring back the consistency question | **[+Edge cases]** Riverstone's scheduler must stay one: two copies would each run the 6:30 schedule and send two Flashes | Senior · 61.5; 61.7 |

---

## 80.3 Data architecture decisions

### Q80-006 · A team wants to build a custom data quality framework in-house instead of buying an existing tool. How do you evaluate that decision?

**Level:** Senior · **Roles:** DE, ARC, LEAD

**Remember it as:** *Build gives you exactly what you need and full control, forever, including forever maintaining it. Buy gives you speed now and someone else's roadmap later.*

**Answer in one line:** Weigh the **total cost of ownership** (TCO: what it costs to get the thing, plus what it costs to run and maintain it for as long as you keep it) on both sides, not just initial cost: building in-house means ongoing engineering time to build *and* maintain it indefinitely, but total control and no vendor lock-in; buying means faster time-to-value and someone else's ongoing investment, at the cost of licensing fees, less customization, and dependency on the vendor's own roadmap and continued existence.

| Tier | What to say |
|---|---|
| Passes | A confident "build" or "buy" recommendation with no stated reasoning for why |
| Strong | The total-cost-of-ownership framing above, with both options scored on the same criteria: time to a working solution, fit, maintenance over the years you'll keep it, cost at current scale, and lock-in |
| Extra points | **[+Business]** the deciding factor is often whether the capability is genuinely core to the business's competitive differentiation (worth owning) or a solved, common problem plenty of vendors already do well (usually not worth reinventing); naming that distinction explicitly is a stronger answer than a generic cost comparison alone<br>**[+Evidence]** Riverstone made this call twice and landed on different sides: ADR-018 kept data quality as SQL tests inside the pipeline rather than buying an observability platform (yet), while Chapter 66's scorecard for a data catalog had buying win on four of five dimensions |

**Likely follow-ups:** How would you structure a pilot to test a vendor tool before fully committing? What's vendor lock-in, and how would you architect around minimizing it even when buying?
**Red flag:** comparing only sticker price without accounting for the ongoing maintenance burden of a build decision.
**Learn it in:** Chapter 66, section 66.5 (build versus buy: a managed data catalog, scored honestly); Chapter 60, section 60.5 (ADR-018).

### Rapid-fire, 80.3

Roles: DE and ARC for every row; LEAD for Q80-009 and Q80-010.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q80-007 | What's a lambda architecture, and what problem does it solve? | Runs both a batch layer (accurate, complete, slower) and a speed/streaming layer (fast, approximate) in parallel, merging their results in a serving layer, so a system gets both eventual accuracy and low-latency freshness | **[+Trade-offs]** the cost is real complexity: maintaining two separate processing paths that must produce reconcilable results | Senior · 62.2 (Lambda and Kappa on one scenario) |
| Q80-008 | What's a kappa architecture, and how does it simplify on lambda? | Treats everything as a stream, including reprocessing historical data by replaying the stream from the beginning, avoiding lambda's need to maintain two separate codebases for batch and speed layers | **[+Trade-offs]** simpler to maintain, but requires a streaming platform capable of efficient full replay; not every system's a good fit | Senior · 62.2 |
| Q80-028 | Is Kappa always simpler than Lambda? | Simpler code (one processing path instead of two), not simpler operations: Kappa needs a log that keeps months of history and can replay it quickly and reliably | **[+Trade-offs]** Riverstone runs the Lambda shape on purpose: its daily correction job is one more asset on the Dagster it already runs, while Kappa would need an always-on, replayable log for a four-person team | Senior · 62.2 |
| Q80-009 | What's an Architecture Decision Record (ADR), and why write one? | A short, versioned document capturing a specific architecture decision, the context that led to it, the options considered, and the reasoning, so a future engineer (including a future version of the same decision-maker) understands *why*, not just *what* | **[+Business]** without one, a "why did we do it this way" question six months later has no answer beyond someone's memory, which fades or leaves the company | Mid · 60.4; 67.3 ("Architecture decision records as institutional memory") |
| Q80-010 | What's a C4 diagram, and what problem does it solve that a single architecture diagram doesn't? | A layered set of diagrams (Context, Containers, Components, Code) at increasing levels of detail, letting different audiences see the appropriate level without one diagram trying to serve everyone at once | **[+Business]** an executive needs the Context level; an engineer joining the team needs Components or Code; one diagram trying to do both usually serves neither well | Mid · 60.2 |

---

## 80.4 Security, governance, and cost

### Q80-011 · How would you approach a "Responsible AI" review for a new model before it ships?

**Level:** Senior · **Roles:** DS, ARC, LEAD

**Remember it as:** *A responsible AI review isn't a single "is this ethical" checkbox. It's a structured check across specific, nameable risks: bias, privacy, explainability, and misuse.*

**Answer in one line:** Structure the review around specific, checkable dimensions: **fairness** (does it perform consistently across relevant segments, Chapter 39, section 39.9's fairness checks), **privacy** (does training or inference expose personal data inappropriately), **explainability** (can a decision be explained to someone affected by it), and **misuse potential** (could this capability be used for harm beyond its intended purpose), rather than one vague "is this responsible" judgment call.

| Tier | What to say |
|---|---|
| Passes | "You'd check if the model is fair and doesn't have bias" (true, incomplete, treats it as a single dimension) |
| Strong | The four-dimension structure above, with a concrete check named for at least two of them |
| Extra points | **[+Evidence]** Chapter 39, section 39.9's segment-level fairness checks are exactly the concrete mechanism behind the fairness dimension here, and Chapter 64's audit shows why the mechanism matters: the lead score put East 14 points below West without ever using region, because company size acted as a proxy, so the fix went into how the sales team uses the score, not into the model's code |

**Likely follow-ups:** Who should own sign-off on a responsible AI review, and why not just the model's own builder? How would you handle a model that passes every technical fairness check but still produces outcomes stakeholders are uncomfortable with?
**Red flag:** treating "responsible AI" as a single vague value judgment rather than a structured set of specific, checkable risks.
**Learn it in:** Chapter 39, section 39.9 (fairness checks); Chapter 64, sections 64.4 (privacy by design), 64.7 (a fairness audit, worked) and 64.8 (model governance and sign-off).

### Rapid-fire, 80.4

Roles: ARC and LEAD for every row; DE for Q80-013 and Q80-014.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q80-012 | What's data governance, at the level an architect owns it? | The policies, standards, and accountability structures defining who can access, modify, and be responsible for specific data, distinct from the technical implementation of any one system | **[+Signpost]** name its four working parts: a catalog, lineage, a named owner for every governed dataset, and policies that are actually enforced | Senior · 64.6 |
| Q80-013 | What's the principle of least privilege? | Grant only the minimum access genuinely needed for a role or system to do its job, nothing more, reducing the damage any single compromised credential or account can do | **[+Business]** this applies as much to a service account calling an internal API as to a human user's login | Mid · 64.2; 64.3 |
| Q80-014 | What's segregation of duties, in a data platform context? | No single person or system should have unchecked end-to-end control over a sensitive process (approving and executing the same financial transaction, say), reducing both fraud risk and the impact of an honest mistake | **[+Evidence]** Chapter 64's model card for the lead score leaves its approver line empty until someone other than the builder signs it: the person who built a model can't approve it for production | Senior · 63.9; 64.8 |
| Q80-015 | What does "showback" mean in cloud cost management, and how is it different from "chargeback"? | Showback reports each team's cloud cost to them for visibility, without actually billing their budget for it; chargeback actually bills the cost to that team's budget | **[+Business]** showback is often a gentler first step toward cost accountability before an organization is ready for full chargeback | Mid · 65.4 (budgets, tagging, and showback) |

### Q80-016 · Calculate the ROI of automating a specific manual task, and use it to justify (or reject) building it

**Level:** Senior · **Roles:** DE, ARC, LEAD

**Remember it as:** *A payback period in months, computed from real numbers, is a far stronger justification than "this will save the team a lot of time."*

**Answer in one line:** Estimate the annual value of time saved (hours saved per run × runs per year × a fully-loaded hourly cost), compare it against the one-time build cost, and compute the **payback period** (one-time cost ÷ monthly net saving: the months until the build has paid for itself); if it's short relative to the automation's expected useful life, it's justified, and if not, it isn't, regardless of how tedious the manual task feels.

**Run it yourself.** Take a weekly task that costs three hours of someone's time each run, and a quote of ₹60,000 to automate it. First, the yearly value of the time saved, at Riverstone's loaded staff cost:

```python
hours_saved_per_run = 3
runs_per_year = 52
hourly_cost = 300   # Riverstone's loaded staff cost per hour, the same as Chapter 20
annual_savings = hours_saved_per_run * runs_per_year * hourly_cost
print(f"Annual savings: ₹{annual_savings:,.0f}")
```

```
Annual savings: ₹46,800
```

**How it works:**

- `hours_saved_per_run`, `runs_per_year` and `hourly_cost` are the three drivers, one per line, so each can be questioned on its own. `hourly_cost = 300` is the loaded cost (salary plus overheads) that Chapter 20, section 20.14 used for the Flash; use your own company's figure in a real interview.
- `annual_savings` multiplies the three drivers: 3 × 52 × 300.
- `print(f"...")` prints it with `:,.0f`, which adds thousands separators and drops the decimals (Chapter 17's f-strings).

Now the payback. Before you run the next cell, predict: is it under a year or over?

```python
build_cost = 60_000   # the one-time quote to build it, in rupees
payback_months = build_cost / (annual_savings / 12)
print(f"Payback period: {payback_months:.1f} months")
```

```
Payback period: 15.4 months
```

**How it works:** `60_000` is Python's way of writing 60000 with a separator you can read; the underscore changes nothing about the number. `annual_savings / 12` is the saving per month, and dividing the one-time cost by it gives the months until the build has paid for itself, the same shape as Chapter 23, section 23.9's customer payback (CAC ÷ monthly gross profit). `:.1f` keeps one decimal place.

The follow-up every interviewer asks: what about the automation's own upkeep? What happens if you change the calculation to include two hours of maintenance a month? The saving shrinks and the payback stretches:

```python
maintenance_hours_per_month = 2
net_annual = annual_savings - maintenance_hours_per_month * 12 * hourly_cost
net_payback_months = build_cost / (net_annual / 12)
print(f"Net annual savings: ₹{net_annual:,.0f}")
print(f"Payback, net of maintenance: {net_payback_months:.1f} months")
```

```
Net annual savings: ₹39,600
Payback, net of maintenance: 18.2 months
```

**How it works:** `maintenance_hours_per_month * 12 * hourly_cost` is the yearly cost of looking after the automation (2 × 12 × 300 = ₹7,200), and `net_annual` takes it off the gross saving. `net_payback_months` is the same division as before, on the net figure.

**Reading it.** At ₹300 an hour this is not an easy yes: the build pays for itself only after about a year and a half, net of upkeep. If the task will still exist in three years, the automation saves ₹1,18,800 against a ₹60,000 build, a gain of ₹58,800; if the process is due to change next year, it never pays back. That's the conversation the number lets you have.

| Tier | What to say |
|---|---|
| Passes | A qualitative "this will definitely save time" with no actual number attached |
| Strong | The real calculation above, net of ongoing maintenance, giving a concrete payback period a business can actually evaluate |
| Extra points | **[+Business]** an 18-month payback is a genuinely different conversation from a 5-month one: the question becomes how long the task will exist, not whether it's tedious; worth having the honest number either way, not just when it's flattering<br>**[+Assume]** say which inputs are measured (the hours, timed before and after, as Chapter 20 insists) and which are assumptions (the maintenance hours), as Chapter 63's ROI table does<br>**[+Edge cases]** a good payback doesn't override a high risk: in Chapter 63, straight-through PO intake had better labour economics than the assisted mode and was still rejected, because its wrong orders cost far more than it saved |

**Likely follow-ups:** How would you estimate the "fully loaded hourly cost" figure honestly? How long does the task have to keep existing for this build to be worth it?
**Red flag:** justifying an automation investment with no quantified payback calculation at all.
**Learn it in:** Chapter 20, section 20.14 (hours saved × loaded rate); Chapter 23, section 23.9 (the payback period); Chapter 63, section 63.2 (value, effort and *risk*); Chapter 66, section 66.3 (the honest business case).

---

## 80.5 Leadership scenarios

### Q80-017 · A senior stakeholder wants you to build something you believe is technically the wrong approach. How do you push back, live?

**Level:** Senior · **Roles:** DE, DS, ARC, LEAD

**Remember it as:** *Lead with the specific risk, in their terms, not a technical objection in yours. And always come with an alternative, not just a "no."*

**Answer in one line:** Frame the pushback in terms of the *business* risk their preferred approach creates (cost, timeline, maintainability, a specific failure mode), not a purely technical objection that doesn't connect to what they actually care about, and always propose a concrete alternative rather than just a disagreement.

**Worked example:**

> "I'd say: 'I want to flag a real risk with this approach before we commit. This choice will likely cost us significantly more to maintain within a year as we scale, based on [specific reason]. Here's an alternative that gets us the same business outcome with a lower long-term cost. I'm glad to move forward with your original approach if there's a constraint I'm not seeing, but I wanted to make sure this trade-off was visible before we're locked in.'"

| Tier | What to say |
|---|---|
| Passes | Either silently complies despite disagreeing, or pushes back in purely technical language the stakeholder can't evaluate |
| Strong | The business-risk framing above, paired with a concrete alternative, not just an objection |
| Extra points | **[+Business]** explicitly leaving room for the stakeholder to have context you don't ("if there's a constraint I'm not seeing") respects their position while still making the risk fully visible, rather than framing it as a pure technical-authority standoff |

**Likely follow-ups:** What if the stakeholder proceeds with their original approach anyway? How would you document this disagreement for the record without it reading as insubordination?
**Red flag:** either silent compliance or a purely technical objection with no business framing and no alternative offered.
**Learn it in:** Chapter 67, section 67.4 ("Saying no"); Chapter 24, section 24.8 (handling pushback).

### Rapid-fire, 80.5

Roles: ARC and LEAD for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q80-018 | What's "influencing without authority," and why does an architect need it specifically? | Getting other teams to adopt a technical direction or standard without having any formal management authority over them, relying instead on credibility, clear reasoning, and genuine relationship-building | **[+Evidence]** in Chapter 67, Meera won the sales team over to data contracts with their own duplicated-macro incident, not an email announcing a standard | Senior · 67.4 ("Influencing without authority") |
| Q80-019 | How would you present a technical architecture decision to a board with no technical background? | Lead with the business outcome and risk in plain language, keep technical detail available only if asked, and anchor the decision in cost, risk, and timeline, the terms a board actually evaluates decisions in | **[+Business]** lead with the number a skeptic would ask for first, and keep a conditional saving out of the total until its condition is shown to hold | Senior · 67.3 ("Presenting to a board"), built on 24.7 |
| Q80-020 | What would your first 90 days look like as a newly hired architect at a company you don't know yet? | Listen and map the current state before proposing changes: understand existing systems, meet key stakeholders, identify quick wins that build credibility, and avoid a sweeping redesign proposal before genuinely understanding why things are the way they are | **[+Signpost]** name the three phases: listen (weeks 1–4), diagnose (weeks 5–8), earn credibility with one small, visible fix (weeks 9–12) | Senior · 67.6 |
| Q80-021 | How would you handle two senior engineers on your team who strongly disagree about a technical direction? | Get both positions fully understood first, look for what each is actually optimizing for underneath the disagreement, and make a clear, explained decision rather than letting the disagreement stay unresolved or quietly picking a side without reasoning | **[+Business]** an unresolved technical disagreement between two senior people tends to quietly split a team's execution, even if nobody says so out loud | Senior · 67.4 (leading people); 67.5 (judgment) |

---

## 80.6 Full architecture design cases

### Q80-022 · Design case: go back to the Riverstone of Parts 2 and 3, which runs everything off its ERP's database, and architect its next three years of data infrastructure

**Level:** Senior · **Roles:** ARC, LEAD, DE

**What they're really testing:** whether a multi-year architecture roadmap is grounded in actual current constraints and growth signals, not a greenfield fantasy design ignoring where the company actually is today. The setting is Riverstone before Part 5 was built: orders and customers in the ERP's PostgreSQL database, the reports and spreadsheets of Part 2, and a Daily Sales Flash sent by a scheduled Python script (Chapter 20). No warehouse, no orchestrator, no models yet.

**Talked through live, start to finish:**

> "I'd start by understanding today's actual pain points and growth trajectory, not designing in a vacuum: what's the current data volume, what's genuinely slow or fragile today, and what's the realistic growth rate. Assuming meaningful growth is expected, I'd propose a staged path, not a single big-bang migration: first, introduce a proper data warehouse alongside the existing operational database, so analytics workloads stop competing with production traffic (row storage for running the business, columnar for understanding it: Chapter 49, section 49.2). Second, once volume genuinely justifies it, introduce the pipeline and orchestration patterns from Chapter 46 to automate what's currently manual. Third, only once there's a genuine multi-team, multi-source scale problem, consider a lakehouse (Chapter 49, section 49.5) or a data mesh (Chapter 62, section 62.4, and only after section 62.6's readiness check passes), resisting the temptation to build for a scale Riverstone doesn't have yet just because it's architecturally interesting."

**Extra-points moves demonstrated:** **[+Business]** explicitly resisted over-engineering for a scale the company doesn't have yet. **[+Signpost]** proposed a staged roadmap, and connected each stage to a specific technique already covered in this book rather than inventing new concepts wholesale. **[+Scale]** tied each stage to a growth trigger (volume, then several teams and sources) rather than a date or a single fixed end-state design.

**Check your roadmap against what happened.** Parts 5 to 7 are what Riverstone actually did: ingestion into a warehouse (Chapters 45 and 49), an orchestrator (Chapter 46; ADR-002 chose Dagster), and then, once it was all running, a design document that described it as one system (Chapter 60, section 60.5). Compare your three stages with that document's containers and ADR index: which of your stages did Riverstone take, in what order, and which did it rightly not take yet? (Chapter 62, section 62.6 scored it not ready for a data mesh.)

**Likely follow-ups:** What would make you accelerate this roadmap, or slow it down? How would you sequence this against the team's existing day-to-day workload?
**Red flag:** a single, final-state architecture diagram with no staged path or connection to current actual constraints.
**Learn it in:** Chapter 60, sections 60.5 (the design document) and 60.6 (evolving a design under real constraints); Chapter 62, section 62.6 (the mesh readiness check); Chapter 66, sections 66.1 (a data strategy on one page) and 66.2 (maturity, scored honestly). The orchestration half is drilled in Chapter 77.

### Q80-023 · Design case: your team's biggest automation just failed silently for a week, causing real financial impact. As the architect, how do you respond, and what changes structurally?

**Level:** Senior · **Roles:** ARC, LEAD

**What they're really testing:** whether the response goes beyond fixing the immediate bug to a genuine structural/governance change, matching the seniority of the role being interviewed for.

**Talked through live, start to finish:**

> "Immediate: fix the specific failure and communicate the actual financial impact honestly to stakeholders, no minimizing it. Then, at the architecture level: this failure mode (silent, no alert) suggests our automation governance has a gap, not just this one automation. I'd propose an automation inventory (Chapter 63, section 63.8) if one doesn't already exist, since 'how many critical automations do we even have, and does each have monitoring' is often the real unanswered question after an incident like this. I'd establish a standard that every business-critical automation must have a defined owner and a minimum monitoring bar (freshness and volume checks, Chapter 47, section 47.5) before it's allowed into that category, and I'd run this as a genuine retrospective with the team, not just a top-down mandate, since the people closest to the work usually know which other automations share this same risk."

**Extra-points moves demonstrated:** **[+Business]** distinguished the immediate technical fix from the structural, governance-level change a senior role is actually being evaluated on. **[+Evidence]** connected to a named organizational tool (an automation inventory) rather than a vague "we'll be more careful" response.

**Likely follow-ups:** How would you prioritize which existing automations to audit first, given limited time? How would you get buy-in for the new standard without it feeling like blame directed at whoever built the original automation?
**Red flag:** a response that only fixes the immediate bug, with no structural or governance-level change proposed.
**Learn it in:** Chapter 63, sections 63.7 (ownership, runbooks, and support) and 63.8 (the automation inventory); Chapter 47, section 47.5 (freshness and volume monitoring); Chapter 78, Q78-018 (the identical incident, examined there at the individual-debugging level instead of the architectural-response level).

---

## 80.7 Predict the number: capacity, availability, and the arithmetic of a design

An architecture interview is mostly discussion, and that is where this chapter has been. But at some point the interviewer stops and asks for a number — how much downtime does that SLA allow, how many machines does that throughput need, what does adding a service cost you in availability. The discussion is where you show judgement; these are where you show you have built something.

They are all arithmetic you can do on a whiteboard, and they are the arithmetic that makes a design real. A reliability target with no downtime figure attached is a slogan.

Say each answer out loud, then read on.

**How these were run.** Plain arithmetic, computed and printed on Python 3.12 with the standard library. Nothing here depends on a vendor, a price list or a product, so none of it goes stale.

### Q80-030 · "We need 99.9% uptime." How much downtime is that?

**Level:** Mid · **Roles:** DE, AE, MLE, Architect

**Remember it as:** *Three nines is about 43 minutes a month. Each extra nine divides it by ten.*

**Answer in one line:** **8.76 hours a year**, or about **43 minutes a month** — which is a great deal more than most people picture when they say "three nines", and is why the number should always be stated in minutes before it is agreed.

```python
year_minutes = 365 * 24 * 60
for label, p in [('99%', 0.99), ('99.9%', 0.999), ('99.99%', 0.9999), ('99.999%', 0.99999)]:
    down = year_minutes * (1 - p)
    print(f"{label:>9}: {down:8.1f} min/yr = {down/60:6.2f} h/yr, {down/12:6.1f} min/month")
```

```
      99%:   5256.0 min/yr =  87.60 h/yr,  438.0 min/month
    99.9%:    525.6 min/yr =   8.76 h/yr,   43.8 min/month
   99.99%:     52.6 min/yr =   0.88 h/yr,    4.4 min/month
  99.999%:      5.3 min/yr =   0.09 h/yr,    0.4 min/month
```

Two nines — which sounds almost like three — allows **three and a half days** a year.

The reason to have this table in your head is that it converts an abstract target into an operational commitment, and the two are usually agreed by different people. Three nines means a single unplanned restart that takes 45 minutes has spent the month's entire budget. Four nines means you cannot deploy during business hours unless the deployment is zero-downtime, because 4.4 minutes a month does not cover a rolling restart that goes wrong.

Four follow-on points that separate a strong answer:

**Each nine costs roughly an order of magnitude** in engineering and infrastructure. The jump from three to four is usually the jump from "one region, good monitoring" to "multi-region with automatic failover", and it is rarely worth it for an internal analytics platform.

**Scheduled maintenance may or may not count**, and that is a contract question, not a technical one. Ask.

**Availability is measured over a window**, and a shorter window is a harder promise. 99.9% monthly is stricter than 99.9% annually, because one bad month cannot be averaged away.

**The number should come from the cost of being down**, not from a round-sounding target. A warehouse that feeds a morning report has a different requirement from a payments API, and an architect who asks "what does an hour of downtime actually cost?" before agreeing a figure is doing the job.

| Tier | What to say |
|---|---|
| Passes | "It's a small amount of downtime" |
| Strong | + 8.76 hours a year and 43 minutes a month, and that each nine is roughly ten times the cost |
| Extra points | **[+Business]** derive the target from the cost of downtime rather than accepting a round number · **[+Clarify]** ask whether planned maintenance counts and over what window it is measured · **[+Edge cases]** a monthly window is stricter than an annual one for the same percentage · **[+Validate]** 45 minutes of restart is a whole month of a three-nines budget, which is the sentence that makes it concrete |

**Likely follow-ups:** What is an error budget? How does an SLO differ from an SLA? *(An SLO is the internal target; an SLA is the contractual promise with consequences, and it is usually set looser.)* How would you measure availability — by uptime, or by successful requests?
**Learn it in:** Chapter 61, section 61.5 (reliability); Chapter 80, Q80-003.

### Q80-031 · A request passes through five services, each 99.9% available. What is the end-to-end availability?

**Level:** Senior · **Roles:** DE, MLE, Architect

**Remember it as:** *Availabilities in series multiply. Five nines-point-nine services give you 99.5%, which is a different world from 99.9%.*

**Answer in one line:** **99.5%** — 0.999⁵, which is 43.7 hours of downtime a year against the 8.76 hours each individual service promises, so the chain is five times worse than any of its parts.

```python
for n in (1, 2, 3, 5, 10, 20):
    avail = 0.999 ** n
    print(f"{n:>2} in series: {avail*100:7.4f}%  ({(1-avail)*365*24*60:8.1f} min/yr down)")
```

```
 1 in series: 99.9000%  (   525.6 min/yr down)
 2 in series: 99.8001%  (  1050.7 min/yr down)
 3 in series: 99.7003%  (  1575.2 min/yr down)
 5 in series: 99.5010%  (  2622.7 min/yr down)
10 in series: 99.0045%  (  5232.4 min/yr down)
20 in series: 98.0189%  ( 10412.7 min/yr down)
```

Twenty services — an ordinary number for a microservice request path — gives **98%**, which is seven days a year.

This is the strongest single argument against decomposition for its own sake, and it is worth being able to make numerically rather than as a preference. Every service you add to a *synchronous* path multiplies its failure in. The architectures that survive this do one of three things:

| Approach | What it does to the arithmetic |
|---|---|
| **Redundancy within each service** | Two independent copies turn 99.9% into 99.9999%, so the chain of five becomes 99.9995% |
| **Remove the service from the critical path** | Make the call asynchronous, or cache its result — an unavailable service that is not on the path contributes nothing |
| **Degrade gracefully** | If a recommendation service is down and the page renders without recommendations, it was never in series |

The redundancy line is the one worth doing out loud: 1 − (1 − 0.999)² = 0.999999. Two independent copies of a three-nines service give six nines — *provided the failures are independent*, which is the assumption that usually breaks. Two copies in the same rack, on the same deployment, behind the same config change, fail together, and the arithmetic quietly stops applying. That is the real content of Q80-029.

| Tier | What to say |
|---|---|
| Passes | "They multiply, so it's lower" |
| Strong | + 99.5%, converts it to 43.7 hours a year, and names the three ways out: redundancy, removing from the path, graceful degradation |
| Extra points | **[+Scale]** 20 services in series is 98%, which is a week a year · **[+Edge cases]** redundancy only multiplies if failures are independent, and shared config, shared rack or a shared deploy breaks that · **[+Trade-offs]** the cheapest fix is usually making the call asynchronous rather than making the service more reliable · **[+Business]** this is the number to bring when someone proposes splitting a service for organisational reasons |

**Likely follow-ups:** What makes two copies non-independent? How does a circuit breaker change this? What is the availability of components in parallel?
**Learn it in:** Chapter 61, section 61.5; Chapter 80, Q80-029.

### Q80-032 · A million events a day. What throughput do you design for?

**Level:** Mid · **Roles:** DE, AE, Architect

**Remember it as:** *The daily average is the wrong number. Traffic is not spread over 86,400 seconds; it arrives in a business day, with a peak inside it.*

**Answer in one line:** The average is **11.6 events a second**, but you size for the peak — and if 80% of the volume arrives in four business hours, the real figure is **55.6 a second**, roughly five times the average.

```python
daily = 1_000_000
print(f"average          : {daily/86400:.1f}/sec")
for peak in (3, 5, 10):
    print(f"  at {peak}x peak   : {daily/86400*peak:6.1f}/sec")
print(f"80% in 4 hours   : {daily*0.8/(4*3600):.1f}/sec")
```

```
average          : 11.6/sec
  at  3x peak   :   34.7/sec
  at  5x peak   :   57.9/sec
  at 10x peak   :  115.7/sec
80% in 4 hours  : 55.6/sec
```

Designing for 11.6 a second gives you a system that falls over every weekday at 11am.

The move that makes this a good answer is doing it from the *shape of the business* rather than applying a generic multiplier. Riverstone's orders arrive during Indian business hours, so the overnight hours contribute almost nothing and the multiplier is around 5. A consumer app has an evening peak. A payroll system has a month-end spike that dwarfs everything — there the peak factor is not 5, it is 50, and the right design may be a queue that absorbs the spike rather than capacity that matches it.

Three further things to say if there is room:

**The peak of the peak.** A busy hour has a busy minute. If the arrival pattern is bursty rather than smooth, a short burst can exceed even the hourly peak rate several times over, which is what the queue depth has to absorb.

**Growth.** Sizing for today's peak means re-architecting next year. A capacity plan carries a horizon.

**Headroom.** Running at 100% of designed capacity leaves nothing for a retry storm (Chapter 78, Q78-031) or a failed node. 70% target utilisation is a common rule.

| Tier | What to say |
|---|---|
| Passes | "About 12 a second" |
| Strong | + that the average is the wrong number, derives a peak from the business day, and lands on roughly 50–60 a second |
| Extra points | **[+Business]** derive the peak factor from when this business is actually busy, not a generic 3× · **[+Scale]** a queue absorbing a spike is often cheaper than capacity matching it, especially for month-end patterns · **[+Edge cases]** the busy hour has a busy minute, and bursts set the queue depth · **[+Validate]** plan for headroom — 70% utilisation — because retries and failures arrive together |

**Likely follow-ups:** How would you handle a 50× month-end spike? What is backpressure? *(Chapter 77, Q77-022.)* How does this change for a streaming system?
**Learn it in:** Chapter 48, section 48.2 (scale); Chapter 80, section 80.1.

### Q80-033 · p50 is 100 ms and p99 is 1 second. A page makes 20 service calls. How often is it slow?

**Level:** Brain-racking · **Roles:** DE, MLE, Architect

**Remember it as:** *The tail is not rare once you multiply it. Twenty calls at a 1% tail means one page in five touches the tail.*

**Answer in one line:** About **18% of page loads** hit at least one second-long call — because the chance of *avoiding* the tail on all 20 is 0.99²⁰ = 0.818, so a "1 in 100" latency is a "1 in 5" page.

```python
p_tail = 0.01
for n in (1, 5, 10, 20, 50):
    print(f"{n:>2} calls: P(at least one in the p99 tail) = {(1-(1-p_tail)**n)*100:5.1f}%")
```

```
 1 calls: P(at least one in the p99 tail) =   1.0%
 5 calls: P(at least one in the p99 tail) =   4.9%
10 calls: P(at least one in the p99 tail) =   9.6%
20 calls: P(at least one in the p99 tail) =  18.2%
50 calls: P(at least one in the p99 tail) =  39.5%
```

This is why **the median latency of a service tells you almost nothing about the experience of a page built from it**, and why engineers who optimise p50 are often surprised that users still complain.

The consequences shape real designs:

**Tail latency is the thing to work on.** Reducing p99 from 1s to 300 ms improves the 20-call page far more than halving the median does, because the median was never the problem.

**Parallelise and the arithmetic changes shape.** Twenty *sequential* calls add their latencies, so the page is slow in total. Twenty *parallel* calls take as long as the slowest, which is almost always a tail call — so parallelism fixes the sum and makes you *more* exposed to the tail, not less.

**Hedged requests** exploit exactly this: send a duplicate request if the first has not returned by p95, and take whichever answers first. It costs about 5% extra load and removes most of the tail.

**Fan-out is the hidden cost of decomposition**, and it is the latency counterpart to Q80-031's availability argument. Each service you add is another draw from the tail.

| Tier | What to say |
|---|---|
| Passes | "The tail matters more than the median" |
| Strong | + the calculation, 1 − 0.99²⁰ = 18%, and that parallelising makes the page's latency equal to the slowest call |
| Extra points | **[+Scale]** optimising p99 beats optimising p50 for any fan-out page · **[+Trade-offs]** hedged requests cut the tail for about 5% more load · **[+Edge cases]** the calculation assumes independence; a shared bottleneck like one overloaded database makes tails correlate and the real figure is worse · **[+Business]** users experience the tail, and averages in a dashboard hide it entirely |

**Likely follow-ups:** What causes tail latency? *(GC pauses, cold caches, queueing, a slow replica.)* What is a hedged request? Why might the independence assumption fail?
**Learn it in:** Chapter 61, section 61.4 (performance); Chapter 80, section 80.1.

### Q80-034 · 100 TB today, replication factor 3, growing 30% a year. What do you provision for three years?

**Level:** Mid · **Roles:** DE, Architect

**Remember it as:** *Multiply by the replication factor, compound the growth, then divide by your target utilisation. Three steps, each of which people forget one of.*

**Answer in one line:** About **940 TB** — 100 TB compounds to 220 TB logical over three years, replication triples it to 659 TB raw, and provisioning to a 70% utilisation target brings it to roughly 940.

```python
base, rf, growth, target_util = 100, 3, 0.30, 0.70
for y in range(4):
    logical = base * (1 + growth)**y
    print(f"year {y}: {logical:6.1f} TB logical, {logical*rf:6.1f} TB raw")
final = base * (1+growth)**3 * rf
print(f"provisioned at {target_util:.0%} utilisation: {final/target_util:.0f} TB")
```

```
year 0:  100.0 TB logical,  300.0 TB raw
year 1:  130.0 TB logical,  390.0 TB raw
year 2:  169.0 TB logical,  507.0 TB raw
year 3:  219.7 TB logical,  659.1 TB raw
provisioned at 70% utilisation: 942 TB
```

The answer people give is 300 TB, which is the replication step alone. The answer is more than three times that.

Each step is a decision worth naming rather than a constant:

**Replication factor** is a durability and availability choice. Three is the common default for HDFS and Cassandra; cloud object storage replicates behind the scenes and you pay for one copy. **Erasure coding** gets similar durability at roughly 1.5× instead of 3×, at the cost of more CPU on reads and slower recovery — and it is the lever that matters most at this scale.

**Growth** should come from measurement, not a guess. And compound growth means the last year costs more than the first two combined, which is why a three-year capacity plan is really a plan to revisit the decision in eighteen months.

**Utilisation headroom** exists because a storage system at 95% behaves very badly — compaction, rebalancing and recovery all need free space, and a node failure must be absorbed by the remaining nodes.

The architect's real move is to question the first number. Three years of 30% growth assumes you keep everything forever. A retention policy that drops raw events after 90 days while keeping aggregates can change 940 TB into 200, and that conversation is worth more than any efficiency in the storage layer.

| Tier | What to say |
|---|---|
| Passes | "300 TB, for the replication" |
| Strong | + compounds the growth and adds utilisation headroom, landing near 940 TB, and names all three steps |
| Extra points | **[+Trade-offs]** erasure coding gives similar durability at about 1.5× rather than 3× · **[+Business]** a retention policy usually beats any storage efficiency — ask what must actually be kept · **[+Scale]** compound growth means year three costs more than years one and two together · **[+Edge cases]** at 95% utilisation compaction and recovery stop working, which is why the headroom is not optional |

**Likely follow-ups:** What is erasure coding? How would you set a retention policy? What is the cost difference between hot and cold storage tiers?
**Learn it in:** Chapter 48, section 48.3 (storage); Chapter 80, section 80.3.

### Q80-035 · 500 requests a second, 200 ms each. How many connections do you need?

**Level:** Senior · **Roles:** DE, MLE, Architect

**Remember it as:** *Little's Law: concurrency = throughput × latency. It is the only capacity formula you have to remember, and it explains why slow systems fall over rather than just slowing down.*

**Answer in one line:** **100 concurrent requests** — 500 per second × 0.2 seconds — so a connection pool of 100 is exactly saturated, and the important part is what happens when latency moves.

```python
throughput = 500
for latency in (0.05, 0.2, 1.0, 2.0):
    print(f"{latency*1000:>5.0f} ms -> {throughput*latency:6.0f} concurrent")
print(f"a pool of 100 serves {100/0.2:.0f} req/s at 200 ms")
print(f"the same pool serves {100/2.0:.0f} req/s if latency degrades to 2 s")
```

```
   50 ms ->     25 concurrent
  200 ms ->    100 concurrent
 1000 ms ->    500 concurrent
 2000 ms ->   1000 concurrent
a pool of 100 serves 500 req/s at 200 ms
the same pool serves  50 req/s if latency degrades to 2 s
```

The last two lines are the whole point, and they describe how most outages actually unfold.

A pool of 100 connections handles 500 requests a second comfortably at 200 ms. The database gets slower — a missing index after a deploy, a long-running report, a failover — and latency goes to 2 seconds. Capacity does not fall by the 10× that latency rose; it falls to **50 requests a second**, and the other 450 queue. The queue grows, queued requests time out, clients retry (Chapter 78, Q78-030), and the retries consume the capacity that was left.

That is why systems **collapse** rather than degrade. The relationship between latency and capacity is multiplicative, and a queue turns a 10× slowdown into a total outage.

What follows from it:

**Size pools from Little's Law and the *worst* acceptable latency**, not the typical one.

**Timeouts are a capacity control, not just an error-handling nicety.** A request that times out at 1 second frees its connection; one with no timeout holds it forever (Chapter 78, Q78-032).

**Load shedding beats queueing.** Rejecting requests you cannot serve keeps the system responsive for the ones you can. An unbounded queue converts a capacity problem into an availability problem.

The law applies everywhere: threads, connections, Kafka consumers, workers in a pool, even people in a support queue.

| Tier | What to say |
|---|---|
| Passes | "100, by Little's Law" |
| Strong | + what happens when latency rises: capacity falls proportionally, the queue grows, and the system collapses rather than degrading |
| Extra points | **[+Scale]** size pools from the worst acceptable latency, not the typical one · **[+Trade-offs]** load shedding keeps a system responsive where an unbounded queue turns slow into down · **[+Edge cases]** timeouts are capacity control, because they return the connection · **[+Business]** this is why an incident goes from "a bit slow" to "entirely down" in minutes with no further trigger |

**Likely follow-ups:** How would you pick a timeout? What is load shedding? How does this interact with autoscaling? *(Badly, if the scaler reacts to CPU — a queue-bound system is not CPU-bound, so it never scales.)*
**Learn it in:** Chapter 61, section 61.4; Chapter 78, Q78-030.

### Rapid-fire, 80.7: numbers an architect should not have to look up

Roles: DE, MLE and Architect for every row.

| # | Question | The answer, and why | Extra point |
|---|---|---|---|
| Q80-036 | Two copies of a 99.9% service — what availability? | 99.9999%, *if* the failures are independent. Shared config, shared rack or a shared deploy breaks that, and then it is still 99.9% | **[+Validate]** ask what the two copies share before claiming the number → Q80-029 |
| Q80-037 | An SLA of 99.9% monthly against 99.9% annually | The monthly one is stricter: a bad month cannot be averaged away across the year | **[+Clarify]** the window is part of the promise → Q80-030 |
| Q80-038 | A batch job takes 4 hours on 1 TB. How long on 10 TB? | Not 40 hours necessarily — it depends on whether the work is linear, and on whether a sort or a join makes it n log n or worse. Measure at two sizes before extrapolating | **[+Scale]** a shuffle or a cross join changes the shape entirely → Ch 48 §48.2 |
| Q80-039 | Is adding a cache always a latency win? | No. It adds a failure mode, a consistency question and a cold-start cliff. A cache that is down or empty makes the system slower than having none | **[+Edge cases]** a popular key expiring sends everything to the database at once → Ch 78 Q78-031 |
| Q80-040 | 1 GB of data over a 100 Mbps link — how long? | About 80 seconds at line rate, and realistically more. Bandwidth is in bits and file sizes in bytes; the factor of 8 is the usual error | **[+Validate]** for very large transfers, shipping disks is still sometimes faster → Ch 48 §48.2 |
| Q80-041 | A "zero-downtime" deploy with a database migration | Only if the schema change is backward compatible with the running version. Add a column, deploy, backfill, then drop — never all at once | **[+Business]** the migration, not the deploy, is what forces the outage → Ch 28 §28.12 |
| Q80-042 | Your p99 improved but users complain more. How? | You may have moved traffic into the tail, or the p99 is now measured over a different population, or the complaints are about p99.9. Percentiles do not aggregate — you cannot average them across servers | **[+Edge cases]** averaging percentiles across hosts is a common and silent monitoring error → Ch 61 §61.4 |
| Q80-043 | Cost of an incident that costs one hour of a 10-person team | Ten hours of salary is the visible part, and usually the smallest. Delayed work, lost trust and the fix's opportunity cost are the rest | **[+Business]** this is the figure that justifies reliability work → Q80-016 |

---

## 80.8 Running it in production

Sections 80.1 to 80.6 are about designing a system. This one is about the half of an architect's job that only exists after something is live, and it is where senior interviews spend more time than candidates expect. A design that cannot be operated is not a good design.

> **Beyond the book: three operational terms this book does not teach.** Chapter 47 covers data incidents, runbooks and alerts, and Chapter 56 covers model monitoring, but these three come from the site-reliability tradition and are worth having one line each before the questions use them.
>
> - **RPO** (recovery point objective) is how much data you can afford to lose, measured in time. An RPO of one hour means losing up to an hour of writes is acceptable.
> - **RTO** (recovery time objective) is how long you can afford to be down. The two are independent: you can have a tight RPO and a loose RTO, and the pair decides the architecture and most of the cost.
> - An **error budget** is the inverse of an availability target. If the SLO is 99.9% monthly, the budget is the 43 minutes 12 seconds of downtime that target permits (Q80-030 does this arithmetic), and spending it is allowed — that is what a budget is for.

### Q80-044 · Your nightly pipeline failed silently for a week. Run the postmortem.

**Level:** Senior · **Roles:** DE, AE, Architect

**Remember it as:** *A postmortem asks what about the system let this run for a week, not who missed it. The detection gap is the finding, not the bug.*

**Answer in one line:** Blamelessly, in writing, with a timeline, and focused on the two questions that matter — **why did it fail**, and far more importantly **why did it take a week to notice** — ending in dated, owned actions, of which at least one must shorten detection rather than fix this one bug.

**The structure, and the one row candidates leave out:**

| | |
|---|---|
| **Timeline** | What happened and when, including when each person learned of it. Facts, no interpretation |
| **Impact** | Quantified: which reports were wrong, who acted on them, what it cost. "Some dashboards were stale" is not an impact statement |
| **Why it failed** | The technical cause, traced past the first answer |
| **Why detection took a week** | **The actual finding.** A one-week gap is a monitoring defect, independent of the bug |
| **What we are changing** | Dated, owned, and small enough to happen. One of them must address detection |
| **What we are not changing** | And why — this is what stops a postmortem becoming a wish list |

**Why the detection row dominates.** The bug is one bug. **The gap is every future bug**, including the ones not yet written. An honest postmortem of a week-long silent failure usually concludes that the pipeline had success/failure alerting but no **freshness or volume check** — it alerted on crashes and was silent on a job that completed having written nothing. Chapter 47, §47.5 is that check; Chapter 46, §46.7 is the stronger version, where delivery only happens after the data passes its tests.

**Blameless, and what that actually means.** Not "nobody is responsible" — the opposite. It means the question is which part of the *system* permitted this, because a postmortem that lands on "X should have noticed" produces no change and guarantees the next one is concealed. Chapter 47, §47.8 makes the same point about data incidents.

| Tier | What to say |
|---|---|
| Passes | Describes finding the root cause and fixing it, perhaps mentioning a postmortem document |
| Strong | The full structure, with the detection gap identified as the primary finding and a dated owned action against it |
| Extra points | + **[+Validate]** the strongest action is a freshness or row-count check, because it catches the whole class rather than this instance + **[+Business]** quantify the impact in decisions taken on wrong numbers, not in hours of downtime, since that is what the business experienced + **[+Edge cases]** a job that completes successfully having written nothing is the hardest failure to detect and the most common cause of a long silent gap + **[+Trade-offs]** include the "not changing" list, or the postmortem generates ten actions and delivers none |

**Likely follow-ups:** What specific check would have caught this on day one? Who should write the postmortem?
**Red flag:** a postmortem that names a person, or one whose only action is fixing the specific bug.
**Learn it in:** Chapter 47, §47.8 (handling a data incident) and §47.5 (observability: freshness, volume, unusual values); Chapter 46, §46.7 (delivery only after the data passes its checks); Chapter 67, §67.6.

### Q80-045 · "We need disaster recovery." What do you ask before designing anything?

**Level:** Senior · **Roles:** DE, Architect · **Beyond the book** (RPO and RTO)

**Remember it as:** *Two numbers decide the whole design: how much data you can lose, and how long you can be down. Everything else is consequence.*

**Answer in one line:** Ask for the **RPO** and the **RTO** as numbers per system, then ask what event you are recovering from — because a single-region outage, a corrupted table and a deleted account need different answers, and the cost scales steeply with both numbers.

**The conversation, in order:**

1. **RPO and RTO, per system, as numbers.** Not "we can't lose data" — that is an infinite budget. The useful question is "if we lost the last hour of orders, what would happen?", and the answer is usually survivable for analytics and not for the ledger.
2. **Recovering from what?** The scenarios have almost nothing in common:
   - A region failing needs a second region, which is the expensive one
   - A table corrupted by a bad deploy needs point-in-time restore
   - A ransomware or deleted-account event needs backups the primary credentials cannot reach
3. **Has the restore ever been tested?** This is the question that separates a real answer from a plan. An untested backup is a belief.
4. **What does the business actually need recovered first?** Rarely everything at once. Order intake before historical reporting.

**The honest framing to offer.** Different systems get different numbers, and saying so is the senior move: Riverstone's order ledger might warrant an RPO near zero, while the analytics warehouse can be rebuilt from source and needs no RPO at all — it needs a documented rebuild procedure instead. Buying one tier of protection for everything is how DR budgets get rejected.

| Tier | What to say |
|---|---|
| Passes | Talks about backups, replication and a second region |
| Strong | Asks for RPO and RTO as numbers per system, distinguishes the failure scenarios, and asks whether restore has been tested |
| Extra points | + **[+Validate]** "when did we last restore from this backup into a working system?" is the question that finds the real state + **[+Business]** differentiate by system: a warehouse rebuildable from source needs a procedure, not a replica, and that distinction is where the budget is saved + **[+Edge cases]** backups reachable with the same credentials as production are not protection against the scenario people most fear + **[+Trade-offs]** a tighter RPO means synchronous replication, which costs write latency in normal operation — a permanent cost for a rare event |

**Likely follow-ups:** What RPO would you argue for on the order ledger, and why? How would you test a region failover without risking production?
**Red flag:** proposing multi-region before anyone has stated a number, or treating "we have backups" as disaster recovery.
**Learn it in:** Chapter 60, §60.3 (non-functional requirements: numbers, not adjectives); Chapter 47, §47.8; Chapter 2, §2.9 (keeping data safe).

### Rapid-fire, 80.8

Roles: DE, AE and Architect for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q80-046 | What is an error budget, and what is it for? | The downtime an availability target permits — 99.9% monthly allows 43 minutes 12 seconds — and its purpose is to make reliability a budget rather than an absolute, so a team with budget remaining can ship faster and one that has spent it stops and fixes things | **[+Business]** it converts "is reliability good enough?" from an argument into a number both sides already agreed to | Senior · 80.7 (Q80-030), 60.3 |
| Q80-047 | What belongs in a runbook? | What this job does, how to tell whether it is healthy, the three things that usually go wrong with the exact command for each, who to escalate to, and what *not* to do — written for a tired person at 3 a.m. who did not build it | **[+Validate]** the test of a runbook is that someone else followed it successfully without calling you | Mid · 47.8, 46.10 |
| Q80-048 | Why does alert fatigue make a system less reliable? | Because an alert that fires often and means nothing trains people to ignore the channel, so the one real alert arrives in a stream of noise — a monitoring system with too many alerts is less effective than one with three that always matter | **[+Signpost]** Chapter 47, §47.9 is titled "Alerts people still read", which is the whole design goal | Mid · 47.9 |
| Q80-049 | Your job succeeded but wrote zero rows. How do you catch it? | A volume check, not a status check: assert the row count is within an expected band for the day, because exit code zero only means the code did not crash and says nothing about whether it did its work | **[+Signpost]** this is the class of failure behind most week-long silent outages (Q80-044) | Mid · 47.5, 46.7 |
| Q80-050 | What should an architect do during an incident, specifically? | Usually not debug: take the communication and the decisions — keep stakeholders informed on a stated cadence, decide whether to roll back or fix forward, and protect the responders from being interrupted for status | **[+Business]** a stated update cadence ("next update in 30 minutes") stops the responders being asked every five | Senior · 47.8, 67.3 |
| Q80-051 | Roll back or fix forward? | Roll back by default when a rollback is safe and the cause is unknown, because it restores service while you investigate; fix forward when the change cannot be undone, such as a migration that has already transformed data | **[+Edge cases]** a deploy that has written data in a new shape may have no rollback, which is a design decision made earlier and felt now | Senior · 56.6, 46.4 |
| Q80-052 | How would you decide whether an incident needs a postmortem? | On impact and on novelty: anything that affected users or produced wrong numbers, plus anything that surprised you — a near-miss nobody noticed is often the cheapest postmortem you will ever get | **[+Business]** writing one for a near-miss is how a team learns without paying for the lesson | Mid · 47.8 |

---

## 80.9 Changing it without breaking it

Every architecture question in an interview is really about change, because a system that never changed would need no architecture. This section is the mechanics of changing a live system, which is the part that separates someone who has operated software from someone who has only designed it.

> **Beyond the book: feature flags.** Chapter 56, §56.6 teaches canary, blue-green and shadow deployment for models. A **feature flag** is the same idea moved into the application: a conditional that turns a code path on or off at runtime, per user or per percentage, so that deploying code and releasing behaviour become two separate events. The cost is that every flag is a branch in the code and an untested combination with every other flag, which is why flags need an owner and a removal date.

### Q80-053 · You are replacing a system that 200 people use daily. How do you cut over?

**Level:** Senior · **Roles:** DE, AE, Architect

**Remember it as:** *Never a big-bang switch. Run both, compare outputs on real traffic, move users in groups, and keep the old one reachable until nobody is using it.*

**Answer in one line:** Incrementally and reversibly — stand the new system up beside the old, run both on the same real inputs and **compare their outputs** until they agree, migrate users in cohorts smallest-risk first, and keep the old path available until usage of it reaches zero.

**The five stages, and the one that does the real work:**

| | Stage | Why |
|---|---|---|
| 1 | **Run in parallel** | Both systems, same inputs, nobody switched |
| 2 | **Compare outputs, automatically** | **This is the stage that finds everything.** Differences are either new bugs or undocumented old behaviour, and both matter |
| 3 | **Migrate a cohort** | Start with the most tolerant group, not the easiest to migrate |
| 4 | **Widen, with a rollback path** | Keep the old system warm and the switch reversible per cohort |
| 5 | **Decommission** | Only after usage is measured at zero, and after the data is retained somewhere |

**Stage 2 is the answer.** An automated output comparison on real traffic is what turns a migration from a hope into a measurement, and it reliably discovers that the old system did something nobody documented — a rounding convention, an exclusion, a special case for one customer. Chapter 14, §14.11's discipline applies directly: reconcile the new to the old and decompose every difference rather than accepting a tolerance.

**The strangler pattern, if asked to name it.** Rather than replacing the whole system at once, put the new system in front, let it handle one slice of functionality, and grow its share until the old system is surrounded and can be removed. Chapter 69A mentions it by name; the point for an interview is that it makes every step individually reversible.

**What to say about the thing everyone forgets.** Decommissioning. A system kept alive "just in case" for two years costs real money, holds the organisation on an old dependency, and quietly becomes a second source of truth that someone will eventually report from. Set the removal date when the migration starts.

| Tier | What to say |
|---|---|
| Passes | Suggests a phased rollout with a pilot group and a rollback plan |
| Strong | The five stages with automated output comparison on real traffic named as the stage that finds the problems, and a decommission date set up front |
| Extra points | + **[+Validate]** compare outputs automatically and investigate every difference, because the differences are where the undocumented old behaviour lives + **[+Business]** migrate the most tolerant cohort first, which is not the same as the easiest to migrate — the easiest is often the most visible + **[+Edge cases]** data written during parallel running needs a rule about which system owns it, or you get two divergent truths + **[+Signpost]** the strangler pattern is the name for stages 1 to 4 done incrementally |

**Likely follow-ups:** What would you do if the outputs differed by 2% and nobody could explain it? Who decides the cutover date?
**Red flag:** a date-based cutover with no parallel run and no output comparison.
**Learn it in:** Chapter 60, §60.6 (evolving a design under real constraints); Chapter 14, §14.11 (reconciling and documenting every decision); Chapter 56, §56.6 (deployment patterns).

### Rapid-fire, 80.9

Roles: DE, MLE and Architect for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q80-054 | Canary, blue-green and shadow — what is the difference? | Canary sends a small share of real traffic to the new version and watches; blue-green runs two complete environments and switches all traffic at once, so rollback is instant; shadow sends real traffic to the new version but discards its output, so you measure behaviour with no user risk | **[+Trade-offs]** blue-green needs double the capacity, canary needs good per-version metrics, shadow proves nothing about the write path | Mid · 56.6 |
| Q80-055 | When is shadow deployment the only safe option? | When the new version's output cannot be allowed to reach anyone until it is trusted — a pricing change, a credit decision, a model whose errors are expensive — because shadow is the only pattern that exercises production traffic with zero user exposure | **[+Edge cases]** shadow does not test writes, so it validates the computation and not the full path | Senior · 56.6 |
| Q80-056 | What is a feature flag, and what is its hidden cost? | A runtime switch that separates deploying code from releasing behaviour; the hidden cost is combinatorial — every flag doubles the number of possible states, few of which are tested — so each one needs an owner and a removal date | **[+Business]** old flags are the most common form of invisible complexity in a mature codebase | Mid · 56.6 |
| Q80-057 | How do you change a schema that live readers depend on? | In backward-compatible steps: add the new column, write both, migrate readers, then remove the old — never rename or drop in one step, because every deployed reader expecting the old shape breaks at once | **[+Signpost]** Q80-041 is this question as arithmetic: a "zero-downtime" deploy is only zero-downtime if the change is backward compatible | Mid · 28.12, 46.4 |
| Q80-058 | Your migration has run for 18 months. What went wrong? | Almost always no decommission date and no forcing function: without a date the old system stays, the team maintains both, and the migration becomes permanent — which is more expensive than either system alone | **[+Business]** maintaining two systems is the most expensive steady state available, and it is the default outcome | Senior · 60.6, 67.2 |
| Q80-059 | How would you make a change reversible when the data cannot be un-transformed? | Keep the input: write the transformed output to a new location rather than in place, so the original remains and a rollback is a pointer change rather than a reverse computation | **[+Signpost]** this is the write–audit–publish pattern, and the reason raw data is never overwritten | Senior · 47.4, 46.4 |
| Q80-060 | A vendor is deprecating an API you depend on in six months. What do you do? | Treat it as a dated project immediately: find every call site, assess whether the replacement is equivalent, build behind an interface you control so the next deprecation is cheaper, and keep the old path until the new one is proven | **[+Business]** wrapping a third-party dependency behind your own interface is what makes the second migration cheap | Mid · 45.10, 66.5 |

---

## 80.10 Leading the architecture, and the people

The scope note at the top of this chapter applies most to this section: these are the questions asked of a senior IC or architect, and they are mostly about whether you understand that the technical answer is rarely the constraint.

### Q80-061 · The platform team is a bottleneck and every analytics team is waiting on it. What do you do?

**Level:** Senior · **Roles:** Architect, DE, AE

**Remember it as:** *A bottleneck team is usually a structure problem wearing a capacity costume. Adding people to it often makes the queue longer.*

**Answer in one line:** Diagnose what the queue is actually made of before changing anything — if most requests are variations of the same ask, the answer is **self-service** rather than more capacity, and the structural question is which decisions genuinely need to be central and which were centralised by habit.

**The diagnosis, which is the whole answer:**

| What the queue contains | What it means | What fixes it |
|---|---|---|
| Many similar small requests | The platform is doing work users could do | Self-service: a template, a paved path, documentation |
| Few large bespoke projects | Genuine capacity shortage | More people, or fewer concurrent projects |
| Approvals and reviews | A governance bottleneck, not an engineering one | Clear criteria so most changes need no review |
| Fixing the platform's own breakages | Reliability debt consuming the team | Stop feature work and fix it; nothing else will work |

**Why adding people usually fails.** A central team that is the only route to production becomes a bottleneck whatever its size, because demand grows with the organisation and coordination cost grows faster than headcount. **Conway's Law is the frame to name here**: the architecture ends up mirroring the communication structure, so if every change must pass through one team, the architecture will have one chokepoint regardless of how the diagram looks. Chapter 62, §62.8 uses the law deliberately as a design tool.

**The structural options, with their honest costs:**

- **Self-service / paved path.** The platform provides a supported default route; teams use it without asking. Best outcome, most work up front, and it fails if the paved path does not cover the real cases.
- **Embedded engineers.** Platform people sit in analytics teams. Faster locally, and it drifts toward divergent practice unless the central standards are real.
- **Federated ownership with central standards** — the data-mesh direction. Works only at a maturity level most organisations have not reached, which Chapter 62, §62.6 scores honestly for Riverstone rather than assuming.

**The answer that earns the role:** "I would spend a week classifying the queue, because the four causes above have four different fixes and three of them are not headcount."

| Tier | What to say |
|---|---|
| Passes | Suggests more people, or prioritising the queue better |
| Strong | Classifies the queue first, identifies self-service as the usual answer, and names the structural options with their costs |
| Extra points | + **[+Signpost]** Conway's Law explains why a single central route produces a single architectural chokepoint whatever the headcount + **[+Business]** quantify the queue — requests per week by type and their wait — because that converts a complaint into a decision + **[+Validate]** a paved path only works if adoption is measured; an unused platform is a worse outcome than a bottleneck + **[+Trade-offs]** federated ownership needs a maturity most organisations lack, so recommending a mesh to a team that cannot staff it is a bad answer |

**Likely follow-ups:** How would you measure whether the paved path is working? What would make you argue *for* centralising something?
**Red flag:** recommending a data mesh, or more headcount, before looking at what the queue contains.
**Learn it in:** Chapter 62, §62.8 (Conway's Law, used as a design tool) and §62.6 (the maturity check, scored honestly); Chapter 66, §66.4 (hiring and structuring data teams); Chapter 67, §67.4.

### Rapid-fire, 80.10

Roles: Architect for every row, plus DE or AE where the work is shared.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q80-062 | How do you get technical debt funded? | Express it in the currency the business uses: delivery time, defect rate, incident frequency or risk — "the next change here takes three weeks instead of three days" gets funded where "we need to refactor" never does | **[+Business]** debt framed as engineering preference loses every prioritisation contest; framed as delivery speed it competes | Senior · 67.2 |
| Q80-063 | What is Conway's Law, and how would you use it deliberately? | That a system's structure comes to mirror the communication structure of the organisation that builds it; used deliberately, you change the team boundaries to get the architecture you want rather than fighting the org chart with a diagram | **[+Signpost]** Chapter 62, §62.8 treats it as a design tool rather than an observation | Senior · 62.8 |
| Q80-064 | What is a bus factor, and how do you raise it? | How many people would have to be unavailable before the work stops — often one — and you raise it with written runbooks and decision records, rotated responsibility, and pairing on the parts only one person understands | **[+Validate]** the test is a planned absence, not a hypothetical | Mid · 47.8, 67.4 |
| Q80-065 | How would you mentor a strong engineer who wants your job? | Deliberately: hand over real decisions rather than tasks, let them present to stakeholders, review their reasoning rather than correcting their output, and be explicit that their progression is the goal | **[+Business]** an architect whose leverage depends on being indispensable has no leverage | Senior · 67.4, 9.6 |
| Q80-066 | What would you look for when hiring a data engineer? | Evidence of having operated something, not only built it: how they found a failure, what they changed afterwards, and whether they can explain a trade-off they got wrong — plus whatever the team is actually missing rather than a generic bar | **[+Clarify]** define the gap before writing the job description, or you hire a copy of the team you have | Senior · 66.4 |
| Q80-067 | What is an RFC process, and when is it worth the overhead? | Writing a proposal for a significant change and circulating it for comment before building; worth it when a decision is expensive to reverse or affects several teams, and pure overhead for anything small and local | **[+Signpost]** the durable record of the outcome is an ADR (Q80-009); the RFC is the conversation that precedes it | Mid · 60.4, 67.3 |
| Q80-068 | How do you say no to a senior stakeholder without damaging the relationship? | Say no to the *approach* while agreeing with the *goal*, give the reason in their terms (cost, risk, time), and offer the alternative you would commit to — refusing without an alternative is where the relationship damage comes from | **[+Signpost]** Q80-017 is this question as a full scenario; Chapter 24, §24.8 is the technique | Senior · 24.8, 67.3 |

---
## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Claiming a system can be fully consistent, available, and partition-tolerant | Reveals a misunderstanding of the CAP theorem's actual constraint | Frame the real trade-off as CP vs. AP during an actual partition |
| Answering an availability question with "we have backups" | The data survives, but the service still stops until the restore finishes | Separate durability from availability; name what takes over while the main copy is down |
| Comparing build vs. buy on sticker price alone | Underestimates a build decision's true long-term cost | Compare total cost of ownership on both sides |
| A single architecture diagram trying to serve every audience | Too detailed for executives, too vague for engineers | Use layered diagrams (C4) matched to each audience |
| Treating "responsible AI" as one vague judgment call | Real, specific risks (fairness, privacy, misuse) go unchecked | Structure the review around named, checkable dimensions |
| Justifying an automation investment with no ROI number | A budget owner has nothing concrete to evaluate | Calculate a real payback period, net of maintenance, before proposing the build |
| Pushing back on a stakeholder in purely technical language | The stakeholder can't evaluate a risk they can't understand | Frame pushback in business-risk terms, with an alternative offered |
| A sweeping architecture proposal in an architect's first weeks | No credibility yet, and often misses real existing constraints | Listen and map the current state before proposing major change |

---

## In the real world: the standard that came from one bad incident

In his previous role, Siddharth inherited a team where a critical nightly automation had failed silently for a week, costing real money before anyone noticed. Interviewing for a Data Architect role a year later, he describes the incident and is asked the pointed follow-up: "Everyone says 'we'll add monitoring' after an incident like this. What did you actually do differently?"

His answer: he didn't just add monitoring to that one automation. He ran a genuine inventory across the team, discovering fourteen other business-critical automations with no monitoring at all, several of which nobody could confidently name an owner for. Rather than mandating a fix top-down, he brought the finding back to the team as a shared problem: "We have fifteen single points of failure like the one that just cost us real money. Which of these worry you most?" The team, not Siddharth alone, prioritized the list, and the resulting standard, every business-critical automation needs a named owner and a minimum monitoring bar before launch, came from the team's own prioritization, not an imposed mandate.

The interviewer's note: *"Turned one incident into a systemic finding, and built the fix as something the team owned, not something handed down."* That's the difference this chapter's leadership sections are built around: a senior technical response fixes the bug; an architectural and leadership response fixes the condition that made the bug possible, and does it in a way the team actually adopts rather than resents.

---

## Project

**Goal:** apply this chapter's frameworks to a real or hypothetical architecture decision.

### Tools you'll need

No software specific to this chapter. A whiteboard or diagramming tool for C4 diagrams and architecture sketches; a shared document for Architecture Decision Records; a spreadsheet for ROI and unit-economics calculations, the same skills Chapters 10–11 taught (and Chapter 70 drills), or the Jupyter notebook from Chapter 17 for Q80-016's cells.

1. Write a one-page ADR for a real technical decision you've made or observed, including the context, options considered, and reasoning, not just the final choice.
2. Calculate a real ROI/payback period for one automation or system you're familiar with, using Q80-016's method, net of maintenance.
3. Draft the business-risk-framed pushback you'd give for a real or hypothetical technical disagreement in your own context.
4. Sketch a staged, three-stage architecture roadmap for a system you know, tied to specific growth triggers rather than a single end-state design.

---

## Key terms

CAP theorem · CP vs. AP · PACELC · eventual consistency · durability vs. availability · single point of failure · horizontal vs. vertical scaling · partitioning vs. sharding · leader-follower (primary-replica) replication · failover · individual contributor (IC) · build vs. buy · total cost of ownership (TCO) · lambda architecture · kappa architecture · Architecture Decision Record (ADR) · C4 diagram · Responsible AI review · data governance · principle of least privilege · segregation of duties · showback vs. chargeback · ROI/payback period · influencing without authority · first-90-days plan (architect) · nines of availability · error budget · SLO against SLA · availability in series · independent failure · peak factor · busy hour · utilisation headroom · tail latency · fan-out · hedged request · replication factor · erasure coding · retention policy · Little's Law · load shedding · queueing collapse

---

## Final-week revision list

Q80-001, Q80-006, Q80-009, Q80-011, Q80-016, Q80-017, Q80-020, Q80-022, Q80-023, Q80-024, Q80-030, Q80-031, Q80-035.

The last three are the arithmetic that makes a design argument concrete: what a reliability target costs in minutes (Q80-030), what a chain of services does to it (Q80-031), and why a slow dependency collapses a system rather than merely slowing it (Q80-035).

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 77 and Chapter 78** already cover the technical single-point-of-failure and monitoring concepts this chapter's leadership scenarios examine at the organizational and governance level instead.
- **Chapter 24's storytelling discipline** (sections 24.7 and 24.8) underlies this chapter's board-presentation and stakeholder-pushback questions.
- **Chapters 60–67 of this book** (Part 7: Architecture, Governance & Leadership) teach the techniques this bank draws on, with Chapter 20 (section 20.14) and Chapter 23 (section 23.9) for the time-saving and payback arithmetic; this chapter tests them rather than re-teaching them.
- **Chapter 81, Behavioral, HR & Offer Conversations,** comes next: the leadership stories you rehearsed here (the pushback, the incident that became a standard) are the raw material for its behavioral answers.
