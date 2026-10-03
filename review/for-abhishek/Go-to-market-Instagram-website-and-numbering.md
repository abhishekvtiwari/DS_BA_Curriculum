# Selling the Interview Readiness Book: Instagram, the website, and one numbering system

*Compounza · proposal, 4 October 2026 · for Abhishek, and for whoever builds the website pages.*

What we sell, to whom, how Instagram brings them in, what the website does when they arrive, and
one numbering system that keeps the books, ads and website saying the same thing.

## 1 · What we sell: three products, kept separate

| Product | What the buyer gets | Price | Status |
|---|---|---|---|
| **The Interview Readiness Book** | *Be Interview Ready*: 1,226 data science and analytics interview questions, worked answers, from the online test to the first 90 days | ₹500 (working) | Ready |
| **Add-on: The Three Volumes** | *First Principles*, *The Working Analyst*, *Builder to Architect*, with the practice files | To set | Ready |
| **Add-on: Projects** | Eleven portfolio projects in four tracks, bought one at a time or as track packs | About ₹150 each (working) | Catalogue only; none built |

**The rule that keeps this clean:** each is a separate product with its own page, price and
download. The interview book never requires the volumes; the volumes never require a project. The
add-ons are offered *after* the first purchase and on the book's page, never forced into it.

## 2 · Who we sell to: five audiences

Each audience gets its own ads, its own landing page and its own first product. One message for
everyone is how ad money is wasted.

| Audience | What keeps them up at night | Our hook (from the book) | First buy | Natural add-on |
|---|---|---|---|---|
| **A · Final-year students and freshers** | The online test and the campus drive | "Your answer passed the sample test and scored 2/10. Here's why." (Ch 68A) | Interview book | Analyst starter pack |
| **B · Career switchers** (commerce, ops, finance into data) | "Do I know enough to be hired?" | "Why Python and not just Excel?" asked the human way (Ch 69A) | Interview book | The Three Volumes |
| **C · Working analysts, 1–3 years** | Switching for a better role | "This one line destroys two-thirds of your dates." (Ch 72B) | Interview book | Data-cleaning series, SQL layer |
| **D · BA and MBA aspirants** | No portfolio for a BA role | "'Send me last month's revenue' has four right answers." (Ch 76B) | Interview book | BA requirements pack (P7) |
| **E · Engineers aiming senior** | System design and leadership rounds | "99.9% uptime: how much downtime is that?" (Ch 80) | Interview book | Engineering starter pack |

Every hook is a real, verified finding from the book, so the ad *is* a sample of the product — and
nobody else can run it, because nobody else has the data behind it.

## 3 · Instagram: organic first, then paid

### The organic engine: four post types, every week

| Post type | Example | What it does |
|---|---|---|
| **Predict the output** (carousel) | Show the code, ask "what prints?", answer on the last slide | Saves and shares: people test their friends |
| **The trap** (reel, under 45 seconds) | "Your SQL is correct and still fails the online test" | Reach |
| **The ambiguity drill** (carousel) | A vague manager request, then the three questions a pro asks | Shows judgement, our differentiator |
| **The proof** (single image) | A page from the book, with the real output | Trust: shows nothing is typed by hand |

The 1,226 questions are a year of posts. Each ends with one line to the link in bio, which opens
the landing page for that post's audience.

### Paid ads: small, separate, measured

- **One campaign per audience**, two or three creatives each from its hook. Start with A and C.
- **A small fixed daily budget** you can afford to lose, for about a week before judging; change one
   thing at a time.
- **Judge by cost per sale, not likes**: rupees spent per book sold, against ₹500 minus fees.
- **Kill, keep, scale**, and turn the winning ads into organic posts.

### The rules every ad and post follows

- **No promise of a job, salary or placement.** Promise what is true: 1,226 questions, worked answers.
- **No fake urgency or invented reviews**; real reader comments only, with permission.
- **The ad, the page and the cover use the same words and numbers** (section 5).

## 4 · The website: what happens when someone taps the ad

### The path, one step at a time

| Step | Page | What it must do |
|---|---|---|
| 1 | **Landing page per audience** (`/for/freshers` …) | Repeat the ad's hook first, two real sample pages, one price, one button |
| 2 | **Product page** | What is inside, the free sample, the price; add-ons *below* the buy button |
| 3 | **Free sample** (e.g. §68A.2) | Needs a free account, which builds our audience list |
| 4 | **Checkout** (Razorpay) | One product, one price, clear refund wording |
| 5 | **Library** | Download appears at once; the server confirms it was paid for |
| 6 | **Add-on offer** | After purchase: the volumes, and the project pack for their audience |

### What the website must and must not do

These come from Compounza's existing rules, and they are binding:

- **The server decides who owns what**: a download works only after the server confirms payment.
- **Minimum data**: name, email, password, purchases. Never phone, age, college or employer.
- **Marketing pages public; material behind a free account.** No chat widget; no claim the books do
  not make.

### Two decisions the website needs from you first

- **Selling books on compounza.in at all.** The server's price table today holds only the BA
   course (₹1,999, ₹2,999 and the ₹1,000 step-up); the books would be three new products in it.
- **The Instagram pixel.** The site allows three outside services (our server, Razorpay, an email
   provider); Meta's pixel would be a fourth, which needs your approval. **Recommendation: start
   with tagged links** (`?src=ig&aud=freshers&ad=72b-dates`) recorded with each sale, and add the
   pixel only if they prove not enough.

## 5 · One naming and numbering system

This is what stops the website, the ads and the books from disagreeing.

### One catalogue file, the single source of truth

One file lists every product, chapter, bank, question count, price and page address. The covers
already count from the book this way; the website should read the same file, so "1,226" is never
typed — when the book changes, cover, page and ads change together.

### Numbering: three separate sequences that never mix

| | Today | Proposed |
|---|---|---|
| **Interview Readiness Book** | Chapters 68, 68A, 69, 69A … 82 (letters, and numbers that imply "Book 4") | **Chapters 1–20**, its own sequence |
| **Question codes** | `Q71-093`, tied to the old chapter number | **Topic codes**: `SQL-093`, `CLEAN-022`, `BA-064` — they never change if chapters move |
| **The Three Volumes** | Chapters 1–67, plus 83 at the end | **Chapters 1–68** without a gap (83 becomes 68), one continuous series |
| **Projects** | P1–P11 | **P1–P11**, unchanged |

**Why the volumes keep their numbers:** the interview book points into them **1,263 times**
("Chapter 25, §25.12"), and every one stays correct; the pointers just gain the volume's name.

**Interview book, new chapter (old chapter, question code):**
1 How hiring works (68) · 2 The rounds nobody prepares for (68A, `ROUND`) · 3 The extra-points method
(69) · 4 Why this, not that (69A, `WHY`) · 5 Excel, Sheets and BI (70, `XL`) · 6 SQL (71, `SQL`) ·
7 Python and pandas (72, `PY`) · 8 Data structures and algorithms (72A, `DSA`) · 9 Data cleaning (72B,
`CLEAN`) · 10 Statistics and experiments (73, `STAT`) · 11 Machine learning (74, `ML`) · 12 Product sense
and cases (75, `CASE`) · 13 Data analyst and scientist (76A, `DA`) · 14 Business analyst (76B, `BA`) ·
15 Data engineering (77, `DE`) · 16 Automation (78, `AUTO`) · 17 GenAI and MLOps (79, `AI`) ·
18 Architecture and leadership (80, `ARCH`) · 19 Behavioural, HR and offers (81, `HR`) · 20 Take-homes
and mock interviews (82).

**The work, done once and checked:** the volumes point into the interview chapters only **134
times**. One scripted pass renames chapters and codes, fixes those 134, rebuilds all four PDFs with
their new titles, and the check scripts confirm nothing is missing or pointing nowhere.

## 6 · Decisions, and the order to do this

**Yours to decide:** (1) books on compounza.in; (2) the volumes' and projects' prices; (3) pixel
now, or tagged links first; (4) yes to the renumbering pass.

| When | What |
|---|---|
| **This week** | Renumbering pass and PDF rebuild; the catalogue file; four weeks of organic posts drafted from the book |
| **Next two weeks** | Website: two landing pages (audiences A and C), product page, sample, checkout, library |
| **Then** | Paid ads for A and C; measure cost per sale for two weeks before adding B, D and E |
| **Alongside** | Build project P1, so the first add-on exists when the first buyers arrive |
