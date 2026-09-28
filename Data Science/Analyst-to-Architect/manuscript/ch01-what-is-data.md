# Chapter 1. What Is Data?

*Part 0 — First Principles: Data from Zero*

> **Chapter at a glance**
>
> **You will learn to:** explain what data is, and how it differs from information, knowledge, and insight · turn everyday records, like a shop receipt, into rows and columns · name the type of any value (number, text, date, true/false) and spot numbers that aren't really numbers · tell qualitative from quantitative data, and discrete from continuous · use the four levels of measurement to decide which calculations make sense · recognize structured, semi-structured, and unstructured data · read and write metadata · say where data comes from · judge whether a small dataset is fit to use.
>
> **Before you start:** nothing. This chapter assumes no technical knowledge at all.
>
> **Time needed:** 3–4 hours, including the exercises and the project.
>
> **Tools:** a pen and a notebook are enough. If you already have Excel or Google Sheets, you can use it for the project, but you don't need to.
>
> **Practice data:** your own week of spending, plus small examples from Riverstone Supplies, the fictional company you'll follow through this book.

---

## Why this matters

Every job in this book, from a junior analyst's first report to an architect's design for a whole company, is built on one raw material: **data**. Tools change every few years. Spreadsheets gave way to databases, databases to cloud warehouses, and now AI assistants can write the formulas for you. The raw material stays the same.

That's why this chapter comes before any tool. People who skip it can learn the buttons in Excel or the words in SQL, the language for asking a database questions, and still produce reports that are confidently wrong: an "average" of PIN codes, a customer counted twice because their name was typed in capitals, a sales total that silently left out every blank row. These mistakes aren't about software. They come from not asking basic questions about the data first: *What does each value mean? What kind of value is it? What calculations does it allow? Where did it come from? Can I trust it?*

By the end of this chapter you'll ask those questions automatically. It's a small habit, and it's the one that experienced analysts are quietly relying on every time they say, "Wait, that number doesn't look right."

---

## In plain English

Picture the owner of a small grocery shop in your neighborhood. Next to the till is a thick notebook. Every time a regular customer buys on credit, the owner writes a line: the date, the customer's name, what they bought, and how much they owe. When the customer pays, another line goes in.

- Each **line** in that notebook is a small, recorded fact. That's **data**.
- At the end of the month, the owner adds up what each customer owes and sees that Mrs. Joshi owes ₹2,400. That total is **information**: data organized to answer a question.
- Over the years, the owner notices that customers who owe more than ₹3,000 often stop coming, because they feel embarrassed. That's **knowledge**: an understanding of *why* things happen.
- So the owner decides to send a friendly reminder whenever anyone's balance passes ₹2,500, before it becomes awkward. That's **insight** turned into action.

Now notice two more things about the notebook. First, the owner writes every line **the same way**: date first, then name, then items, then amount. That consistent layout is what makes adding things up possible. Second, some lines are hard to use: a smudged amount, a name written as "Joshi aunty" one day and "Mrs. Joshi" the next. That's a **data quality** problem, and every business, from this shop to the largest bank, has the same problem at a bigger scale.

Everything in this chapter is a version of that notebook.

> **Meet Riverstone.** Riverstone Supplies is the fictional company you'll follow through this book. It makes and sells plastic storage boxes, kitchenware, industrial crates, and a small range of furniture to shops, hotels, and wholesalers. It has two plants, at Taloja and Chakan, and one warehouse, at Bhiwandi.
>
> You'll practice on two of its datasets:
>
> - **The mini database:** 12 orders from January to March 2026, small enough to check by eye. Chapters 1–5 and 12 use it.
> - **The one-year database:** all of 2025, 173 orders plus 2 that were cancelled. You'll use it from Chapter 4 onward.
>
> Every table and figure of Riverstone numbers says which of the two it comes from. These are the people you'll meet:
>
> | Who | Role | First met in |
> |---|---|---|
> | Meera Iyer | sales coordinator | Chapter 1 |
> | Anita Rao | Sales Head | Chapter 1 |
> | Vikram Singh | Sales Manager | Chapter 3 |
> | Neha Kulkarni, Rahul Mehta, Farah Khan | sales executives | Chapters 1–2 |
> | Suresh Menon | Finance Manager | Chapter 3 |
> | Imran | ran sales operations before Meera joined | Chapter 2 |

---

## 1.1 What data actually is

**Data is a recorded observation about the world.** Something happened, someone or something noticed it, and a note was made that can be looked at later.

Three parts of that definition matter:

1. **Observation.** Data describes something: a sale, a temperature, a step, a click, an opinion.
2. **Recorded.** A thought in your head isn't data until it's written, typed, photographed, or saved. The recording is what lets other people, and computers, use it.
3. **Later use.** Data is kept because someone expects to look at it again: to add it up, compare it, check it, or prove something.

You create and use data all day, usually without calling it that:

| Everyday thing | The data in it |
|---|---|
| A shop receipt | what you bought, how many, at what price, when, and how you paid |
| Your phone's step counter | a count of steps for each hour and each day |
| A train timetable | train numbers, stations, and arrival and departure times |
| A class attendance register | each student, each date, present or absent |
| A food-delivery app | the restaurant, the items, the delivery address, the time taken, your rating |
| A photo on your phone | the picture itself, plus the date, time, and often the place it was taken |

In the singular, one recorded value is sometimes called a **datum**, but almost everyone, including this book, simply says "data" for one value or many.

> **Try it.** Look at your phone for thirty seconds. Name five kinds of data it recorded about you today without you typing anything. (Some ideas: steps, screen time, battery use, location, photos, missed calls.)

---

## 1.2 From data to information, knowledge, and insight

People often use *data* and *information* as if they mean the same thing. In data work, the difference matters, because your job is to move up from one to the next. A common way to picture it is a four-step ladder, sometimes called the **DIKW** model (data, information, knowledge, wisdom). This book uses *insight* for the top step, because that's the word businesses use.

| Step | What it is | The question it answers |
|---|---|---|
| **Data** | raw recorded facts | What was recorded? |
| **Information** | data organized, summarized, or put in context | What happened? |
| **Knowledge** | an understanding of patterns and causes | Why did it happen? |
| **Insight** | a conclusion that points to an action | So what should we do? |

Here's the ladder with real numbers from Riverstone's mini database.

![The ladder from data to insight, with Riverstone's first quarter](figures/fig1-1-data-to-insight.svg)

*Figure 1.1 — The same twelve orders at four levels of usefulness. Mini database (Jan–Mar 2026).*

- **Data.** Riverstone's system holds twelve orders from January to March 2026. Each has an order number, a customer, a date, and a status such as *Delivered*, *Shipped*, or *Pending*. On their own, twelve rows tell a manager nothing.
- **Information.** Add up the value of delivered and shipped orders for each month: January ₹1,04,210, February ₹1,61,700, March ₹31,800. Now there's a clear message: March fell by 80% compared with February.
- **Knowledge.** Look closer and you learn *why*. Most of Riverstone's revenue comes from a few big wholesale orders, and none were placed in March. One more March order, worth ₹26,220, exists but is still *Pending*, so it isn't counted yet.
- **Insight.** So March is not the collapse the headline number suggests. The useful actions are to ship the pending order before the quarter closes, and to call the big wholesale buyers this week to find out why they haven't reordered.

Notice what made each step possible. Information needed a **question** ("how much did we sell each month?") and a **rule** ("count only delivered and shipped orders"). Knowledge needed a closer look at **detail and context**. Insight needed **judgment about the business**. Tools help most with the first step; your value as an analyst grows as you climb.

> **Watch out: a number is not an insight.** "March revenue: ₹31,800" is information. Reports that stop there leave the reader to guess what it means, and people often guess wrong. Add the "why" and the "so what" before you send it.

---

## 1.3 Records, fields, and datasets

Data becomes easy to use when it's arranged in a **table**: a grid of rows and columns. Almost every tool in this book, from spreadsheets to databases to Python, a programming language, works with tables.

Here's a receipt from a neighborhood store, and the same receipt as a table.

![A shop receipt turned into a table, one row per item](figures/fig1-2-receipt-to-table.svg)

*Figure 1.2 — Each line on the receipt becomes a row; each kind of detail becomes a column.*

The vocabulary:

- A **row** (also called a **record**) holds the details of one thing. Here, one row is **one item on one bill**.
- A **column** (also called a **field**, **variable**, or **attribute**) holds one kind of detail for every row: `item`, `qty`, `unit_price`.
- A **value** is what sits where a row and a column meet: `4` in the `qty` column of the milk row.
- A **dataset** is a collection of related data. It might be one table (every bill from the shop this year) or several tables that belong together.

Two ideas from this small example will stay with you for the whole book.

**1. Decide what one row means.** In Figure 1.2, one row is one *item* on a bill, not one *bill*. That's why `bill_no`, `bill_date`, and `paid_by` are repeated on all five rows: each row needs to stand on its own. The level of detail one row represents is called the **grain** of a table. When two people disagree about a number, they're very often counting at different grains: "5 sales" (items) versus "1 sale" (bill).

**2. Store the ingredients, calculate the results.** The receipt prints a total of ₹1,092, but the table has no "total" row. You can always calculate it: 165 + 540 + 112 + 135 + 140 = ₹1,092. A total typed in as a row would get added in again by anyone who sums the column, and it would be wrong the moment someone corrected a line. Keep the detailed facts; calculate summaries when you need them.

Two more habits make a table easy to work with:

- **One kind of fact per column.** A column called `item` shouldn't also hold "Toor dal 1 kg, 2 packets" with the quantity mixed into the text. Split it: `item` and `qty`.
- **One value per cell.** "UPI + cash" in one cell can't be added up. If a bill was split between two payment methods, that's two payment rows.

> **Try it.** Take any receipt from your wallet or your email. Write its first three lines as rows of a table with the same seven columns as Figure 1.2. What is the grain of your table?

---

## 1.4 Kinds of values: data types

Every column holds one **type** of value. The type tells you, and the computer, what you can do with it. Four types cover almost everything you'll meet:

| Type | Holds | Examples | You can… |
|---|---|---|---|
| **Number** | amounts and counts, whole or with decimals | `4`, `28`, `1450.50` | add, average, compare |
| **Text** (also called a **string**) | letters, words, codes | `Toor dal 1 kg`, `UPI`, `Pune` | sort alphabetically, search, group |
| **Date and time** | a moment or a calendar day | `2026-09-14`, `18:42` | sort in time order, find days between, group by month |
| **True/false** (also called **Boolean**) | yes-or-no facts | `TRUE`, `FALSE` | count how many are true, filter |

Getting the type right matters more than beginners expect.

**Numbers that aren't numbers.** A PIN code like `411038` is made of digits, but you would never add two PIN codes together or calculate an average one. The same goes for phone numbers, employee codes, bank account numbers, and bill numbers. They're **identifiers** or **codes**, and they should be treated as text. Store a phone number as a number and a spreadsheet may drop its leading zero (`022…` becomes `22…`) or display a long number as `9.82E+09`. **Rule of thumb: if you'd never do arithmetic with it, it's text.**

**Dates stored as text.** `03/04/2026` means 3 April in India and the UK, but 4 March in the United States. A computer that reads it as text can't tell, and it will sort `10/01/2026` before `9/01/2026`, because the character `1` comes before `9`. The safest way to write a date is **year-month-day**, `2026-04-03`, which sorts correctly and means the same thing everywhere. It's an international standard (ISO 8601), and it's how dates are written in this book's data.

**Missing values.** Sometimes a value simply wasn't recorded. A blank is not the same as zero: a blank "discount" might mean *no discount* or *nobody wrote it down*. Databases use a special marker, **NULL**, for "unknown", and Chapter 12 shows how it trips up calculations. For now, whenever you see a blank, ask: **does this mean zero, "not applicable", or "unknown"?**

> **Watch out: the type you see isn't always the type that's stored.** A spreadsheet can *show* `14-09-2026` while storing it as text, and then refuse to sort or group it by month.

---

## 1.5 Qualitative and quantitative data

A second way to describe data is by what it measures.

**Quantitative data** is measured or counted in numbers, and the numbers mean an amount: 4 packets of milk, ₹540, 12,000 steps, 38.5 °C.

**Qualitative data** (also called **categorical data**) describes a quality or puts things into groups: the payment method (UPI, card, cash), a city, a product category, a customer's comment, "satisfied" or "not satisfied".

Quantitative data splits once more:

- **Discrete** data can only take separate, countable values, usually whole numbers: the number of orders, children, or items in a cart. You can have 3 orders or 4, but not 3.7.
- **Continuous** data can take any value in a range, limited only by how precisely you measure: weight, height, time taken, temperature. A parcel can weigh 2.4 kg, 2.43 kg, or 2.4318 kg.

Money is technically discrete (you can't pay a fraction of a paisa), but because it has so many possible values, it's usually treated as continuous in analysis.

| Column from the receipt | Qualitative or quantitative | If quantitative |
|---|---|---|
| `item` | qualitative | — |
| `qty` | quantitative | discrete |
| `unit_price` | quantitative | continuous (in practice) |
| `paid_by` | qualitative | — |
| `bill_no` | qualitative (it's a label, not an amount) | — |

This isn't just labeling. It decides which **chart** fits (a bar chart for categories, a histogram for continuous amounts) and which **summary** makes sense (a count of each payment method, but an average of prices).

---

## 1.6 Levels of measurement: which math is allowed

Not all numbers support the same calculations. A useful way to think about this is the four **levels of measurement**, described by the psychologist S. S. Stevens in the 1940s and still taught in every statistics course. Each level can do everything the level before it can, plus something new.

![The four levels of measurement and the calculations each allows](figures/fig1-3-levels-of-measurement.svg)

*Figure 1.3 — From labels to true amounts: each level unlocks more calculations.*

**1. Nominal: names and labels.** The values are categories with no natural order: city, product category, payment method, customer segment. You can **count** how many are in each group and find the most common one (the **mode**). You can't sort them in any meaningful way. Even when nominal data uses digits, like PIN codes or jersey numbers, the digits are just labels.

**2. Ordinal: order matters, but the gaps don't.** The values have a clear order, but the distance between them isn't defined: T-shirt sizes (S, M, L, XL), priority (Low, Medium, High), exam rank, or a satisfaction rating from 1 to 5. You can say one is **higher** than another and find the **median** (the middle value). But the gap from "Poor" to "Average" isn't necessarily the same as the gap from "Good" to "Excellent".

**3. Interval: equal gaps, but no true zero.** The distance between values is meaningful, but zero doesn't mean "none". Temperature in degrees Celsius is the classic example, and calendar dates are another. The **difference** between two values makes sense (it's 20 degrees warmer; the invoice is 30 days late), and so does the mean. But **ratios** don't: 0 °C isn't "no temperature", so 40 °C is not "twice as hot" as 20 °C.

**4. Ratio: equal gaps and a true zero.** Zero means *none of it*: revenue, quantity, weight, distance, age, time taken. Every calculation works here, including "twice as much" and percentage change. ₹2,000 of sales really is twice ₹1,000, and ₹0 really means no sales.

Most business amounts are ratio data, so most of the time every calculation is allowed. The levels matter at the edges, and those edges are where reports go wrong.

### Worked example 1: the average rating that hides the story

Riverstone asks customers to rate two delivery partners from 1 (very poor) to 5 (excellent). Each partner receives five ratings:

| Partner | Ratings | Mean | Median |
|---|---|---|---|
| Swift Movers | 3, 3, 3, 3, 3 | 3.0 | 3 |
| Rapid Wheels | 5, 5, 5, 1, 1 | 3.4 | 5 |

Check the means by hand: 15 ÷ 5 = 3.0, and 17 ÷ 5 = 3.4. ✓

On the mean, Rapid Wheels looks slightly better. But look at the ratings themselves. Swift Movers is consistently average. Rapid Wheels delights most customers and badly fails two out of five, which, for a supplier delivering to hotels, might mean a banquet with no plates. The mean treats the gap between 1 and 5 as four equal steps, which a rating scale doesn't promise. For ordinal data, the **median** and the **count in each category** ("two of five customers gave a 1") are more honest summaries.

### Worked example 2: twice as hot?

Riverstone's warehouse was 20 °C in the morning and 40 °C in the afternoon. A report says it was "twice as hot". It wasn't: 0 °C isn't "no heat", so Celsius numbers can't be divided like that. The honest sentence is *"the temperature rose by 20 degrees"*.

### Worked example 3: dates

An invoice dated 10 March and due on 9 April: you can subtract the dates to get 30 days, a perfectly meaningful difference. But "20 March is twice 10 March" is nonsense. Dates are interval data.

> **Watch out: averaging codes.** Put a column of PIN codes or employee IDs into a spreadsheet and it will happily calculate their average. The result is meaningless. Before you summarize any column, ask which level of measurement it is.

---

## 1.7 Structured, semi-structured, and unstructured data

The last way to describe data is by its **shape**: how organized it is when you receive it. Here's the same Riverstone order, for 20 storage boxes and 50 water bottles, in three shapes.

![One order as a table, as JSON, and as an email](figures/fig1-4-three-shapes-of-data.svg)

*Figure 1.4 — Same facts, three shapes. The less structure, the more work before you can count anything. Mini database (Jan–Mar 2026), order 5001.*

**Structured data** fits a fixed layout of rows and columns, where every row has the same fields and every column has one type. Sales tables, bank statements, attendance registers, and stock lists are structured. It's the easiest to add up, sort, filter, and combine, and it's what spreadsheets and databases are built for. Much of a data analyst's day is spent with structured data.

**Semi-structured data** has labels that travel with the values, but no fixed table layout. The most common format is **JSON** (say "jay-son"), which websites and apps use to send data to each other. In the middle panel of Figure 1.4, every value has a name (`"qty": 20`), and the `items` list can hold one item or fifty. Two orders don't have to have exactly the same fields. Other examples are XML files and the logs that apps write. Semi-structured data is easy for computers to read, and usually needs a step of **flattening** into tables before analysis. Chapter 2 introduces these formats.

**Unstructured data** has no predefined layout at all. The meaning is in the words, pixels, or sounds: emails, WhatsApp messages, PDF contracts, product photos, call recordings, customer reviews. A person can read Rakesh's email in Figure 1.4 and understand the order instantly. A computer has to work out that "the 10L storage boxes" means product 101, and that "the rates you quoted" means ₹450 and ₹120. Most of the information inside organizations is unstructured, and for a long time most of it went unused. Modern AI tools have made it much easier to pull structured facts out of unstructured text, and that's one of the big changes in data work in recent years.

| Shape | Examples |
|---|---|
| Structured | spreadsheets, database tables, CSV files |
| Semi-structured | JSON, XML, app and website logs |
| Unstructured | emails, PDFs, images, audio, free-text reviews |

> **Real-life example: the order that arrives by email.** In many companies, including plenty of manufacturers and distributors, customers still send orders by email or WhatsApp, and someone re-types them into the billing system. Each re-typing is a chance for a mistake: 50 bottles becomes 500, or the discount is missed. Turning that unstructured message into a structured order automatically is a classic automation project.

---

## 1.8 Metadata: data about data

**Metadata** is data that describes other data. Your phone already shows you plenty:

- A photo's metadata includes the date, time, camera model, and often the GPS location where it was taken.
- A file's metadata includes its name, size, type, and when it was last changed.
- A song's metadata includes the title, artist, album, and length.

In data work, the most important kind of metadata is a **data dictionary**: a short document that explains what each column in a dataset means. Here's one for the receipt table from Figure 1.2:

| Column | Type | Meaning | Allowed values or format | Can be blank? |
|---|---|---|---|---|
| `bill_no` | text | the number printed on the bill | digits only | no |
| `bill_date` | date | the date the bill was printed | YYYY-MM-DD | no |
| `item` | text | the product name as printed | any text | no |
| `qty` | number (whole) | how many units were bought | 1 or more | no |
| `unit_price` | number (₹, 2 decimals) | price of one unit, before any discount | more than 0 | no |
| `amount` | number (₹, 2 decimals) | `qty` × `unit_price` | more than 0 | no |
| `paid_by` | text | how the bill was paid | UPI, Card, Cash | no |

It looks like a small thing. It's one of the most valuable things a data team produces. Without it, people guess: *Is `amount` before or after discount? Does "date" mean the order date or the delivery date? Is the price in rupees or thousands of rupees?* Guesses become arguments, and arguments become two departments reporting different numbers for the same month. Other useful metadata includes **where the data came from**, **when it was last updated**, and **who owns it**, meaning who to ask when something looks wrong.

> **Try it.** Pick one column from any table you use at work or college. Could a new colleague understand exactly what it means from its name alone? If not, write the one-line meaning they'd need.

---

## 1.9 Where data comes from

Every piece of data was created by someone or something. Knowing the source tells you a lot about how far to trust it.

| Source | How it's created | Examples | Typical problems |
|---|---|---|---|
| **People** | typed, written, selected, or spoken | order forms, surveys, a salesperson updating a CRM (the sales team's contact system), the shop owner's notebook | typos, blanks, inconsistent spelling, fields filled in "just to get past the screen" |
| **Machines and sensors** | measured automatically | step counters, temperature sensors on a production line, GPS in delivery vans, electricity meters | faulty or drifting sensors, gaps when a device goes offline, huge volumes |
| **Business systems** | recorded as a side effect of doing work | billing software, a website's shopping cart, a bank's payment system, attendance swipes | only as good as the process around them; changes when the system is upgraded |
| **Outside sources** | collected by someone else | government statistics, weather data, market prices, data bought from partners | different definitions, delays, unclear collection methods |

Two more distinctions you'll hear:

- **Primary data** is collected by you or your organization for your own purpose, like Riverstone's order records or a survey you run. **Secondary data** was collected by someone else for another purpose, like census figures. Secondary data is quicker to get, but you have to check that its definitions match your question.
- **First-party data** is what an organization collects directly from its own customers and operations. **Third-party data** is bought or obtained from outside. The terms come up often in marketing.

Notice where the problems cluster. **Whenever a person types data by hand, and especially when the same data is re-typed from one place into another, errors creep in.** Data captured automatically, at the moment something happens, is usually more complete and more consistent. That single observation explains why so much of a data team's work, and a whole thread of this book from Chapter 3 to the architecture chapters, is about capturing data once, at the source, and letting it flow automatically to reports, dashboards, and other systems.

> **Watch out: personal data.** Some data describes people: names, phone numbers, addresses, health details, salaries, locations. Most countries now have laws about how it may be collected, stored, and shared, including India's Digital Personal Data Protection Act, 2023, and the European Union's GDPR. As a beginner, follow two rules: never copy personal data from work to your own devices or accounts, and use only what you need for the task. Chapter 64 covers privacy and governance properly.

---

## 1.10 Data quality in one page

Data is **fit for use** when it's good enough for the decision it supports. A rough count of website visitors can be a little off; the amount on a tax invoice can't. Data quality is usually judged on six dimensions:

| Dimension | Question to ask | Example of a problem |
|---|---|---|
| **Accuracy** | Does the value match reality? | a signup date in the year 2062 |
| **Completeness** | Is anything missing? | a customer with no city |
| **Consistency** | Is the same thing recorded the same way everywhere? | "Mumbai", "mumbai", and "Bombay" |
| **Validity** | Does the value follow the agreed format and rules? | an email address with no `@` |
| **Uniqueness** | Is each real thing recorded only once? | the same customer entered twice |
| **Timeliness** | Is it up to date for the decision? | a stock report from last month used to promise delivery today |

Here's a small extract from a customer list that was kept by hand in a spreadsheet for a few months. Look at it for a minute before reading on.

```
 customer_name     | city     | email                        | signup_date
-------------------+----------+------------------------------+-------------
 Sharma Hardware   | Mumbai   | sharma.hardware@example.com  | 2025-11-04
 Metro Mart        | mumbai   | metromart@example.com        | 2026-01-22
 METRO MART        | Mumbai   | METROMART@EXAMPLE.COM        | 22/01/2026
 Coastal Foods     | Chennai  | coastalfoods.example.com     | 2025-10-20
 Sunrise Caterers  |          |                              | 2026-02-03
 Western Logistics | Bombay   | westernlogistics@example.com | 2062-04-01
```

There are at least six problems, one or more for every dimension except timeliness:

1. **Uniqueness.** Metro Mart appears twice, once in capitals. It's the same customer, with the same email address in different letters.
2. **Consistency.** Mumbai is written three ways: "Mumbai", "mumbai", and "Bombay", the city's former name. (The third row also has an invisible space after "Mumbai", which you can't see here but a computer can.)
3. **Validity.** The third row's date is written `22/01/2026` while every other row uses year-month-day.
4. **Validity.** Coastal Foods' email address has no `@`, so no email will ever reach it.
5. **Completeness.** Sunrise Caterers has no city and no email.
6. **Accuracy.** Western Logistics signed up on 1 April **2062**, forty years in the future. Someone almost certainly meant 2026.

Now try a simple question: **how many customers are in Mumbai?** A computer that matches the exact text "Mumbai" finds **one**: Sharma Hardware. ("mumbai" has a small *m*, "Bombay" is different text, and the third row's "Mumbai" has a trailing space.) The real answer is **three different customers**: Sharma Hardware, Metro Mart, and Western Logistics. And for Sunrise Caterers, the honest answer is "unknown".

Nothing in that table looks dramatic. Each problem is one small slip by a busy person. Together they turn a simple question into a wrong answer, and nobody sees an error message. **This is why analysts check data before they trust it.**

---

## Common mistakes and how to spot them

| Mistake | Symptom | Fix |
|---|---|---|
| Treating codes as numbers | an "average PIN code", phone numbers showing as `9.82E+09`, lost leading zeros | Store identifiers as text; ask "would I ever do arithmetic with this?" |
| Not deciding what one row means | two people report different counts for the same thing | State the grain: "one row = one item on one bill" |
| Storing totals as rows | column sums come out double | Keep the detail; calculate totals when needed |
| Treating a blank as zero, or zero as blank | totals or averages silently wrong | Ask whether a blank means zero, not applicable, or unknown |
| Writing dates in local formats | 3 April read as 4 March; months sort in the wrong order | Use year-month-day: `2026-04-03` |
| Averaging ordinal ratings without looking at the spread | a polarizing supplier looks "above average" | Report the median and the count in each category |
| Saying "twice as much" for interval data | "twice as hot", "twice as late in the month" | Describe the difference instead: "20 degrees warmer" |
| Stopping at information | a report full of numbers that nobody acts on | Add the "why" and the "so what" |
| Trusting data because it's in a system | wrong counts from duplicates, spelling variations, and typos | Check a small sample against the six quality dimensions first |
| Using a column without knowing its meaning | "amount" assumed to include tax when it doesn't | Read, or write, the data dictionary |

---

## In the real world: Meera's first week

Meera Iyer has just joined Riverstone Supplies as a sales coordinator. On her second day, Anita Rao, the Sales Head, stops by her desk. "We're planning a customer meet in Mumbai next month. How many customers do we have there? I need the number by lunch."

Meera opens the shared customer spreadsheet. It has 240 rows. She filters the city column for "Mumbai" and gets 31. It would be easy to send "31" and move on. Instead, she spends twenty minutes using what she learned in this chapter.

**1. What does one row mean?** She scrolls and notices some customers appear more than once. Asking around, she learns that the sales team adds a new row whenever a customer opens a new branch. So one row isn't one customer; it's one *customer location*. Anita wants to invite customers, not branches.

**2. Is the city column consistent?** She sorts the column and finds "Mumbai", "mumbai", "Bombay", "Mumbai " with a trailing space, "Navi Mumbai", "Thane", and "Mum". She groups the obvious variations of Mumbai together, and notes that Navi Mumbai and Thane are separate cities in the same metropolitan region. Whether to invite them is a business question, not a spreadsheet question.

**3. What's missing?** Eleven rows have no city at all. She checks their addresses, which are in a different column, and finds that four are in Mumbai.

**4. Can the data be trusted?** She spots two customers marked "closed" in a notes column.

At 12:30 she sends this:

> *"We have **38 active customers with locations in Mumbai** (44 locations in total). The filter on 'Mumbai' alone shows 31, because the city is spelled several ways and some rows have no city. Another **9 customers are in Navi Mumbai and Thane**; should we invite them too? I've excluded 2 customers marked closed. I've also listed the spelling issues I found, in case we want to clean up the sheet."*

Look at what Anita received: a number she can use, the reason it differs from the "obvious" number, a decision only she can make, and a small fix that will help everyone next time. None of it needed an advanced tool. It needed Meera to ask *what does a row mean*, *what does each value mean*, and *can I trust it*. That's the whole of this chapter, applied in twenty minutes.

---

## Tools

- **A notebook and pen.** Enough for every exercise in this chapter. Sketching a table by hand is still one of the best ways to think about data.
- **Excel or Google Sheets** (optional). Chapter 10 teaches both from the beginning. If you already have either, use it for the project; Google Sheets is free with a Google account.
- **Your phone.** It's full of data about you: steps, screen time, photos, payments. It's the most convenient practice dataset you own.

Each tool is installed in the chapter that first uses it; Chapter 6 shows when.

---

## The project: a week of your own spending

**Goal:** collect a real dataset, describe it the way a data professional would, and turn it into one piece of insight about your own life.

**Step 1. Collect.** For seven days, record every payment you make: cash, card, and UPI. Write one row per payment with these columns:

| Column | What to write |
|---|---|
| `date` | year-month-day, e.g. `2026-09-07` |
| `time` | 24-hour clock, e.g. `19:30` |
| `item` | what you paid for |
| `category` | Food, Transport, Groceries, Bills, Entertainment, Shopping, Health, or Other |
| `amount_rs` | the amount in rupees (or your currency) |
| `payment_method` | UPI, Card, or Cash |
| `shop` | where you paid |
| `necessary` | Yes or No: would you have been fine without it? |

Here's how the first three days looked for Kavya, a college student in Mumbai:

| `date` | `time` | `item` | `category` | `amount_rs` | `payment_method` | `shop` | `necessary` |
|---|---|---|---|---|---|---|---|
| 2026-09-07 | 08:40 | Tea and poha | Food | 60 | UPI | Station stall | No |
| 2026-09-07 | 09:15 | Metro card top-up | Transport | 500 | UPI | Metro station | Yes |
| 2026-09-07 | 19:30 | Vegetables | Groceries | 240 | Cash | Local market | Yes |
| 2026-09-08 | 13:05 | Lunch thali | Food | 180 | Card | Canteen | Yes |
| 2026-09-08 | 21:10 | Movie ticket | Entertainment | 350 | UPI | Online | No |
| 2026-09-09 | 08:45 | Tea and poha | Food | 60 | UPI | Station stall | No |
| 2026-09-09 | 18:20 | Mobile recharge | Bills | 299 | UPI | Online | Yes |
| 2026-09-09 | 20:00 | Auto rickshaw | Transport | 90 | Cash | Street | Yes |

**Step 2. Describe the dataset.** Write down:

- the **grain** (what one row means);
- for every column: its **type**, whether it's **qualitative or quantitative** (and discrete or continuous), and its **level of measurement**;
- a **data dictionary**, using the table in section 1.8 as a model;
- the **source** of the data, and which rows you're least sure about (a cash payment you only remembered the next day, for example).

**Step 3. Check the quality.** Go through the six dimensions. Did you miss any payments? Did you write a category two different ways ("Food" and "Snacks")? Is every date in the same format?

**Step 4. Climb the ladder.** Answer these, by hand or in a spreadsheet:

1. *Information:* What did you spend in total, and in each category? Which payment method did you use most, by amount?
2. *Knowledge:* What explains your biggest category? Is it one large payment or many small ones?
3. *Insight:* What is one specific change you'd make next week, and how much would it save?

For Kavya's three days: she spent ₹1,779 in total, about ₹593 a day. Transport was her largest category at ₹590, mostly one metro card top-up, which will last her weeks, so it isn't really a daily cost. UPI covered ₹1,269, or 71.3% of her spending. She marked ₹470 (26.4%) as not necessary, and ₹120 of that was two identical breakfasts at the station stall. Her insight: *"Carrying breakfast from home three days a week would save about ₹180 a week, and the metro top-up shouldn't count as three days of spending."*

**Stretch goals:**

- Keep the log for a month and compare weeks.
- Add a `mood` column (happy, neutral, stressed) and see whether your "not necessary" spending changes with it. What level of measurement is `mood`?
- Download a month of your UPI or bank statement and compare it with your hand-kept log. Which payments did you forget to write down? That gap is a completeness problem, and a very common one.

---

## You've got it when…

- [ ] I can explain the difference between data, information, knowledge, and insight with an example from my own life or work.
- [ ] I can turn a receipt, register, or form into a table and state its grain.
- [ ] I name a column's type before I use it, and I treat codes and phone numbers as text.
- [ ] I can say whether a column is qualitative or quantitative, and which level of measurement it is.
- [ ] I don't average ratings or codes without thinking, and I don't say "twice as hot".
- [ ] I can tell structured, semi-structured, and unstructured data apart.
- [ ] I can write a data dictionary for a small table.
- [ ] I check a small dataset against the six quality dimensions before trusting a number from it.
- [ ] I've logged a week of my own spending and turned it into one insight.

---

## Recap

- **Data** is a recorded observation. **Information** is data organized to answer a question. **Knowledge** explains why. **Insight** points to an action. Analysts earn their value by climbing that ladder.
- Data is easiest to use in **tables**: **rows** (records), **columns** (fields), and **values**. Always decide what one row means: the **grain**.
- Store detailed facts and **calculate** totals, rather than typing totals into the data.
- The four common **data types** are number, text, date/time, and true/false. Codes that look like numbers are text. Write dates as year-month-day. A blank isn't automatically zero.
- **Quantitative** data measures amounts (discrete or continuous); **qualitative** data describes categories.
- The **levels of measurement**, nominal, ordinal, interval, and ratio, decide which calculations make sense.
- Data comes in three shapes: **structured** (tables), **semi-structured** (JSON, logs), and **unstructured** (emails, PDFs, images).
- **Metadata** describes data. A **data dictionary** says what every column means, and saves hours of argument.
- Data comes from **people, machines, business systems, and outside sources**. Every manual re-typing adds errors, which is why capturing data once, at the source, matters.
- **Data quality** is judged on accuracy, completeness, consistency, validity, uniqueness, and timeliness. Check before you trust.

---

## Practice exercises

### Warm-up

1. Which of these are data? For each "no", say what would make it data. (a) A train timetable on a station wall. (b) A tune you're humming. (c) The number of likes on a post. (d) A thought that you should call your aunt. (e) A doctor's handwritten prescription.
2. Label each statement as data, information, knowledge, or insight:
   (a) "Order 5012 was placed on 15 March and is Pending."
   (b) "We should give customers who haven't ordered in 60 days a call before the festive season."
   (c) "Riverstone sold ₹1,61,700 in February."
   (d) "Hotels order less during the monsoon, because fewer events are held."
3. Give the data type (number, text, date/time, or true/false) of each: an Aadhaar-style ID number, a delivery date, the weight of a parcel, whether an invoice is paid, a customer's PIN code, the number of items in a cart.

### Core

4. State the level of measurement (nominal, ordinal, interval, or ratio) of each: T-shirt size, monthly revenue, customer segment, temperature in °C, a student's rank in class, the number of years a customer has been with Riverstone, a calendar year such as 2026, and a star rating from 1 to 5.
5. Classify each as structured, semi-structured, or unstructured: a CSV file of bank transactions, a recorded customer-support phone call, the JSON a weather app receives, a scanned PDF invoice, an Excel sheet of attendance with one row per student per day, and a set of Google reviews.
6. Which of these calculations make sense? Explain each in one sentence. (a) The average PIN code of your customers. (b) The median T-shirt size sold. (c) "Revenue in March was 20% lower than in February." (d) "15 March is 50% later than 10 March." (e) The most common payment method.
7. Write a data dictionary entry (type, meaning, allowed values, can it be blank) for these four columns of an attendance register: `student_id`, `class_date`, `status`, `minutes_late`.

### Stretch

8. Find every data quality problem in this extract, and name the dimension each one belongs to:

```
 order_id | customer_name  | order_date | quantity | unit_price
----------+----------------+------------+----------+------------
 7001     | Green Leaf     | 2026-04-02 |       10 |     450.00
 7002     | Patel Kitchen  | 2026-04-02 |       -5 |     780.00
 7002     | Patel Kitchen  | 2026-04-02 |       -5 |     780.00
 7003     | Blue Bay Cafe  | 2026-13-01 |       20 |
 7004     | blue bay cafe  | 2026-04-05 |       15 |    120.00
```

9. Using the delivery-partner ratings from section 1.6 (Swift Movers: 3, 3, 3, 3, 3; Rapid Wheels: 5, 5, 5, 1, 1), Riverstone's operations manager asks, "Which partner should we use for hotel banquets?" Write a three-sentence answer that uses the right summaries for ordinal data.
10. Kavya's log has a `necessary` column (Yes/No) and an `amount_rs` column. What is the level of measurement of each? Name two summaries you could calculate from `necessary` and one you couldn't.

### Think about it (no calculation needed)

11. Your phone's step counter says you walked 12,000 steps yesterday. How could that number be wrong? What metadata would help you decide how much to trust it?
12. The sales head says, "Our customer data is bad." You've been asked to fix it. What three questions would you ask before touching the data?
13. On an order form, the discount box is blank. List three different things the blank could mean, and say who in the company should decide how blanks are treated in reports.

---

## Key terms

data · datum · information · knowledge · insight · DIKW · table · row / record · column / field / variable / attribute · value · dataset · grain · data type · number · text / string · date and time · Boolean · identifier · ISO 8601 date · missing value / NULL · quantitative · qualitative / categorical · discrete · continuous · levels of measurement · nominal · ordinal · interval · ratio · mode · median · mean · structured data · semi-structured data · JSON · unstructured data · flattening · metadata · data dictionary · primary data · secondary data · first-party data · third-party data · personal data · data quality · accuracy · completeness · consistency · validity · uniqueness · timeliness · fit for use

*(All terms are defined in the Glossary, Appendix A.)*

---

## Where this leads

- **Chapter 2, How Computers Store, Move and Protect Data,** shows where data lives: files and formats (CSV, Excel, JSON, Parquet), databases, the cloud, and APIs.
- **Chapter 3, How a Business Runs on Data,** follows one Riverstone order from enquiry to cash, and shows every system that records data along the way.
- **Chapter 4, Numbers Without Fear,** builds the everyday math for working with quantitative data: percentages, growth, and averages.
- **Chapters 10 and 12** put this chapter's ideas into tools: data types and tables in spreadsheets, including how to check what a cell really contains, then in databases, including how getting the grain wrong makes totals double-count.
- **Chapter 14, Data Cleaning & Preparation,** fixes the quality problems from section 1.10 at scale, and **Chapter 47** shows how data teams catch them automatically before a report goes out.
- **Chapter 15** matches each kind of data to the chart that fits it, and **Chapter 21, Descriptive Statistics & Probability,** explains which averages suit each level of measurement.
- **Chapter 18** flattens semi-structured data such as JSON into tables.
- **Chapter 24** shows how to write the "so what" that turns a number into a decision.
- **Chapters 41 and 55** work with unstructured text, and in **Chapter 58** you'll build the email-order automation from section 1.7.
- **Interview preparation:** questions on data types, levels of measurement, and data quality appear in the Statistics bank (Chapter 73) and the Business Analyst bank (Chapter 76), with model answers.

---

## Answers to practice exercises

**1.** (a) Yes: it's recorded information about trains and times. (b) No, not until it's recorded, for example as an audio file or written music. (c) Yes: a recorded count. (d) No, until you write it in a to-do list or set a reminder; then it's a recorded note. (e) Yes: it's recorded, even though it's handwritten and unstructured, which makes it harder to use.

**2.** (a) Data: a single recorded fact. (b) Insight: an action based on understanding. (c) Information: orders summarized into a monthly total. (d) Knowledge: an explanation of a pattern.

**3.** ID number: text (a code; you'd never add two). Delivery date: date. Parcel weight: number. Invoice paid: true/false. PIN code: text. Items in a cart: number (a whole number).

**4.** T-shirt size: ordinal. Monthly revenue: ratio. Customer segment: nominal. Temperature in °C: interval. Rank in class: ordinal (the gap between 1st and 2nd isn't the same as between 2nd and 3rd). Years as a customer: ratio (zero means none). Calendar year: interval (the year 0 isn't "no time", so 2026 isn't twice 1013). Star rating: ordinal.

**5.** CSV of bank transactions: structured. Recorded phone call: unstructured. Weather app JSON: semi-structured. Scanned PDF invoice: unstructured (it's a picture of a document, even though the invoice itself had a layout). Attendance sheet: structured. Google reviews: unstructured text (though each review sits in a semi-structured record with a date and a star rating).

**6.** (a) No: PIN codes are nominal labels, so an average has no meaning. (b) Yes: sizes are ordinal, so the middle value is meaningful. (c) Yes: revenue is ratio data, so percentage change works. (d) No: dates are interval data; you can say "5 days later", but not "50% later". (e) Yes: counting and finding the most common value works for nominal data.

**7.** One good answer:

| Column | Type | Meaning | Allowed values | Can be blank? |
|---|---|---|---|---|
| `student_id` | text | the school's ID for the student | the ID format used by the school | no |
| `class_date` | date | the day of the class | YYYY-MM-DD, a school day | no |
| `status` | text | attendance for that day | Present, Absent, Late, Leave | no |
| `minutes_late` | number (whole) | minutes after the start time the student arrived | 0 or more | yes: blank when `status` isn't Late |

The last row is the kind of detail that prevents arguments later: a blank `minutes_late` means "not applicable", not zero.

**8.** Problems and dimensions:

- Order 7002 appears twice: **uniqueness**.
- Quantity −5 isn't possible for an order (unless the business records returns this way, which should be stated in the data dictionary): **validity**.
- `2026-13-01` has a month 13: **validity** (and it can't be trusted for **accuracy**).
- Order 7003 has no unit price: **completeness**.
- "Blue Bay Cafe" and "blue bay cafe": **consistency**.
- "Green Leaf" and "Patel Kitchen" may be shortened names of Green Leaf Hotels and Patel Kitchenware, which would be a **consistency** problem if other tables use the full names. Worth checking.

**9.** A sample answer: *"The average ratings are close (3.0 and 3.4), but they hide an important difference: every Swift Movers delivery was rated 3, while two of Rapid Wheels' five deliveries were rated 1, the lowest possible. For hotel banquets, where one failed delivery can ruin an event, consistency matters more than the occasional excellent delivery, so I'd use Swift Movers. With only five ratings each, we should keep collecting ratings and review the choice in a quarter."*

**10.** `necessary` is nominal (two categories, Yes and No; you could argue it's ordinal if "Yes" is seen as higher, but it's usually treated as nominal). `amount_rs` is ratio. From `necessary` you can calculate the **count** (or share) of Yes and No rows, and the **total amount** in each group, such as Kavya's ₹470 marked No. You can't calculate an **average of the Yes/No values** themselves, unless you deliberately code Yes as 1 and No as 0, in which case the average is simply the share of Yes rows.

**11.** The counter could count arm movements as steps (while cooking or on a bumpy bus ride), miss steps while the phone sat on a desk, or double-count if both a watch and a phone were synced. Useful metadata: which device recorded it, whether the phone was carried all day, the hourly breakdown (12,000 steps between 2 and 3 a.m. would be suspicious), and whether data from several devices was combined.

**12.** Good questions include: *"Bad for what decision? What were you trying to do when the data let you down?"* (fit for use), *"Which fields matter most: names, contact details, cities, or something else?"* (scope), and *"Who enters and updates customer data today, and how?"* (the source, because fixing the data without fixing how it's captured means it will be bad again in six months).

**13.** The blank could mean *no discount was given*, *a discount was given but not recorded*, or *the discount wasn't decided yet* (for example, pending approval). The treatment should be decided by the people who own the rule: usually finance, together with sales. The analyst's job is to raise the question, document the answer in the data dictionary, and apply it consistently in every report.
