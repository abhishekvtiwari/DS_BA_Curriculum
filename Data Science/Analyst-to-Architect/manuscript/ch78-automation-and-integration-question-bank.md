# Chapter 78. Automation & Integration Question Bank

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will learn to:** choose the right automation approach for a given problem, macro, script, low-code tool, or RPA, instead of defaulting to whichever one you know best · design report and alert automations that actually get read · reason correctly about APIs, webhooks, and reverse ETL · build retry and idempotency logic that survives a flaky upstream system · investigate an automation that silently stopped working, the way an interviewer actually wants.
>
> **Before you start:** Chapter 69 (the three answer tiers and the twelve extra-point moves). The questions test Chapters 19–20 (spreadsheet and report automation), 45 and 51 (APIs, webhooks, reverse ETL), 58 and 63 (intelligent automation, automation architecture), with retries from Chapter 29, section 29.9 and the circuit breaker from Chapter 57, section 57.8. This chapter tests those skills; it doesn't teach them again.
>
> **Time needed:** 3.5–4 hours for a first pass (about 10 minutes per core question answered aloud, 1–2 minutes per rapid-fire row, and 30 minutes to run the four code demos yourself); 30 minutes for the final-week list. Section 78.7 adds about an hour.
>
> **How this chapter is built.** Same format as Chapters 70–77: every core question leads with a **"Remember it as…"** hook, a one-line answer, and a compact tier table whose extra points carry Chapter 69's tags (**[+Edge cases]**, **[+Business]** and so on). Rapid-fire sections are scan tables. **Every Python pattern in this chapter was actually executed**, not described from memory: webhook idempotency, rate limiting, retry-with-backoff, and upsert-based CRM sync are all shown with their real output. The order: choosing a tool first, then the basic-but-tricky questions, then the specific automation types (reports, APIs, sync), then failure handling, then a full design case pulling it together.
>
> **Levels and roles.** Each question carries a level and the roles that usually ask it. **Fresher:** screening calls and first-job interviews. **Mid:** one to three years in the role. **Senior:** lead or specialist rounds. **AUT** automation (macro, script and integration) roles · **DA** data analyst · **BA** business analyst · **BI** BI developer · **DE** data engineer.
>
> **Learn it in** pointers name the chapter and section that teach each idea, mainly Chapters 19–20 (spreadsheet and report automation), 45 and 51 (APIs, webhooks, reverse ETL), 57–58 and 63 (automation at scale). In the rapid-fire tables, the last column gives the level and the section numbers.

---

## 78.1 Choosing the right automation approach

### Q78-001 · A stakeholder wants a manual weekly task automated. Walk through how you'd choose between a macro, a script, a low-code tool, and RPA

**Level:** Mid · **Roles:** AUT, DA, BA

**Remember it as:** *The right tool depends on how the task touches its systems: inside one app (macro); across systems with APIs, calling them yourself (script); across systems with APIs that already have ready-made connectors, clicking them together (low-code); or across systems with no API at all, mimicking clicks (RPA). Each one is a step further from "clean" and a step closer to "works on anything."*

**Answer in one line:** A **macro** (VBA, Apps Script) suits automation entirely inside one application; a **script** (Python, calling APIs directly) suits automation across systems that expose clean APIs; a **low-code tool** (Zapier, Power Automate) suits cross-system automation where a visual builder and pre-built connectors save real development time; **RPA** (robotic process automation, simulating clicks and keystrokes) is the last resort for systems with no API and no low-code connector at all, brittle but sometimes the only option.

| Tier | What to say |
|---|---|
| Passes | Names the four options but matches them to tasks only loosely |
| Strong | The four-way decision framework above, correctly matching each option to what it's actually suited for |
| Extra points | + **[+Business]** RPA should be treated as a genuine last resort, not a default: it's the most fragile option, since it depends on a UI's exact layout never changing, and breaks immediately if a vendor redesigns their interface + **[+Edge cases]** the same task can move between categories over time: an RPA solution built because no API existed should be revisited once a real API becomes available, rather than left in place purely out of inertia |

**Likely follow-ups:** When would you choose a low-code tool over writing a script, even though you're capable of writing the script? What's the maintenance cost difference between these four options?
**Red flag:** defaulting to RPA or a macro for a task that a clean, available API would handle far more reliably.
**Learn it in:** Chapter 63, section 63.3 (choosing the right tool for the job); Chapter 20, sections 20.1 (the automation ladder), 20.3 (choosing the delivery tool) and 20.10 (low-code automation); Chapter 51, section 51.10 and Chapter 58, section 58.1 (RPA); macros themselves: Chapter 19. **Practise it with:** Chapter 70, sections 70.5–70.6 (the same platforms, tested there for syntax, here for when to reach for them at all).

### Rapid-fire, 78.1

Roles: AUT, DA and BA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q78-002 | What's the main maintenance risk of a low-code automation platform? | The logic lives inside a third-party tool's UI, often without version control, making it harder to review changes, roll back, or hand off to another person than a plain script would be | **[+Trade-offs]** the speed of building in a low-code tool is a real, genuine advantage; the maintainability trade-off is the honest cost of that speed | Fresher · 20.10, 63.3 |
| Q78-003 | Why might a company deliberately choose a script over a low-code tool even when both could do the job? | Version control, code review, and testing infrastructure the team already has for scripts, plus avoiding a recurring per-automation cost that many low-code platforms charge | **[+Business]** the "cheaper to build" option (low-code) and the "cheaper to maintain at scale" option (a well-engineered script) are often different tools | Mid · 20.3, 63.3 |
| Q78-004 | What's the single biggest failure mode of an RPA-based automation? | Any change to the target application's UI, even a cosmetic one, silently breaks the automation, since it's simulating a specific sequence of clicks tied to a specific layout | **[+Evidence]** an RPA bot that clicks "the third button from the left" breaks the moment a fourth button gets added anywhere before it | Fresher · 51.10, 58.1 |
| Q78-005 | How would you decide whether a task is even worth automating in the first place? | Weigh the time saved per run times how often it runs against the time it would take to build and maintain the automation, including the cost of it eventually breaking | **[+Business]** a task done once a year, however tedious, is rarely worth automating; the same task done daily almost always is | Fresher · 63.2, 20.14 |

---

## 78.2 Basic-but-tricky automation questions

### Q78-023 · Does automating a broken manual process actually fix it?

**Level:** Fresher · **Roles:** AUT, DA, BA

**Remember it as:** *Automating a bad process just makes it fail faster and more consistently. Fix the process, then automate it, not the other way around.*

**Answer in one line:** No: automating a process that's fundamentally flawed (wrong logic, unclear ownership, missing edge-case handling) usually just executes the same flaw faster and more consistently, and can make the underlying problem *harder* to notice, since a human doing the task manually might catch an obviously wrong result before acting on it, while an automation won't.

| Tier | What to say |
|---|---|
| Passes | Says the process should be reviewed first, without saying why |
| Strong | Explicitly names the risk: automation removes the human sanity-check step that was, often invisibly, catching errors before |
| Extra points | + **[+Business]** the right sequence is almost always: understand and fix the process first, *then* automate the corrected version, not automate first and hope problems surface on their own |

**Likely follow-ups:** How would you know, before automating, whether a manual process has a hidden human sanity-check step worth preserving? What would you add to the automated version to replace that lost check?
**Red flag:** treating "we automated it" as inherently synonymous with "we improved it."
**Learn it in:** Chapter 20, section 20.2 (map the flow before you automate); Chapter 58, section 58.10 (when not to automate). **Practise it with:** Chapter 76B, §76B.4 (Q76B-021: as-is vs. to-be).

### Rapid-fire, 78.2

Roles: AUT, DA and BA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q78-024 | Is "no-code" the same thing as "no technical skill required"? | No: a no-code tool removes the need to write syntax, but building a genuinely reliable automation in one still requires the same logical thinking (edge cases, error handling) a script would need | **[+Business]** a poorly-designed no-code automation fails in exactly the same ways a poorly-designed script does, just without a stack trace to help debug it | Fresher · 20.10 |
| Q78-025 | Why might a "quick win" automation built by a single enthusiastic employee become a long-term liability? | If it's undocumented and only that one person understands it, the automation becomes a single point of failure the moment they leave or go on leave, exactly the same risk as an undocumented process | **[+Evidence]** this is one of the most common real sources of "nobody knows why this stopped working" incidents | Fresher · 20.13, 63.8 |
| Q78-026 | Should every manual task with any repetition at all be automated eventually? | No: some tasks are rare enough, or variable enough in their exact steps, that the automation's build and maintenance cost never pays back the time saved | **[+Business]** ask Chapter 58's four questions in order: volume, variability, whether the rules can be written down, and the cost of an error; a task that fails the last one stays manual even at high volume | Fresher · 58.2, 58.10 |
| Q78-027 | What's the risk of over-customizing an automation for one specific stakeholder's exact preferences? | It becomes fragile and hard to extend to a second stakeholder with slightly different needs, and often duplicates logic that should have been one shared, parameterized design | **[+Scale]** with Q78-006's one-template, per-recipient-filter design, a second stakeholder is a new row in the recipient table, not a copy of the automation | Mid · 20.12 |

---

## 78.3 Report and alert automation

### Q78-006 · Design an automated daily MIS email sent to 200 managers, each seeing only their own team's numbers

**Level:** Mid · **Roles:** AUT, DA, BI

**Remember it as:** *One template, one query per recipient (or one query, filtered per recipient), not 200 separately hand-built reports.*

**Answer in one line:** Build one parameterized report template and one data pull that includes every manager's team, then loop over the recipient list, filtering the data to each manager's own scope and rendering the same template with their specific numbers, rather than maintaining 200 separate report definitions.

**Worked structure:**

> "One query pulls every manager's team performance in a single pass, tagged by manager ID. A loop iterates over the 200 managers, filters that single dataset down to each manager's rows, renders a shared HTML template with their specific numbers substituted in, and sends it via a transactional email service, not a personal inbox, so delivery is tracked and rate-limited sensibly. I'd log every send (recipient, timestamp, success or failure) so a manager who says 'I never got mine' can be checked against a real record instead of a guess, and I'd build in a retry for any individual send that fails, without blocking the other 199 emails from going out on time."

| Tier | What to say |
|---|---|
| Passes | One template, but with a hand-maintained recipient list and no failure isolation |
| Strong | The one-template, one-filtered-pull, per-recipient-loop structure above |
| Extra points | + **[+Edge cases]** an individual send failure (a bad email address, a temporary mail server issue) shouldn't block the other 199, exactly the "partial failure isolation" principle from Chapter 77's pipeline design, applied here to email delivery instead of data loading + **[+Business]** the send log is what turns "a manager complains they didn't get it" from a debugging mystery into a two-second lookup |

**Likely follow-ups:** How would you handle a manager who should see two teams' data, not one? What would you monitor to know the whole batch actually completed successfully?
**Red flag:** a design that fails the entire batch if any single recipient's send fails.
**Learn it in:** Chapter 20, sections 20.5–20.6 (the report as an email, sending mail from code safely) and 20.12 (recipients and confidentiality: per-recipient filtering); logging every run: section 20.11; Chapter 19, section 19.7 (the VBA and Outlook version). **Practise it with:** Chapter 70, section 70.5 (the same pattern, tested for syntax).

### Rapid-fire, 78.3

Roles: AUT, DA and BI for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q78-007 | Why does an automated report need a "no news" state, not just "here's today's numbers"? | If a report silently sends nothing when there's genuinely nothing to report (versus when the pipeline feeding it failed), the recipient can't tell the difference between "all quiet" and "broken" | **[+Edge cases]** send a short "no sales were recorded" note on an empty day, so a missing email always means a broken job; see also Q77-031 | Fresher · 20.8, 20.11 |
| Q78-008 | What's the risk of sending an automated alert on every single anomaly, however small? | Alert fatigue (Chapter 77, Q77-032): recipients start ignoring the automation entirely, including the one alert that actually mattered | **[+Business]** tune thresholds deliberately conservative for anything that emails a human directly, rather than flagging every minor fluctuation | Fresher · 20.8, 47.9 |
| Q78-009 | Should a report automation retry immediately on failure, or wait? | Usually wait, with backoff (Q78-017): an immediate retry against a system that's down or overloaded often just adds to the load causing the failure in the first place | **[+Edge cases]** retry only errors that might go away (a timeout, a busy server); a wrong password fails the same way every time | Fresher · 45.9, 46.6; §78.5 |
| Q78-010 | How would you let a stakeholder unsubscribe from an automated report without filing an IT ticket? | Build a simple self-service preference mechanism (a link, a form, a shared settings sheet) rather than requiring a developer to manually edit a recipient list every time | **[+Business]** the absence of self-service unsubscribe is a common, avoidable source of stakeholders quietly filtering the automation to spam instead of asking for changes | Mid · 20.12 |

---

## 78.4 APIs, webhooks, and reverse ETL

### Q78-011 · What's the difference between polling an API and receiving a webhook, and when does each make sense?

**Level:** Mid · **Roles:** AUT, DE

**Remember it as:** *Polling is you repeatedly asking "anything new?" A webhook is the other system calling you the moment something happens, so you never have to ask.*

**Answer in one line:** **Polling** means repeatedly calling an API on a schedule to check for new data, simple to build but wasteful (most calls find nothing new) and inherently delayed by the polling interval; a **webhook** means the source system calls your endpoint the moment an event happens, near-instant and efficient, but requires the source to support webhooks at all and requires you to run a reliably available endpoint to receive them.

| Tier | What to say |
|---|---|
| Passes | "Webhooks are more real-time" (true, no discussion of the trade-off or when polling is still the right choice) |
| Strong | The efficiency-vs-availability trade-off above, with a concrete case for each: polling suits a source with no webhook support, or where a few minutes of delay genuinely doesn't matter; webhooks suit anything needing near-real-time reaction |
| Extra points | + **[+Edge cases]** a webhook can be delivered more than once for the same event (network retries on the sender's side), so the receiving endpoint needs idempotent processing (Q78-012), exactly the same discipline Chapter 77 tests for pipeline loads + **[+Business]** a webhook receiver going down, even briefly, can silently lose events forever unless the sender has its own retry/redelivery mechanism, worth confirming before relying on webhooks alone for anything critical |

**Likely follow-ups:** How would you design a fallback in case your webhook receiver goes down for an hour? *(A scheduled reconciliation sync underneath the webhook: Chapter 51, section 51.7.)* What's a webhook signature, and why does an endpoint need to verify one?
**Red flag:** treating webhook delivery as guaranteed and exactly-once, with no idempotency handling.
**Learn it in:** Chapter 51, sections 51.6 (webhooks: pushing instead of polling, and HMAC signatures) and 51.7 (reconciliation as the safety net); delivery guarantees: Chapter 50, section 50.3. **Practise it with:** Chapter 77, Q77-008.

### Q78-012 · Build a webhook handler that safely processes a "lead created" event, even if the same event gets delivered twice

**Level:** Mid · **Roles:** AUT, DE

**Remember it as:** *Every webhook payload should carry its own unique event ID. Check the ID before processing; record it only once processing has succeeded, ideally in the same transaction.*

**Answer in one line:** Check the incoming event's unique ID against a record of already-processed events before doing any work; if it's already been seen, acknowledge success and skip processing entirely, rather than reprocessing (and potentially duplicating downstream effects like creating a second CRM record).

**Verified, live.** A set of processed IDs stands in for the database table, and a list stands in for the CRM. Before you run it, predict what the second call prints, and how many leads the CRM holds at the end:

```python
processed_ids = set()
crm_leads = []

def process_webhook(event_id, payload):
    if event_id in processed_ids:
        return "skipped (already processed)"
    crm_leads.append(payload)        # the real work: create the lead
    processed_ids.add(event_id)      # record the ID only after the work succeeded
    return f"processed: {payload}"

print(process_webhook("evt_123", "lead created"))
print(process_webhook("evt_123", "lead created"))   # the same event, delivered twice
print("leads in the CRM:", len(crm_leads))
```

```
processed: lead created
skipped (already processed)
leads in the CRM: 1
```

**How it works.**

- `processed_ids` is a set, so `event_id in processed_ids` is an instant membership check (Chapter 33, section 33.2).
- `crm_leads.append(payload)` is the work the event asks for. Only after it succeeds does `processed_ids.add(event_id)` record the ID. If the work raised an error, the ID would never be recorded, so the sender's retry would be processed properly instead of skipped and lost.
- The second call finds `evt_123` already recorded and returns without touching the CRM: one lead, not two.

| Tier | What to say |
|---|---|
| Passes | Knows duplicates can happen and suggests checking the database for an existing record |
| Strong | The event-ID-check pattern above, correctly skipping a genuine duplicate, with the ID recorded only after the work succeeds |
| Extra points | + **[+Validate]** the real output above: the second identical delivery is correctly skipped, and the CRM holds one lead, not two + **[+Business]** in production, `processed_ids` would be a persistent store (a database table), not an in-memory set, since a set held only in memory is lost the moment the process restarts, silently reopening the exact duplicate-processing risk this pattern exists to close + **[+Edge cases]** two copies arriving at the same moment can both pass an in-memory check; a `UNIQUE` constraint on `event_id` in the database closes that race |

**Likely follow-ups:** What HTTP status code should the webhook handler return, and why does that matter to the sender's retry behavior? How would you handle a webhook payload that fails processing partway through? *(Don't record its ID, so the sender's retry processes it again; that's safe only if the work itself can be repeated.)*
**Red flag:** an in-memory-only duplicate check presented as a complete, production-ready solution with no mention of its persistence gap.
**Learn it in:** Chapter 51, sections 51.6 (webhooks: "expect duplicates") and 51.3–51.4 (idempotency keys, and proving a write is idempotent). **Practise it with:** Chapter 77, Q77-007 (idempotent upserts, the same principle applied to a database load instead of an event handler).

### Rapid-fire, 78.4

Roles: AUT and DE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q78-013 | What's reverse ETL, and how is it different from normal ETL/ELT? | Normal ETL/ELT moves data *into* a warehouse for analysis; reverse ETL moves already-transformed, warehouse-computed data (like a churn score) *out* to operational tools (a CRM, an email platform) so business teams can act on it directly in the tools they already use | **[+Business]** reverse ETL is what turns a model's output (Chapters 36–39) into something a sales rep actually sees inside their CRM, not just a table in a warehouse only analysts can query | Fresher · 51.1–51.4 |
| Q78-014 | Why does a reverse ETL sync into a CRM need to be an upsert, not a plain insert? | Re-running the sync (daily, say) would otherwise create a duplicate CRM record for every lead on every single run, instead of updating the existing one's score | **[+Validate]** Q78-028 runs it: `lead_101`'s new score updates the existing record (72 → 80) rather than creating a second one, and the count stays at 3 after a new and an existing lead are synced, and again after a re-run | Mid · 51.4 |
| Q78-015 | What's an API rate limit, and why does an integration need to respect it proactively? | A cap on how many requests a system will accept in a given time window; exceeding it usually gets your requests rejected or your access temporarily blocked, which is worse for the automation than simply pacing itself | **[+Validate]** the limiter below allows 3 calls in a 1-second window, rejects the 4th and 5th, and allows the next call once the window has moved on | Mid · 29.9, 45.9 |
| Q78-016 | What's an API key vs. OAuth, at a level useful for an integration decision? | An API key is a single, simple secret string identifying the calling application; OAuth is a more complex flow granting scoped, revocable, user-specific access without ever sharing the user's actual password | **[+Business]** OAuth is the right choice whenever an integration needs to act *on behalf of a specific user*, not just as an application in general | Mid · 51.3, 52.6 |

### Worked example: a rate limiter (Q78-015)

The plan: remember the times of the calls you allowed; before each new call, forget any that are a full window old; allow the call only if fewer than the cap remain. The times are passed in as numbers of seconds, so the run comes out the same every time; a real limiter passes the clock's current reading instead.

```python
from collections import deque

MAX_CALLS = 3      # at most 3 calls...
WINDOW = 1.0       # ...in any 1-second window
recent = deque()   # times of the calls allowed so far

def allow(now):
    while recent and now - recent[0] >= WINDOW:
        recent.popleft()
    if len(recent) < MAX_CALLS:
        recent.append(now)
        return True
    return False

for t in [0.0, 0.1, 0.2, 0.3, 0.4, 1.05]:
    print(f"call at {t:.2f}s:", "allowed" if allow(t) else "rejected")
```

```
call at 0.00s: allowed
call at 0.10s: allowed
call at 0.20s: allowed
call at 0.30s: rejected
call at 0.40s: rejected
call at 1.05s: allowed
```

**How it works.**

- `deque()` is the double-ended queue from Chapter 33, section 33.4: `append` adds a time at the right, and `popleft()` removes the oldest from the left.
- `MAX_CALLS` and `WINDOW` are the cap: 3 calls per 1.0 second.
- The `while` loop drops every remembered call that is `WINDOW` or more seconds older than `now`; `recent and …` stops it when the deque is empty.
- `len(recent) < MAX_CALLS` asks whether there's room. If there is, the call is remembered and allowed (`True`); if not, it's rejected (`False`) and not remembered.
- At 1.05 s, the call made at 0.00 s is more than a second old, so it's dropped; two remain, and the new call fits.

In an integration, "rejected" means *wait*, not *give up*: the script sleeps until the oldest call leaves the window, then sends. A server that rejects you anyway answers 429, and Chapter 45, section 45.9 retries it after the `Retry-After` wait.

---

## 78.5 Failure handling and monitoring for automations

### Q78-017 · An automation calls a flaky third-party API that sometimes fails transiently. Build retry logic that doesn't hammer the failing service

**Level:** Mid · **Roles:** AUT, DE

**Remember it as:** *Retrying immediately just adds load to a service that's already struggling. Waiting longer after each failure gives it room to recover.*

**Answer in one line:** Use **exponential backoff**: retry after a short delay, and double that delay after each subsequent failure, up to a maximum number of attempts, so a transient blip gets a quick retry while a sustained outage doesn't get hammered with rapid-fire requests that make the underlying problem worse.

**Verified, live, in three cells.** First, a stand-in for the flaky API: it fails on its first two calls and works on the third. A dictionary keeps the call count, so the function can change it:

```python
import time

state = {"calls": 0}

def flaky():
    state["calls"] += 1
    if state["calls"] <= 2:
        raise ConnectionError("service unavailable")
    return "data received"
```

- `import time` gives `time.sleep()`, which the next cell uses to wait.
- `state["calls"] += 1` counts each call. The first two raise `ConnectionError`, Python's built-in error for a failed connection; the third returns a result.

Next, the retry function. It prints what it does, so you can watch it:

```python
def call_with_retry(func, max_attempts=5, base_delay=0.01):
    for attempt in range(1, max_attempts + 1):
        try:
            result = func()
            print(f"succeeded on attempt {attempt}")
            return result
        except ConnectionError:
            if attempt == max_attempts:
                raise
            delay = base_delay * (2 ** (attempt - 1))
            print(f"attempt {attempt} failed, retrying in {delay:.3f}s")
            time.sleep(delay)
```

- `func` is the call to protect, passed in without brackets so that `call_with_retry` can call it. `max_attempts=5` caps the tries; `base_delay=0.01` is the first wait in seconds (tiny here; a real API gets a second or more).
- `range(1, max_attempts + 1)` counts the attempts 1 to 5.
- `except ConnectionError:` catches only that transient error. Anything else (a wrong password, a missing record) isn't caught, so it fails fast instead of being retried.
- `if attempt == max_attempts: raise` gives up on the last attempt. A bare `raise`, with nothing after it, re-throws the error that just happened, so the caller sees the real failure.
- `2 ** (attempt - 1)` is 1, 2, 4, 8…, so the delay doubles after each failure: 0.010 s, then 0.020 s, then 0.040 s.

Before you run it, predict how many lines it prints:

```python
print(call_with_retry(flaky))
```

```
attempt 1 failed, retrying in 0.010s
attempt 2 failed, retrying in 0.020s
succeeded on attempt 3
data received
```

**Reading it.** Two failures, each followed by a longer wait than the last, then success on the third attempt; the last line is `flaky()`'s own result, passed back through. **What happens if you change it:** give it a service that never recovers, and only three attempts:

```python
def always_down():
    raise ConnectionError("service unavailable")

try:
    call_with_retry(always_down, max_attempts=3)
except ConnectionError as err:
    print("gave up:", err)
```

```
attempt 1 failed, retrying in 0.010s
attempt 2 failed, retrying in 0.020s
gave up: service unavailable
```

- `always_down()` raises `ConnectionError` on every call: a service that never comes back.
- `call_with_retry(always_down, max_attempts=3)` allows three attempts instead of five.
- `try:` … `except ConnectionError as err:` catches the error that `call_with_retry` finally re-throws; `as err` names it, so `print("gave up:", err)` can show its message.

The third failure isn't retried: `raise` hands it to the caller, which reports it. Without the cap, this loop would run forever.

| Tier | What to say |
|---|---|
| Passes | Adds a fixed delay between retries, with a cap |
| Strong | The exponential backoff pattern above, with a maximum attempt cap so it eventually gives up rather than retrying forever, and retries only transient errors (429, 503, timeouts), not 400, 401 or 404 |
| Extra points | + **[+Validate]** the real runs above: two failures, each with a longer wait than the last, then success on the third attempt; and a clean give-up when the service never recovers + **[+Edge cases]** a real implementation should add jitter (a small random amount added to each delay) so that if many clients are retrying the same recovering service at once, they don't all retry at exactly the same synchronized moment and cause a new spike |

**Likely follow-ups:** What's the difference between a transient error worth retrying and a permanent one that isn't? How would you decide the maximum number of attempts?
**Red flag:** a retry loop with no delay at all, or no maximum attempt limit, risking an infinite retry loop.
**Learn it in:** Chapter 29, section 29.9 (exponential backoff with jitter); Chapter 45, section 45.9 (which errors to retry, and `Retry-After`); Chapter 46, section 46.6 (retry policies and timeouts); why a retry must be idempotent: Chapter 46, section 46.4.

### Q78-018 · An automation that's run reliably for months silently stopped working last week. Walk through how you'd find out, and how you'd prevent it happening silently again

**Level:** Mid · **Roles:** AUT, DA, DE

**Remember it as:** *"It stopped running" and "it ran but did nothing useful" are two different failures, and the second one is far more dangerous because nothing looks broken from the outside.*

**Answer in one line:** First check whether it's actually still executing at all (a scheduler log, a "last run" timestamp) versus running but silently failing partway through or producing empty/wrong output; then check what changed around the time it stopped (an expired credential, an upstream API change, a permissions change); then, regardless of the specific cause found, add a monitoring check so the *next* silent failure surfaces immediately instead of a week later.

**Worked structure:**

> "I'd check the scheduler first: did it even attempt to run? If yes, I'd check its logs for the actual error, most commonly an expired API token or OAuth credential, a changed API response format, or a permissions change on the target system. If it ran with no error but produced no visible effect, I'd suspect a silent logic issue, like a filter condition that now matches zero rows because of an upstream data change. Either way, once I've found and fixed the specific cause, I'd add a monitoring check (a freshness or heartbeat check, Chapter 47, section 47.5 and Q77-031, applied here to an automation instead of a data pipeline): alert if this automation hasn't successfully completed within its expected window, rather than relying on someone noticing its absence."

| Tier | What to say |
|---|---|
| Passes | Investigates and fixes the immediate cause with no mention of preventing a future silent recurrence |
| Strong | The two-stage diagnosis above (did it run at all vs. did it run but do nothing useful), plus a monitoring fix to close the loop |
| Extra points | + **[+Business]** explicitly distinguishes "stopped executing" from "executed but silently did nothing," since the second is a genuinely harder, more dangerous failure mode to notice: Chapter 46's bad morning (section 46.7), when a load reported "0 new" as if it were a normal quiet day, now applied to a business-facing automation instead of a data pipeline |

**Likely follow-ups:** What's the most common real-world cause of an automation silently failing after months of working fine? How would you design the monitoring alert to avoid false positives on a legitimately quiet day (a holiday, say)?
**Red flag:** fixing the immediate cause with no monitoring added to catch the next occurrence automatically.
**Learn it in:** Chapter 20, section 20.11 (making an automation trustworthy: log every run, alert on failure); Chapter 47, section 47.5 (freshness); Chapter 63, section 63.7 (ownership and runbooks). **Practise it with:** Chapter 77, Q77-028 and Q77-031.

### Rapid-fire, 78.5

Roles: AUT, DA and DE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q78-019 | What's the most common real cause of a previously-working automation breaking without any code change? | An expired credential, API key, or OAuth token; these have finite lifespans and their expiry is rarely tied to any code deployment, so nothing in version control explains the sudden failure | **[+Business]** tracking credential expiry dates proactively (a calendar reminder, a monitoring check) avoids being surprised by this specific, very common failure mode | Fresher · 51.3, 52.6 |
| Q78-020 | Why should an automation log its own successful runs, not just its failures? | Without a positive "last successful run" record, there's no way to distinguish "silently broken for a week" from "just ran successfully an hour ago" | **[+Validate]** a separate check reads the "last successful run" time and alerts when it's too old, so the monitor doesn't depend on the automation remembering to complain; see also Q77-031 | Fresher · 20.11, 47.5 |
| Q78-021 | What's a circuit breaker pattern, in automation terms? | After a certain number of consecutive failures calling an external system, stop trying entirely for a cooldown period, rather than continuing to retry a system that's clearly down | **[+Trade-offs]** trades a short window of "giving up early" against not making a struggling system's outage worse by continuing to hammer it | Mid · 57.8, 58.6, 61.6 |
| Q78-022 | Should an automation's failure alert go to an individual person or a team channel? | Generally a team channel or shared on-call rotation, not one individual, so the automation doesn't silently go unmonitored the day that one person is on leave | **[+Business]** a single point of alerting failure is exactly as fragile as a single point of automation failure | Mid · 63.7 |

On Q78-021: Chapter 57 (section 57.8, exercise 12) described a circuit breaker for calls to a model provider; Chapter 58 (section 58.6) built one that stops a whole batch when too many items fail; Chapter 61 (section 61.6) sets it beside timeouts and retries.

---

## 78.6 Full design case

Q78-006, Q78-018 and Q78-001 are also full design cases; practise them aloud as well.

### Q78-028 · Design case: sync lead scores into the CRM without creating duplicates

**Level:** Senior · **Roles:** AUT, DE

**What they're really testing:** whether the upsert discipline gets applied correctly to a live, operational sync target, not just a data warehouse table.

**Talked through live:** "Each lead needs a stable external ID shared between the scoring system and the CRM, either the CRM's own record ID if the scoring system already knows it, or an agreed common key like email. The sync checks for an existing record by that ID: if found, update its score field; if not, create a new record. This is exactly the upsert pattern from idempotent loads, just targeting a CRM's API instead of a database table."

**Verified, live.** A dictionary stands in for the CRM, keyed by lead ID:

```python
existing_crm_records = {"lead_101": {"score": 72}, "lead_102": {"score": 55}}

def sync_lead_score(lead_id, score):
    if lead_id in existing_crm_records:
        old = existing_crm_records[lead_id]["score"]
        existing_crm_records[lead_id]["score"] = score
        return f"updated {lead_id}: {old} -> {score}"
    existing_crm_records[lead_id] = {"score": score}
    return f"created {lead_id} with score {score}"

print(sync_lead_score("lead_101", 80))
print(sync_lead_score("lead_103", 60))
print("records in the CRM:", len(existing_crm_records))
```

```
updated lead_101: 72 -> 80
created lead_103 with score 60
records in the CRM: 3
```

**How it works.**

- `existing_crm_records` is the CRM: each key is the stable external ID, each value the record.
- `if lead_id in existing_crm_records:` is the "look up by external ID" step. If the lead exists, the function keeps the `old` score for the message and overwrites the score field: an update.
- Otherwise it adds a new record: a create. Update-or-create is the **upsert**.
- `len(existing_crm_records)` counts the records: 3, because `lead_101` was updated in place, not added a second time.

Now the test that matters for a daily sync: run the same writes again.

```python
print(sync_lead_score("lead_101", 80))
print(sync_lead_score("lead_103", 60))
print("records in the CRM:", len(existing_crm_records))
```

```
updated lead_101: 80 -> 80
updated lead_103: 60 -> 60
records in the CRM: 3
```

The second run changes nothing and adds nothing: the sync is safe to repeat.

**Extra-points moves demonstrated:** **[+Signpost]** explicitly connected this to the upsert pattern of idempotent loads rather than treating it as a new problem. **[+Edge cases]** named the stable-external-ID requirement as the actual precondition for this working at all, not an afterthought. **[+Validate]** the real record count (3, not 4), after both runs, proves no duplicate was created.

**Likely follow-ups:** What would you do if the CRM's API doesn't support a native upsert operation, only separate create and update calls? *(Look the lead up by its ID, then `PATCH` the one field or create the record, with an idempotency key on each write: Chapter 51, sections 51.3–51.4.)* How would you handle a lead that exists in the CRM but was deleted from the source scoring system?
**Red flag:** a sync design using a plain "create" call on every run, with no check for an existing record first.
**Learn it in:** Chapter 51, sections 51.3–51.5 (writing through an API, idempotent writes, system of record). **Practise it with:** Chapter 77, Q77-007 (the database version).

---

## 78.7 Predict the number: schedules, retries, and defaults

The rest of this chapter is about deciding what to automate and designing it so it survives. This section is about the arithmetic underneath — the schedule that does not mean what it reads, the retry policy whose total is twenty times longer than anyone intended, and the library default that lets a job hang for a week.

These are cheap questions to ask and they separate people who have run automations in production from people who have written them. Read the setup, say the number, then read on.

**How these were run.** Python 3.12 with `requests` installed. The cron and backoff figures are plain arithmetic you can check by hand; the jitter demonstration uses `numpy` with a fixed seed. The setup for this section:

```python
import inspect, json, socket, urllib.parse
import numpy as np
import requests
```

### Q78-029 · `*/7 * * * *` in cron: does it run every seven minutes?

**Level:** Mid · **Roles:** DE, AE, DA

**Remember it as:** *A cron step restarts at the top of every hour. `*/7` is "minutes divisible by 7", not "every 7 minutes".*

**Answer in one line:** **No** — it fires nine times an hour at minutes 0, 7, 14 … 56, and then waits only **four minutes** until the next hour's zero, so one gap in every nine is short.

```python
minutes = [m for m in range(60) if m % 7 == 0]
gaps = [minutes[i+1] - minutes[i] for i in range(len(minutes)-1)] + [60 - minutes[-1]]
print(f"fires at: {minutes}")
print(f"gaps    : {gaps}")
print(f"runs per hour: {len(minutes)}")
```

```
fires at: [0, 7, 14, 21, 28, 35, 42, 49, 56]
gaps    : [7, 7, 7, 7, 7, 7, 7, 7, 4]
runs per hour: 9
```

Genuinely every seven minutes would be 8.57 runs an hour, which is not a whole number, which is the clue that cron cannot express it. The `*/n` syntax enumerates the values in the field that are divisible by `n`, and the field resets at the hour.

It only matters when the job's duration is close to its interval. A task that takes five minutes is fine on a seven-minute gap and overlaps itself on the four-minute one — once an hour, which makes it look intermittent and random. The same applies to `*/45` on minutes, which fires at 0 and 45 and then waits fifteen; and to `*/5` on the **day of month** field, which fires on the 1st, 6th, 11th … 26th, 31st and then on the 1st again, one day later.

Where the interval must be exact, do not use cron's step syntax. Enumerate the values (`0,7,14,21,28,35,42,49,56`) if that is what you want and be explicit that the last gap is short, or use a scheduler with real interval semantics — an orchestrator's `timedelta(minutes=7)`, or a systemd timer with `OnUnitActiveSec`.

| Tier | What to say |
|---|---|
| Passes | "It runs at minutes divisible by 7" |
| Strong | + the nine runs, the four-minute wrap-around gap, and that a true 7-minute interval is not expressible in cron |
| Extra points | **[+Edge cases]** `*/5` on the day-of-month field skips from the 31st to the 1st, giving a one-day gap · **[+Business]** a five-minute job on this schedule overlaps itself once an hour, which presents as an intermittent fault · **[+Trade-offs]** an orchestrator with interval semantics, or `OnUnitActiveSec`, means what people think `*/7` means |

**Likely follow-ups:** What does `@daily` mean exactly? *(Midnight, in the server's timezone — see Q77-042.)* How do you prevent a job overlapping itself? *(A lock file, or the orchestrator's max-active-runs.)* What is the difference between `0 */2 * * *` and every two hours? *(Nothing, because 24 is divisible by 2 — the bug only appears when the step does not divide the field.)*
**Learn it in:** Chapter 47, section 47.6 (scheduling); Chapter 20, section 20.6.

### Q78-030 · Five retries with exponential backoff from one second. How long before it gives up?

**Level:** Mid · **Roles:** DE, AE

**Remember it as:** *Doubling means the last wait is longer than all the others put together. Five retries is half a minute; eight is four minutes.*

**Answer in one line:** **31 seconds**, not five — the waits are 1, 2, 4, 8 and 16 seconds, and because each is larger than the sum of everything before it, the total is always just under double the final wait.

```python
for base, n in [(1, 5), (1, 8), (2, 5)]:
    waits = [base * 2**i for i in range(n)]
    print(f"base {base}s, {n} retries: {waits}  total {sum(waits)}s")

capped = [min(60, 2**i) for i in range(10)]
print(f"10 retries capped at 60s: total {sum(capped)}s")
```

```
base 1s, 5 retries: [1, 2, 4, 8, 16]  total 31s
base 1s, 8 retries: [1, 2, 4, 8, 16, 32, 64, 128]  total 255s
base 2s, 5 retries: [2, 4, 8, 16, 32]  total 62s
10 retries capped at 60s: total 303s
```

Eight retries — which sounds modest, and which plenty of HTTP client configurations use — is **four and a quarter minutes** of a worker sitting still holding a connection. Ten uncapped would be seventeen minutes.

Three consequences worth naming:

**It can exceed the job's own timeout.** A task with a five-minute limit and eight retries will be killed mid-backoff, so the final attempts never happen and the logs show a timeout rather than the real error.

**It holds resources.** A thread or a database connection asleep for four minutes is a thread not doing work, and under load that is how a retry policy turns one failing dependency into an exhausted connection pool.

**The cap is the important parameter**, not the count. `min(60, 2**i)` keeps ten retries to five minutes instead of seventeen, and it is the line most often left out.

| Tier | What to say |
|---|---|
| Passes | "It's 1 + 2 + 4 + 8 + 16" |
| Strong | + 31 seconds, that the total is always about twice the last wait, and what eight retries costs |
| Extra points | **[+Scale]** backoff holds a worker or a connection for its whole duration, so a retry storm exhausts a pool · **[+Edge cases]** the total can exceed the task's own timeout, so the last retries never run and the error is reported as a timeout · **[+Trade-offs]** cap the individual wait, and set a total deadline rather than a retry count · **[+Business]** retry only what is safe to repeat; a non-idempotent POST retried five times can create five records (Q78-012) |

**Likely follow-ups:** Which errors should you *not* retry? *(4xx other than 429 — the request is wrong and will stay wrong.)* What is a budget-based retry? How does this interact with a circuit breaker? *(Q78-021 — the breaker stops you retrying a dependency that is already known to be down.)*
**Learn it in:** Chapter 78, Q78-017 (retry logic); Chapter 47, section 47.7.

### Q78-031 · A thousand clients hit a failing API and all retry after exactly two seconds

**Level:** Brain-racking · **Roles:** DE, AE

**Remember it as:** *A fixed backoff synchronises everyone. The failure becomes a metronome, and the recovering server is hit by the whole crowd at once.*

**Answer in one line:** **All 1,000 arrive in the same instant** — a fixed delay preserves the synchronisation the outage created, where full jitter spreads the same thousand retries so that no quarter-second holds more than 137 of them.

```python
rng = np.random.default_rng(78)
n = 1000
no_jitter   = np.full(n, 2.0)
full_jitter = rng.uniform(0, 2.0, n)

for name, arr in [("no jitter", no_jitter), ("full jitter", full_jitter)]:
    hist, _ = np.histogram(arr, bins=np.arange(0, 2.25, 0.25))
    print(f"{name:<12} busiest 0.25s bucket: {hist.max():4d} of {n}   {hist.tolist()}")
```

```
no jitter    busiest 0.25s bucket: 1000 of 1000   [0, 0, 0, 0, 0, 0, 0, 1000]
full jitter  busiest 0.25s bucket:  137 of 1000   [116, 112, 129, 118, 135, 126, 127, 137]
```

A **7.3× reduction in peak load** from one line of code, and nothing else changed — same number of retries, same average delay.

The mechanism is worth stating because it is counter-intuitive: the outage itself is what synchronises the clients. They were spread out before, they all failed at the same moment, and a deterministic backoff preserves that alignment forever. Each retry round arrives as a single spike, which is often enough to knock over a server that had just come back, producing the next synchronised failure. That is the **thundering herd**, and it is how a brief outage becomes a long one.

Full jitter — `random.uniform(0, backoff)` rather than `backoff` — is the standard fix, and note what it does to the *average* wait: it halves it. So jitter is not merely politer, it recovers faster on average as well as spreading load.

This is also why "all our retries are exponential" is not on its own a good answer. Exponential backoff without jitter still synchronises; it just synchronises at wider and wider intervals.

| Tier | What to say |
|---|---|
| Passes | "You should add jitter" |
| Strong | + names the thundering herd, explains that the outage is what synchronises the clients, and reads off the peak reduction |
| Extra points | **[+Scale]** full jitter also halves the mean wait, so it recovers faster as well as spreading load · **[+Edge cases]** exponential backoff *without* jitter still synchronises, just at wider intervals · **[+Business]** the spike often re-breaks a server that had recovered, turning a 30-second outage into a 10-minute one · **[+Trade-offs]** decorrelated jitter is slightly better again, at the cost of being harder to explain |

**Likely follow-ups:** What is decorrelated jitter? Where else does the thundering herd appear? *(Cache expiry — a popular key expiring sends every request to the database at once.)* How does a circuit breaker help?
**Learn it in:** Chapter 78, Q78-017; Chapter 61, section 61.5 (resilience).

### Q78-032 · `requests.get(url)` with no `timeout`. How long can it hang?

**Level:** Mid · **Roles:** DE, AE, DA

**Remember it as:** *There is no default timeout. Not a long one — none. The call waits as long as the network will let it.*

**Answer in one line:** **Forever** — `requests` defaults `timeout` to `None`, and Python's socket default is also `None`, so a request to a server that accepts the connection and then goes quiet will block until the OS gives up, which can be hours.

```python
import inspect, socket, requests

print(f"requests timeout default: "
      f"{inspect.signature(requests.Session.request).parameters['timeout'].default!r}")
print(f"socket.getdefaulttimeout(): {socket.getdefaulttimeout()}")
```

```
requests timeout default: None
socket.getdefaulttimeout(): None
```

Two `None`s. Nothing in the stack will interrupt the call.

The failure mode is specific and worth describing, because it is not the one people picture. A server that is *down* is harmless: the connection is refused immediately and you get an error in milliseconds. The dangerous server is the one that is **up and wedged** — it completes the TCP handshake and then never sends a byte. Your code is now waiting on a socket that will never deliver, and the scheduler sees a task that is still "running".

That is how a daily job is found three days later still holding the lock, with the next three runs skipped because the orchestrator would not start a second instance.

Always pass a timeout, and pass both halves of it:

```python
requests.get(url, timeout=(3.05, 27))   # (connect timeout, read timeout)
```

The connect timeout should be short — a few seconds is generous for establishing a connection. The read timeout is per-chunk, not for the whole response, which is the detail most people get wrong: a server that dribbles out one byte every twenty seconds never trips a 27-second read timeout. For a hard ceiling on total duration you need your own deadline around the call.

| Tier | What to say |
|---|---|
| Passes | "You should always set a timeout" |
| Strong | + that the default is `None` and means no limit at all, and that the dangerous case is a server that accepts and then stalls, not one that is down |
| Extra points | **[+Edge cases]** the read timeout is between bytes, not for the whole response, so a slow trickle never trips it · **[+Business]** a hung job holds its lock and silently skips the next runs, which reads as "the job stopped" rather than "the job is stuck" · **[+Validate]** an alert on run *duration*, not only on failure, catches this; a job that has not finished is not the same as a job that failed (Q78-018) · **[+Scale]** without timeouts, one slow dependency exhausts a connection pool and takes down things that do not depend on it |

**Likely follow-ups:** What is the difference between the connect and read timeouts? How would you enforce a total deadline? What should the orchestrator do about a task that never finishes? *(An execution timeout, which is a separate setting from the retry policy.)*
**Red flag:** assuming a sensible default exists. It is the most common missing line in integration code.
**Learn it in:** Chapter 78, Q78-017; Chapter 20, section 20.5 (calling an API).

### Q78-033 · A JSON API returns `"order_id": 9007199254740993`

**Level:** Brain-racking · **Roles:** DE, AE

**Remember it as:** *JSON has one number type and JavaScript reads it as a float64. Past 2⁵³, ids change value in transit — in the browser, not on your server.*

**Answer in one line:** Python reads it **exactly**, but any JavaScript consumer reads it as **9007199254740992** — the id changes by one between your server and the browser, with no error at either end.

```python
raw = '{"order_id": 9007199254740993, "amount": 1500.10}'
d = json.loads(raw)

print(f"python  : {d['order_id']}  exact: {d['order_id'] == 9007199254740993}")
print(f"as JS   : {int(float(d['order_id']))}")
print(f"re-dumped: {json.dumps(d)}")
```

```
python  : 9007199254740993  exact: True
as JS   : 9007199254740992
re-dumped: {"order_id": 9007199254740993, "amount": 1500.1}
```

Python's `int` is arbitrary precision, so the server side is fine and every test you write in Python will pass. JavaScript has a single `number` type, which is a float64, so `JSON.parse` of that same payload gives a different id — the same 2⁵³ limit as Q77-037, arriving through the wire format instead of through a dataframe.

The consequences are the kind that take a long time to diagnose, because the data is correct everywhere you look:

- A dashboard links to order ...992, which either 404s or opens **someone else's order**.
- A webhook signature computed over the id fails verification, because the two sides serialised different numbers.
- Two different orders in the same page can collapse to one key in a front-end list.

Notice also the third line: `1500.10` came back as `1500.1`. JSON has no decimal type, so trailing zeros are not preserved and money should not be sent as a JSON number if the exact representation matters.

The fix is boring and universal: **send large ids as strings.**

```json
{"order_id": "9007199254740993", "amount": "1500.10"}
```

Twitter did this in 2010 and published an `id_str` field beside `id` for exactly this reason; most large APIs have done the same since.

| Tier | What to say |
|---|---|
| Passes | "Big numbers lose precision in JSON" |
| Strong | + that the loss happens in the *JavaScript consumer* rather than in JSON itself, names 2⁵³, and gives "send ids as strings" as the fix |
| Extra points | **[+Business]** a link to the wrong order is worse than a broken link, because it is a data-exposure issue, not a 404 · **[+Edge cases]** JSON has no decimal type either, so `1500.10` comes back as `1500.1` and money belongs in a string · **[+Validate]** a signature or checksum over a payload containing a big integer will fail across languages · **[+Scale]** Snowflake-style and timestamp-derived ids are routinely 18 to 19 digits, so this is the normal case now |

**Likely follow-ups:** Why does Twitter's API have `id_str`? What about 64-bit integers in Protobuf? *(The JSON mapping also encodes them as strings, for this reason.)* How would you detect this in testing? *(Test with an id above 2⁵³; a small test id will never reveal it.)*
**Learn it in:** Chapter 77, Q77-037; Chapter 20, section 20.5 (APIs).

### Q78-034 · `unquote(quote_plus("North America +1"))`

**Level:** Mid · **Roles:** DE, AE

**Remember it as:** *In a query string a space is `+` and a real plus is `%2B`. Encode and decode with the matching pair, or the plus eats the space.*

**Answer in one line:** **`'North+America++1'`** — the encoder turned spaces into `+` and the plus into `%2B`, but `unquote` does not know that `+` means space, so the spaces come back as literal plus signs and the value is corrupted.

```python
v = "North America +1"
print(f"quote()      -> {urllib.parse.quote(v)}")
print(f"quote_plus() -> {urllib.parse.quote_plus(v)}")
print(f"unquote(quote_plus(v))      -> {urllib.parse.unquote(urllib.parse.quote_plus(v))!r}")
print(f"unquote_plus(quote_plus(v)) -> {urllib.parse.unquote_plus(urllib.parse.quote_plus(v))!r}")
```

```
quote()      -> North%20America%20%2B1
quote_plus() -> North+America+%2B1
unquote(quote_plus(v))      -> 'North+America++1'
unquote_plus(quote_plus(v)) -> 'North America +1'
```

Two encodings, and they are not interchangeable. `quote` is for a URL **path**, where a space is `%20`. `quote_plus` is for a **query string** value, where a space is `+` by the form-encoding convention. Mix the pairs and you get the result above: a value that is not what was sent, and that still looks like a plausible string, so nothing downstream complains.

Where it reaches production is phone numbers (`+91 98765 43210` is the worst possible case — a plus *and* spaces), email addresses with a `+` tag, and any free-text filter passed to a reporting API.

In practice you should not be calling either function by hand. Let the library build the query string:

```python
requests.get(url, params={"region": "North America +1"})
```

`params=` encodes each value correctly, and the server's framework decodes with the matching function. Hand-assembled query strings are the only place this bug lives.

| Tier | What to say |
|---|---|
| Passes | "It's a URL-encoding mismatch" |
| Strong | + names which function belongs to the path and which to the query string, and that `+` means space only in a query |
| Extra points | **[+Business]** phone numbers in E.164 format are a plus followed by digits, so this corrupts exactly the field you least want corrupted · **[+Edge cases]** an email with a `+` tag becomes a space, so the address silently stops matching · **[+Validate]** pass `params=` and let the client encode, rather than building the string · **[+Edge cases]** a value containing `&` or `=` splits the query into extra parameters, which is the same bug with a worse ending |

**Likely follow-ups:** What happens if the value contains `&`? Which encoding does a browser form use? *(`application/x-www-form-urlencoded`, the `+` one.)* What about encoding a path segment containing a slash?
**Learn it in:** Chapter 20, section 20.5 (calling an API); Chapter 64, section 64.2.

### Q78-035 · "100 requests per minute." Can you send 100 in one second?

**Level:** Brain-racking · **Roles:** DE, AE

**Remember it as:** *It depends entirely on how the limit is counted, and the commonest implementation lets you send double the limit across a window boundary.*

**Answer in one line:** **It depends on the algorithm, and under the most common one you can send 200 in two seconds** — a fixed window resets at the minute mark, so 100 requests at 10:00:59 and another 100 at 10:01:00 both pass while neither minute ever exceeds 100.

| Algorithm | 100 in one second? | The burst it permits |
|---|---|---|
| **Fixed window** | Yes, if the window has room | 200 across a boundary, in as little as two seconds |
| **Sliding window / log** | No | Exactly 100 in any 60-second span |
| **Token bucket** | Up to the bucket size | Bucket size as a burst, then a steady 100/60 per second |
| **Leaky bucket** | No | Strictly paced output, whatever the input |

The fixed-window boundary burst is the one to be able to describe, because it is the most widely deployed limiter and the behaviour surprises both callers and implementers. Nobody exceeded the stated limit; the server still received twice the rate it was sized for.

What it means on each side of the integration:

**As the caller**, you cannot infer your safe rate from the stated limit. 100 per minute does not license 1.67 per second, and it does not license 100 at once. Pace yourself below the limit, read the `X-RateLimit-Remaining` and `Retry-After` headers when the API sends them, and treat 429 as routine rather than exceptional.

**As the implementer**, a fixed window is simple and cheap and leaves you exposed to twice your intended peak. A token bucket costs one counter and a timestamp per client and gives a defined burst with a defined steady rate, which is usually what you actually meant.

And note how this compounds with Q78-031: a 429 that triggers an un-jittered retry sends the same synchronised crowd back at the same moment.

| Tier | What to say |
|---|---|
| Passes | "It depends on how the rate limit works" |
| Strong | + names fixed window against token bucket, and the boundary burst of 200 in two seconds |
| Extra points | **[+Business]** the caller cannot derive a safe rate from the headline number; read the headers · **[+Scale]** a fixed window means capacity planning must assume twice the stated limit · **[+Edge cases]** 429 plus un-jittered retry is a thundering herd generator (Q78-031) · **[+Trade-offs]** a token bucket gives an explicit burst allowance, which is usually the intended behaviour |

**Likely follow-ups:** What do `X-RateLimit-*` headers tell you? How would you implement a shared limit across several workers? *(A central counter — Redis, typically — because per-process limits do not compose.)* What is the difference between throttling and backpressure? *(Q77-022.)*
**Learn it in:** Chapter 78, Q78-015 (rate limits); Chapter 61, section 61.5.

### Rapid-fire, 78.7: automation arithmetic and defaults

Roles: DE, AE and DA for every row.

| # | Question | The answer, and why | Extra point |
|---|---|---|---|
| Q78-036 | A job runs at 00:05 for "yesterday", computed from `date.today()`. It runs late at 00:02 the next day. | It asks for the wrong day and skips one entirely. Take the logical date from the orchestrator, never from the clock | **[+Business]** this is why every orchestrator supplies an execution date → Ch 77 Q77-051 |
| Q78-037 | An HTTP 200 response with `{"status": "error"}` in the body | `raise_for_status()` passes, because the transport succeeded. Check the body as well as the code | **[+Validate]** many older APIs return 200 for everything → Ch 20 §20.5 |
| Q78-038 | Retrying a POST that creates a record, after a timeout | May create a second record: you do not know whether the first one succeeded. Use an idempotency key | **[+Edge cases]** a timeout is the one failure where you cannot tell what happened → Q78-012 |
| Q78-039 | An automated email to 200 managers, each with their own 2 MB attachment | 400 MB of attachments in one run, and most mail servers cap a single message at 10–25 MB. Link to a report instead of attaching it | **[+Business]** attachments also leak data when forwarded → Q78-006 |
| Q78-040 | A CSV attachment opened in Excel before anyone looks at it | Leading zeros gone, long ids in scientific notation, dates re-interpreted by locale. The file was fine; Excel changed it | **[+Edge cases]** `dd/mm` against `mm/dd` silently swaps the first twelve days of a month → Ch 77 Q77-036 |
| Q78-041 | An API key in the script, committed to a private repository | Still a leak: every clone, every CI log, every future contributor. Rotate it; private is not secret | **[+Business]** git history keeps it even after you delete the line → Ch 26 §26.5 |
| Q78-042 | A sync that runs every 5 minutes and takes 7 minutes | Overlapping runs competing for the same rows, duplicating work or deadlocking. Take a lock, or cap concurrent runs at one | **[+Validate]** a run duration alert catches this before the data does → Q78-018 |
| Q78-043 | Does a webhook that returns 500 get redelivered? | Usually yes, with backoff — so your handler must be idempotent, and must return 2xx *after* the work is durable, not before | **[+Edge cases]** returning 200 then crashing loses the event with no retry → Q78-012 |
| Q78-044 | A daily sync comparing "rows changed since yesterday" using local timestamps across two systems | Clock skew and timezone differences give gaps or overlaps. Normalise to UTC and allow an overlap window | **[+Edge cases]** NTP drift of a few seconds is enough on a per-second watermark → Ch 77 Q77-040 |
| Q78-045 | An alert that fires on every failed run of a job that retries | Three alerts for one incident, and alert fatigue. Alert on the final failure, or on a duration or freshness breach | **[+Business]** the cost of noise is a real alert ignored → Q78-032 |

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Defaulting to RPA or a macro regardless of fit | A fragile automation where a clean API would have worked | Match the tool to how the task actually touches its systems (§78.1) |
| An immediate, no-delay retry loop against a flaky API | Adds load to an already-struggling service, can worsen an outage | Exponential backoff with a maximum attempt cap |
| A webhook handler with no duplicate-event check | A duplicate delivery creates a duplicate downstream record | Check a unique event ID before processing, persisted, not in-memory only |
| A CRM sync using plain "create" every run | Duplicate records pile up on every sync cycle | Upsert by a stable external ID |
| No monitoring for an automation's own silent failure | A break goes unnoticed for days or weeks | Alert on absence of a successful run, not just on explicit errors |
| Automating a broken process as-is | The flaw executes faster and more consistently, harder to notice | Fix the process first, then automate the corrected version |
| One person quietly owning an undocumented "quick win" automation | A single point of failure when that person is unavailable | Document ownership and logic; don't let critical automation live in one person's head |
| Reading `*/n` in cron as 'every n' | One short gap per cycle, so a long job overlaps itself once an hour | Enumerate the values, or use a scheduler with interval semantics (Q78-029) |
| An uncapped exponential backoff | Eight retries is four minutes of a worker doing nothing, and may outlast the task timeout | Cap the individual wait and set a total deadline (Q78-030) |
| Retrying on a fixed delay | Every client returns at the same instant and re-breaks the recovering service | Full jitter: `uniform(0, backoff)` (Q78-031) |
| Calling an HTTP API with no timeout | The default is no limit; a stalled server hangs the job for days while it still looks 'running' | `timeout=(connect, read)` on every call, plus a duration alert (Q78-032) |
| Sending ids over 2⁵³ as JSON numbers | The id changes value in any JavaScript consumer, linking to the wrong record | Send large ids as strings (Q78-033) |
---

## In the real world: the automation that broke because of a renamed column

Meera is asked in an interview to describe debugging a real automation failure. She describes a weekly commission-calculation automation that had run correctly for over a year, then started producing wrong numbers, not failing outright, just quietly wrong, which took two pay cycles to notice because nobody was checking the automation's output against a manual calculation anymore, exactly the trust that made the automation valuable in the first place also made its silent failure harder to catch.

She traces it to a source spreadsheet where someone had renamed a column from "Discount %" to "Discount Percentage," and her script had been reading that column by its exact name. The rename didn't break the script outright, since the script's error handling silently defaulted a missing column to zero rather than crashing, meaning discounts were being read as zero for every single row for two full pay cycles, quietly inflating every calculated commission.

The interviewer's follow-up: what did she change? Her answer: two things, not one. First, the immediate fix: read the column by name, and fail loudly with a clear message if that name isn't found, instead of silently defaulting to zero. Second, and the part she says mattered more: "I stopped treating 'the automation ran without an error' as proof it worked correctly. Now it validates its own output against a rough expected range before sending anything downstream, so a silently wrong result gets caught the same day, not two pay cycles later." That's this chapter's whole method: the fix for the specific bug matters less than the systemic change that catches the *next* silent failure automatically.

---

## Project

**Goal:** apply this chapter's method to a real automation of your own.

### Tools you'll need

**Python** for scripted automation and API integration; **VBA/Apps Script** (Chapter 19) for in-application macros; common low-code platforms (Zapier, Power Automate, Make; Chapter 20, section 20.10) for cross-system automation without custom code; a scheduler (cron, Chapter 20, section 20.7, or an orchestrator such as Dagster, Chapter 46) for anything running on a timer. Every code pattern in this chapter uses only Python's standard library (`time` and `collections`), so it runs in the environment Chapter 17 set up, with nothing new to install.

1. Pick one manual, repetitive task from your own work and run it through Q78-001's decision framework: which of the four approaches actually fits, and why.
2. Add retry-with-backoff logic to one real script you have that calls an external system, and test that it actually waits longer between successive failures.
3. Add a duplicate-event or duplicate-record check to one integration you maintain, and prove (the way Q78-012 and Q78-028 did) that running it twice doesn't create a duplicate.
4. Write the monitoring check you'd add to catch your most critical automation silently failing, and say specifically what "silently failing" would look like for that one.

---

## Key terms

macro vs. script vs. low-code vs. RPA · report automation · alert fatigue · polling vs. webhook · webhook idempotency · reverse ETL · API rate limit · API key vs. OAuth · exponential backoff · jitter · circuit breaker · silent failure · monitoring (absence of success) · upsert (in an integration context) · single point of failure (undocumented automation) · cron step syntax (`*/n`) · wrap-around gap · exponential backoff · backoff cap · total deadline · jitter (full, decorrelated) · thundering herd · connect timeout against read timeout · idempotency key · fixed window against token bucket · boundary burst · `429 Too Many Requests` · `Retry-After` · 2⁵³ in JSON · `id_str` · percent-encoding against form-encoding (`quote` / `quote_plus`) · logical (execution) date · overlapping runs

---

## Final-week revision list

Q78-001, Q78-006, Q78-011, Q78-012, Q78-013, Q78-017, Q78-018, Q78-023, Q78-028, Q78-030, Q78-031, Q78-032.

The last three are the ones that turn a small fault into a long outage: what a retry policy actually costs in wall-clock time (Q78-030), why un-jittered retries re-break a server that had recovered (Q78-031), and the missing timeout that leaves a job hanging for days (Q78-032).

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 77, Data Engineering & Data System Design Bank,** already covers idempotency, delivery guarantees, and monitoring from the data-pipeline angle; this chapter applies the identical discipline to business-facing automation and integrations. Retries with backoff are taught in Chapter 45, section 45.9 and Chapter 29, section 29.9.
- **Chapter 63, section 63.3, and Chapter 20, sections 20.1, 20.3 and 20.10,** teach the tool choice behind §78.1, and Chapter 51, section 51.10 and Chapter 58, section 58.1 cover RPA; **Chapter 70, sections 70.5–70.6,** test the VBA/Apps Script syntax this chapter's framework helps decide when to actually reach for.
- **Chapter 76B, §76B.4 (Q76B-021),** tests the as-is-before-to-be discipline this chapter's Q78-023 reuses for automation; Chapter 20, section 20.2 teaches it.
