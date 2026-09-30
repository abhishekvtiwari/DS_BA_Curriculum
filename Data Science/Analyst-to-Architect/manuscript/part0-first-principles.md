# Part 0 — First Principles: Data from Zero

Part 0 starts from nothing. It assumes no technical knowledge, no math beyond school arithmetic, and no tools. By the end of it, you'll understand what data is, where it lives, how a business creates and uses it, how to work with numbers confidently, how to think through a business question, and you'll have a plan for how and when you'll learn the rest.

Every example uses **Riverstone Supplies**, the fictional manufacturer you'll follow through the whole book, and every number was checked against its practice databases.

Before Chapter 1, read **How to Use This Book** at the front: it shows how each chapter is laid out, how to read the code and its output, and where the answers and companion files are.

| Chapter | What you'll be able to do | Time needed |
|---|---|---|
| **1. What Is Data?** | tell data from information and insight; name types and levels of measurement; judge data quality | 3–4 hours |
| **2. How Computers Store, Move and Protect Data** | work with files and formats from CSV to Parquet; explain databases, the cloud, and APIs; keep data safe | 3–4 hours |
| **3. How a Business Runs on Data** | follow an order from enquiry to cash; tell bookings from billings from collections; define KPIs; find manual work | 3–4 hours |
| **4. Numbers Without Fear** | calculate percentages, points, growth, and CAGR; choose the right average; read charts; estimate | 4–5 hours |
| **5. Thinking Like an Analyst** | turn vague requests into precise questions; build issue trees; test hypotheses; spot bias; decide with data | 3–4 hours |
| **6. Planning Your Learning** | estimate your hours honestly; set a weekly rhythm; know which chapter brings each tool; read documentation; learn with AI assistants; plan your first 90 days | 2–3 hours |

In total, allow 18–24 hours, including the exercises and projects. After Part 0, Part 1 (Chapters 7–9) shows the map of data careers, and Part 2 (Chapters 10–27) builds the analyst's toolkit.


# Chapter 1. What Is Data?

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

## Common mistakes

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

## Project: a week of your own spending

**Goal:** collect a real dataset, describe it the way a data professional would, and turn it into one piece of insight about your own life.

### Tools you'll need

- **A notebook and pen.** Enough for every exercise in this chapter. Sketching a table by hand is still one of the best ways to think about data.
- **Excel or Google Sheets** (optional). Chapter 10 teaches both from the beginning. If you already have either, use it for the project; Google Sheets is free with a Google account.
- **Your phone.** It's full of data about you: steps, screen time, photos, payments. It's the most convenient practice dataset you own.

Each tool is installed in the chapter that first uses it; Chapter 6 shows when.

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

## Key terms

data · datum · information · knowledge · insight · DIKW · table · row / record · column / field / variable / attribute · value · dataset · grain · data type · number · text / string · date and time · Boolean · identifier · ISO 8601 date · missing value / NULL · quantitative · qualitative / categorical · discrete · continuous · levels of measurement · nominal · ordinal · interval · ratio · mode · median · mean · structured data · semi-structured data · JSON · unstructured data · flattening · metadata · data dictionary · primary data · secondary data · first-party data · third-party data · personal data · data quality · accuracy · completeness · consistency · validity · uniqueness · timeliness · fit for use

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

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

## Exercises

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

## Answers

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
- **Interview preparation:** questions on data types and data quality appear in the Python and pandas bank (Chapter 72, Q72-038) and the Data Engineering bank (Chapter 77, section 77.6), with model answers.


# Chapter 2. How Computers Store, Move and Protect Data

> **Chapter at a glance**
>
> **You will learn to:** explain how a computer stores letters and numbers as bits and bytes · read file sizes from bytes to terabytes, and work out how long a download takes · tell memory from storage · work with files, folders, paths, and extensions without surprises · choose between CSV, Excel, JSON, XML, PDF, and Parquet for a job, and avoid each format's traps · explain what a database, a server, the internet, and the cloud are · describe what an API does and read its replies · protect data with good passwords, encryption, access rules, and backups.
>
> **Before you start:** Chapter 1 (what data is: rows, columns, types, and quality).
>
> **Time needed:** 3–4 hours, including the exercises and the project.
>
> **Tools:** any computer. For the project: a spreadsheet program (Excel or Google Sheets) and a plain-text editor (Notepad on Windows, TextEdit on a Mac, or any code editor).
>
> **Practice data:** four Riverstone orders from the mini database (Jan–Mar 2026), saved in five formats in the companion files (Appendix E), and the replies of a small demonstration API. Every file size and every reply in this chapter is real.

---

## Why this matters

In Chapter 1 you learned what data *is*. This chapter is about where it *lives*, how it *travels*, and how it's *kept safe*. That sounds like IT's job, and some of it is. But these everyday situations all land on a data person's desk:

- A colleague emails a CSV export, you open it in Excel, and every product code that started with zero has quietly lost it.
- A report that took two seconds to open last year now takes two minutes, and the file is 80 MB.
- The finance team's figures in the monthly deck don't match yours, because they're working from `Sales_Report_FINAL_v3.xlsx` and you're working from `Sales_Report_FINAL_v4.xlsx`.
- Your manager asks whether the new CRM "has an API" so the weekly report can update itself.
- A laptop with a customer list on it is left in a taxi.

None of these needs you to be an engineer. Each needs you to understand, in plain terms, how computers store, move, and protect data. People who do understand it waste less time, lose less data, and are trusted with more of it, which is exactly the path this book is about.

---

## In plain English

Imagine Riverstone's old paper office before any computers arrived.

- Everything was written in an **alphabet** of letters and digits. A computer has an even smaller alphabet: just 0 and 1.
- Records were kept on **shelves** in a storage room, where they stayed even when the lights went off. That's a computer's **storage**: its disk.
- To work on a record, a clerk carried it to a **desk**. The desk was fast to work at but small, and cleared every evening. That's the computer's **memory**.
- Records sat in **folders with labels**, and the label said what kind of paper was inside. Those are **files**, **folders**, and **extensions**.
- The same information could be written as a **ledger** with neat columns, a **letter**, or a **form** with labeled boxes. Those are **file formats**.
- Documents traveled between branches by **courier**. That's the **network** and the **internet**.
- Other companies didn't walk into the storage room. They came to a **counter window**, filled in a request slip, and a clerk brought back exactly what they asked for. That's an **API**.
- The storage room had **locks**, only some staff had **keys**, and important ledgers were **copied** and kept in another building in case of fire. That's **security** and **backups**.

Every section below is one part of that office, in modern form.

---

## 2.1 Bits and bytes: how computers store everything

### Everything is 0s and 1s

Deep down, a computer can only store and move **two states**: on or off, charged or not charged, magnetized one way or the other. We write those states as **1** and **0**. One of these on/off values is a **bit** (short for *binary digit*).

One bit can only tell two things apart: yes or no. But put bits together and the number of possibilities doubles with each bit you add:

| Bits | Possible patterns | Enough for… |
|---|---|---|
| 1 | 2 | yes/no |
| 2 | 4 | the four seasons |
| 8 | 256 | every English letter, digit, and punctuation mark |
| 16 | 65,536 | a whole number up to 65,535 |
| 32 | 4,294,967,296 | a whole number up to about 4.3 billion |

A group of **8 bits** is a **byte**, and the byte is the basic unit for measuring data. When someone says a file is 364 bytes, they mean it takes 364 × 8 = 2,912 on/off switches to store.

### How text is stored

To store text, computers agree on a table that gives every character a number, and store the number. The capital letter `A` is number 65, which in 8 bits is `01000001`. The digit `7` is number 55. A space is number 32. This agreement, first made for English as **ASCII** in the 1960s, fits every English letter, digit, and common symbol into one byte each.

English isn't the world's only language, of course. **Unicode** is the modern table: it gives a number to almost every character in every writing system, including ₹, Hindi, Tamil, Chinese, and emoji. The most common way to store Unicode as bytes is **UTF-8**, which keeps plain English letters at one byte each and uses two, three, or four bytes for everything else. Here's what some characters really take:

| Text | Characters | Bytes in UTF-8 |
|---|---|---|
| `A` | 1 | 1 |
| `Pune` | 4 | 4 |
| `é` | 1 | 2 |
| `₹` | 1 | 3 |
| `न` (Hindi *na*) | 1 | 3 |
| `नमस्ते` | 6 | 18 |
| `😀` | 1 | 4 |
| `₹14,700` | 7 | 9 |

So "one character is one byte" is only true for plain English text. It's why a report with a lot of Hindi or Tamil text is bigger than the same report in English, and why a column limited to "100 characters" in one system can overflow a "100 bytes" limit in another.

### When the table is wrong: garbled text

If a file is saved in one encoding and opened as if it were another, the bytes are read with the wrong table, and you get nonsense. Here's what happens when the UTF-8 bytes for `₹14,700` are opened as an older Windows encoding:

```
â‚¹14,700
```

And `Café` becomes `CafÃ©`. If you've ever seen `Ã©` or `â€™` in a report, a mismatched encoding is almost always the cause. The fix is to open or import the file with the correct encoding, which is usually UTF-8. Section 2.5 shows where this bites in practice.

### How numbers are stored

Whole numbers are stored exactly, as binary. Numbers with decimals are trickier. Most software stores decimals approximately, in a format called **floating point**, which is fast. Add 0.1 and 0.2 in many programs and the true stored answer is 0.30000000000000004, a hair more than 0.3. That's why systems that handle money store it in an exact decimal type.

So text, numbers, photos, music, and video are all, in the end, long rows of 0s and 1s. What makes them different is the **agreement** about how to read those bits: the encoding or format.

> **Try it.** Open any plain `.txt` file, count roughly how many characters it has, then check its size in bytes (right-click → *Properties* on Windows, or *Get Info* on a Mac). For English text, the two numbers should be close.

---

## 2.2 How big is big? From kilobytes to terabytes

Because data sizes range from a few bytes to many billions, we use prefixes, just as we say kilometers instead of thousands of meters.

![File size units from bytes to petabytes, with everyday examples](figures/fig2-1-how-big-is-big.svg)

*Figure 2.1 — Each step is a thousand times bigger. The examples are typical sizes, not fixed rules.*

A few sizes worth remembering: a page of plain English text is about 2–3 KB; a phone photo is typically a few MB; and an hour of HD video is typically a few GB.

> **Watch out: why your 1 TB drive shows 931 GB.** A drive sold as 1 TB holds a trillion bytes. Windows divides by 1,024 at each step instead of 1,000, so it shows about 931 GB. Nothing is missing.

### Bits for speed, bytes for size

Internet speeds are quoted in **megabits per second (Mbps)**, with a small *b*. File sizes are in **megabytes (MB)**, with a capital *B*. Since a byte is 8 bits, divide by 8:

- A 100 Mbps connection moves at most 100 ÷ 8 = **12.5 MB per second**.
- Downloading a 5 GB file on it takes at least 5,000 MB ÷ 12.5 MB/s = **400 seconds**, about **6.7 minutes**. In practice it takes longer, because the connection is shared and rarely runs at full speed.

> **Watch out: b and B.** "My file is 80 Mb" and "my file is 80 MB" differ by a factor of eight. In data work, sizes are almost always bytes (MB, GB); speeds are almost always bits (Mbps, Gbps). When a number looks eight times too big or too small, check the letter.

### Size limits you'll actually hit

- **Excel** holds at most **1,048,576 rows** and **16,384 columns** per sheet. Long before that, a large workbook becomes slow to open and save. A dataset with millions of rows belongs in a database (section 2.6) or a format such as Parquet (section 2.5).
- **Email attachments** are usually limited to a few tens of megabytes, which is one reason teams share large files by link instead.
- **Cloud storage plans, phone storage, and laptop drives** are all limited, and duplicate copies of large files (`report_v1`, `report_v2`, `report_final`…) fill them quickly.

---

## 2.3 Memory and storage: the desk and the shelves

Every computer has two very different places to keep data.

| | Memory (RAM) | Storage (SSD or hard disk) |
|---|---|---|
| Office analogy | the desk you're working at | the shelves in the storage room |
| What it holds | whatever you have open right now | every file, program, and photo you've saved |
| Speed | very fast | slower (SSDs are much faster than older spinning hard disks) |
| Size on a typical laptop | about 8–32 GB | about 256 GB–2 TB |
| When the power goes off | **everything in it is lost** | everything stays |

Three everyday consequences:

1. **Unsaved work lives only in memory.** If Excel crashes before you save, the changes since your last save were never on the shelves. Save often, or turn on your program's autosave.
2. **Opening a file copies it into memory.** A 200 MB workbook needs well over 200 MB of RAM to work with, often several times more once formulas and formatting are loaded. When a big spreadsheet slows your whole computer, memory is usually what's run out.
3. **Where "saved" means.** Your file might be saved on your own computer's drive, on a **shared network drive** at the office, or in **cloud storage** such as Google Drive or OneDrive, which keeps a copy on the provider's computers and **syncs** it to your devices. Knowing which one matters when you ask, "Can my colleague see this?" or "Is this backed up?"

---

## 2.4 Files, folders, paths, and extensions

A **file** is a named chunk of data on storage. A **folder** (or *directory*) is a container for files and other folders. Every file has a **path**, its full address, which lists every folder you pass through to reach it:

```
Windows:  C:\Users\Kavya\Documents\Finance\2026-09_spending_log.xlsx
macOS:    /Users/kavya/Documents/Finance/2026-09_spending_log.xlsx
```

Windows separates folders with a backslash `\` and starts with a drive letter such as `C:`. macOS and Linux use a forward slash `/`. You'll type paths when you load files into SQL, Python, or Power BI, and most "file not found" errors are a path with one folder or one letter wrong.

### Extensions: what kind of file is this?

The letters after the last dot in a file name are its **extension**. The extension tells the computer which program should open the file:

| Extension | What it usually is |
|---|---|
| `.txt` | plain text |
| `.csv` | comma-separated values: a table as plain text |
| `.xlsx` | an Excel workbook (`.xls` is the older format; `.xlsm` can contain macros) |
| `.json`, `.xml` | structured text, often exchanged between systems |
| `.pdf` | a document laid out for reading and printing |
| `.jpg`, `.png` | images |
| `.parquet` | a compressed, column-based data file (section 2.5) |
| `.sql` | a text file of SQL statements |
| `.py` | a Python program |
| `.zip` | a compressed bundle of other files |
| `.exe` | a Windows program that runs when you open it |

Renaming `sales.csv` to `sales.xlsx` doesn't convert it into an Excel file. It only changes the label, and Excel will warn that the file doesn't match its name. To convert, open the file and use *Save As*.

> **Watch out: hidden extensions.** Windows hides known extensions by default, so a file named `invoice.pdf.exe` appears as `invoice.pdf`, with a harmless-looking name and a program hidden inside. It's a classic trick in phishing emails. Turn on *File name extensions* in File Explorer's *View* menu, and never open an unexpected attachment that turns out to end in `.exe`, `.js`, `.bat`, `.scr`, or `.xlsm` from someone you don't know.

### Naming files so people can find them

Compare these two folders:

```
Report final.xlsx                     2026-01-31_monthly_sales_report.xlsx
Report final (2).xlsx                 2026-02-28_monthly_sales_report.xlsx
Report FINAL v3 use this one.xlsx     2026-03-31_monthly_sales_report.xlsx
```

The right-hand names follow four habits: **a date first, written year-month-day**, so files sort in time order automatically (Chapter 1); **the same pattern every time**; **lower-case words joined with underscores or hyphens**, which avoids problems in code and web links; and **no words like "final"**, which are always eventually wrong. If you need versions, use the version history in Google Drive, OneDrive, or SharePoint (section 2.9), or, for queries and code, a version-control tool called Git.

---

## 2.5 Data file formats: the same data, packed five ways

Riverstone's sales coordinator exports four February orders. Here is exactly the same data saved in five formats (and a note on PDF). Look at what each one looks like inside; the differences explain when to use each.

### CSV: a table as plain text

*Mini database (Jan–Mar 2026): orders 5006 to 5009.*

```
order_id,customer_name,order_date,status,sales_rep,net_revenue,delivery_note
5006,Metro Mart,2026-02-06,Delivered,Rahul Mehta,14640.00,
5007,Coastal Foods,2026-02-11,Delivered,Rahul Mehta,32625.00,Call before delivery
5008,Sunrise Caterers,2026-02-19,Delivered,,23325.00,
5009,Northgate Distributors,2026-02-25,Shipped,Farah Khan,76560.00,"Gate 2, Okhla Phase II"
```

**CSV** (comma-separated values) is the simplest data format there is: one line per row, commas between values, and usually a first line of column names. Any spreadsheet, database, and programming language can read it, which is why "export to CSV" is the universal language between systems. This file is **364 bytes**.

Look closely and you'll find three of CSV's limits:

1. **Commas inside values need quotes.** Northgate's delivery note contains a comma, so it's wrapped in double quotes. Without them, a program would see an extra column.
2. **A blank is just nothing.** Order 5008's missing sales rep is two commas in a row. CSV can't tell "unknown", "not applicable", and an empty text value apart (Chapter 1).
3. **There are no types.** Everything in a CSV is text. When a program reads this file back, `2026-02-06` arrives as text, not a date, unless the program guesses or you tell it.

> **Watch out: opening a CSV in Excel changes it.** When Excel opens a CSV directly, it guesses a type for every value, and some guesses silently change your data: product codes like `00451` lose their leading zeros and become `451`; long ID numbers turn into `4.52E+13`; codes like `3-4` or `1/2` can become dates. If you then save, the damage is written back into the file. Instead, use *Data → From Text/CSV* (Excel) or *File → Import* (Google Sheets), and set code and ID columns to **Text** before loading. If `₹` or accented names appear garbled, choose **UTF-8** as the file's encoding in that same import window (section 2.1).

### Excel (.xlsx): a workbook for people

An `.xlsx` file looks like a grid in Excel, but it isn't plain text. It's actually a **zip file** holding a small collection of XML files. Unzip the four-order workbook and you find ten files inside, including:

```
[Content_Types].xml
xl/workbook.xml
xl/worksheets/sheet1.xml
xl/sharedStrings.xml
xl/styles.xml
```

That structure lets a workbook hold far more than a CSV: several sheets, real dates and numbers, formulas, formatting, charts, and pivot tables. It also means the file isn't meant to be read as text, and needs software that understands the format. This tiny workbook is **5,674 bytes**, more than fifteen times the CSV, because the structure itself takes space. Excel is the right choice when **people** will open, read, and work with the file.

### JSON: data with labels, for systems

```json
[
  {
    "order_id": 5006,
    "customer_name": "Metro Mart",
    "order_date": "2026-02-06",
    "status": "Delivered",
    "sales_rep": "Rahul Mehta",
    "net_revenue": 14640.0,
    "delivery_note": null
  },
  {
    "order_id": 5008,
    "customer_name": "Sunrise Caterers",
    "order_date": "2026-02-19",
    "status": "Delivered",
    "sales_rep": null,
    "net_revenue": 23325.0,
    "delivery_note": null
  }
]
```

*(Two of the four orders shown; the file has all four.)*

**JSON** (JavaScript Object Notation) is the semi-structured format from Chapter 1. Each record is a set of **"name": value** pairs inside curly braces `{ }`, and a list of records goes inside square brackets `[ ]`. Notice what JSON can express that CSV can't: text is in quotes and numbers aren't, so some types survive; and a missing value is written as `null`, clearly different from an empty text value `""`. A record can also contain a list, such as an order with its order lines inside it. JSON is how most **apps and APIs** exchange data (section 2.8). Because every record repeats every column name, it's larger: **894 bytes** here.

### XML: labels as tags

```xml
<order id="5009">
  <customer_name>Northgate Distributors</customer_name>
  <order_date>2026-02-25</order_date>
  <status>Shipped</status>
  <sales_rep>Farah Khan</sales_rep>
  <net_revenue>76560.00</net_revenue>
  <delivery_note>Gate 2, Okhla Phase II</delivery_note>
</order>
```

**XML** (eXtensible Markup Language) does the same job as JSON with **tags**: every value sits between an opening `<name>` and a closing `</name>`, and an empty value can be written `<sales_rep/>`. It's older and wordier (the four-order file is **1,118 bytes**), and you'll meet it in banking and government systems, e-invoicing, older business software, and inside Office files like the workbook above.

### PDF: made for reading, not for data

A **PDF** fixes exactly how a document looks on screen and on paper, which makes it ideal for invoices, contracts, and reports people read. It's poor for data: a table in a PDF is stored as text placed at positions on a page, not as rows and columns, so copying it into a spreadsheet often scrambles the columns. When someone offers you data "as a PDF", ask whether the CSV or Excel export behind it exists.

### Parquet: built for large-scale analysis

**Parquet** is a format built for analyzing large datasets, and it's the standard format of cloud data platforms. You can't read it as text: it's compressed binary data.

![Row storage in CSV compared with column storage in Parquet](figures/fig2-2-row-vs-column-storage.svg)

*Figure 2.2 — CSV stores data row by row; Parquet stores it column by column. The four sales lines are an example, not from either Riverstone database.*

A CSV stores data **row by row**; Parquet stores it **column by column**, so a program that totals one column reads only that column, and similar values sitting together **compress** very well. Parquet also stores each column's **type**, so dates come back as dates. For four orders its advantages are invisible (the file is **4,872 bytes**, bigger than the CSV, because it also describes its own structure); they appear when a file holds millions of rows.

### Compression

**Compression** makes files smaller by writing repeated patterns more efficiently. There are two kinds:

- **Lossless** compression (ZIP, gzip, and the compression inside Parquet and `.xlsx`) gives back **exactly** the original bytes when you unpack it. Data files must only ever use lossless compression.
- **Lossy** compression (JPEG photos, MP3 music, most video) throws away detail people won't notice: that's how photos and music are made so small. It's fine for a photo, and unacceptable for a sales ledger.

### Choosing a format

| Format | People can read it as text? | Keeps types? | Size | Best for |
|---|---|---|---|---|
| **CSV** | yes | no | small | moving tables between systems; simple exports |
| **Excel** | no (needs Excel or similar) | yes | medium | files people will read, filter, and work in |
| **JSON** | yes | partly | large | apps and APIs; nested records |
| **XML** | yes | partly | large | older systems, e-invoicing, Office internals |
| **PDF** | no | no | varies | documents for reading and printing |
| **Parquet** | no | yes | smallest | large datasets for analysis |

> **Real-life example: why the data team asks for "the raw export".** A manager sends a PDF of last quarter's sales, laid out beautifully. To analyze it, the analyst has to copy 40 pages of tables by hand or with a converter, and check every row. The same data exported from the billing system as CSV takes ten seconds to load. The rule most data teams follow: **PDF and formatted Excel for people who read; CSV, JSON, or Parquet for machines that process.**

---

## 2.6 Databases: data that many people can use at once

Files are fine for one person and one moment in time. Business data needs more. Picture Riverstone's orders kept as a shared Excel file: three salespeople edit it at once, two copies drift apart, someone sorts one column without the others and scrambles every order, and the file grows until it no longer opens.

A **database** is software built to avoid those problems. It keeps data in **tables** (rows and columns, like a strict spreadsheet), and it:

- lets **thousands of people and programs** read and write at the same time without overwriting each other;
- enforces **rules**: no order for a customer who doesn't exist, no negative quantities, no duplicate invoice numbers;
- answers **questions** in a language called **SQL**, even across millions of rows, in seconds;
- controls **who may see or change** each table;
- keeps a record of changes so it can recover after a crash.

Most business databases run as a **database server**: a program on a computer, usually in a data center or the cloud, that other programs connect to over the network. (A few, like SQLite, which runs inside many phone apps, store the whole database in a single file.) Underneath, a database still saves its data in files on storage; you just never touch those files directly.

This one page is only a preview; later chapters teach databases and SQL properly, from creating your first table onward.

---

## 2.7 Servers, the internet, and the cloud

### Clients and servers

When you open Gmail, two computers are involved. Your laptop or phone is the **client**: it asks for something. A computer in one of Google's data centers is the **server**: it listens for requests and answers them. A server isn't a special kind of machine; it's a computer whose job is to serve requests, usually running all day in a **data center**, a building full of such computers with reliable power, cooling, and network connections.

### How a request finds its way

The **internet** is a worldwide network of networks that carries data between clients and servers. Three ideas explain most of it:

- **IP address.** Every device on a network has an address, such as `203.0.113.14`, so data knows where to go, like a postal address.
- **DNS** (Domain Name System). People remember names like `riverstone.example`, not numbers. DNS works like a phone book, turning a name into an IP address before your request is sent.
- **HTTP and HTTPS.** These are the rules for how a browser or program asks a web server for something and gets a reply. **HTTPS** is the secure version: everything sent is **encrypted**, so people along the route can't read or change it. The padlock icon in a browser means the connection uses HTTPS. It does *not* mean the website itself is trustworthy.

### The cloud

"The cloud" sounds mysterious. It's simpler than it sounds: **the cloud is computers in someone else's data center that you rent over the internet**, instead of buying and running your own. The largest providers include Amazon Web Services (AWS), Microsoft Azure, and Google Cloud.

Companies rent anything from bare computers to finished applications like Gmail or a CRM. The finished-application kind is called **SaaS**, software as a service, and it's the kind you'll meet first at work.

Why companies move to the cloud: they **pay for what they use** instead of buying servers upfront, they can **grow or shrink** in minutes, and the provider handles power, hardware failures, and much of the security. The trade-offs: bills that grow quietly if nobody watches them, dependence on one provider, and questions about **where the data is physically stored**. Many companies, and some laws, require certain data to stay in a particular country, so cloud services let customers choose a region for their data.

---

## 2.8 APIs: how systems talk to each other

Riverstone's sales system, its accounting software, its website, and its payment gateway are separate programs, often from separate companies. For a website order to appear in the sales system, or for a weekly report to pull the latest invoices, the programs need a way to ask each other for data. That way is an **API** (Application Programming Interface).

![A program sends a request to an API, which queries the database and sends back a response](figures/fig2-3-api-request-response.svg)

*Figure 2.3 — An API is the waiter between your program and someone else's kitchen.*

The restaurant analogy is the classic one. You don't walk into the kitchen and take food off the stove; you'd get in the way, and you might take someone else's dish. You give a **waiter** a clear order from the **menu**, and the waiter brings back what you asked for. An API is the waiter: it offers a menu of requests it will accept, checks you're allowed to ask, fetches what's needed from the system behind it, and brings back a reply in an agreed format, usually JSON. The system's database (the kitchen) is never opened up to outsiders.

### A real request and response

Riverstone has a small demonstration API that serves orders from the mini database (Jan–Mar 2026). A **request** asks for one order by its address, and includes an **API key**, a secret code that proves the caller is allowed in. Here's the full reply the demonstration API sends back when a program asks for order 5009:

```
HTTP/1.0 200 OK
Server: RiverstoneAPI/1.0
Date: Wed, 16 Sep 2026 10:30:00 GMT
Content-Type: application/json
Content-Length: 147

{
  "order_id": 5009,
  "customer_name": "Northgate Distributors",
  "order_date": "2026-02-25",
  "status": "Shipped",
  "net_revenue": 76560.0
}
```

Every **response** has two parts. The top is the **header**: a **status code** (`200 OK`) that says how the request went, plus details such as the type of content coming back. After a blank line comes the **body**: the data itself, here in JSON.

Ask for an order that doesn't exist, and the status code changes:

```
HTTP/1.0 404 Not Found
Server: RiverstoneAPI/1.0
Date: Wed, 16 Sep 2026 10:30:00 GMT
Content-Type: application/json
Content-Length: 38

{
  "error": "order 5099 not found"
}
```

Leave out the API key, and the API refuses before it even looks for the order:

```
HTTP/1.0 401 Unauthorized
Server: RiverstoneAPI/1.0
Date: Wed, 16 Sep 2026 10:30:00 GMT
Content-Type: application/json
Content-Length: 44

{
  "error": "missing or invalid API key"
}
```

### Status codes worth knowing

The first digit tells you who's responsible: **2** means it worked, **4** means the request has a problem (your side), **5** means the server has a problem (their side).

| Code | Meaning | What to do |
|---|---|---|
| `200 OK` | it worked | read the body |
| `401 Unauthorized` | no valid key or login | check the API key |
| `404 Not Found` | no such record or address | check the ID and the address |
| `429 Too Many Requests` | you've hit the API's **rate limit** | slow down and retry later |
| `500 Internal Server Error` | the server failed | retry later; tell the API's owner if it persists |

### Why APIs matter to data people

Most modern business software, including CRMs, accounting tools, payment gateways, e-commerce platforms, and ad platforms, offers an API. That's what makes automation possible: a script can pull yesterday's invoices every morning without anyone logging in and clicking *Export*, and a dashboard can refresh itself.

Two more terms you'll hear:

- A **webhook** is an API in reverse. Instead of your program asking "anything new?" every five minutes, the other system calls *your* address the moment something happens, such as "payment received".
- **API keys are passwords.** Anyone who has the key can do whatever the key allows. Never paste one into a spreadsheet, a shared document, a chat, or code you publish online.

---

## 2.9 Keeping data safe

### The three goals: confidentiality, integrity, availability

Security professionals describe what they protect with three words, often called the **CIA triad**:

| Goal | Means | Example of failure at Riverstone |
|---|---|---|
| **Confidentiality** | only the right people can see the data | the customer price list is emailed to a competitor by mistake |
| **Integrity** | the data is accurate and hasn't been changed without authorization | someone edits invoice amounts in a shared spreadsheet, and nobody can tell |
| **Availability** | the data is there when people need it | ransomware locks the sales server during the busiest week of the year |

Every habit below protects one or more of the three.

### Accounts and passwords

Most data breaches start with a person, not a clever technical attack: a reused password, a shared login, or a click on a fake email.

The habits that prevent most of them:

- **Long and unique.** A long passphrase is harder to guess than a short password full of symbols, and **every account needs a different one**. When one website is breached, attackers try the same email and password everywhere else.
- **Use a password manager.** Nobody can remember fifty unique passphrases. A password manager remembers them, fills them in, and warns you about reused ones.
- **Turn on multi-factor authentication (MFA).** A second step, such as a code from an authenticator app or a prompt on your phone, stops most attacks even when a password leaks.
- **Never share logins.** A CRM password shared in a team chat means you can't tell who changed what, and you can't remove one person's access without locking everyone out. Each person gets their own account.
- **Be suspicious of urgency.** Phishing emails pressure you to act now: "Your account will be closed", "Pay this invoice today". Check the sender's real address, hover over links before clicking, and confirm unusual payment requests by phone.

### Access: the principle of least privilege

**Give each person and program only the access they need, and nothing more.** An analyst who builds sales reports needs to *read* the sales tables, not change them, and doesn't need salary data at all. That's why many companies give analysts **read-only** accounts. Least privilege limits the damage from a mistake or a stolen password.

### Encryption

**Encryption** scrambles data with a key so that only someone with the right key can read it. You rely on it in two places:

- **In transit**, while data moves: HTTPS websites, secure email, and encrypted connections to databases.
- **At rest**, while data sits on storage: an encrypted laptop drive (BitLocker on Windows, FileVault on a Mac) means a stolen laptop's files are unreadable without your login. For any laptop that carries work data, this should be switched on.

### Integrity checks: fingerprints for files

How do you know a file hasn't been changed, even by one character? Computers calculate a **hash**, a "fingerprint" of the data: the same data always gives the same fingerprint, and the smallest change gives a completely different one. Here are the first 12 characters of the fingerprints of two payment lines that differ only in the order of two digits:

```
Pay Rs 14,700 to Riverstone Supplies    f4251ff3fb71…
Pay Rs 17,400 to Riverstone Supplies    9d2f842c5011…
```

Software uses hashes to check that downloads arrived undamaged, that backups match the original, and that passwords are stored safely (systems store a hash of your password, not the password itself).

### Backups and versions

Hardware fails, laptops are stolen, files are deleted by mistake, and **ransomware** (malicious software that locks files and demands payment) can encrypt everything a computer can reach. The only complete protection is a copy you can restore. The widely used rule of thumb is **3-2-1**:

![The 3-2-1 backup rule](figures/fig2-4-three-two-one-backups.svg)

*Figure 2.4 — Three copies, two kinds of storage, one kept elsewhere.*

Two points people often miss:

- **Syncing is not backing up.** Cloud storage such as Google Drive or OneDrive **copies every change** to every device, including deleting a file or saving over it with a mistake. Version history and a recycle bin help, but only for a limited time. A true backup is a separate copy that your everyday mistakes don't touch.
- **Test your restore.** Many organizations discover their backups were incomplete only on the day they need them.

**Version history** is backup's everyday cousin. Google Drive, OneDrive, and SharePoint keep earlier versions of a file, so you can see who changed what and roll back a bad edit. Use it instead of saving `report_v7_FINAL.xlsx`. For SQL queries and code, Git does the same job more precisely.

### Personal data

Some data is about **people**: names, phone numbers, addresses, ID numbers, health information, salaries. Handle it with extra care. India's Digital Personal Data Protection Act, 2023, the European Union's GDPR, and similar laws elsewhere set rules for collecting, storing, and sharing it. The everyday habits: collect and keep only what you need; don't copy it to personal devices, personal email, or personal cloud accounts; share it only with people entitled to see it; and use anonymized or sample data for practice and demos. Chapter 64 covers privacy and governance in depth.

> **If you make a mistake, say so immediately.** Emailed a customer list to the wrong person? Clicked a suspicious link? Lost a laptop? Tell your manager and IT **straight away**. Minutes matter: a password can be reset, a sent email sometimes recalled, a laptop wiped remotely. Organizations forgive a reported mistake far more easily than a hidden one.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Opening a CSV directly in Excel and saving it | leading zeros gone, IDs as `4.52E+13`, codes turned into dates | Import with *Data → From Text/CSV*; set ID columns to Text |
| Wrong text encoding | `â‚¹`, `Ã©`, `â€™` in names and amounts | Import as UTF-8 |
| Confusing Mbps with MB/s | downloads "eight times slower than expected" | Divide Mbps by 8 for MB/s |
| Renaming a file's extension to "convert" it | the file won't open, or opens with a warning | Open the file and use *Save As* |
| Using "final", "new", or "(2)" in file names | nobody knows which file is current | Date-first names plus version history |
| Sending data as PDF | the receiver re-types or mis-copies tables | Share the CSV or Excel export |
| Keeping millions of rows in Excel | files take minutes to open; rows cut off at 1,048,576 | Use a database or Parquet |
| Pasting API keys or passwords into files and chats | anyone with the file can use the account | Store secrets in a password manager or secure settings |
| Sharing one login among a team | no record of who changed what | One account per person, with only the access they need |
| Treating cloud sync as a backup | a deletion or a bad save spreads to every copy | Keep separate, tested backups (3-2-1) |
| Unencrypted work laptop | a lost laptop becomes a data breach | Turn on drive encryption |
| Hiding a security mistake | a small incident becomes a large one | Report it immediately |

---

## In the real world: the Friday file

Before Meera (Chapter 1) joined, Riverstone's weekly sales report worked like this. Every Friday afternoon, Imran, who ran sales operations, exported orders from the billing system as CSV, opened the file in Excel, added a few formulas and a pivot table, and saved it as `Weekly Sales FINAL.xlsx` on his laptop. Then he emailed it to eleven people. Over one bad month, four things went wrong:

1. **Product codes broke.** Riverstone's new product range used codes such as `00731`. Excel turned them into `731`, and the lookup to the price list failed for every new product. Two weeks of reports understated new-product sales.
2. **Nobody knew which file was current.** Imran sent a corrected report on a Monday, as `Weekly Sales FINAL (2).xlsx`. Half the recipients kept using the Friday version, and the regional managers argued about numbers that came from two different files.
3. **The file grew until it choked.** Each week's data was pasted under the last. At 40 MB the workbook took four minutes to open, and some recipients' email rejected it.
4. **The laptop was stolen** from a car. It wasn't encrypted, and the workbook held two years of customer names, phone numbers, and prices.

Riverstone's fix used nothing more advanced than this chapter:

- The export was **imported** with codes set to text, and the billing system's **API** later replaced the manual export entirely.
- The report moved to **one shared location** with version history, and the email became a **link** to it, with the date in the file name. Everyone saw the same, current file.
- History moved out of the workbook into a **database**, and the report kept only the latest weeks, so it opened in seconds.
- Every company laptop was **encrypted**, customer phone numbers were removed from reports that didn't need them, and the IT team set up **tested 3-2-1 backups**.

None of those changes required a data engineer. They required someone who understood files, formats, APIs, and basic security well enough to notice what was wrong. Later in the book you'll automate a report of exactly this kind, Riverstone's Daily Sales Flash, end to end.

---

## Project: one dataset, five formats

**Goal:** see with your own eyes what each format stores, what it loses, and how each program treats it.

### Tools you'll need

- **A plain-text editor.** Notepad (Windows), TextEdit in plain-text mode (Mac), or a free code editor such as Visual Studio Code. Opening a CSV or JSON file in a text editor shows you what's really inside, without a spreadsheet's guesses.
- **Excel or Google Sheets**, for the project. Learn the *import* routes (*Data → From Text/CSV* in Excel; *File → Import* in Google Sheets), not just double-clicking.
- **A password manager and an authenticator app.** Set them up for your own accounts this week.
- **The companion files** (Appendix E): `orders_feb_2026` in five formats, for the project.

**Option A:** use the companion files `orders_feb_2026.csv`, `.xlsx`, `.json`, and `.xml`.
**Option B:** use your spending log from Chapter 1's project, and create the formats yourself: save it from your spreadsheet as `.xlsx` and as CSV (UTF-8), then type a JSON version of the first three rows by hand in a text editor, using section 2.5 as your model.

**Steps:**

1. **Open each file in a plain-text editor.** Which ones can you read? For the `.xlsx`, what do you see, and why?
2. **Find the missing values.** How does each format show a blank sales rep or delivery note? Can you tell "unknown" from "empty text" in each?
3. **Find the types.** In which formats can you tell that `net_revenue` is a number and `order_date` is a date, just by looking?
4. **Import the CSV into Excel or Google Sheets twice:** once by double-clicking, once through the import screen with every column set to Text. Add a row with a code like `00731` to your copy first. What differs?
5. **Compare sizes.** Record each file's size in bytes. Which is smallest? Why is the Excel file larger than the CSV for so little data?
6. **Break a CSV on purpose.** Remove the quotes around `"Gate 2, Okhla Phase II"`, save, and reimport. What happens to the columns?
7. **Write it up.** A one-page comparison table: format, readable as text, keeps types, shows blanks as, size, and "I would use it for…". Finish with three sentences of advice for a colleague who is about to email a CSV.

**Stretch goals:**

- Save the same data as a ZIP file and compare its size with the CSV.
- Type `₹` into one value in your spreadsheet, save it once as *CSV UTF-8* and once as plain *CSV (Comma delimited)*, then open both files in a text editor. Does the symbol survive in each?
- Check which of your own accounts have MFA switched on, and switch it on for the rest.

---

## Recap

- Computers store everything as **bits** (0s and 1s), grouped into **bytes**. Text is stored through an **encoding** such as **UTF-8**; the wrong encoding produces garbled characters. Decimals are usually stored approximately, which is why money needs exact types.
- Sizes go **KB → MB → GB → TB → PB**, each 1,000 times the last (or 1,024 in some software). Speeds are in **bits**, sizes in **bytes**: divide Mbps by 8.
- **Memory** is fast and temporary; **storage** is slower and permanent. Unsaved work lives only in memory.
- Files have **paths** and **extensions**. Name them date-first, never "final", and watch for hidden extensions.
- **CSV** is universal but has no types; **Excel** is for people; **JSON** and **XML** carry labeled data between systems; **PDF** is for reading; **Parquet** is compact, typed, and fast for large-scale analysis. Import CSVs carefully.
- **Databases** let many people use data at once, with rules and SQL.
- A **server** answers a **client's** requests over the **internet**; **HTTPS** encrypts the connection; the **cloud** is rented computers and services, up to finished applications (**SaaS**).
- An **API** is the waiter between programs: a request goes in, a response with a **status code** and usually JSON comes back. API keys are passwords.
- Protect **confidentiality, integrity, and availability**: unique passwords, MFA, least privilege, encryption, hashes, tested **3-2-1 backups**, version history, careful handling of personal data, and reporting mistakes immediately.

---

## Key terms

bit · byte · binary · ASCII · Unicode · UTF-8 · encoding · garbled text (mojibake) · floating point · kilobyte (KB) · megabyte (MB) · gigabyte (GB) · terabyte (TB) · petabyte (PB) · megabits per second (Mbps) · memory (RAM) · storage (SSD, hard disk) · file · folder / directory · path · extension · CSV · Excel workbook (.xlsx) · JSON · XML · PDF · Parquet · compression · lossless · lossy · database · database server · client · server · data center · internet · IP address · DNS · HTTP / HTTPS · cloud · SaaS · API · request · response · header · body · status code · API key · rate limit · webhook · CIA triad · confidentiality · integrity · availability · password manager · multi-factor authentication (MFA) · phishing · least privilege · encryption in transit · encryption at rest · hash · ransomware · backup · 3-2-1 rule · sync · version history · personal data

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can explain bits, bytes, and why `₹` takes more space than `R`.
- [ ] I can convert between KB, MB, GB, and TB, and between Mbps and MB/s, and I know why a 1 TB drive shows 931 GB.
- [ ] I know the difference between memory and storage, and what "saved" means for my work.
- [ ] I name files so they sort by date and never need the word "final".
- [ ] I can say which format I'd use for a person, an app, or a large dataset, and why.
- [ ] I import CSV files instead of double-clicking them when codes or IDs are involved.
- [ ] I can explain a server, the cloud, and an API to a non-technical colleague.
- [ ] I can read an API response and tell from its status code whether the problem is mine or the server's.
- [ ] My own accounts use unique passwords from a password manager, with MFA.
- [ ] I can explain the 3-2-1 rule and why syncing isn't a backup.

---

## Exercises

### Warm-up

1. Convert: (a) 3.5 GB to MB; (b) 250,000 KB to MB; (c) 2 TB to GB.
2. How many bytes does each take in UTF-8: `Riverstone`, `₹500`?
3. A friend's new laptop has "512 GB" of storage, but Windows shows about 476 GB. Is anything wrong? Explain in two sentences.
4. What file type is each of these, and which program would normally open it: `2026-03-31_stock.csv`, `invoice_9007.pdf`, `po_template.xlsm`, `export.json`, `setup.exe`?

### Core

5. How long, at best, does it take to download a 2 GB file on a 50 Mbps connection?
6. Choose the best format for each job, and say why in one line: (a) a monthly summary your manager will open and filter; (b) a website sending a new order to the sales system; (c) two years of sensor readings from Riverstone's machines, to be analyzed in the cloud; (d) a tax invoice sent to a customer; (e) a one-off list of 3,000 customers to import into a new email tool.
7. This line comes from a CSV file with seven columns. What's wrong with it, and how should it be written?
   `5010,Green Leaf Hotels,2026-03-03,Delivered,Farah Khan,20100.00,Leave at reception, back gate`
8. A script calls Riverstone's API and gets these replies on different days: `401`, `404`, `429`, `503`. For each, say whether the problem is probably on the script's side or the server's, and what you'd do.
9. Section 2.9 shows the hashes of two payment lines. A colleague sends you a backup file and its hash. You calculate the hash of the file you received and get a different value. What does that tell you, and what doesn't it tell you?

### Stretch

10. Kavya keeps her only copy of her spending logs in a Google Drive folder that syncs to her laptop. Does her setup meet the 3-2-1 rule? Describe one thing that could lose her data anyway, and a change that would fix it.
11. Riverstone's new product codes look like `00731`. Describe exactly how a code can lose its leading zeros between the billing system's CSV export and the price lookup in a workbook, and give two ways to prevent it.
12. Why must a sales ledger only ever be compressed losslessly? Give one example of what lossy compression would do to it.

### Think about it (no calculation needed)

13. A team shares one login for the company's CRM, and the password is pinned in a group chat. List three risks, and propose a better setup.
14. Your manager asks, "Should we keep our sales database on our own server in the office, or move it to the cloud?" Give two advantages of each option, and one question you'd ask before deciding.
15. You receive an email from "Riverstone Accounts" with an attachment called `Payment_Details.pdf` and the message "Urgent: confirm today or the supplier contract will be cancelled." What do you check before opening it?

---

## Answers

**1.** (a) 3.5 × 1,000 = **3,500 MB**. (b) 250,000 ÷ 1,000 = **250 MB**. (c) 2 × 1,000 = **2,000 GB**. (Counting in steps of 1,024 instead, as Windows does, the answers would be 3,584, about 244, and 2,048. Either is acceptable if you say which you used.)

**2.** `Riverstone` is 10 plain English letters: **10 bytes**. `₹500` is **6 bytes**: 3 for `₹` and 1 for each digit.

**3.** Nothing is wrong. The maker counts 512 GB as 512,000,000,000 bytes, while Windows divides by 1,024 at each step (1,024 × 1,024 × 1,024) and shows about 476.8 GB; it's the same storage counted a different way.

**4.** `2026-03-31_stock.csv`: a CSV table as plain text; a spreadsheet or text editor. `invoice_9007.pdf`: a PDF document; a PDF reader or browser. `po_template.xlsm`: an Excel workbook that can contain macros; Excel (be careful enabling macros from unknown senders). `export.json`: JSON data; a text editor, code editor, or a program that reads JSON. `setup.exe`: a Windows program that runs when opened; only open it if you trust exactly where it came from.

**5.** 50 Mbps ÷ 8 = 6.25 MB per second. 2,000 MB ÷ 6.25 = **320 seconds, about 5.3 minutes**, and in practice a little longer.

**6.** (a) **Excel**: people will read and filter it, and it keeps formatting and types. (b) **JSON through an API**: it's what apps exchange, and it can carry an order with its lines nested inside. (c) **Parquet**: large, typed, compressed, and fast to analyze by column. (d) **PDF**: a fixed document the customer reads and keeps, which looks the same everywhere. (e) **CSV**: nearly every tool imports it; set the ID and phone columns to text.

**7.** The delivery note contains a comma but isn't in quotes, so the line splits into **eight** values instead of seven: `Leave at reception` and ` back gate` become separate columns, and every program reading it will either reject the row or shift the data. Correct version:
`5010,Green Leaf Hotels,2026-03-03,Delivered,Farah Khan,20100.00,"Leave at reception, back gate"`

**8.** `401 Unauthorized`: the script's side. The API key is missing, wrong, or expired, so check how the key is stored and whether it has been changed. `404 Not Found`: usually the script's side: the ID or the address is wrong, or the record really doesn't exist. Check the ID before assuming the API is broken. `429 Too Many Requests`: the script's side. It's calling too often, so add a pause between calls and retry later. `503` (a 5xx code): the server's side. Retry after a delay, and if it continues, check the provider's status page or contact the API's owner.

**9.** Different hashes mean **the two files are not identical**: the file was changed or damaged somewhere between your colleague and you, or they calculated the hash on a different version. It doesn't tell you **what** changed, **where**, or **whether** the change was accidental or deliberate. Ask for the file again, compare the hashes, and don't use the backup until they match.

**10.** No. She has one copy that appears in two places, not three independent copies, and nothing is kept separately from her synced accounts. If she deletes a file, saves over it by mistake, or ransomware encrypts her laptop, the change **syncs to Drive** too. Version history might rescue her, but only for a limited time. A fix: a regular backup to an external drive kept at home, plus a second copy in a separate cloud backup service or account that doesn't sync changes automatically, and an occasional test that she can restore a file.

**11.** The billing system writes `00731` correctly into the CSV as text. When someone **double-clicks** the CSV, Excel guesses that `00731` is a number and stores **731**. If the file is saved, the damage is written back. The price list still says `00731`, so a lookup for `731` finds nothing. Prevention: (1) import the CSV with *Data → From Text/CSV* and set the product code column to **Text** before loading; (2) better still, get the data from the source system through a connection or an API that keeps the column's type, so no one opens the raw CSV at all. (Adding a letter prefix to codes, such as `P00731`, also prevents it, but changing codes is a business decision.)

**12.** A sales ledger can't lose a single digit: every amount, date, and code must come back exactly as it was written, so only **lossless** compression, such as ZIP, which restores exactly the original bytes, is safe. **Lossy** compression throws detail away, which is fine for a photo but not for data. On a ledger it might, for example, round ₹14,640.00 to ₹14,600 or turn product code `00731` into something close but different, and nobody could get the original values back. Ledgers compress well losslessly anyway, because columns such as status, product, and customer repeat the same values many times.

**13.** Risks: (1) nobody can tell who made a change or deleted a record, so mistakes and misuse can't be traced; (2) when someone leaves the team, they still know the password, and removing their access means changing it for everyone; (3) anyone who can read the chat, on any device, including a lost phone, can log in; and a single leaked password exposes the whole CRM. Better: one account per person, with permissions matched to each role (least privilege), MFA switched on, and access removed promptly when people leave.

**14.** *Own server:* direct physical control of where the data is; can work on the office network even when the internet is down. *Cloud:* no hardware to buy or maintain, with backups, updates, and failover handled by the provider; easy to scale up as data grows, and reachable securely from anywhere. Useful questions include: *"What happens if our office server fails at 2 a.m., and who fixes it?"*, *"Are there rules about which country our customer data must stay in?"*, and *"What would the cloud cost each month at our size, compared with buying and running our own server?"*

**15.** Check the **sender's real email address**, not just the display name; check whether the attachment is really a PDF, with extensions visible, because `Payment_Details.pdf.exe` is a program; notice the **pressure** ("urgent", "today", "cancelled"), a classic phishing sign; and **confirm by phone**, using a number you already have rather than one in the email, before opening the attachment or acting on it. If in doubt, report it to IT without opening it.

---

## Where this leads

- **Chapter 3, How a Business Runs on Data,** follows one Riverstone order through every system that stores and passes along its data.
- **Chapters 10 and 11** teach spreadsheets properly, including importing CSV files without damage.
- **Chapter 12, Databases & SQL Foundations,** turns the one-page preview in section 2.6 into a full, hands-on skill, including the exact decimal type databases use for money, and read-only accounts for analysts.
- **Chapter 17** shows the 0.1 + 0.2 surprise from section 2.1 in Python, with the code you run yourself.
- **Chapter 18** reads CSV, Excel, JSON, and Parquet files in Python, and calls real APIs, including the demonstration API from section 2.8.
- **Chapter 20** automates a report of exactly the Friday file's kind, Riverstone's Daily Sales Flash, including storing API keys safely.
- **Chapter 26** uses Git to keep versions of queries and code.
- **Part 5 (Chapters 45–52)** builds on formats, compression, the cloud, and APIs at company scale: hashes that detect changed files (Chapter 45), Parquet and columnar storage tested at scale (Chapter 49), how whole systems exchange data (Chapter 51), and the levels of cloud service (Chapter 52). **Chapter 58** extracts tables from PDFs with AI tools, with checks. **Chapter 64** covers security, privacy, and governance in depth, and **Chapter 65** keeps cloud bills under control.
- **Interview preparation:** file formats, APIs, and data security questions appear in the Data Engineering bank (Chapter 77) and the Automation & Integration bank (Chapter 78).


# Chapter 3. How a Business Runs on Data

> **Chapter at a glance**
>
> **You will learn to:** name a company's departments and the data each creates · follow one order from enquiry to cash, and say which system records each step · explain what ERP, CRM, HRMS, POS, e-commerce, and support systems do · tell a transaction from a report, and bookings from billings from collections · define a KPI so two people calculate the same number · describe how dashboards, meetings, and decision rights turn data into decisions · find where people copy, re-type, and email data by hand, and estimate the cost.
>
> **Before you start:** Chapter 1 (rows, columns, grain, data quality) and Chapter 2 (files, databases, and APIs).
>
> **Time needed:** 3–4 hours, including the exercises and the project.
>
> **Tools:** a pen and a notebook. A spreadsheet or a free diagram tool is useful for the project, but optional.
>
> **Practice data:** Riverstone Supplies' first quarter of 2026: twelve orders, ten invoices, and ten payments from the mini database you'll query yourself in Chapter 12. Every number in this chapter was calculated from that database and checked by script.

---

## Why this matters

In Chapter 1 you learned what data is. In Chapter 2 you learned where it lives. This chapter answers the question that sits between those and every job in this book: **why does a business have all this data in the first place, and who uses it?**

The short answer is that a company *is* a chain of people handing work to each other. A salesperson hands an order to the warehouse. The warehouse hands a delivery to finance. Finance hands a number to the managing director. Every handover leaves a record, and those records are the data you'll clean, query, chart, and model for the rest of your career.

Analysts who understand this chain are far more useful than analysts who only know the tools. When a manager asks, *"What were sales last month?"*, the analyst who knows the chain asks one question back: *"Orders placed, invoices raised, or cash received?"* Those are three different numbers. At Riverstone Supplies in January 2026 they were ₹1,16,210, ₹1,04,210, and ₹0. By the end of this chapter you'll know exactly why, and you'll never again hand over a "sales" number without saying which one it is.

This chapter also starts the book's **automation** thread. Before you can automate anything, you have to see where people work by hand. Section 3.7 shows you how.

---

## In plain English

Think of a relay race. Four runners, one baton. Each runner takes the baton, runs their stretch, and hands it on. Races are often lost at the handovers.

A business works the same way, and **data is the baton**. The salesperson writes down what the customer wants and passes it on. The warehouse packs the goods, records what it shipped, and passes that on. Finance sends a bill, records what was paid, and passes it on to the people who write reports.

Three things follow from the picture:

- **Each runner only sees their own stretch.** The warehouse doesn't care how long the customer took to decide; sales doesn't see when the cash arrives. That's why different departments quote different numbers for the "same" thing.
- **Handovers are where things go wrong.** An order typed twice can be typed wrong once. A file emailed around can be out of date by the time it's opened.
- **Someone has to watch the whole race.** Managers need to know how the team is doing, not just each runner. That's what reports, KPIs, and dashboards are for, and it's where analysts come in.

---

## 3.1 The departments of a company and the data they create

Meet the company. **Riverstone Supplies** makes and distributes plastic storage boxes, kitchenware, industrial crates, and a small range of furniture. Its customers are retailers (like Sharma Hardware in Mumbai), hotels and caterers (like Green Leaf Hotels in Pune), and wholesalers (like Coastal Foods in Chennai). It has two plants:

- **Plant 1, Taloja** (Navi Mumbai), which makes storage boxes and kitchenware.
- **Plant 2, Chakan** (Pune), which makes industrial crates and furniture.

Finished goods go to the central warehouse, **Bhiwandi Main**, near Mumbai, and are shipped to customers from there.

Each department exists to do a job, and creates data as a side effect of doing it. Figure 3.1 shows the eight you'll meet most often.

![Eight departments of Riverstone Supplies, each listing the data it creates, all feeding management decisions](figures/fig3-1-departments-and-their-data.svg)

*Figure 3.1 — Every department creates data while doing its own job. Management needs all of it to decide.*

| Department | Its job | Data it creates | A question the data answers |
|---|---|---|---|
| **Sales** | win and keep customers | enquiries (**leads**), quotes, orders, visit notes | *Which customers are ordering less than last year?* |
| **Marketing** | make the right people aware of the products | campaigns, website visits, trade-fair contacts | *Which campaign brought in enquiries that became orders?* |
| **Purchasing** | buy raw materials and packaging | suppliers, purchase orders, goods received | *Which supplier delivers late most often?* |
| **Production** | make the goods | production plans, machine runs, output, scrap | *How much plastic did we waste last month, and on which machine?* |
| **Warehouse and dispatch** | store, pick, pack, and ship | stock levels, picking lists, **delivery challans**, proofs of delivery | *How many orders left the warehouse late?* |
| **Finance** | bill customers, collect cash, pay bills, keep the books | invoices, payments, expenses, budgets, tax records | *How much are customers overdue, and who?* |
| **HR** | hire, pay, and look after employees | employee records, attendance, payroll, hiring | *How long does it take to fill a job?* |
| **Customer support** | fix problems after the sale | complaints, **tickets**, returns, resolution times | *Which product causes the most complaints?* |

A **lead** is a possible customer who has shown interest but hasn't bought. A **delivery challan** is the document that travels with goods in India, listing what's in the truck (elsewhere, a delivery note).

Finance needs sales' orders to raise invoices. Production needs them to plan what to make. Management needs everything to decide where to spend money. **Data created in one department is almost always used in another**, and that is the root of most of the problems, and most of the jobs, in this book.

> **Try it.** Pick a company you've dealt with recently: a food delivery app, your bank, a hospital. Name three departments it must have and one record each creates about *you*.

---

## 3.2 Following one order from enquiry to cash

To see how departments depend on each other's data, follow one piece of business all the way through. This journey is called **order to cash**, or **lead to cash** when it includes winning the customer.

Here is a real order from Riverstone's database: **order 5001**, from Sharma Hardware, a retail customer in Mumbai. The order has two lines:

| Product | Quantity | List price | Discount | Line value |
|---|---|---|---|---|
| Storage Box 10L | 20 | ₹450 | 0% | ₹9,000 |
| Water Bottle 1L | 50 | ₹120 | 5% | ₹5,700 |
| **Total** | | | | **₹14,700** |

*Source: Mini database (Jan–Mar 2026).*

Check it by hand: 20 × ₹450 = ₹9,000. 50 × ₹120 = ₹6,000, less 5% is ₹5,700. ₹9,000 + ₹5,700 = ₹14,700. ✓ (As in the rest of this book, tax is left out to keep numbers simple.)

The order row only says *who ordered what, when*. But it has a history before it and a future after it, and every step was recorded somewhere. Figure 3.2 shows all ten steps.

![Ten steps of order 5001, from a website enquiry in October 2025 to the January 2026 sales report, with the date, what happened, and the record created at each step](figures/fig3-2-one-order-enquiry-to-cash.svg)

*Figure 3.2 — One order, ten steps. Each box shows the date, what happened, and the record it left behind.*

**1. Enquiry (22 October 2025).** Rakesh, the buyer at Sharma Hardware, fills in the enquiry form on Riverstone's website: name, shop, city, phone, and "interested in storage boxes for our shop". The form creates a **lead** in the CRM, the sales team's system for tracking deals (section 3.3). Sharma Hardware isn't a customer yet; it's a row with a status of *New*.

**2. New customer (4 November 2025).** Neha Kulkarni, a sales executive, visits the shop. Rakesh wants to buy on credit, so finance runs a credit check and agrees **payment terms** of 30 days: Sharma Hardware can pay up to 30 days after each invoice. Finance creates the customer in the ERP, Riverstone's main business system, where it gets **customer ID 1** and a signup date of 2025-11-04. Every later order, invoice, and payment carries that ID.

**3. Quote (22 December 2025).** Rakesh asks for prices. Neha builds a quote, Q-2025-118, in a spreadsheet, emails it as a PDF, and logs it against the lead in the CRM. A **quote** is an offer: *these products, at these prices, until this date*.

**4. Order (5 January 2026).** Rakesh replies to the quote email: "Please send 20 of the 10-litre boxes and 50 bottles." Neha opens the ERP and **types the order in**: customer 1, two lines, prices, a 5% discount on the bottles that she agreed on the phone. The ERP creates **order 5001** with a status of *Pending*, dated 2026-01-05, with Neha as the sales rep.

**5. Stock check (5 January 2026).** Both products are **made to stock**: Plant 1 at Taloja makes them in advance and sends them to Bhiwandi Main. But Bhiwandi Main updates the ERP's stock figures once a day from its own spreadsheet, so Neha phones the warehouse to be sure. The stock is **reserved** for order 5001.

**6. Dispatch (6 January 2026).** The warehouse prints a **picking list**, picks and packs the boxes and bottles, and ships them with a delivery challan. The ERP marks the order *Shipped*.

**7. Invoice (6 January 2026).** When goods ship, the ERP raises **invoice 9001** for ₹14,700, dated 2026-01-06, **due** on 2026-02-05, 30 days later, because of the terms agreed in step 2. An **invoice** is the formal request for payment: the sale becomes money the customer owes.

**8. Delivery (8 January 2026).** The truck arrives. Rakesh signs a paper **proof of delivery** (POD). Someone at Bhiwandi Main scans it, emails it to finance, and updates the order to *Delivered*.

**9. Payment (2 February 2026).** Sharma Hardware pays ₹14,700 by bank transfer. The bank statement shows a short reference, "SHARMA HW JAN". A finance assistant works out that it pays invoice 9001 and records **payment 1** against it.

**10. Report (3 February 2026).** The team prepares the **January sales report**. Invoice 9001 is one of the three behind the line *"January: ₹1,04,210"*.

**It took a long time.** From enquiry to cash was 103 days. Once the order existed, things moved faster: order to invoice 1 day, invoice to payment 27 days, order to cash 28 days. Each gap comes from subtracting two dates recorded by two different departments.

**The data lives in several places.** The lead and quote are in the CRM; the customer, order, invoice, and payment in the ERP; the proof of delivery is a scanned image in someone's email; the report is an Excel file. To answer *"How long does it take to turn an enquiry into cash?"* you need two systems that don't share an ID for Sharma Hardware: the CRM knows it by a lead number, the ERP as customer 1.

**People carried the baton by hand at several handovers.** Neha re-typed the order and phoned about stock; someone scanned paper, matched a bank line by eye, and built the report. Section 3.7 puts a cost on these steps.

> **Simplification note.** Real processes have more branches: partial shipments, back orders, credit holds, returns, and credit notes. Order 5001 is a clean run. You'll meet messier cases in the data itself: order 5004 was cancelled, invoice 9002 was paid in two instalments, and invoice 9007 hasn't been paid at all.

---

## 3.3 Business systems: ERP, CRM, HRMS, POS, and e-commerce

A **business system** is software a department uses for its daily work, storing the records in a database (section 2.6). You'll hear these abbreviations in your first week of any data job.

| System | What it's for | Typical records | Main users | Examples of real products |
|---|---|---|---|---|
| **ERP** (enterprise resource planning) | running the core of the business: sales orders, stock, production, purchasing, invoicing, and accounts, all in one system | customers, products, orders, invoices, payments, stock movements, purchase orders | sales operations, warehouse, production, purchasing, finance | SAP, Oracle NetSuite, Microsoft Dynamics 365, Odoo; TallyPrime is common in smaller Indian firms |
| **CRM** (customer relationship management) | winning and keeping customers | leads, contacts, calls, meetings, quotes, deals and their stages | sales, marketing, customer success | Salesforce, HubSpot, Zoho CRM |
| **HRMS** (human resource management system) | managing employees | employee records, attendance, leave, payroll, hiring | HR, managers, every employee for leave and payslips | Workday, Zoho People, Keka |
| **POS** (point of sale) | recording sales at a shop counter | bills, items scanned, payment method, cashier, time | shop staff | the billing app at Sai Krupa General Store (Chapter 1); supermarket tills |
| **E-commerce platform** | selling online | product listings, carts, online orders, payments, website visits | online sales, marketing | Shopify, WooCommerce, marketplaces |
| **Support desk** (ticketing system) | tracking customer problems until they're fixed | tickets, messages, categories, status, time to resolve | customer support | Zendesk, Freshdesk |

Riverstone's set-up is typical for a mid-sized manufacturer. This book names its systems by type, because the lessons don't depend on the brand:

- **The ERP** holds customers, products, employees (as sales reps), orders, order lines, invoices, and payments, plus stock, production, and purchasing. People at Riverstone still call its invoicing module "the billing system"; that's where Imran exported his Friday file from in Chapter 2. **The mini database behind this chapter's numbers is a small copy of the ERP's sales tables.**
- **The CRM** holds leads, contacts, quotes, and the sales pipeline.
- **The website** shows the catalog and feeds enquiries to the CRM (customers don't order online). **The support desk** records complaints and returns. **The HRMS** holds employees and payroll.
- **Spreadsheets and email** fill every gap between them: quotes, the warehouse's stock sheet, the monthly report.

Riverstone has no POS, because it sells to businesses. But Sharma Hardware's POS knows exactly which Riverstone boxes sell on a Saturday afternoon, and Riverstone never sees that unless Sharma shares it: **the most useful data about your products often sits in someone else's system.**

### Systems of record and the gaps between systems

Every important fact should have one official source, its **system of record** (or **source of truth**). At Riverstone, that's the ERP for orders and invoices, the CRM for leads, and the HRMS for employees. When the CRM and the ERP disagree about what Sharma Hardware bought, the ERP wins.

The trouble is the gaps. Riverstone's CRM and ERP aren't connected: when a quote becomes an order, someone must mark the deal *Won* in the CRM, and a cancellation in the ERP never reaches the CRM unless someone remembers. Connecting systems so data flows between them automatically is **integration**.

> **Watch out: a spreadsheet can become the system of record by accident.** If the warehouse's stock sheet is more current than the ERP, the sheet is now the source of truth for stock, with no access control or history (section 2.9).

---

## 3.4 Transactions and reports: booked, billed, and collected

Everything recorded in Figure 3.2 is a **transaction**: a record of one business event, written when it happens. *Invoice 9001 was raised for ₹14,700.* Transactions are the rows in a business system's database.

A **report** summarizes many transactions to answer a question (*"How much did we invoice in January?"*), at a point in time, using rules someone chose.

| | Transaction | Report |
|---|---|---|
| **What it is** | one event | a summary of many events |
| **Grain** (Chapter 1) | one order, one invoice, one payment | one month, one customer, one product |
| **Created** | by the business system, as work happens | by a person or a scheduled job, after the fact |
| **Changes?** | should be corrected, not rewritten; a cancellation is a new status or a new record | changes whenever the data or the rules change |
| **Example** | invoice 9001: ₹14,700, due 2026-02-05 | "January billings: ₹1,04,210" |

Systems for transactions are tuned to write one record quickly and safely; reporting needs to read millions and add them up. That's why growing companies move reporting into a separate **data warehouse**.

### Three numbers called "sales"

Because reports apply rules, **two reports built from correct transactions can give different answers to the same question.** The classic case is "sales", which can mean three things, each counted at a different step of Figure 3.2:

- **Bookings**: the value of orders placed (step 4). The earliest sign of sales work.
- **Billings**: the value of invoices raised (step 7). Money customers owe.
- **Collections**: cash that arrived (step 9). What pays salaries and suppliers.

Here are all three for Riverstone's first quarter of 2026:

| Month | Booked (orders placed) | Billed (invoiced) | Collected (cash in) |
|---|---|---|---|
| January | ₹1,16,210 | ₹1,04,210 | ₹0 |
| February | ₹1,61,700 | ₹1,61,700 | ₹64,700 |
| March | ₹58,020 | ₹31,800 | ₹1,32,550 |
| **Quarter** | **₹3,35,930** | **₹2,97,710** | **₹1,97,250** |

*Source: Mini database (Jan–Mar 2026).*

![Labelled horizontal bars for January, February, and March 2026 showing booked, billed, and collected amounts](figures/fig3-3-booked-billed-collected.svg)

*Figure 3.3 — Same company, same quarter, three honest answers to "what were sales?"*

Every gap traces to specific transactions:

- **January booked ₹1,16,210 but billed ₹1,04,210.** The difference, ₹12,000, is order 5004 from Green Leaf Hotels: 100 water bottles, placed on 20 January and cancelled. Figure 3.3 and the table count bookings the way Riverstone's sales team reports them from the CRM, as every order placed, so the cancelled order is in. It was never shipped or invoiced.
- **January collected ₹0.** Every January invoice had 30-day terms, so none was due until February. Sharma Hardware's ₹14,700 arrived on 2 February.
- **February's three numbers.** All five February orders shipped and were invoiced in February, so bookings and billings match at ₹1,61,700. The ₹64,700 collected was for *January's* invoices: ₹14,700 from Sharma Hardware, ₹40,000 of Coastal Foods' ₹73,260, and ₹10,000 of Patel Kitchenware's ₹16,250.
- **March booked ₹58,020 but billed ₹31,800.** Order 5012 from Metro Mart, worth ₹26,220, is still *Pending* on 31 March: booked, not yet shipped, so not invoiced. ₹58,020 − ₹26,220 = ₹31,800. ✓
- **March collected more than it billed**, mostly February's invoices being paid. Cash lags billings by about the payment terms.

And the quarter reconciles:

- Bookings ₹3,35,930 − cancelled ₹12,000 − pending ₹26,220 = billings ₹2,97,710. ✓
- Billings ₹2,97,710 − collected ₹1,97,250 = **₹1,00,460 still owed by customers**, which finance calls **receivables** (or accounts receivable). ✓

> **Watch out: "sales" without a definition.** If you don't know which of the three is meant, ask. If you can't, give the name and rule with the number: *"Billed sales (invoices raised) in January: ₹1,04,210."* Otherwise two departments argue about who is wrong when both are right.

> **Simplification note.** Accountants recognize **revenue** under formal accounting standards, which decide exactly when a sale counts. This book uses invoices as a stand-in for revenue, as the rest of the book does. In a real company, ask finance which rule applies before publishing a revenue number; this is general information, not accounting advice.

### When a report runs matters too

**Timing** also makes reports differ. Run on 31 March, a report shows order 5012 as *Pending*; run on 10 April, after it ships, it shows the order billed in April. Good reports state their run date and **cut-off** ("orders placed up to 31 March 2026"), which is why this book fixes "today" for each dataset.

---

## 3.5 What a KPI is

Managers can't read thousands of transactions or dozens of reports. They need a few numbers that show at a glance whether the business is on track.

A **metric** is any number you measure. A **KPI** (key performance indicator) is a metric chosen as one of the few that matter most, with a target, an owner, and a regular review.

Here are nine KPIs Riverstone's management could track, calculated for the first quarter of 2026 as of 31 March:

| KPI | Definition | Q1 2026 | Owner |
|---|---|---|---|
| **Bookings** | value of orders placed, excluding cancelled orders | ₹3,23,930 (includes ₹26,220 pending) | Sales Head |
| **Billings** | value of invoices raised | ₹2,97,710 | Finance Manager |
| **Collections** | cash received from customers | ₹1,97,250 (66.3% of billings) | Finance Manager |
| **Gross margin** | (billings − cost of the products sold) ÷ billings | 22.6% | Finance Manager |
| **Average order value (AOV)** | billings ÷ number of invoiced orders | ₹29,771 | Sales Head |
| **Cancellation rate** | cancelled orders ÷ all orders placed | 8.3% (1 of 12) | Sales Head |
| **Overdue receivables** | unpaid amounts on invoices past their due date | ₹88,760 of ₹1,00,460 owed | Finance Manager |
| **Average days to collect** | days from invoice to final payment, for fully paid invoices | 31.6 days | Finance Manager |
| **Active customers** | customers with at least one non-cancelled order in the period | 7 of 8 | Sales Head |

*Source: Mini database (Jan–Mar 2026).*

Check two of them by hand. **Gross margin:** the products on invoiced orders cost Riverstone ₹2,30,450 to make, so the margin is ₹2,97,710 − ₹2,30,450 = ₹67,260, and ₹67,260 ÷ ₹2,97,710 = 22.6%. ✓ **Average days to collect:** five invoices are fully paid, taking 27, 51, 26, 33, and 21 days; they add up to 158, and 158 ÷ 5 = 31.6 days. ✓ (Invoice 9001, the one from Figure 3.2, is the 27.)

### A KPI needs a definition, not just a name

"Average order value" sounds precise. It isn't. Divide bookings by orders and you get ₹3,23,930 ÷ 11 non-cancelled orders = ₹29,448. Divide billings by invoiced orders and you get ₹29,771. Both are reasonable; they're different KPIs with the same name. You've already met the same problem with bookings: the table in section 3.4 counts the cancelled order (₹3,35,930 for the quarter), and the KPI table above leaves it out (₹3,23,930). A usable KPI definition answers six questions:

1. **Formula:** exactly what's divided by what?
2. **Inclusions and exclusions:** are cancelled orders in? Pending? Returns? Tax?
3. **Time:** which date decides the month: order date, invoice date, or payment date?
4. **Source:** which system and table? (The ERP's `invoices` table, not the CRM.)
5. **Owner:** who decides when the definition changes?
6. **Target and review:** what's good, and who looks at it how often?

Together, those answers are a **KPI definition**: Chapter 1's data dictionary one level up, saying what a number on a dashboard means.

> **Watch out: a KPI that can be improved without improving the business.** If reps earn a bonus on bookings, a large order booked at quarter-end and later cancelled raises bookings and gains nothing. Pair KPIs that keep each other honest: bookings *with* cancellation rate, billings *with* collections.

### Leading and lagging

**Lagging indicators**, like collections and gross margin, report what already happened: accurate, but too late to change. **Leading indicators**, like new leads, quotes, and bookings, move first: less certain, but early enough to act on. In Figure 3.2, the early steps lead and the late steps lag. A sales head who watches only collections learns about a bad quarter three months late.

---

## 3.6 Dashboards, meetings, and who decides what

Data changes nothing until someone uses it to decide, usually on **dashboards** and in **meetings**.

A **dashboard** is a screen of a few KPIs and charts, usually refreshed automatically from the systems of record, that answers the questions its viewer asks every week.

Companies look at their numbers on a rhythm. Riverstone's is typical:

| When | Meeting | Who attends | What they look at | Decisions made |
|---|---|---|---|---|
| **Every morning** | dispatch stand-up at Bhiwandi Main | warehouse supervisor, dispatch team | orders to ship today, stock shortfalls | which orders ship first; what to chase from the plants |
| **Every Monday** | weekly sales review | Anita Rao (Sales Head), Vikram Singh (Sales Manager), sales executives | bookings, quotes sent, top open deals | which deals to push; which customers to visit |
| **First week of each month** | monthly business review | managing director, department heads | booked, billed, and collected; margin; overdue receivables | where to spend; which problems to fix; whether to change prices |
| **Every quarter** | board review | managing director, board of directors | results against the annual plan | strategy, investment, targets for next year |

The closer a meeting is to daily work, the more detailed its data; the more senior, the more summarized and lagging. A common first analyst job is building the monthly business review pack.

### Decision rights: who decides what

Written rules for who owns which decision are called **decision rights**. Riverstone's discount rules are an example: the bigger the discount, the more senior the approver.

| Discount on an order line | Who approves | Data they need to decide |
|---|---|---|
| up to 5% | the sales executive | the customer's order history |
| over 5% and up to 10% | the Sales Manager (Vikram Singh) | order history, the margin on the product at that price |
| over 10% | the Sales Head (Anita Rao), after checking with the Finance Manager (Suresh Menon) | margin at that price, the customer's payment record, overdue amounts |

The data follows the rules: Neha's 5% on order 5001 needed no approval. Rahul's 10% on Coastal Foods' orders 5002 and 5007 went to Vikram. Farah's 12% on Northgate Distributors' 60 industrial crates (order 5009) needed Anita.

Anita needed margin and payment data from finance and order history from the ERP. **The person who decides is rarely the person who holds the data.** Getting the right data to them, in time, in a form they can read in a minute, is the job this book trains you for.

---

## 3.7 Where manual work hides

Go back to Figure 3.2 and ask one question at every step: *did a person copy, re-type, check, or carry data by hand here?* Figure 3.4 marks the answers.

![The same ten steps of order 5001, with six steps outlined and marked with an exclamation badge where a person copies, re-types, or checks data by hand](figures/fig3-4-where-manual-work-hides.svg)

*Figure 3.4 — Six of the ten steps depend on someone moving data by hand.*

| Step | What a person does by hand | What can go wrong |
|---|---|---|
| **3. Quote** | builds the quote in a spreadsheet, saves a PDF, emails it, and logs it in the CRM | old price list used; quote never logged, so the CRM undercounts |
| **4. Order** | reads the customer's email and re-types the order into the ERP | wrong quantity, wrong product code, discount forgotten |
| **5. Stock check** | phones the warehouse, because the ERP's stock figures are updated once a day from a spreadsheet | promises stock that's already gone |
| **8. Delivery** | scans a signed paper POD, emails it to finance, updates the order status | lost paper; order left as *Shipped* for weeks |
| **9. Payment** | reads the bank statement and matches each payment to an invoice | payment matched to the wrong invoice; customer chased for money they've paid |
| **10. Report** | exports data, pastes it into Excel, fixes formulas, emails the file | the Friday file problems from Chapter 2: wrong version, broken formulas, a report on one laptop |

These steps have names:

- **Re-keying**: typing data that already exists in one place into another (step 4), inviting the typing errors from Chapter 1.
- **Copy-paste integration**: moving data between spreadsheets or systems by copying it (step 10).
- **Emailing files around** (steps 3, 8, and 10): the data stops updating the moment it's attached.
- **Manual matching**, or **reconciliation**: pairing up two sets of records by eye (step 9).
- **Shadow systems**: personal spreadsheets that hold data the official system should hold, like the warehouse's stock sheet (step 5).

### Why it matters

**Time.** Manual work is small per item and large in total. Suppose a sales team re-types 40 emailed orders a week at about 6 minutes each: 240 minutes, or 4 hours a week, which over a 50-week year is 200 hours, about five working weeks of one person's time. (Round numbers for illustration; exercise 9 works a similar estimate.)

**Errors, delay, and people.** Mistyped orders are found when the customer receives the wrong goods. A report built by hand on the third of the month can't be seen on the first. And when only one person knows how the report is put together, like Imran and his Friday file in Chapter 2, it stops when they're on leave.

### How to find manual work in any process

Ask five questions at every step:

1. **Where does this data first enter a system?** Ideally once, at the source (Chapter 1).
2. **Is it typed again anywhere later?** If yes, that's re-keying.
3. **Does it travel by email, chat, phone, or paper?** Each of those is a handover with no record in a system.
4. **Does anyone keep their own spreadsheet of it?** That's a shadow system.
5. **Does someone check or match things by eye?** That's reconciliation, and usually the slowest step.

Then estimate *how many times a week, how many minutes each*. A list of manual steps with hours attached is where every automation project starts.

### Not every manual step should be automated

Anita approving a 12% discount is a judgment, and it should stay with a person; what can be automated is sending her the margin and payment data. And automating a broken process gives you a fast broken process: fix the process first. The book returns to each of Riverstone's manual steps later, and shows how to automate the ones that should be.

> **Interview extra point.** When an interviewer asks, *"What were sales last month?"*, or gives you a case with a "revenue" figure, say which definition you're using (booked, billed, or collected) before you calculate. It shows in one sentence that you understand the business, not only the tools. Chapter 75 has practice questions.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Quoting "sales" without saying which | two managers argue about a ₹12,000 difference | Name the number: booked, billed, or collected, with its rule |
| Treating a difference between reports as an error | hours spent hunting for a bug that isn't there | Reconcile first: cancellations, pending orders, timing, and payment terms explain most gaps |
| Assuming systems agree | CRM "won deals" total doesn't match ERP orders | Find the system of record for each fact and use it |
| Reporting a KPI without a written definition | the same KPI name gives different values in different files | Write the formula, inclusions, date rule, source, and owner |
| Rewarding a single KPI | bookings rise while cancellations rise too | Pair KPIs that keep each other honest |
| Ignoring the report's run date | the same report shows a different March on 10 April | State the cut-off and the date the report was run |
| Automating before fixing | wrong numbers delivered faster | Fix the process and the data, then automate |
| Automating away a judgment | a discount approved by a rule nobody questions | Keep decisions with people; automate getting them the data |

---

## In the real world: three numbers for January

It's Tuesday, 3 February 2026. The managing director's monthly business review is on Thursday, and two numbers for January have just reached the MD's inbox. Anita's weekly sales summary, pulled from the CRM's pipeline, says **January sales: ₹1,16,210**. Suresh Menon, the Finance Manager, sent his month-end report from the ERP: **January sales: ₹1,04,210**, and underneath it, **cash received in January: ₹0**.

The MD replies to both: *"Which one is right? And why did we collect nothing?"*

Anita asks Meera Iyer to find out. Meera doesn't start by deciding who's wrong. She asks: *which step of the order does each report count?*

**1. What does each report count?** Anita's summary adds up deals marked *Won* in the CRM, which happens when an order is placed: that's **bookings**. Suresh's report adds up invoices in the ERP: **billings**. His second line is **collections**.

**2. What's in one and not the other?** Meera lists January's orders from the ERP and January's won deals from the CRM side by side:

| Order | Customer | ERP status | Value | In CRM "won"? | Invoiced? |
|---|---|---|---|---|---|
| 5001 | Sharma Hardware | Delivered | ₹14,700 | yes | yes, 9001 |
| 5002 | Coastal Foods | Delivered | ₹73,260 | yes | yes, 9002 |
| 5003 | Patel Kitchenware | Delivered | ₹16,250 | yes | yes, 9003 |
| 5004 | Green Leaf Hotels | Cancelled | ₹12,000 | yes | no |

*Source: Mini database (Jan–Mar 2026).*

The CRM total is ₹1,16,210. The invoiced total is ₹1,04,210. The difference is exactly order 5004: Green Leaf Hotels cancelled its 100 water bottles in the ERP, and nobody updated the deal in the CRM, because the systems aren't connected.

**3. Why no cash?** All three invoices had 30-day terms. The earliest, 9001, was due on 5 February. Sharma Hardware paid ₹14,700 yesterday, 2 February, three days early. Coastal Foods' due date is 9 February and Patel Kitchenware's is 14 February. Every invoice raised in January falls due in February, and no older invoices were waiting to be paid, so zero cash in January is exactly what 30-day terms predict.

**4. Does it reconcile?** ₹1,16,210 − ₹12,000 = ₹1,04,210. ✓

On Wednesday afternoon, Meera sends Anita and Suresh a half-page note:

> *"Both reports are correct; they count different steps. **Booked** in January (orders placed, per the CRM): ₹1,16,210. **Billed** (invoices raised, per the ERP): ₹1,04,210. The ₹12,000 difference is Green Leaf Hotels' order 5004, cancelled in the ERP but still marked Won in the CRM; I've asked Neha's team to update it. **Collected**: ₹0, because January's invoices aren't due until 5–14 February; ₹14,700 has already arrived. Suggestion: the monthly pack shows all three lines with a one-line definition under each, and the ERP is the source for billed and collected."*

On Thursday the pack has three lines instead of one, and the meeting discusses what the numbers mean instead of which is true.

Meera used no tool or formula, only the order's journey, systems of record, three definitions of "sales", and a reconciliation to the rupee. She also found a failed manual handover and fixed it. That's this chapter, applied in an afternoon.

---

## Project: map the data flow of one process

**Goal:** map one real process the way Figure 3.2 maps order 5001, find its manual work, and propose one improvement.

### Tools you'll need

- **A notebook and pen.** Enough for every exercise, and the best way to draw your first process map.
- **A spreadsheet** (Excel or Google Sheets, optional). Useful for the project's step table and time estimates. Chapter 10 teaches both from the beginning.
- **A diagram tool** (optional). diagrams.net (also called draw.io) is free and runs in a browser; PowerPoint, Google Slides, and Google Drawings work too. Boxes and arrows are all you need.
- **The Riverstone mini database.** Not needed yet; Chapter 12 installs it and queries the orders, invoices, and payments you followed here.

**Step 1. Choose a process** you can observe or ask about: an expense claim, a customer return, a monthly report, or outside work, how a local shop restocks or a clinic books appointments.

**Step 2. List 6 to 12 steps** in order, recording six things for each:

| Column | What to write |
|---|---|
| `step` | a number and a two-word name |
| `who` | the role (not a person's name) |
| `what_happens` | one sentence |
| `data_created_or_used` | the record: a form, a bill, a row in a system |
| `where_it_lives` | system, spreadsheet, paper, email, someone's memory |
| `how_it_moves_on` | automatic, typed again, emailed, phoned, carried |

**Step 3. Draw it.** Boxes for steps, arrows for handovers, the record written under each box, as in Figure 3.2.

**Step 4. Mark the manual work.** Ask the five questions from section 3.7 at every step. Mark each manual handover with a symbol, as Figure 3.4 does with "!".

**Step 5. Put a number on it:** hours per month for each manual step, with your assumptions.

**Step 6. Name one KPI** that shows whether the process works (for example, "days from return request to refund"), defined with section 3.5's six questions.

**Step 7. Propose one improvement** in three sentences: what changes, what it saves, and what could go wrong.

Here is a short worked start, for the restocking process at Sai Krupa General Store from Chapter 1:

| step | who | what_happens | data_created_or_used | where_it_lives | how_it_moves_on |
|---|---|---|---|---|---|
| 1 Spot low stock | shop assistant | notices a shelf is nearly empty | item name | memory | told to the owner |
| 2 Write list | owner | writes items and quantities to reorder | reorder list | paper notebook | photographed and sent by chat |
| 3 Place order | distributor's salesperson | types the list into the distributor's app | purchase order | distributor's system | automatic |
| 4 Receive goods | shop assistant | checks delivered items against the paper bill | delivery bill | paper | carried to the owner |
| 5 Update stock | owner | adds received quantities in the billing app | stock levels | billing app (POS) | typed again |

Steps 1, 2, and 5 are manual, and step 5 re-keys what the bill already says. If the billing app flagged low stock, step 1 wouldn't depend on someone noticing.

**Deliverable:** the table, drawing, hours estimate, KPI definition, and proposal. Keep it for Chapter 25.

---

## Recap

- A company is a chain of departments handing work to each other. **Every handover leaves data**, and data created in one department is almost always used in another.
- **Lead to cash** follows one piece of business from enquiry to payment. Riverstone's order 5001 took ten steps: 103 days from enquiry to cash, 28 from order to cash.
- **Business systems** record daily work: **ERP** (orders, stock, invoices, accounts), **CRM** (leads, quotes, deals), **HRMS** (employees, payroll), **POS** (shop sales), **e-commerce** (online orders), and **support desks** (tickets). Spreadsheets and email fill the gaps between them.
- Each fact should have one **system of record**. Systems that aren't **integrated** drift apart.
- A **transaction** records one event; a **report** summarizes many, using rules, at a point in time.
- "Sales" can mean **bookings** (orders placed), **billings** (invoices raised), or **collections** (cash received). For Riverstone's January: ₹1,16,210, ₹1,04,210, and ₹0, all correct. Reconcile them with cancellations, pending orders, and payment terms.
- A **KPI** is a chosen metric with a **definition**, an owner, a target, and a review. Pair KPIs so none can be gamed alone; watch **leading** as well as **lagging** indicators.
- **Dashboards and meetings** turn data into decisions on a rhythm. **Decision rights** say who decides; the decider rarely holds the data.
- **Manual work hides** in re-keying, copy-paste, emailed files, manual matching, and shadow systems. Find it with five questions, count it in hours, fix the process first, and keep judgment with people.

---

## Key terms

department · lead · quote / quotation · order · delivery challan / delivery note · picking list · proof of delivery (POD) · invoice · due date · payment terms · payment · made to stock · lead to cash · order to cash · business system · ERP · CRM · HRMS · POS · e-commerce platform · support desk / ticketing system · ticket · system of record / source of truth · integration · transaction · report · data warehouse · bookings · billings · collections · receivables / accounts receivable · revenue · cut-off · metric · KPI · KPI definition · leading indicator · lagging indicator · gross margin · average order value (AOV) · cancellation rate · overdue · dashboard · decision rights · re-keying · copy-paste integration · reconciliation / manual matching · shadow system · KPI tree

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can name the main departments of a company and one kind of data each creates.
- [ ] I can walk through lead to cash for one order and say what record each step leaves, and in which system.
- [ ] I can explain what an ERP, CRM, HRMS, POS, e-commerce platform, and support desk are for.
- [ ] I can tell a transaction from a report, and I know what a system of record is.
- [ ] I never say "sales" without saying booked, billed, or collected, and I can reconcile the three.
- [ ] I can write a KPI definition that two people would calculate the same way.
- [ ] I can find re-keying, copy-paste, emailed files, manual matching, and shadow systems in a process, and estimate their cost in hours.
- [ ] I've mapped the data flow of one real process and proposed one improvement.

---

## Exercises

### Warm-up

1. Match each record to the department that creates it: (a) a delivery challan, (b) a purchase order to Western Polymers for plastic granules, (c) a payslip, (d) a complaint about a cracked crate, (e) a quote, (f) a record of how much plastic was scrapped on a machine, (g) a list of people who visited Riverstone's stall at a trade fair.
2. Transaction or report? (a) Payment 3: ₹33,260 against invoice 9002 on 2026-03-02. (b) "Overdue receivables by customer, as of 31 March 2026." (c) Order 5012, placed 2026-03-15, status Pending. (d) "Average days to collect in Q1: 31.6." (e) Ticket 208: "lid doesn't fit", opened 2026-03-18.
3. Which Riverstone system would you look in first to answer each question? (a) How many enquiries came through the website last week? (b) Has invoice 9007 been paid? (c) How many days of leave does Neha have left? (d) How many storage boxes are in stock at Bhiwandi Main? (e) Which quotes are still waiting for a customer's reply?
4. For each event, say whether it changes bookings, billings, collections, or none of them: (a) Metro Mart places an order. (b) Coastal Foods pays ₹20,000 against invoice 9006. (c) A customer asks for a quote. (d) Order 5011 ships and the ERP raises an invoice. (e) Order 5004 is cancelled before shipping. (f) A lead is marked *Qualified* in the CRM.

### Core

5. February 2026 at Riverstone: orders 5005 to 5009 were placed (₹14,550, ₹14,640, ₹32,625, ₹23,325, ₹76,560), all shipped and invoiced in February, and none was cancelled. Payments received in February: ₹14,700 (invoice 9001), ₹40,000 (invoice 9002), ₹10,000 (invoice 9003). Calculate February's booked, billed, and collected amounts, and explain in two sentences why collections are so much lower than billings.
6. A department head writes this KPI definition: *"Sales growth: sales this month compared with last month."* List at least four things that are missing or ambiguous, then rewrite it as a complete definition using the six questions in section 3.5.
7. In March 2026, three orders were placed: 5010 (₹20,100, Delivered), 5011 (₹11,700, Shipped), and 5012 (₹26,220, Pending). Only 5010 and 5011 were invoiced. Calculate (a) the cancellation rate for March, (b) average order value on billings, and (c) average order value on bookings. Explain why (b) and (c) differ.
8. List every manual handover in this process and name its type (re-keying, copy-paste, emailed file, manual matching, or shadow system): *"An employee fills in a paper expense form with receipts, and their manager signs it. The employee scans and emails it to finance. A finance assistant types each line into the ERP and checks the total against the receipts. Every Friday, the assistant copies the week's claims into the Finance Manager's budget spreadsheet."*
9. Riverstone's finance team types 25 supplier invoices a day into the ERP, taking about 3 minutes each, on 22 working days a month. How many hours a month is that? Show your working, and name two costs of this work that the hours don't capture.

### Stretch

10. It's 31 March 2026. Northgate Distributors placed order 5009 on 25 February: 60 industrial crates at ₹1,450 with a 12% discount. Invoice 9008 was raised on 26 February with 30-day terms, due 28 March. Northgate paid ₹30,000 on 20 March. The order's status is *Shipped*. Answer: (a) Check the order value by hand. (b) How much is booked, billed, and collected for this order? (c) How much does Northgate still owe, and is it overdue? By how many days? (d) What would you check before calling Northgate about the balance?
11. Build a simple **KPI tree** for collections: write "Collections" at the top and break it into the two or three things that drive it, then break each of those down one more level. For each box at the bottom, name the department that can influence it.
12. Farah wants to offer Northgate Distributors 15% off another order of industrial crates, which cost ₹1,100 to make and list at ₹1,450. (a) Who approves it? (b) Calculate the gross margin per crate at list price, 12% off, and 15% off. (c) What other data should the approver look at, and what should they ask before agreeing?

### Think about it (no calculation needed)

13. Riverstone is considering paying sales executives a commission of 1% of the bookings they bring in. Describe two ways this could reward the wrong behavior, and suggest a better basis for the commission, or a second KPI to pair with it.
14. At the monthly business review, the Sales Head wants "sales" to mean bookings and the Finance Manager wants it to mean billings. Who should decide, and how would you present the numbers so that the meeting can move on?
15. The Sales Manager makes ten CRM fields mandatory before a lead can be saved, including the customer's annual turnover. What will happen to the quality of those fields, and what would you suggest instead?

---

## Answers

**1.** (a) Warehouse and dispatch. (b) Purchasing. (c) HR (payroll). (d) Customer support. (e) Sales. (f) Production. (g) Marketing.

**2.** (a) Transaction: one payment event. (b) Report: a summary of many invoices and payments at a cut-off date. (c) Transaction: one order. (d) Report: an average over several invoices. (e) Transaction: one support ticket.

**3.** (a) The CRM, where the website form creates leads. (b) The ERP, where payments are recorded against invoices. (c) The HRMS. (d) The ERP, but its stock is updated once a day (section 3.2), so for an urgent answer also check with Bhiwandi Main. (e) The CRM.

**4.** (a) Bookings. (b) Collections. (c) None: a quote isn't a sale. (d) Billings. (e) Bookings go down if you count bookings net of cancellations (the KPI definition in section 3.5); nothing is billed or collected. (f) None: it's a leading indicator, not a sale.

**5.** Booked: ₹14,550 + ₹14,640 + ₹32,625 + ₹23,325 + ₹76,560 = **₹1,61,700**. Billed: all five were invoiced in February, so also **₹1,61,700**. Collected: ₹14,700 + ₹40,000 + ₹10,000 = **₹64,700**. Collections are lower because all three payments were for January's invoices; February's invoices have 30-day terms and weren't due until March.

**6.** Missing: which "sales" (booked, billed, or collected); whether cancellations, returns, and tax count; whether "compared" means rupees or percent; which date decides the month; the source system; the owner and target. One good rewrite:

| Question | Answer |
|---|---|
| Name | Monthly billings growth |
| Formula | (billings this month − billings last month) ÷ billings last month, as a percentage to one decimal |
| Inclusions and exclusions | invoices raised; net of discount; tax excluded; credit notes subtracted in the month they're raised |
| Time | invoice date decides the month; calendar months |
| Source | ERP, `invoices` table |
| Owner, target, review | Finance Manager; target set in the annual plan; reviewed at the monthly business review |

**7.** (a) 0 cancelled out of 3 placed: **0%**. (b) ₹20,100 + ₹11,700 = ₹31,800, divided by 2 invoiced orders = **₹15,900**. (c) ₹58,020 ÷ 3 orders placed = **₹19,340**. They differ because order 5012 (₹26,220), the largest of the three, is booked but not yet invoiced. Neither is wrong; a report must say which it uses.

**8.** (1) Paper form and receipts: data created on paper instead of in a system. (2) Scanning and emailing the form to finance: **emailed file**. (3) Typing each line into the ERP: **re-keying**. (4) Checking totals against receipts: **manual matching**. (5) Copying the week's claims into the Finance Manager's spreadsheet: **copy-paste** into a **shadow system** (the budget tracker lives outside the ERP).

**9.** 25 × 3 = 75 minutes a day. 75 × 22 = 1,650 minutes a month. 1,650 ÷ 60 = **27.5 hours a month**, more than three working days. Costs the hours don't show: typing errors (paying a supplier the wrong amount), delay (untyped invoices make reports of what Riverstone owes out of date), and dependence on the people who do it.

**10.** (a) 60 × ₹1,450 = ₹87,000; 12% off is ₹10,440; ₹87,000 − ₹10,440 = **₹76,560**. ✓ (b) Booked ₹76,560 (in February); billed ₹76,560 (in February); collected ₹30,000 (in March). (c) ₹76,560 − ₹30,000 = **₹46,560** owed. It was due on 28 March, so on 31 March it's **3 days overdue**. (d) Whether the goods were delivered (the status is still *Shipped*, so Northgate may be waiting for them), whether a payment arrived but isn't recorded, and whether there's an open complaint. Three days overdue after a part-payment calls for a polite reminder, not an escalation.

**11.** One good tree (other sensible splits are fine):

- **Collections**
  - **Billings**: orders shipped (sales, warehouse) · average order value (sales) · invoicing accuracy (finance)
  - **Share paid on time**: payment terms and credit checks (sales, finance) · disputes from wrong deliveries or missing proof of delivery (warehouse, support)
  - **Overdue recovered**: reminders and escalation (finance, sales)

When collections drop, you can ask which branch moved, and each branch has an owner.

**12.** (a) Over 10%, so the Sales Head, Anita Rao, after checking with the Finance Manager, Suresh Menon. (b) At list price: (₹1,450 − ₹1,100) ÷ ₹1,450 = **24.1%**. At 12% off: price ₹1,276; (₹1,276 − ₹1,100) ÷ ₹1,276 = **13.8%**. At 15% off: price ₹1,232.50; (₹1,232.50 − ₹1,100) ÷ ₹1,232.50 = **10.8%**. 15% off leaves less than half the list-price margin. (c) Northgate's payment record (₹46,560 overdue, exercise 10), the volume the discount would win, and competitors' prices. A sensible question before agreeing: *"Can we settle the overdue balance first, or tie the discount to paying on time?"*

**13.** (1) Reps can book large orders that are later cancelled: bookings rise, no cash arrives. (2) Reps are pushed toward customers who pay late, or heavy discounts at poor margins. Better: pay on **collections**, or on billings less cancellations and long-unpaid invoices; or pair bookings with **cancellation rate** and **gross margin**.

**14.** The managing director, because the definition affects everyone who reads the pack (often finance proposes and management approves). Meanwhile, don't pick a winner: show **booked, billed, and collected** as labeled lines with definitions and sources, reconciled, as Meera did.

**15.** People fill mandatory fields with anything that gets past the screen: "0", "NA", or a guess at turnover. The fields become full but untrustworthy, which is worse than blank (Chapter 1 lists this problem for data typed by people). Better: require only what's known at that stage (name, contact, interest), collect the rest later, use pick-lists, and offer an "unknown" option.

---

## Where this leads

- **Chapter 4, Numbers Without Fear,** teaches the percentages, averages, and growth rates behind every KPI in section 3.5.
- **Chapter 5, Thinking Like an Analyst,** turns vague questions like "why is January low?" into precise ones, the way Meera did.
- **Chapters 10 and 12** put the order-to-cash records into tools: a spreadsheet sales tracker, then the ERP's `orders`, `invoices`, and `payments` tables in SQL, where you'll calculate booked, billed, and collected yourself.
- **Chapters 15 and 16** design and build dashboards like the ones in section 3.6.
- **Chapters 19 and 20** automate reports: macros and Apps Script first, then scheduled email reports and alerts. Chapter 20 automates a report of exactly this kind, Riverstone's Daily Sales Flash.
- **Chapter 23, Business Acumen, KPIs & Metrics,** builds a full KPI tree for Riverstone and adds finance and operations metrics such as days sales outstanding.
- **Chapter 25, The Business Analyst Track,** maps Riverstone's order-to-cash process formally and writes requirements for an improvement.
- **Chapters 45, 49, and 51** connect the systems: moving data from the ERP and CRM into a data warehouse (Chapter 49 explains how warehouses are built), and sending results back into them.
- **Chapter 58** automates the re-typing of emailed purchase orders with AI, with a person checking uncertain cases.
- **Interview preparation:** metric definitions, KPI trees, and business-process questions appear in Chapter 75 (product sense, metrics, and case studies) and Chapter 76B (the Business Analyst question bank), with model answers.


# Chapter 4. Numbers Without Fear

> **Chapter at a glance**
>
> **You will learn to:** calculate percentages forward and backward, and see why a rise and an equal fall don't cancel · tell percentage points from percent change · choose the right denominator for a ratio or rate · measure growth month by month and year by year, and calculate compound growth and CAGR · choose between mean, median, and mode, and use weighted averages · round without changing the story · read tables and charts without being fooled · think about probability as "how often, out of how many" · estimate quickly and sanity-check any number · spot the number tricks in business news.
>
> **Before you start:** Chapter 1 (especially section 1.6, levels of measurement) and Chapter 3 (bookings, billings, KPIs).
>
> **Time needed:** 4–5 hours, including the exercises and the project.
>
> **Tools:** a calculator with a power key (your phone's, turned sideways), a pen, and a notebook.
>
> **Practice data:** Riverstone's 2025 sales from the one-year database: monthly revenue, targets, and margins, and 173 orders. Every number was checked by script.

---

## Why this matters

Data work is mostly arithmetic. Not advanced math: percentages, averages, growth rates, and a little probability. The difficulty isn't the calculation. It's knowing *which* calculation answers the question, and noticing when a number that looks right is wrong.

Here are three sentences a manager at Riverstone could say in a meeting, each built on a real 2025 number:

- *"Revenue grew 13.1% a month on average."* True arithmetic, badly misleading. The steady monthly rate that gets from January to December is 7.3%.
- *"Margin fell 3.9% in November."* It fell 3.9 percentage points, which is a 14.0% fall.
- *"Our average order is ₹24,243."* That's an average of monthly averages. The real average order is ₹25,061, and half of all orders are below ₹21,375.

None of these is a lie. Each is a small slip that changes what people decide. By the end of this chapter you'll catch all three on sight, and you'll never be the person who makes them.

This chapter has no code. Every idea is worked by hand with real numbers, because being able to check a number on the back of an envelope is what makes you trustworthy when the tools do the work later.

---

## In plain English

A shop has a sign: **"50% off, and an extra 20% off at the till!"** How much do you save?

It's tempting to add them: 70%. But the second discount is taken from the *already reduced* price. On a ₹1,000 item, 50% off leaves ₹500. Then 20% off ₹500 is ₹100 off, leaving ₹400. You pay 40% of the original price, so you save **60%**, not 70%.

That one example holds the most important idea in this chapter: **every percentage is a percentage *of* something.** When the "something" changes, the same percentage means a different amount. Most number mistakes in business, and most number tricks in the news, come from losing track of what the percentage is *of*.

Keep asking two questions and you'll be right far more often than wrong:

1. **Of what?** What's the base, the denominator, the starting point?
2. **Compared with what?** Last month, last year, the target, another group?

---

## 4.1 Percentages: of, back, and change

A **percentage** is a fraction out of 100. 12% means 12 out of every 100, or 0.12. There are three everyday calculations, and it helps to name them.

**1. A percentage *of* a number.** Multiply by the percentage as a decimal.

*"What is a 12% discount on an Industrial Crate listed at ₹1,450?"* 0.12 × ₹1,450 = **₹174**. The crate sells for ₹1,450 − ₹174 = ₹1,276, which is the same as ₹1,450 × 0.88. (That's order 5009's price per crate, from Chapter 3.)

**2. What percentage one number is *of* another.** Divide the part by the whole.

*"What share of 2025 revenue came from Sharma Hardware?"* ₹5,02,775 ÷ ₹43,35,471 = 0.116, or **11.6%**.

**3. Percent change.** The change, divided by the *starting* value:

> percent change = (new − old) ÷ old

*"How did November's revenue compare with October's?"* October was ₹6,81,071, November ₹6,33,408. (₹6,33,408 − ₹6,81,071) ÷ ₹6,81,071 = −0.070, or **−7.0%**.

### Working backward

*"Northgate paid ₹1,276 per crate after a 12% discount. What was the list price?"*

The tempting wrong answer is to add 12% back: ₹1,276 × 1.12 = ₹1,429.12. That's wrong because the 12% was taken off ₹1,450, not off ₹1,276. The right way: ₹1,276 is 88% of the list price, so the list price is ₹1,276 ÷ 0.88 = **₹1,450**. ✓

> **Watch out: undoing a percentage.** To reverse "*x* % off", divide by (1 − *x* %). To reverse "*x* % added", divide by (1 + *x* %). Never add or subtract the same percentage again.

### Rises and falls don't cancel

![Two bar charts: 100 rises 50% to 150 then falls 50% to 75; 100 falls 20% to 80 then rises 20% to 96](figures/fig4-1-percent-changes-dont-cancel.svg)

*Figure 4.1 — A 50% rise followed by a 50% fall leaves you at 75, not 100.*

Figure 4.1 shows why. Up 50% takes ₹100 to ₹150. Down 50% is half of ₹150, which is ₹75. Down 20% then up 20% leaves ₹96. The fall and the rise are each calculated on a different base.

Two consequences come up all the time:

- **Recovering from a fall needs a bigger rise.** After a 50% fall, you need a 100% rise to get back. After a 20% fall, you need 25%.
- **Discounts stack by multiplying.** A 10% trade discount followed by an extra 5% for early payment is 0.90 × 0.95 = 0.855 of the price, a total of **14.5%** off, not 15%.

---

## 4.2 Percentage points and percent change

When the thing that changes is *itself* a percentage, there are two different ways to describe the change, and mixing them up is one of the most common errors in business writing.

Riverstone's gross margin (Chapter 3, section 3.5) was **27.9%** in October 2025 and **24.0%** in November.

- The difference is 27.9 − 24.0 = **3.9 percentage points**. A **percentage point** is the unit for the plain difference between two percentages.
- The **percent change** is (24.0 − 27.9) ÷ 27.9 = **−14.0%**. The margin is 14.0% smaller than it was.

Both are correct. They answer different questions, and they sound very different. *"Margin fell 3.9%"* is wrong: it mixes the size of one with the unit of the other, and it makes the fall sound less than a third as big as it was.

Here are three more from Riverstone's data:

| Measure | Before | After | Change in points | Percent change |
|---|---|---|---|---|
| Gross margin, January → February 2025 | 29.2% | 26.0% | −3.1 points | −10.8% |
| Revenue as % of target, August → September 2025 | 102.9% | 146.9% | +44.0 points | +42.8% |
| Win rate, each enquiry counted once → duplicate enquiries counted too | 20.0% | 14.0% | −6.0 points | −30.2% |

*Source: One-year database (2025).*

(The first row shows −3.1 points, not 29.2 − 26.0 = 3.2, because it's calculated from the unrounded margins, 29.18% and 26.04%. Section 4.6 is about exactly this kind of rounding.)

**Which should you report?** Use **points** when you talk about the level of a rate: *"conversion fell 6 points, from 20% to 14%"*. Use **percent change** when you want the relative size: *"a 30% drop in conversion"*. Whenever you can, give the before and after values too, and the reader can see both.

> **Watch out: "percent" for a change in a percentage.** When a rate, share, margin, or interest rate moves, say "percentage points" (or "points") for the difference. If a loan's interest rate goes from 8% to 9%, it rose 1 point, which is a 12.5% increase in what you pay in interest.

---

## 4.3 Ratios and rates: always ask about the denominator

A **ratio** compares two quantities by dividing one by the other. A **rate** is a ratio where the bottom is a unit of something else: per day, per customer, per 1,000 people. The bottom number is the **denominator**, and choosing it is the whole skill.

Here are Riverstone's three customer segments in 2025:

| Segment | Revenue | Orders | Customers | Revenue per customer | Average order value |
|---|---|---|---|---|---|
| Wholesale | ₹17,02,658 | 55 | 6 | ₹2,83,776 | ₹30,957 |
| Retail | ₹14,88,774 | 59 | 8 | ₹1,86,097 | ₹25,233 |
| Hospitality | ₹11,44,039 | 59 | 9 | ₹1,27,115 | ₹19,390 |
| **Total** | **₹43,35,471** | **173** | **23** | **₹1,88,499** | **₹25,061** |

*Source: One-year database (2025).*

Hospitality has the most customers and ties for the most orders, but the least revenue. Which segment is "biggest" depends entirely on the denominator you pick:

- **By customers:** Hospitality (9).
- **By revenue:** Wholesale (₹17,02,658).
- **Per customer:** Wholesale again, and by a lot. A wholesale customer brings in ₹2,83,776 ÷ ₹1,27,115 = **2.23 times** as much as a hospitality customer.

Rates also make different-sized periods comparable. ₹43,35,471 in a year is about **₹11,878 per day** (÷ 365), and 173 orders is about **3.3 orders per week** (÷ 52). Neither is a number anyone at Riverstone reports, but both are useful sanity checks: if someone claims a single ordinary day brought in ₹2 lakh, you know to ask what happened that day.

A **share** (or proportion) is a ratio where the part is inside the whole, like Sharma Hardware's 11.6%. Shares of a whole add up to 100%. Ratios between separate groups, like 2.23 times, don't add up to anything.

> **Try it.** Riverstone collected ₹1,97,250 of ₹2,97,710 billed in the first quarter of 2026 (Chapter 3; mini database, Jan–Mar 2026). What's the collection rate? If next quarter it's 75.0%, how many points is that up, and what percent change?

---

## 4.4 Growth, compounding, and CAGR

### Month-over-month growth

Here is Riverstone's revenue for every month of 2025, with the percent change from the month before.

| Month | Revenue | Change from previous month |
|---|---|---|
| January | ₹2,02,640 | |
| February | ₹2,53,664 | +25.2% |
| March | ₹2,78,008 | +9.6% |
| April | ₹2,10,282 | −24.4% |
| May | ₹3,29,359 | +56.6% |
| June | ₹1,86,928 | −43.2% |
| July | ₹2,32,692 | +24.5% |
| August | ₹3,29,282 | +41.5% |
| September | ₹5,58,315 | +69.6% |
| October | ₹6,81,071 | +22.0% |
| November | ₹6,33,408 | −7.0% |
| December | ₹4,39,824 | −30.6% |
| **Year** | **₹43,35,471** | |

*Source: One-year database (2025). Monthly figures are rounded to the rupee, so they add to ₹43,35,473 (₹2,02,640 + ₹2,53,664 + ₹2,78,008 + ₹2,10,282 + ₹3,29,359 + ₹1,86,928 + ₹2,32,692 + ₹3,29,282 + ₹5,58,315 + ₹6,81,071 + ₹6,33,408 + ₹4,39,824); the exact annual total is ₹43,35,471.*

The monthly changes swing wildly, from −43.2% to +69.6%. Most of that is the calendar: monsoon months are slow and the festive season is busy. Month-over-month percentages exaggerate seasonal patterns, which is why businesses with more than a year of data also compare each month with the same month last year.

### The average of growth rates is a trap

*"What was the typical monthly growth in 2025?"*

The tempting method is to average the eleven monthly changes. They add up to 143.8, and 143.8 ÷ 11 = **13.1%**. It sounds reasonable. It's wrong, and you can prove it: start with January's ₹2,02,640 and grow it by 13.1% eleven times. You get **₹7,82,621** for December. The real December was ₹4,39,824.

The problem is Figure 4.1 again. A +56.6% month and a −43.2% month don't cancel, because each is a percentage of a different base. Averaging percentages that compound on each other always overstates growth when the numbers bounce around.

The right question is: *what single, steady monthly rate would take ₹2,02,640 to ₹4,39,824 in eleven steps?* That's the **compound growth rate**:

> compound growth rate = (end ÷ start)^(1 ÷ number of periods) − 1

₹4,39,824 ÷ ₹2,02,640 = 2.17. The eleventh root of 2.17 is 1.073. So the compound monthly growth rate is **7.3%**. Grow ₹2,02,640 by 7.3% eleven times and you land exactly on December.

"The eleventh root" sounds hard, but a root only undoes a power. 1.073 multiplied by itself 11 times gives 2.17, so 1.073 is the "eleventh root" of 2.17. You never work it out by hand: type `2.17`, press the power key (xʸ), then `(1 ÷ 11)`.

![Line chart of Riverstone's monthly revenue in 2025, with a steady 7.3% compound path ending at December's actual value and a 13.1% path overshooting to ₹7,82,621](figures/fig4-2-average-growth-vs-compound.svg)

*Figure 4.2 — The 13.1% path, built from the average of the monthly changes, overshoots December by ₹3,42,797. The 7.3% compound path connects the real start and end.*

> **Watch out: start and end points drive compound growth.** The compound rate only uses the first and last values. From June (₹1,86,928, the lowest month) to October (₹6,81,071, the highest), revenue grew **264.3%**, a number that's true and tells you almost nothing about the year. Always ask why a growth figure starts and ends where it does.

### Compounding

**Compounding** means growth that builds on previous growth. ₹100 growing 10% a year becomes ₹110, then ₹121, then ₹133.10 after three years. Simple growth, adding ₹10 a year, would give ₹130. The extra ₹3.10 is growth on growth. Over short periods the gap is small. Over long periods it dominates: that's why a loan's interest and a company's growth rate both matter so much over ten years.

A handy shortcut is the **rule of 72**: a quantity growing at *r*% a year doubles in about 72 ÷ *r* years. At 12%, about 6 years (the exact answer is 6.12). At 8%, about 9 years (exactly 9.01). It's for quick thinking in meetings, not for reports.

### CAGR

**CAGR** (compound annual growth rate) is the compound growth rate when the periods are years. It's the standard way to describe growth over several years in company reports, investor decks, and interviews.

*"Anita wants the business in the one-year database to reach ₹60 lakh (₹60,00,000) of revenue by 2028, three years after 2025's ₹43,35,471. What growth rate does she need each year?"*

1. Ratio of end to start: ₹60,00,000 ÷ ₹43,35,471 = 1.384.
2. Three years, so take the cube root: 1.384^(1/3) = 1.1144.
3. Subtract 1: **CAGR = 11.4% a year.**

Check it by growing forward: ₹43,35,471 × 1.1144 = ₹48,31,418 in 2026, ₹53,84,098 in 2027, and ₹60,00,000 in 2028. ✓

Two tempting shortcuts both get the plan wrong:

- **Splitting the gap evenly.** ₹60,00,000 − ₹43,35,471 = ₹16,64,529, or ₹5,54,843 a year. That's 12.8% of 2025's revenue, but a fixed rupee amount is a smaller percentage each year, so it isn't a growth rate at all.
- **Rounding down to a nice number.** 10% a year for three years reaches ₹57,70,512, which is ₹2,29,488 short. Over several years, one percentage point matters.

---

## 4.5 Averages: mean, median, mode, and weighted

An **average** is one number that stands for many. There are three common kinds, and Chapter 1 (section 1.6) showed that the level of measurement decides which ones make sense. This section shows how to choose between them for amounts, like order values, where all three are allowed.

- The **mean** adds up the values and divides by how many there are. It's what most people mean by "average".
- The **median** is the middle value when the values are sorted. Half are below it, half above.
- The **mode** is the most common value.

Riverstone received 173 orders in 2025 (not counting the two that were cancelled), worth ₹43,35,471 in total.

- **Mean:** ₹43,35,471 ÷ 173 = **₹25,061**.
- **Median:** sort the 173 order values; the 87th is **₹21,375**.
- **Mode:** order values are almost never exactly equal, so the mode of the values themselves is useless here. The mode is useful for categories and repeated counts instead: the most commonly ordered product is the Storage Box 10L (on 76 order lines), the most common quantity on a line is 15, and the most common discount is 0% (140 of 326 lines).

![Histogram of 173 order values in 10,000-rupee bands, most between 0 and 40,000, with a long tail to ₹1,00,278; the median line at ₹21,375 sits left of the mean line at ₹25,061](figures/fig4-3-order-values-mean-vs-median.svg)

*Figure 4.3 — Most orders are small; a few large ones stretch the tail to the right and pull the mean above the median.*

Why is the mean higher than the median? Look at Figure 4.3. Most orders are under ₹40,000, but a handful are much larger: the biggest five are ₹65,818, ₹68,875, ₹74,218, ₹82,250, and ₹1,00,278. Large values pull the mean toward them; they don't move the median at all, because the median only cares about which value is in the middle. Data with a long tail on the high side is called **right-skewed**, and it's everywhere in business: order values, salaries, house prices, time to resolve a ticket.

The result: only **70 of the 173 orders (40.5%)** are above the "average" order. If a sales executive is told the average order is ₹25,061, most of their orders will feel below average.

**Which to use?**

| Situation | Use | Why |
|---|---|---|
| Amounts that add up to a total you care about (revenue, cost, hours) | mean | mean × count = total, so it connects to budgets and plans |
| Amounts with a long tail (order values, salaries, delivery times) | median, alongside the mean | tells you what's *typical*; the gap between them shows the skew |
| Categories (products, payment methods, segments) | mode | the only average that works for nominal data (Chapter 1) |
| Ratings and ranks (ordinal data) | median, plus the count in each category | the gaps between ratings aren't equal (Chapter 1) |

### Weighted averages

*"What's Riverstone's average discount?"*

Every order line has a discount of 0%, 5%, 8%, 10%, or 12%. The simple average of the discount on all 326 lines is **4.06%**. But a 12% discount on a ₹50,000 line costs far more than 12% on a ₹1,000 line. To know how much discounting costs the business, each line's discount must count in proportion to its value. That's a **weighted average**:

> weighted average = sum of (value × weight) ÷ sum of weights

Weighted by each line's value before discount, the average discount is **4.69%**. You can check it without a formula: the lines were worth ₹45,48,725 at list price and ₹43,35,471 after discounts, so discounts took ₹2,13,254, and ₹2,13,254 ÷ ₹45,48,725 = 4.69%. ✓ Larger lines tend to get larger discounts (5.3% on average for lines worth ₹20,000 or more, 3.8% for smaller ones), which is why the weighted figure is higher.

The same trap appears with prices. Riverstone's four product categories sold at average net prices of ₹435 (Storage), ₹341 (Kitchen), ₹1,273 (Industrial), and ₹1,121 (Furniture) per unit. The simple average of those four prices is ₹793. But the company sold 9,475 units for ₹43,35,471, an average of **₹458 per unit**, because Storage and Kitchen sold thousands of units and Furniture sold 30. **An average of averages ignores how many items stand behind each one.**

### The average of averages

The monthly business review pack often shows a row of monthly averages. Averaging that row gives the wrong annual figure:

- Average of the twelve monthly average order values: **₹24,243**.
- Actual average order value for the year: ₹43,35,471 ÷ 173 orders = **₹25,061**.

The busy months (September to November, with 18 to 21 orders each and high order values) count the same as quiet January with 8 orders. To combine averages, go back to the totals: add up all the revenue, add up all the orders, then divide.

---

## 4.6 Rounding and significant figures

Rounding makes numbers readable. It also creates small puzzles that make careful readers distrust a report.

### Shares that don't add up to 100%

Riverstone's 2025 revenue by segment, rounded to whole percentages:

| Segment | Share (whole %) | Share (one decimal) |
|---|---|---|
| Wholesale | 39% | 39.3% |
| Retail | 34% | 34.3% |
| Hospitality | 26% | 26.4% |
| **Total** | **99%** | **100.0%** |

*Source: One-year database (2025).*

Nothing is missing. The unrounded shares are 39.27%, 34.34%, and 26.39%, and each one rounded down a little. Rounding to one decimal happens to fix it here, but not always: the same thing can happen at any precision (exercise 8). You have three honest options: show one more decimal place, add a note ("shares may not add to 100% because of rounding"), or leave it and expect the question. Never quietly change one number to force the total, because then the table no longer matches the data.

### Round at the end, not in the middle

Rounding in the middle of a calculation carries the error forward. Section 4.2's margin example showed it: from rounded margins, the January to February fall looks like 3.2 points; from the real ones, it's 3.1. Keep full precision in the spreadsheet or calculator, and round only what you show.

### Significant figures and false precision

The **significant figures** of a number are the digits that carry meaning. ₹43,35,471 has seven. Does the reader need all seven? In a finance reconciliation, yes. In a meeting, "about ₹43 lakh" or "₹4.3 million" says the same thing and is easier to remember.

The opposite mistake is **false precision**: more digits than the data can support. *"Customers take an average of 31.6 days to pay"* (Chapter 3) is correct arithmetic from five invoices. With five invoices, "about a month" is more honest. The number of digits you write is a claim about how sure you are.

A rough guide for reports:

- **Money in tables:** whole rupees in detail tables; thousands or lakhs in summaries, with the unit stated in the header.
- **Percentages:** one decimal place, unless the numbers are small samples (then whole numbers or "about").
- **Averages of small counts:** round more, and give the count: "31.6 days (5 invoices)".

---

## 4.7 Reading tables and charts correctly

Before you read any number in a table or chart, read the frame around it. Five checks catch most misreadings:

1. **Units.** Rupees, thousands, lakhs, crores, or millions? Percent or percentage points? A column headed "Revenue (₹ lakh)" with a value of 43.4 means ₹43,40,000.
2. **Period and cut-off.** A month, a quarter, year to date? Chapter 3 showed that the same report run on different dates gives different numbers.
3. **Per-period or cumulative.** A **cumulative** (running total) line always goes up as long as the values are positive, even in a terrible month. December 2025's revenue fell 30.6%, but the year-to-date line still rose.
4. **Definition.** Booked, billed, or collected? With or without cancellations? (Chapter 3.)
5. **The axis.** Where does it start?

The last one deserves a picture.

![Two bar charts of the same twelve monthly gross margins; with the axis starting at 23% November's bar looks tiny, with the axis starting at 0% it looks like a modest dip](figures/fig4-4-same-numbers-two-axes.svg)

*Figure 4.4 — The same twelve numbers. A bar chart whose axis doesn't start at zero turns a 3.9-point dip into what looks like a collapse.*

In the left chart of Figure 4.4, the axis starts at 23%, so November's 24.0% bar is about a fifth the height of October's 27.9%. The eye reads "November's margin was a fifth of October's". In the right chart, starting at zero, the bars are 24 and 28 units tall, and the dip looks like what it is.

The rule: **bar charts must start at zero**, because readers compare bar *lengths*. Line charts can start elsewhere, because readers compare *positions* and *slopes*, but the axis should be labeled clearly. Chapter 15 covers chart choice and design in depth.

> **Watch out: one chart, two axes.** A chart with revenue on a left axis and margin on a right axis lets the designer stretch either line to make them appear to move together. When you see two vertical axes, read each line against its own axis before believing the pattern.

---

## 4.8 Probability: how often, out of how many

A **probability** is how often something happens, out of how many chances. Written as a fraction, a decimal, or a percentage, it's always between 0 (never) and 1 (always), or 0% and 100%. You don't need formulas to use it well; you need to keep asking "out of how many?"

### Counting what happened

In 2025, **2 of 175 orders** were cancelled. As a rate: 2 ÷ 175 = **1.1%**, or about 1 order in 88. In the first quarter of 2026 (the mini database), 1 of 12 orders was cancelled: **8.3%**.

Did Riverstone's customers get seven times more likely to cancel? Almost certainly not. With 12 orders, a single cancellation moves the rate by 8.3 points. **Small counts make rates jumpy.** Before comparing two rates, look at how many cases each is based on; Chapter 22 shows how to judge whether a difference is bigger than chance.

### "At least one"

*"If each order has a 1.1% chance of being cancelled, what's the chance that at least one of the next 20 orders is cancelled?"*

It's easier to work out the chance that *none* is cancelled and subtract from 1. The chance one order goes through is 1 − 0.0114 = 0.9886. The chance all 20 go through is 0.9886 multiplied by itself 20 times, which is 0.795. So the chance of at least one cancellation is 1 − 0.795 = **20.5%**. Using the first quarter's 8.3% rate instead gives **82.5%**. The rate you assume changes the answer completely.

(This assumes one order's cancellation doesn't affect another's, which is called **independence**. If one big customer cancels several orders at once, the assumption breaks.)

### Chaining stages

Riverstone's 2025 sales funnel took 30 unique leads to 22 contacted, 14 quoted, and 6 won. Each step has its own rate: 22 of 30 (73.3%), 14 of 22 (63.6%), and 6 of 14 (42.9%). The chance that a new lead is eventually won is the rates multiplied: 0.733 × 0.636 × 0.429 = **0.200**, or 20%, which matches 6 of 30. ✓

That makes planning concrete. To win 10 new customers at a 20% win rate, the sales team needs about 10 ÷ 0.20 = **50 leads**. To win more with the same number of leads, improve the weakest step.

### The order of "given" matters

Of the 173 orders, 16 were worth more than ₹50,000, and 10 of those came from wholesale customers, who placed 55 orders in all.

- Chance an order is over ₹50,000: 16 ÷ 173 = **9.2%**.
- Chance a **wholesale** order is over ₹50,000: 10 ÷ 55 = **18.2%**. This is a **conditional probability**: the chance of one thing *given* another. The denominator shrinks to wholesale orders only.
- Chance a large order is **from wholesale**: 10 ÷ 16 = **62.5%**.

The last two sound alike and differ by a factor of more than three, because the denominators differ. Mixing them up is one of the most common errors in medicine, law, and business alike: "most large orders are wholesale" is not the same as "most wholesale orders are large".

---

## 4.9 Orders of magnitude and quick estimation

The **order of magnitude** of a number is its rough size in powers of ten: thousands, lakhs, millions, crores. Getting the order of magnitude right catches more errors than any formula, because the most damaging mistakes are the ones that are off by a factor of 10 or 100: a misplaced decimal, a figure in thousands read as rupees, an extra zero.

### Indian and international units

Indian business writing uses lakhs and crores; international writing uses thousands, millions, and billions. You'll switch between them constantly.

| Indian | Written the Indian way | Written the international way | International |
|---|---|---|---|
| 1 lakh | 1,00,000 | 100,000 | 100 thousand |
| 10 lakh | 10,00,000 | 1,000,000 | 1 million |
| 1 crore (100 lakh) | 1,00,00,000 | 10,000,000 | 10 million |
| 100 crore | 1,00,00,00,000 | 1,000,000,000 | 1 billion |

The Indian way puts a comma after the thousands and then after every two digits; the international way puts one after every three. Riverstone's 2025 revenue in the one-year database, ₹43,35,471, is about ₹43.4 lakh, ₹0.43 crore, or ₹4.3 million. This book writes rupee amounts the Indian way, as you've just seen. Numbers that aren't money, such as counts of orders or units, keep the international grouping.

### Sanity checks: does the number fit?

When a number arrives, check it against another number you already trust. Two examples from Riverstone:

- **Revenue per day.** ₹43 lakh a year is about ₹11,878 a day. Separately, 173 orders ÷ 52 weeks ÷ 7 days × ₹25,061 an order is about ₹11,911 a day. (Keep 173 ÷ 52 = 3.327 orders a week unrounded: rounded to 3.3, it gives ₹11,814, the drift section 4.6 warns about.) Two different routes land within ₹50 of each other, so both numbers are probably sound.
- **Units from revenue.** October's revenue was ₹6,81,071, and the year's average price was ₹458 a unit. So October probably shipped about ₹6,81,071 ÷ ₹457.57 ≈ **1,488 units**. The database says **1,625**. The estimate is 8.4% low, because October sold relatively more low-priced kitchen items and fewer ₹1,450 industrial crates than the year as a whole, but it's the right order of magnitude. If the database had said 16,250 or 162, you'd know something was wrong before looking at a single row.

### Estimating from nothing

Sometimes there's no data yet: *"Is it worth building a report for this?"* or, in interviews, *"How many plastic storage boxes are sold in Mumbai each year?"* These are called **Fermi estimates** or **guesstimates**. The method is always the same:

1. Break the unknown into smaller pieces you can guess: households, share that buy boxes, boxes per purchase, purchases per year.
2. Write each assumption down with a round number.
3. Multiply, and round the answer to one or two significant figures.
4. Sanity-check the answer against anything you know, and say which assumption matters most.

Being close matters less than being clear. A reader can replace a bad assumption; they can't fix reasoning they can't see.

---

## 4.10 Number tricks in business news

Most misleading numbers in headlines, press releases, and sales decks are true. They mislead through what they leave out. Here are the common tricks, with invented examples, and the question that exposes each one.

| Trick | Example | Question to ask |
|---|---|---|
| **Tiny base** | "Profits up 300%!" (from ₹2 lakh to ₹8 lakh) | *300% of what?* |
| **Relative without absolute** | "New process doubles the risk of a defect" (from 1 in 10,000 to 2 in 10,000) | *What are the actual numbers before and after?* |
| **Cherry-picked period** | "Revenue up 264% since June" (the slowest month to the busiest) | *Why start and end there? What about the same period last year?* |
| **"Up to"** | "Up to 70% off" (on one item) | *How many items, and what's the typical discount?* |
| **Percent for points** | "Interest rates rise 1%" (from 8% to 9%) | *Points or percent?* |
| **Average hiding the spread** | "Average order ₹25,061" (most orders are smaller) | *What's the median?* |
| **Truncated axis** | a bar chart starting at 23% (Figure 4.4) | *Where does the axis start?* |
| **Mixed units** | "₹43 lakh" next to "₹4.3 million" in the same slide | *Are these in the same unit?* |
| **Record without context** | "Our best month ever!" (October, in a seasonal business) | *Best compared with the same month last year?* |
| **Survivors only** | "Our customers grew 40% on average" (counting only customers who stayed) | *Who was left out?* |

A good habit is to rewrite a headline number into a plain sentence with both numbers and the base: *"Profit rose from ₹2 lakh to ₹8 lakh, a fourfold increase from a small base."* If the rewritten sentence sounds much less exciting, the original was relying on a trick.

> **Interview extra point.** When a case interview gives you a growth figure or a percentage, restate it with its base and period before you use it: *"So revenue went from ₹20 lakh to ₹32 lakh over four years, which is about 12.5% a year compounded."* It shows you check numbers before trusting them, which is what interviewers for analyst roles are testing. Chapter 73 (statistics and probability) and Chapter 75 (metrics, case studies, and guesstimates) have practice questions.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Adding percentages that apply one after another | "50% + 20% off = 70% off" | Multiply what remains: 0.5 × 0.8 = 0.4, so 60% off |
| Reversing a percentage by adding it back | list price from a discounted price comes out too low | Divide by (1 − discount) |
| Saying "percent" for a change in a percentage | "margin fell 3.9%" when it fell 3.9 points | Use points for the difference; give before and after |
| Averaging growth rates that compound | typical monthly growth of 13.1% when the steady rate is 7.3% | Use (end ÷ start)^(1/periods) − 1 |
| Quoting growth between hand-picked months | "up 264%" from the slowest to the busiest month | Compare like with like: full years, or same month last year |
| Reporting only the mean for skewed data | most orders feel "below average" | Report the median too |
| Averaging averages | ₹24,243 instead of ₹25,061 | Go back to the totals and divide once |
| Using a simple average when items differ in size | average discount 4.06% instead of 4.69% | Weight by value, units, or count |
| Rounding in the middle of a calculation | small errors that grow, points that don't match | Keep full precision; round only what you show |
| Too many digits | "31.6 days" from five invoices | Match the digits to how sure you are; give the count |
| Bar charts with a truncated axis | a small dip looks like a collapse | Start bars at zero |
| Comparing rates from very different sample sizes | 1.1% vs 8.3% cancellation read as a real change | Give the counts; be cautious with small samples |
| Confusing "A given B" with "B given A" | "most large orders are wholesale" read as "most wholesale orders are large" | Say the denominator out loud |

---

## In the real world: the board slide

It's the first week of January 2026. The managing director is presenting Riverstone's year to the board, and Vikram Singh's team has drafted the sales slide. Before it goes to the MD, Anita asks Meera Iyer to check the numbers. "Nothing fancy. Make sure nothing on it will embarrass us."

The draft slide has six claims. Meera takes them one at a time, and for each one asks: *of what, and compared with what?*

**1. "2025 revenue up 117%."** Meera finds where it comes from: December's ₹4,39,824 against January's ₹2,02,640. That's true, but it compares two single months of a seasonal business, and it isn't "2025 revenue" at all. The slide has no 2024 figures to compare with, so it can't support any year-on-year growth claim. What the board can use: *full-year revenue ₹43.4 lakh (₹43,35,471), 102.3% of the annual target.*

**2. "Average monthly growth: 13.1%."** The average of the eleven monthly changes. Meera grows January by 13.1% eleven times and gets ₹7,82,621 for December, almost double the real figure. The compound rate is 7.3%, but she recommends dropping the line entirely: in a year that peaks in October and dips in the monsoon, a "monthly growth rate" describes nothing real.

**3. "Gross margin down 3.9% in November."** It was 27.9% in October and 24.0% in November: down 3.9 *points*, a 14.0% fall. More useful for a board: *full-year gross margin 26.2%; November was the lowest month.*

**4. "Average order value: ₹24,243."** Meera recognizes the number from the monthly pack: it's the average of the twelve monthly averages. The real figure is ₹43,35,471 ÷ 173 = **₹25,061**. She adds the median, **₹21,375**, because the MD is likely to be asked what a typical order looks like.

**5. The segment pie chart: Wholesale 39%, Retail 34%, Hospitality 26%.** They add to 99%. A board member will notice. One decimal fixes it: 39.3%, 34.3%, 26.4%.

**6. The margin bar chart.** Its axis starts at 23%, so November's bar is a stub. Meera redraws it from zero (Figure 4.4).

There's also a note under the slide's goal for 2028, ₹60 lakh: *"That's about ₹5.5 lakh more each year."* Meera adds the growth rate that the plan really needs, **11.4% a year**, because the board will think in percentages and "₹5.5 lakh a year" gets harder every year as a percentage.

She sends the corrected slide back with a four-line note explaining each change and the check behind it. Vikram's reply: "The 117% was the best number on the slide." Anita's: "It was also the one the board would have questioned first."

Nothing Meera did needed more than a calculator and two questions. What it needed was the habit of never passing a number on without knowing what it's a percentage *of*.

---

## Project: check five statistics

**Goal:** take five numbers from the real world and check each one the way Meera checked the board slide.

### Tools you'll need

- **A calculator.** Your phone's calculator in landscape (scientific) mode has a power key (xʸ or ^) for compound growth.
- **A pen and a notebook.** Write each calculation out in full, with its units, so you can check it later. When spreadsheets arrive in Chapter 10, you'll redo this chapter's numbers there.

**Step 1. Collect five statistics.** Find them in news articles, company annual reports or investor presentations, advertisements, or presentations at your workplace. Aim for variety: at least one growth figure, one percentage or share, one average, one chart, and one comparison between two groups. Copy the exact wording and note the source and date.

**Step 2. Record each one in a table.**

| Column | What to write |
|---|---|
| `claim` | the exact words, e.g. "Sales up 40% in three years" |
| `source_and_date` | where and when it was published |
| `base` | what the number is a percentage *of*, or an average *of* |
| `comparison` | what it's compared with: which period, group, or target |
| `type` | percent change, points, share, ratio, average, probability, chart |
| `check` | your recalculation, or the missing information you'd need |
| `trick_found` | none, or which trick from section 4.10 |
| `rewrite` | an honest one-sentence version with both numbers and the base |

**Step 3. Recalculate** whatever you can from the numbers given. For growth over several years, work out the CAGR. For a percentage, find both the part and the whole. For a chart, check the axis and the units.

**Step 4. Name what's missing.** Many claims can't be checked because the base, the period, or the sample size isn't given. Saying exactly what's missing is a result.

**Step 5. Rewrite each claim** as one honest sentence.

**Step 6. Write a three-line summary:** how many of the five held up, the most common problem, and the one question you'll ask next time you see a number like it.

**Deliverable:** your table and summary. Keep it; Chapter 5 asks you to turn one of these claims into an analyst's question.

---

## Recap

- **Every percentage is a percentage of something.** Ask *of what?* and *compared with what?*
- Percent change is (new − old) ÷ old. Reverse a discount by dividing by (1 − discount). Rises and falls don't cancel, and discounts stack by multiplying.
- The difference between two percentages is measured in **percentage points**. Riverstone's margin fell from 27.9% to 24.0%: 3.9 points, a 14.0% fall.
- **Ratios and rates** depend on the denominator. Wholesale earned 2.23 times as much per customer as Hospitality, though Hospitality had more customers.
- **Compound growth** = (end ÷ start)^(1/periods) − 1. Riverstone's 2025 compound monthly rate was 7.3%; averaging the monthly changes gives a misleading 13.1%. **CAGR** is the yearly version: ₹43.4 lakh to ₹60 lakh in three years needs 11.4% a year. The **rule of 72** estimates doubling time.
- The **mean** (₹25,061 per order) is pulled up by large values; the **median** (₹21,375) shows what's typical; the **mode** suits categories. Use **weighted averages** when items differ in size (average discount 4.69%, not 4.06%), and never average averages.
- **Round at the end.** Shares may not add to 100%; say so or add a decimal. Don't claim more precision than the data has.
- **Read the frame first:** units, period, cumulative or not, definition, and where the axis starts. Bar charts start at zero.
- **Probability** is how often, out of how many. Small counts make rates jumpy. "At least one" = 1 − chance of none. Chained stages multiply. "A given B" isn't "B given A".
- **Estimate** to catch errors of 10× or 100×, and convert confidently between lakhs, crores, and millions.
- **Number tricks** leave out the base, the absolute numbers, the period, or the spread. Rewrite the claim with both numbers and the base.

---

## Key terms

percentage · percent of · share / proportion · percent change · reverse percentage · percentage point · ratio · rate · denominator · month-over-month growth · compound growth rate · compounding · rule of 72 · CAGR (compound annual growth rate) · average · mean · median · mode · right-skewed · weighted average · average of averages · rounding · significant figures · false precision · cumulative / running total · truncated axis · probability · independence · conditional probability · order of magnitude · lakh · crore · sanity check · Fermi estimate / guesstimate · base effect · relative vs absolute change

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can calculate a percentage of a number, a share, a percent change, and a list price from a discounted price.
- [ ] I know that a rise and an equal fall don't cancel, and that discounts stack by multiplying.
- [ ] I say "percentage points" for the difference between two percentages.
- [ ] I ask what the denominator is before comparing ratios or rates.
- [ ] I calculate compound growth and CAGR, and I never average growth rates that compound.
- [ ] I choose between mean, median, and mode for a purpose, and use weighted averages when items differ in size.
- [ ] I don't average averages.
- [ ] I round only at the end, and I don't write more digits than the data supports.
- [ ] I check a chart's units, period, and axis before reading its bars.
- [ ] I can work out "at least one" and conditional probabilities by counting.
- [ ] I sanity-check numbers by estimating them another way.
- [ ] I've checked five real statistics and rewritten each one fairly.

---

## Exercises

### Warm-up

1. Calculate: (a) a 5% discount on an order worth ₹14,550; (b) what percentage ₹26,220 is of ₹58,020 (order 5012's share of March 2026 bookings, Chapter 3); (c) the price of a ₹780 Storage Box 25L after 8% off.
2. From Riverstone's 2025 revenue by quarter and category (one-year database): Kitchen revenue was ₹1,33,888 in the first quarter of 2025 and ₹4,61,146 in the fourth; Industrial was ₹2,75,450 in the third quarter and ₹2,92,040 in the fourth. Calculate each percent change.
3. Wholesale's share of revenue was 39.3% in 2025. If it's 42.0% next year, what's the change in percentage points, and what's the percent change? Write one correct sentence for each.
4. The 11 non-cancelled orders in the mini database (first quarter of 2026) were worth: ₹14,700, ₹73,260, ₹16,250, ₹14,550, ₹14,640, ₹32,625, ₹23,325, ₹76,560, ₹20,100, ₹11,700, ₹26,220. Find the mean, the median, and the mode. Which better describes a typical order, and why?

### Core

5. (a) Northgate paid ₹76,560 for an order after a 12% discount. What was the order worth at list price? (b) Riverstone raises a price by 8%, then gives a customer 8% off the new price. Is the customer paying more or less than before, and by what percent?
6. A distributor's revenue grew from ₹25 lakh to ₹40 lakh over five years. (a) What was its CAGR? (b) Using the rule of 72, roughly how long would it take to double at that rate? (c) Why is "it grew 12% a year" (60% ÷ 5) wrong?
7. Riverstone's 2025 gross margin by category was: Storage 26.9% on ₹22,97,974 of revenue; Kitchen 33.2% on ₹12,08,030; Industrial 13.6% on ₹7,95,830; Furniture 24.2% on ₹33,638. (a) What's the simple average of the four margins? (b) What's the margin weighted by revenue? (c) Which one is the company's gross margin, and why are they different?
8. The categories' shares of 2025 revenue, to one decimal place, are Storage 53.0%, Kitchen 27.9%, Industrial 18.4%, and Furniture 0.8%. A manager says the table is wrong. Explain what's happening and write the note you'd put under the table.
9. Riverstone wins 20% of its unique leads. (a) How many leads does it need to win 15 new customers? (b) If three new leads arrive this week and each has a 20% chance of being won, what's the chance at least one is won? (c) What assumption does (b) make, and when might it be false?

### Stretch

10. A local newspaper profile of Riverstone runs the headline *"Riverstone revenue soars 264%"*, based on June 2025 (₹1,86,928) and October 2025 (₹6,81,071). Explain in two sentences why the headline misleads, and write an honest replacement using numbers from this chapter.
11. November 2025's revenue was ₹6,33,408. Using the year's average price of ₹458 per unit, estimate how many units Riverstone shipped in November. The database says 1,355. How far off is your estimate, in percent? Is that good enough for a sanity check, and why?
12. In 2025, Riverstone received 29 orders worth ₹7,34,312 in the first quarter and 59 orders worth ₹17,54,302 in the fourth. (a) Calculate each quarter's average order value. (b) Calculate the average order value for the two quarters combined. (c) Explain why the average of your two answers in (a) isn't the answer to (b).

### Think about it (no calculation needed)

13. A company's press release says, "Our employees earn an average of ₹18 lakh a year." What else would you want to know before believing that this describes a typical employee?
14. A sales dashboard shows only a year-to-date revenue line, and it has gone up every month. Explain how this chart could hide a bad month, and suggest a better chart to put next to it.
15. A sales manager announces, "Our win rate went up 50% this quarter!" Write the two questions you'd ask before sharing the news.

---

## Answers

**1.** (a) 0.05 × ₹14,550 = **₹727.50**. (b) ₹26,220 ÷ ₹58,020 = 0.452, so **45.2%**. (c) ₹780 × 0.92 = **₹717.60**.

**2.** Kitchen: (₹4,61,146 − ₹1,33,888) ÷ ₹1,33,888 = **+244.4%**; revenue more than tripled. Industrial: (₹2,92,040 − ₹2,75,450) ÷ ₹2,75,450 = **+6.0%**.

**3.** 42.0 − 39.3 = **2.7 percentage points**: "Wholesale's share rose 2.7 points, from 39.3% to 42.0%." (42.0 − 39.3) ÷ 39.3 = **6.9%**: "Wholesale's share of revenue grew by 6.9%." The first is clearer for most readers.

**4.** Total ₹3,23,930 ÷ 11 = **mean ₹29,448**. Sorted: ₹11,700, ₹14,550, ₹14,640, ₹14,700, ₹16,250, **₹20,100**, ₹23,325, ₹26,220, ₹32,625, ₹73,260, ₹76,560; the sixth value is the **median, ₹20,100**. No value repeats, so there's **no mode**. The median describes a typical order better: two large wholesale orders (₹73,260 and ₹76,560) pull the mean up, and 8 of the 11 orders are below it.

**5.** (a) ₹76,560 ÷ 0.88 = **₹87,000**. (Check: 12% of ₹87,000 is ₹10,440, and ₹87,000 − ₹10,440 = ₹76,560. ✓) (b) 1.08 × 0.92 = 0.9936. The customer pays **0.64% less** than the original price, because the 8% discount is taken from a bigger number than the 8% rise was.

**6.** (a) ₹40 lakh ÷ ₹25 lakh = 1.6. 1.6^(1/5) = 1.0986, so the CAGR is **9.9% a year**. (b) 72 ÷ 9.9 ≈ **7.3 years** (the exact answer is 7.4). (c) 60% ÷ 5 = 12% ignores compounding: each year's growth is calculated on a bigger base, so a steady 9.9% a year is enough to add 60% in five years. Growing ₹25 lakh by 12% a year for five years would reach about ₹44 lakh, not ₹40 lakh.

**7.** (a) (26.9 + 33.2 + 13.6 + 24.2) ÷ 4 = **24.5%**. (b) Weighted by revenue, the margin is **26.2%**: total revenue ₹43,35,471 minus total product cost ₹31,98,250, divided by revenue. (c) The weighted figure is the company's gross margin. The simple average gives tiny Furniture (under 1% of revenue) the same say as Storage (more than half), and it gives low-margin Industrial (18.4% of revenue) a quarter of the weight, which drags the simple average down.

**8.** Nothing is wrong. The unrounded shares (53.00%, 27.86%, 18.36%, 0.78%) add up to 100%, but three of them rounded up, so the rounded shares add to 100.1%. Note: *"Shares are rounded to one decimal place and may not add to exactly 100%."* Don't adjust one share to force the total.

**9.** (a) 15 ÷ 0.20 = **75 leads**. (b) Chance none is won: 0.8 × 0.8 × 0.8 = 0.512. Chance at least one is won: 1 − 0.512 = **48.8%**. (c) It assumes the leads are **independent** and each has the same 20% chance. It's false if, for example, all three come from the same company or from a trade fair where one bad impression affects everyone, or if one lead is far warmer than the others.

**10.** It compares the slowest month with the busiest month of a seasonal business, so most of the "growth" is the calendar, and it says nothing about the year. A single-month comparison can't be called revenue growth for the company. Honest replacement: *"Riverstone's 2025 revenue was ₹43.4 lakh, 2.3% above its annual target, with a festive-season peak of ₹6.8 lakh in October."*

**11.** ₹6,33,408 ÷ ₹458 ≈ **1,383 units** (using the unrounded ₹457.57, about 1,384). Against the actual 1,355, that's about **2.1% too high**. That's good enough: a sanity check is looking for errors of 10 times or 100 times, and an estimate within a few percent confirms the order of magnitude. Differences in the product mix explain the rest.

**12.** (a) First quarter: ₹7,34,312 ÷ 29 = **₹25,321**. Fourth quarter: ₹17,54,302 ÷ 59 = **₹29,734**. (b) (₹7,34,312 + ₹17,54,302) ÷ (29 + 59) = ₹24,88,614 ÷ 88 = **₹28,280**. (c) The average of the two quarterly figures, ₹27,528, gives each quarter equal weight, but the fourth quarter had twice as many orders. The combined figure must come from the totals.

**13.** Whether "average" is the mean or the median (a few very high salaries, such as senior leaders', pull the mean up); the median and the range; who is included (full-time only? contractors? leaders?); whether it's salary alone or includes bonuses and benefits; and the date and location. The median, with the number of employees, describes a typical employee far better.

**14.** A cumulative line rises whenever a month's revenue is positive, so a month that fell sharply (like December 2025, down 30.6%) still shows as the line going up, only less steeply. Put a monthly bar chart next to it (starting at zero), ideally with each month's target or the same month last year, so a bad month is visible as a short bar.

**15.** (1) *From what to what?* A rise from 10% to 15% is "up 50%" but only 5 points; a rise from 2% to 3% is also "up 50%". (2) *Out of how many leads, and were they counted the same way?* With a small number of leads, one or two extra wins can move the rate a lot, and a change such as removing duplicate leads raises the win rate without any change in selling.

---

## Where this leads

- **Chapter 5, Thinking Like an Analyst,** turns the questions *of what?* and *compared with what?* into a method for breaking down any business question.
- **Chapters 10 and 11** build these calculations into spreadsheets: percentages, weighted averages, and pivot tables of shares and averages.
- **Chapter 13** calculates month-over-month growth, running totals, and moving averages in SQL on the same 2025 data you used here.
- **Chapter 15, Data Visualization Principles,** goes deeper into honest charts: axes, chart choice, and the visual tricks from section 4.7.
- **Chapter 21, Descriptive Statistics & Probability,** adds spread, percentiles, distributions, and Bayes' rule.
- **Chapter 22, Statistics Without Fooling Yourself,** shows how to tell whether a difference between two rates is real or chance.
- **Chapter 23, Business Acumen, KPIs & Metrics,** applies growth rates, margins, and ratios to reading a company's financial statements.
- **Interview preparation:** probability questions appear in Chapter 73 (statistics, probability, and experimentation), and guesstimates and metric questions in Chapter 75, with model answers.


# Chapter 5. Thinking Like an Analyst

> **Chapter at a glance**
>
> **You will learn to:** ask the questions that turn a request into useful analysis · rewrite a vague request as a precise question tied to a decision · write hypotheses that data can prove wrong · break a problem into an issue tree whose branches are MECE (no overlaps, no gaps) · tell facts from opinions and assumptions · check a claim or chart before believing it, including correlation that isn't causation · recognize the biases that bend how people read data, including your own · structure a decision so that data can inform it.
>
> **Before you start:** Chapter 1 (the data-to-insight ladder), Chapter 3 (booked, billed, and collected), and Chapter 4 (percentages, averages, and small numbers).
>
> **Time needed:** 3–4 hours, including the exercises and the project.
>
> **Tools:** a pen and paper, or a whiteboard. Issue trees are easiest to draw by hand first.
>
> **Practice data:** Riverstone's first quarter of 2026 (the mini database) for the worked example, and its 2025 CRM leads (the one-year database) for the story. Every number was checked by script.

---

## Why this matters

Two analysts get the same message from the Sales Head: *"March was terrible. Can you look into it?"*

The first opens the database, pulls every number about March, builds twelve charts, and sends a 15-slide deck two days later. It's accurate. Nobody knows what to do with it.

The second replies with one question: *"Do you mean billed revenue, and is this for the plan you're making with the team next week?"* Then she lists five possible reasons revenue could have fallen, checks each against the data in an afternoon, rules out three, and sends a half-page note: *"Most of the fall is three customers who ordered in February and not in March. All three owe us money. I'd call them before offering anything."*

Both know the same tools. The second knows how to **think about the problem before touching the data**, and that's what separates analysts people ask for by name from analysts who produce reports.

It's a method, not a talent: ask what the question is for, list the possible answers before looking, break the problem into pieces that don't overlap, test each piece, and notice when your own expectations are steering you. Every later chapter gives you a new tool. This chapter decides whether you point it at the right thing.

---

## In plain English

Think about a good doctor.

You walk in and say, *"I feel terrible."* A bad doctor prescribes something for "feeling terrible". A good doctor asks questions. *Since when? Where does it hurt? Any fever? Did you eat anything unusual?* In their head, they're listing possible causes and ruling them out one by one. Only then do they decide on treatment, and they tell you what to watch for in case they're wrong.

An analyst does the same thing with a business problem:

- **"I feel terrible"** is the vague request: *"Sales are down."*
- **The doctor's questions** turn it into a precise question: *which sales, compared with when, and what are you trying to decide?*
- **The list of possible causes** is a set of hypotheses, organized into an issue tree.
- **The tests** are queries, counts, and comparisons.
- **The diagnosis and treatment** are the conclusion and the recommendation.

A doctor who orders every test on every patient isn't thorough; they're lost. The same is true of an analyst who pulls every number.

---

## 5.1 Curiosity and asking good questions

### Four kinds of question

Chapter 1 (section 1.2) introduced the ladder from data to insight. Business questions climb the same ladder, and knowing which rung a question is on tells you what kind of work it needs.

| Kind | The question | Riverstone example | What it needs |
|---|---|---|---|
| **Descriptive** | What happened? | *What was billed revenue in March 2026?* | Counting and summarizing |
| **Diagnostic** | Why did it happen? | *Why did March fall 80.3% from February?* | Breaking down, comparing, testing hypotheses (this chapter) |
| **Predictive** | What will happen? | *What will April's revenue be?* | Patterns over time and models |
| **Prescriptive** | What should we do? | *Should sales offer a discount to customers who didn't reorder?* | Options, criteria, and judgment (section 5.8) |

Most requests arrive as descriptive questions but are really diagnostic or prescriptive underneath. *"What was March revenue?"* usually means *"Is March a problem, and what should we do about it?"* Answering only the surface question is the most common way to do correct work that doesn't help.

### The habit questions

Keep these in your head, or on a card next to your screen:

1. **What is this for?** What decision will the answer inform, and who makes it?
2. **Of what?** What exactly is being counted or measured? (Chapter 4)
3. **Compared with what?** Last month, last year, the target, another group? (Chapter 4)
4. **How do we know?** Where does the number come from, and can we trust it? (Chapter 1)
5. **So what?** If the answer is X, what changes? If nothing changes whatever the answer, why are we asking?
6. **What else could explain it?** Before accepting the first explanation, name at least one other.

The last one is the one people skip, and it catches the most mistakes.

---

## 5.2 From a vague request to a precise question

Real requests are almost always vague, because the people asking are busy and know what they mean. Your first job is to turn the request into a question precise enough that two analysts would answer it the same way.

![A vague request, "Sales are down. Find out why.", passes through five checks (metric and definition, period and comparison, scope, decision it serves, deadline and precision) and becomes a precise question about March 2026 billed revenue](figures/fig5-1-vague-to-precise-question.svg)

*Figure 5.1 — Five checks turn a vague request into a question with one answer.*

A precise question pins down five things:

1. **The metric and its definition.** "Sales" could be booked, billed, or collected (Chapter 3). Name one.
2. **The period and the comparison.** March 2026 compared with February? With January? With the quarter's average? Each gives a different story: March was 80.3% below February, 69.5% below January, and 68.0% below the quarter's monthly average of ₹99,237.
3. **The scope.** All customers? One segment? Including the pending order or not?
4. **The decision it serves.** *"What should the sales team do in the first week of April?"* needs a different depth from *"What do we tell the board?"*
5. **The deadline and precision.** An answer by Wednesday to the nearest ₹1,000 is a different job from a perfect answer next month.

You don't always need to ask all five. Often you can choose sensibly, state it, and let the requester correct you: *"I'm reading 'sales' as billed revenue and comparing March with February; tell me if you meant something else."* That one sentence prevents most wasted work.

### Chapter 3's question, made precise

In Chapter 3's story, the managing director asked, *"Which one is right? And why did we collect nothing?"* about January. Meera's first move was to turn "January sales" into three precise questions: *What was booked in January? What was billed? What was collected?* Once the questions were precise, the "disagreement" disappeared, because the two reports were answering different ones. **A surprising number of business arguments are two people answering different questions with correct numbers.**

> **Try it.** Take this request from a store manager: *"Our customers aren't happy. Can you check?"* Write down three different precise questions it could mean, each with a metric, a period, and a comparison.

---

## 5.3 Hypotheses: possible answers you can test

A **hypothesis** is a possible answer to a question, stated clearly enough that data could show it's wrong. It's a guess with a test attached.

For *"Why did March 2026 billed revenue fall 80.3% from February?"* here are some hypotheses:

- **H1.** Fewer customers placed orders in March.
- **H2.** Customers placed orders of the same number but smaller size.
- **H3.** Orders were placed in March but haven't been invoiced yet.
- **H4.** Wholesale customers, who place the largest orders, didn't order in March.
- **H5.** March is always a slow month for this business.
- **H6.** A competitor cut prices and took our customers.

### What makes a hypothesis useful

| Weak | Strong | Why the strong one is better |
|---|---|---|
| "Something happened with customers." | "Customers who ordered in February didn't order in March." | It says which customers and what they did, so you can check it. |
| "Pricing is a problem." | "Customers who didn't reorder were offered smaller discounts than those who did." | It points to specific data (discounts by customer) that could prove it wrong. |
| "The market is tough." | "March is always slow: March revenue is lower than February in previous years too." | It names the evidence: March in earlier years. |

A strong hypothesis is **specific** (who, what, when), **testable** with data you have or could get, and **falsifiable**: you can say in advance what result would prove it wrong. "The market is tough" can't be proved wrong by any number, which is exactly why people like saying it.

### Write them down before you look

**List your hypotheses before you open the data.** If you look first, you'll find a pattern, build a story around it, and stop looking. Writing them first makes you check the ones you didn't expect, and records what you ruled out, which is often as valuable as what you found.

Some hypotheses can't be tested with the data you have. H5 needs March in earlier years, and the mini database only holds the first quarter of 2026. H6 needs information about competitors that no Riverstone table contains. Say so plainly, and name what would test them (last year's data from the ERP; a conversation with customers). **"This data can't answer that" is a legitimate finding.**

![A loop of six steps: question, hypotheses, data needed, test, conclude, act or ask](figures/fig5-2-hypothesis-loop.svg)

*Figure 5.2 — The hypothesis loop. Most loops end with a better question, which starts the next loop.*

Every analysis in this book follows the loop in Figure 5.2, whether the test is a pivot table, a SQL query, or a machine learning model.

---

## 5.4 Breaking problems down: issue trees and MECE

A list of six hypotheses is a start. But lists get long, overlap, and miss things. An **issue tree** organizes a question into branches, each branch into smaller branches, until every leaf is small enough to check with one piece of data.

### MECE: no overlaps, no gaps

The branches of a good tree are **MECE** (pronounced "mee-see"): **mutually exclusive** (no two branches cover the same thing) and **collectively exhaustive** (together they cover everything). The term comes from management consulting, but the idea is plain logic.

![Two ways to split Riverstone's eight customers: "big, in Mumbai, new in 2026" overlaps and leaves Patel Kitchenware out; "retail, wholesale, hospitality" puts every customer in exactly one group](figures/fig5-3-mece-bad-and-good-splits.svg)

*Figure 5.3 — The top split double-counts two customers and misses one. The bottom split is MECE.*

In Figure 5.3, splitting customers into "big", "in Mumbai", and "new in 2026" puts Metro Mart and Northgate in two groups each and Patel Kitchenware in none, so group totals won't match the company's revenue, and a conclusion like "the problem is new customers" might really be about Mumbai. Split by segment instead, and every customer sits in exactly one group.

Four reliable ways to get MECE branches:

| Split by | Example | Why it's MECE |
|---|---|---|
| **A formula** | billed revenue = number of invoiced orders × average order value | math can't overlap or leave gaps |
| **A category with one value per record** | segment, product category, region | each customer or product has exactly one |
| **A process** | lead → quote → order → invoice → payment (Chapter 3) | each step follows the last |
| **Opposites** | inside our control / outside it; new customers / existing | "not A" covers everything that isn't A |

Splits like "people, process, technology" feel MECE but usually overlap. When in doubt, use a formula or a single-valued category.

### Working through March

Here is the question from section 5.2, answered with an issue tree. All the numbers come from the mini database.

![An issue tree for why March 2026 billed revenue fell 80.3%: fewer invoiced orders (main cause), smaller orders (contributes), and timing or season (partly), with second-level branches for which customers stopped, overdue balances, wholesale mix, the pending order, and seasonality](figures/fig5-4-issue-tree-march-revenue.svg)

*Figure 5.4 — The March issue tree, with what the data says about each branch.*

**Step 1. Split with a formula.** Billed revenue = number of invoiced orders × average invoiced order value.

| | Invoiced orders | Average order value | Billed revenue |
|---|---|---|---|
| February 2026 | 5 | ₹32,340 | ₹1,61,700 |
| March 2026 | 2 | ₹15,900 | ₹31,800 |

*Source: Mini database (Jan–Mar 2026).*

Both parts fell. How much of the ₹1,29,900 fall does each explain? If March had kept February's average order value, 2 orders would have brought ₹64,680. So the drop in the **number** of orders accounts for ₹1,61,700 − ₹64,680 = **₹97,020** (74.7% of the fall), and the smaller **size** of March's orders accounts for the remaining ₹64,680 − ₹31,800 = **₹32,880** (25.3%). ✓ ₹97,020 + ₹32,880 = ₹1,29,900.

> **Simplification note.** The shares depend slightly on whether you change count or size first; the ranking doesn't.

**Step 2. Fewer orders: which customers?** Five customers had orders invoiced in February: Sharma Hardware, Metro Mart, Coastal Foods, Sunrise Caterers, and Northgate Distributors. In March, only Sharma Hardware and Green Leaf Hotels were invoiced. Metro Mart ordered in March, but its order is still pending. So three customers ordered in February and not at all in March: **Coastal Foods, Sunrise Caterers, and Northgate Distributors**.

Is that unusual? Coastal Foods ordered on 9 January and 11 February, 33 days apart; by 31 March it's been 48 days. Worth noticing, though two orders are a thin pattern (Chapter 4).

**Step 3. Timing: is something stuck?** Order 5012 from Metro Mart, worth ₹26,220, was placed on 15 March and is still *Pending*. It's booked, not billed. With it, March would be ₹58,020, still 64.1% below February. **H3 is true but explains only a part.**

**Step 4. Smaller orders: the mix.** February's two wholesale orders (Coastal Foods ₹32,625 and Northgate ₹76,560) were ₹1,09,185, or 67.5% of February's billed revenue. No wholesale customer ordered in March. Wholesale orders are the largest, so losing them shrinks both the count and the average. **H4 is supported.**

**Step 5. Why didn't they reorder?** The ERP's orders can't answer "why", but the invoices and payments can add a clue. On 31 March:

| Customer | Ordered in March? | Owed | Overdue |
|---|---|---|---|
| Northgate Distributors | no | ₹46,560 | ₹46,560 |
| Sunrise Caterers | no | ₹23,325 | ₹23,325 |
| Coastal Foods | no | ₹12,625 | ₹12,625 |
| Patel Kitchenware | no (last order in January) | ₹6,250 | ₹6,250 |
| Sharma Hardware | yes | ₹11,700 | ₹0 (not yet due) |
| Green Leaf Hotels | yes | ₹0 | ₹0 |
| Metro Mart | yes (pending) | ₹0 | ₹0 |

*Source: Mini database (Jan–Mar 2026).*

Every customer with an overdue balance placed no order in March, and no customer who ordered in March had anything overdue. The three customers from step 2 owe ₹82,510 between them, all of it overdue.

That's a striking pattern, and it's exactly the moment to slow down. It doesn't say *which way* the connection runs, or whether there is one. A customer short of cash might stop ordering until it pays. A customer unhappy with a delivery might both withhold payment and stop ordering, so a single cause would explain both (section 5.6). Or, with seven customers, it could be coincidence. One detail points to a specific question: Northgate's February order still shows *Shipped*, not *Delivered*. If the crates never arrived, Northgate isn't a late payer; it's a customer waiting for its goods.

This branch ends as a **hypothesis to test outside the data**: a phone call to each of the three customers, and a check of the delivery records for Northgate.

**Step 6. The branches the data can't reach.** H5 (March is always slow) needs last year's March, which isn't in the mini database. H6 (a competitor) needs information from customers. Both go on the list of open questions, not in the conclusion.

**What to tell Anita.** A good answer is short, ranked, and honest about confidence:

> *"March billed revenue was ₹31,800, down 80.3% from February. About three-quarters of the fall is fewer orders: Coastal Foods, Sunrise Caterers, and Northgate didn't reorder in March, and February's two wholesale orders alone were 67.5% of that month. Metro Mart's ₹26,220 order is still pending; shipping it brings March to ₹58,020. All three customers who didn't reorder have overdue balances (₹82,510 in total), and Northgate's order still shows as not delivered. I'd call all three this week, starting with Northgate, before offering any discounts. I can't tell yet whether March is seasonally slow; that needs last year's data."*

---

## 5.5 Fact, opinion, and assumption

Meetings mix three kinds of statement, often in the same sentence. Separating them is one of the quickest ways to make a discussion productive.

- A **fact** is a statement that can be checked against a record, and has been. *"March billed revenue was ₹31,800."* (It still depends on a definition, so a good fact states it.)
- An **opinion** is a judgment. It may be wise, but it isn't checkable as stated. *"Northgate is a difficult customer."*
- An **assumption** is something treated as true without checking, usually because checking is hard or slow. *"Northgate will pay next week."*

Here are statements from Riverstone's Monday sales review, sorted:

| Statement | Type | What to do with it |
|---|---|---|
| "March billed revenue was ₹31,800." | fact | Use it, with its definition. |
| "Coastal Foods orders about once a month." | a claim from very little data | Treat as a hypothesis: two orders, one gap of 33 days. |
| "Our prices are too high for wholesalers." | opinion | Turn it into a testable hypothesis: *wholesale customers who didn't reorder were quoted higher prices than those who did.* |
| "Northgate will pay next week." | assumption | Write it down, give it an owner, and check it by a date. |
| "Northgate is a difficult customer." | opinion | Ask what experience it's based on; check the delivery status first. |

*Source: Mini database (Jan–Mar 2026).*

Businesses run on opinions and assumptions, because there's never time to check everything. The danger is when they're **presented as facts**, or an old assumption quietly becomes "what we know". List your assumptions in one place, so anyone can challenge them.

---

## 5.6 Checking claims and charts

Chapter 4 (section 4.10) covered number tricks. This section is about the reasoning behind a claim. Before accepting one, from anyone including yourself, ask five questions:

1. **Who says so, and how do they know?** A measured count, a survey, a guess, or an anecdote?
2. **Compared with what?** A number with no comparison can't be "high" or "low".
3. **How many cases, and which ones?** Five customers or five thousand? Chosen how?
4. **What's the mechanism?** Is there a believable reason why A would cause B?
5. **What else could explain it?** Chance, reverse causation, a common cause, or selection.

**Correlation is not causation.** Two things that move together are **correlated**. That doesn't mean one causes the other. There are three common alternatives:

- **Reverse causation: B causes A.** *"Order lines with bigger discounts are bigger lines, so discounts make customers buy more."* In the mini database, the four order lines worth ₹20,000 or more had an average discount of 10.5%; the other fifteen averaged 1.67%. But Riverstone's own rules (Chapter 3, section 3.6) give larger discounts to larger orders. The size comes first; the discount follows. The data can't show that discounts grow orders.
- **A common cause: C causes both.** In section 5.4, overdue balances and missing reorders went together. A delivery problem could cause both: the customer won't pay for goods it hasn't received, and won't reorder either. Chasing payment harder would then make things worse.
- **Selection: the cases were chosen in a way that creates the pattern.** *"Customers who attend our trade fair order more."* Maybe the ones who attend were already the most engaged customers.

And sometimes it's **chance**: with seven customers, patterns appear by accident. Chapter 22 shows how to judge whether a pattern is bigger than chance.

> **Watch out: your own analysis is a claim too.** The five questions apply to what you're about to send. The note to Anita in section 5.4 states a measured fact ("about three-quarters of the fall is fewer orders") and a recommendation ("I'd call them"), but it's careful not to say "customers stopped ordering *because* they owe us money".

---

## 5.7 Bias in how we see data

A **cognitive bias** is a predictable way in which people's judgment drifts from the evidence. Everyone has them, including experienced analysts. You can't switch them off, but you can recognize the common ones and build habits that catch them.

| Bias | What it looks like at Riverstone | Antidote |
|---|---|---|
| **Confirmation bias**: noticing evidence that fits what you already believe | Vikram is sure a competitor is undercutting prices, so he asks for lost deals that mention price, and not for the ones that don't | Write hypotheses first (section 5.3); look for evidence that would prove your favorite wrong |
| **Anchoring**: judging a number against the first number you saw | March looks like a disaster against February's ₹1,61,700. But February was unusual: Northgate's first order alone was ₹76,560, 47.3% of the month. Against the quarter's monthly average of ₹99,237, March is still weak, but the comparison is fairer | Compare against several baselines: the previous month, the average, the same month last year, the target |
| **Regression to the mean**: an unusually high or low value tends to be followed by a more ordinary one | A month boosted by one big first order is likely to be followed by a lower month, even if nothing went wrong | Before explaining a change, ask whether the starting point was unusual |
| **Survivorship bias**: studying only the cases that made it through | Studying won deals to learn "what works", without looking at the lost and never-contacted leads that went through the same steps | Always include the cases that dropped out |
| **Availability and recency**: overweighting what's vivid or recent | One angry phone call from a customer on Friday becomes "customers are unhappy" on Monday | Count: how many complaints, out of how many customers, over what period? |
| **Small numbers**: trusting patterns from very few cases | "All the customers who owe us stopped ordering" is based on four customers | Give the counts; call it a hypothesis until more cases agree (Chapter 4, section 4.8) |
| **The analyst's own bias**: wanting an interesting finding | A clean story about overdue balances is more exciting than "one big order made February unusual", so it's tempting to lead with it | State the ordinary explanation first if it's the bigger one |

*Source for the Riverstone numbers: Mini database (Jan–Mar 2026).*

The last row matters most. Analysts are rewarded for insights, so there's a pull toward the surprising story; a good reputation rests on being right, which often means reporting the ordinary explanation clearly.

---

## 5.8 Deciding with data

Analysis exists to help someone decide. Data rarely decides by itself; it narrows the options, estimates consequences, and shows where the uncertainty is.

| Part | Question | For the three customers who didn't reorder |
|---|---|---|
| **Decision** | What exactly is being decided, and by whom? | What sales does about Coastal Foods, Sunrise Caterers, and Northgate this week (Anita decides) |
| **Options** | What are the choices, including doing nothing? | A. Wait. B. Call each customer to ask why, and check Northgate's delivery. C. Offer 5% off their next order. D. Put overdue accounts on hold until they pay. |
| **Criteria** | What matters in choosing? | Revenue, margin, cash owed, the customer relationship |
| **Evidence** | What does the data say about each option? | All three owe ₹82,510, all overdue. Northgate's order isn't marked delivered. A 5% discount on an Industrial Crate cuts its margin from 24.1% to 20.1%. |
| **Reversibility** | How costly is it to be wrong? | A call is cheap and can't do much harm. A discount sets a price expectation that's hard to take back. A hold could lose a customer whose goods never arrived. |
| **Recommendation and confidence** | What should we do, and how sure are we? | B this week; decide on C or D after the calls. Medium confidence: the pattern is clear, but it's four customers and the cause is unknown. |
| **What would change my mind** | Which new fact would change the recommendation? | If customers say price is the reason and their balances are paid, reconsider C. If goods weren't delivered, fix the delivery before anything else. |

*Source: Mini database (Jan–Mar 2026).*

Three principles sit behind the table:

- **Match the effort to the decision.** A reversible, cheap decision (a phone call) needs less evidence than an irreversible, expensive one (a price change or a hire).
- **Include "do nothing".** It's often the real alternative, and it has costs too.
- **Say what would change your mind.** It shows where the uncertainty is and what to watch.

> **Interview extra point.** In a case interview or a take-home question ("Revenue fell 20%. Why?"), don't start calculating. Spend the first minute restating the question precisely, then sketch a MECE split out loud (for example, number of orders × average order value, then by segment), and say which branch you'd check first and why. Interviewers are grading the structure of your thinking more than the final number. Chapter 75 (product sense, metrics, and case studies) has practice cases with model answers.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Answering the surface question | correct numbers nobody can act on | Ask what the answer is for, and who decides |
| Starting with the data instead of the question | a pile of charts and no conclusion | Write the precise question and hypotheses first |
| Hypotheses that can't be wrong | "the market is tough" survives any evidence | Make each one specific, testable, and falsifiable |
| Branches that overlap or leave gaps | group totals don't add up to the whole | Split by a formula, a single-valued category, or a process |
| Stopping at the first explanation | a confident story that's partly true | Name at least one other explanation and check it |
| Reading correlation as causation | "discounts make customers buy more" | Check reverse causation, common causes, selection, chance |
| Comparing against one unusual baseline | a normal month looks like a disaster | Use several baselines: average, target, same month last year |
| Over-analyzing a small, reversible decision | a week spent on something a phone call would settle | Match the effort to the cost of being wrong |

---

## In the real world: do we need another sales executive?

It's the first week of January 2026. Vikram Singh, the Sales Manager, has asked the managing director for a fourth sales executive. His reason: *"Leads are piling up. The CRM shows 43 enquiries last year, and my team can't keep up."* The MD forwards it to Anita with one line: *"Is this right?"* Anita asks Meera Iyer to look before Friday.

**1. What's the decision, and what's the precise question?** The decision is whether to hire. The question underneath: *"Did Riverstone lose new business in 2025 because the sales team didn't have time to handle its leads?"* A hire fixes capacity, not a slow process, poor routing, or poor leads, so the question must separate those.

**2. The issue tree**, following the lead's journey:

- **Too many leads?** How many real enquiries arrived, per executive?
- **Leads missed or handled slowly?** How many were never contacted, and how long did first contact take?
- **Leads contacted but lost?** What share of contacted leads were won?
- **Capacity or something else?** If the team is too busy, the busiest people should be the ones missing leads.

**3. The tests.** All from the one-year database.

- **Volume.** The 43 rows include duplicates: the same enquiry submitted two or three times. There were **30 real enquiries** in the year, about 2.5 a month, or fewer than one a month per sales executive. "Piling up" isn't about volume.
- **Missed and slow.** **8 of the 30 (26.7%) were never contacted at all.** The other 22 waited an average of **9.7 days** for a first contact. One referral, Tulip Mart, has been waiting since 23 September, 99 days.
- **Lost after contact.** 6 of the 22 contacted leads were won (27.3%). Of the leads contacted within a week, 3 of 8 were won; of those contacted later, 3 of 14. That fits "faster is better", but with numbers this small it's a hypothesis, not a finding.
- **Capacity.** If the team were overloaded, the executives handling the most customer orders should miss the most leads. The data says the opposite:

| Sales executive | Orders handled in 2025 | Leads assigned | Never contacted | Average days to first contact |
|---|---|---|---|---|
| Farah Khan | 64 | 5 | 0 | 7.7 |
| Rahul Mehta | 53 | 10 | 3 | 10.9 |
| Neha Kulkarni | 46 | 15 | 5 | 9.8 |

*Source: One-year database (2025 CRM leads).*

Farah, with the most orders, missed none of her leads. Neha, with the fewest orders, was assigned half of all leads, including 9 of the 14 website enquiries, and missed 5. Website leads were the most often missed: 5 of 14 were never contacted.

**4. Checking herself.** The CRM doesn't record time spent on visits, calls, or complaints, so orders aren't the whole workload. And reading the table as "Neha is the problem" would be unfair: she got as many leads as Rahul and Farah combined, including most website enquiries. The pattern points at **how leads are routed and followed up**, not at a person.

**5. The recommendation.** She sends Anita a half-page note:

> *"The data doesn't support hiring for lead volume: 30 real enquiries came in last year (the CRM's 43 includes duplicates), fewer than one a month per executive. The problem is follow-up: 8 enquiries were never contacted and the rest waited almost 10 days on average. Missed leads are concentrated among website enquiries and in the largest lead list, not with the busiest executive. I'd (1) call the 8 uncontacted leads this week, starting with the Tulip Mart referral, (2) spread website leads evenly, (3) set a two-working-day rule for first contact with a daily reminder, and (4) fix the duplicate website submissions. What would change my mind: if leads grow sharply, or if response times are still slow after a quarter of the new routing, a hire is worth revisiting. The CRM doesn't record time spent, so I can't rule out that the team is busy with work outside orders and leads."*

Anita forwards it to the MD and Vikram. Vikram's first reaction is irritation. His second, after reading the table, is to ask Meera how to set up the daily reminder (you'll build that reminder yourself later in the book).

The request was a solution ("hire"). Meera turned it into a question about a cause, tested each branch, avoided blaming one person, stated what she couldn't see, and recommended cheap, reversible steps first, with a clear condition for revisiting the expensive one.

---

## Project: an issue tree for a real question

**Goal:** take one real business question, make it precise, and build an issue tree that shows exactly which data would answer each branch.

### Tools you'll need

- **Pen and paper, or a whiteboard.** Issue trees are fastest by hand. Draw the first version in five minutes; tidy it later.
- **A spreadsheet or document** for the hypothesis log: one row per hypothesis, with the data needed, the result, and the status (supported, rejected, open).
- **A diagram tool** (optional): diagrams.net, PowerPoint, or Google Slides for sharing a tree.
- **SQL and spreadsheets** for the tests, from Chapter 10 onward. This chapter's numbers came from short queries on the Riverstone databases.

**Step 1. Choose a question** from your work, a local business, or your Chapter 4 project: turn one checked claim into an analyst's question. *"Sales up 40% in three years"* becomes *"Did the company's revenue grow faster than its market over those three years, and where did the growth come from?"*

**Step 2. Make it precise.** Write the metric and its definition, the period and the comparison, the scope, the decision it serves, and the deadline (section 5.2).

**Step 3. Write at least five hypotheses** before looking at any data. Make each specific and testable (section 5.3).

**Step 4. Build the tree** two or three levels deep, starting with a MECE split (section 5.4). Check each split for overlaps and gaps.

**Step 5. Add the data to every leaf.** For each leaf, write:

| Column | What to write |
|---|---|
| `branch` | the leaf's question |
| `hypothesis` | what you expect, stated so it could be wrong |
| `data_needed` | the table, file, report, or conversation that would test it |
| `available` | yes, no, or "needs to be collected" |
| `test` | the count, comparison, or query you'd run |
| `result_that_rejects_it` | what you'd have to see to drop this branch |

**Step 6. Label facts, opinions, and assumptions** in anything the question's owner has said about it.

**Step 7. Name one bias** that could affect this analysis (yours or the requester's), and how you'll guard against it.

**Deliverable:** the precise question, the tree, the data table, and a three-sentence plan for which branch you'd test first and why. If you have access to the data, test one branch and write a half-page note like Meera's.

---

## Recap

- Questions are **descriptive, diagnostic, predictive, or prescriptive**. Most requests are diagnostic or prescriptive underneath.
- Keep asking: *what is this for? of what? compared with what? how do we know? so what? what else could explain it?*
- A **precise question** pins down the metric, the period and comparison, the scope, the decision it serves, and the deadline.
- A **hypothesis** is a possible answer that data could prove wrong. **Write hypotheses before you look.** "This data can't answer that" is a legitimate finding.
- An **issue tree** breaks a question into branches until each leaf can be tested. Branches should be **MECE**: no overlaps, no gaps. Split by a formula, a single-valued category, a process, or opposites.
- March 2026's 80.3% fall split into **fewer orders (₹97,020)** and **smaller orders (₹32,880)**, then into three customers who didn't reorder, the missing wholesale orders, and a pending order, ending in a hypothesis to test by phone.
- Separate **facts, opinions, and assumptions**, and list assumptions where everyone can see them.
- **Correlation isn't causation.** Check for reverse causation, a common cause, selection, and chance.
- **Biases** (confirmation, anchoring, regression to the mean, survivorship, availability, small numbers, and the analyst's own) bend everyone's judgment; counter them with habits.
- **Decide with data** by laying out options (including doing nothing), criteria, evidence, reversibility, a recommendation with confidence, and what would change your mind.

---

## Key terms

descriptive question · diagnostic question · predictive question · prescriptive question · habit questions · precise question · hypothesis · testable · falsifiable · issue tree · MECE · mutually exclusive · collectively exhaustive · decomposition (count × size) · fact · opinion · assumption · claim · correlation · causation · reverse causation · common cause · selection · chance · cognitive bias · confirmation bias · anchoring · regression to the mean · survivorship bias · availability bias · recency · small-numbers bias · decision rights · reversibility · confidence · "what would change my mind"

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I ask what an analysis is for before I start it.
- [ ] I can turn a vague request into a precise question with a metric, period, comparison, scope, and decision.
- [ ] I write hypotheses before looking at the data, and each one could be proved wrong.
- [ ] I can build an issue tree with MECE branches, and I know four reliable ways to split.
- [ ] I label statements as fact, opinion, or assumption.
- [ ] I check claims for reverse causation, common causes, selection, and chance.
- [ ] I can name the common biases and the habit that counters each one.
- [ ] I can structure a decision with options, criteria, evidence, reversibility, confidence, and what would change my mind.
- [ ] I've built an issue tree for a real question, with the data for every branch.

---

## Exercises

### Warm-up

1. Label each question as descriptive, diagnostic, predictive, or prescriptive: (a) *How many orders did Sunrise Caterers place in February?* (b) *Should we stop offering 12% discounts?* (c) *Why did Kitchen revenue grow every quarter of 2025?* (d) *How much will we collect in April?* (e) *Which customers owe us money?*
2. Label each statement as fact, opinion, or assumption, and say what you'd do with it: (a) "Invoice 9007 hasn't been paid." (b) "Sunrise Caterers is a bad customer." (c) "The new price list will be ready by Monday." (d) "Hotels don't care about price." (e) "Blue Bay Cafe signed up on 1 March 2026."
3. Is each split MECE? If not, say whether it overlaps, leaves gaps, or both. (a) Orders: Pending, Shipped, Delivered, Cancelled. (b) Customers: large, loyal, new. (c) Revenue: Storage, Kitchen, Industrial, Furniture. (d) Reasons for a late delivery: warehouse delay, truck problem, customer not available, bad weather. (e) Leads: from the website, from referrals, from Mumbai.
4. Rewrite each vague request as a precise question with a metric, period, comparison, and the decision it might serve: (a) "How are we doing with hotels?" (b) "Is the website worth it?" (c) "Check if customers are paying on time."

### Core

5. For the question *"Why did hospitality customers bring in less revenue in March 2026 than in February?"*, write three hypotheses that data could prove wrong, and for each, name the data you'd use. (Hospitality billed ₹23,325 in February and ₹20,100 in March in the mini database.)
6. Billed revenue rose from ₹1,04,210 in January 2026 (3 invoiced orders) to ₹1,61,700 in February (5 invoiced orders). (a) Calculate each month's average invoiced order value. (b) Split the ₹57,490 increase into the part from more orders (holding January's average order value) and the part from the change in order size. (c) Which explains more?
7. Chapter 3 showed that Riverstone collected ₹1,97,250 of ₹2,97,710 billed in the first quarter of 2026 (66.3%). Build a two-level MECE issue tree for *"Why did we collect only two-thirds of what we billed?"* For each leaf, name the data that would test it.
8. Name the bias in each situation and suggest one habit that would counter it: (a) After one customer complains about a cracked crate, a manager says, "Our quality has slipped." (b) An analyst studies the five best customers to learn why customers stay. (c) Revenue drops after a record month, and the team spends a week looking for what went wrong. (d) A manager who wanted a new CRM highlights only the figures that make the old one look bad.
9. A manager says: *"Customers with overdue balances order less. So chasing payments hurts sales, and finance should send fewer reminders."* Give three other explanations for the pattern, and describe what data would help decide between them.

### Stretch

10. Using the table from the story: Farah handled 64 orders and missed none of her 5 leads; Neha handled 46 orders and missed 5 of her 15. (a) What does this data support? (b) What doesn't it support? (c) What additional data would you want before saying anything about individual performance?
11. In the story, leads contacted within a week were won 3 times out of 8 (37.5%); leads contacted later were won 3 times out of 14 (21.4%). (a) Why isn't this proof that faster contact wins more deals? (b) Name one alternative explanation. (c) How could Riverstone test the idea properly?
12. Blue Bay Cafe signed up on 1 March 2026 and hadn't placed an order by 31 March. Structure the decision *"What should sales do about Blue Bay Cafe?"* using the table in section 5.8: at least three options (including doing nothing), criteria, the evidence you'd look for, reversibility, and what would change your mind.

### Think about it (no calculation needed)

13. When should you stop analyzing and give an answer? Describe two signals that you've done enough, and one signal that you haven't.
14. A senior manager says, "I've already decided to cut the Furniture range. Can you find me some numbers that support it?" How would you respond, and what would you offer to do instead?
15. You ask an AI assistant why March revenue fell, and it gives a fluent, confident explanation. Using this chapter, list three things you'd check before repeating it.

---

## Answers

**1.** (a) Descriptive. (b) Prescriptive. (c) Diagnostic. (d) Predictive. (e) Descriptive.

**2.** (a) Fact (checkable in the payments table); use it. (b) Opinion; ask what it's based on and turn it into something checkable, such as "Sunrise pays later than other customers". (c) Assumption (a plan); give it an owner and confirm it. (d) Opinion, and a sweeping one; turn it into a hypothesis, such as "hotel customers accept price increases as often as retailers". (e) Fact (the `signup_date` in the customers table); use it.

**3.** (a) MECE, as long as every order has exactly one of these four statuses. (b) Not MECE: it overlaps (a new customer can be large; a large customer can be loyal) and has gaps (a small, occasional, long-standing customer is none of them). (c) MECE: each product belongs to one category, and the four cover every product. (d) Not MECE: it can overlap (a truck problem caused by bad weather) and has gaps (a wrong address, missing stock, a paperwork delay). Add "other" and define each reason so that one is chosen. (e) Not MECE: "Mumbai" is a location, not a source, so a website lead from Mumbai is in two groups, and leads from trade fairs or cold calls are in none.

**4.** One good version of each: (a) *"What was billed revenue from hospitality customers in the first quarter of 2026, compared with the previous quarter, and which customers drove the change? (For deciding on an April hotel promotion.)"* (b) *"How many 2025 website enquiries became customers, and how much revenue did they bring, compared with referrals and trade fairs? (For next year's website budget.)"* (c) *"What share of first-quarter 2026 invoices were paid by their due date, and which customers are most often late? (For deciding whom finance calls first.)"*

**5.** Examples: (1) *Fewer hospitality customers ordered in March than in February.* Data: orders by customer and month (Sunrise Caterers ordered in February, Green Leaf Hotels in March). (2) *Hospitality customers who ordered placed smaller orders.* Data: order values by customer and month. (3) *The hospitality order that would have made the difference is still pending or was cancelled.* Data: order status for hospitality customers in March. Note that the gap is small (₹3,225) and each month has one order, so almost any difference is normal variation.

**6.** (a) January: ₹1,04,210 ÷ 3 = **₹34,737**. February: ₹1,61,700 ÷ 5 = **₹32,340**. (b) Holding January's average order value, 5 orders would bring 5 × ₹34,736.67 = ₹1,73,683, which is ₹69,473 more than January: that's the **count effect, +₹69,473**. The change in size is 5 × (₹32,340 − ₹34,736.67) = **−₹11,983**. Check: ₹69,473 − ₹11,983 = ₹57,490. ✓ (c) The increase came entirely from **more orders**; the average order actually got a little smaller.

**7.** One good tree:

- **Collected only 66.3% of billings**
  - **Not yet due** (the amount billed recently, within 30-day terms). Data: invoices by due date as of 31 March (invoice 9010's ₹11,700 isn't due until 10 April).
  - **Due but unpaid (overdue)**
    - *Customers can't or won't pay.* Data: overdue by customer; payment history; credit checks.
    - *Customers dispute the invoice.* Data: support tickets, delivery status, proof of delivery.
    - *Riverstone hasn't chased.* Data: reminder logs from finance.
  - **Paid but not recorded yet.** Data: bank statement lines not yet matched to invoices.

The first split (not yet due / overdue / paid but unrecorded) is MECE for the money not collected. From Chapter 3: ₹1,00,460 is unpaid, of which ₹88,760 is overdue and ₹11,700 is not yet due.

**8.** (a) **Availability** (one vivid complaint). Habit: count complaints over a period, out of how many deliveries. (b) **Survivorship** (studying only customers who stayed). Habit: compare with customers who left. (c) **Regression to the mean** (after a record month, a lower one is normal). Habit: compare with the average and the same month last year before searching for a cause. (d) **Confirmation bias**. Habit: write down in advance what evidence would show the old CRM is fine, and look for it.

**9.** (1) **Common cause**: a delivery or quality problem makes customers both withhold payment and stop ordering. (2) **Reverse causation**: customers who order less have less reason to keep their account current. (3) **Cash-strapped customers** pay late and order less, whatever the reminders. Data that helps: complaints and delivery records for overdue customers; whether ordering fell before or after the balance became overdue; and a few customer conversations.

**10.** (a) Missed leads weren't concentrated with the executive handling the most orders, so "too busy with orders" isn't supported, and lead assignment was very uneven. (b) Nothing about individual effort or ability: the numbers are tiny, Neha got most website leads, and orders aren't all of anyone's work. (c) Time spent on other work, each person's lead sources, how leads were assigned, and absences over the year.

**11.** (a) The counts are very small (6 wins in total), so the difference could well be chance (Chapter 22), and the leads weren't assigned a response time at random. (b) Executives may contact the most promising leads first, such as referrals, so the leads contacted quickly were already more likely to be won (selection, or a common cause: lead quality affects both speed and winning). (c) Run a simple experiment (Chapter 30): for a quarter, randomly assign new leads to "contact within two working days" or "normal process", then compare win rates, or at least compare fast and slow contact within the same lead source.

**12.** **Decision:** what sales does about Blue Bay Cafe in April. **Options:** A. wait; B. call or visit to understand its needs; C. a first-order offer; D. send the catalog and a sample. **Criteria:** chance of a first order, cost, margin, fit. **Evidence:** 30 days since signup without an order; what it enquired about; how long other new customers took (Green Leaf Hotels signed up on 8 January and placed its first order on 20 January). **Reversibility:** a call is cheap; a discount sets an expectation. **Recommendation:** B first, then D if interest is confirmed. **What would change my mind:** a specific, large first order that depends on price would make C worth considering.

**13.** Enough: more precision wouldn't change the decision; the remaining branches can't be answered with available data, and you've said so. Not enough: you can't yet explain most of the change, or the recommendation would flip on a branch you haven't checked.

**14.** Don't cherry-pick; it risks your credibility and the manager's. Offer a fair picture instead: *"I'll look at Furniture's revenue, margin, and trend. If it supports cutting the range, that's a stronger case; if not, better you hear it from me than from the board."* Chapter 24 covers handling this kind of pressure.

**15.** (1) **Are its numbers right?** Check the metric, definition, and figures against the database. (2) **Is it presenting hypotheses as facts?** Order tables can't tell you *why* customers behaved as they did. (3) **What has it left out?** Compare with your own issue tree: timing, mix, and the limits of the data. Chapter 26 covers working with AI assistants.

---

## Where this leads

- **Chapter 6, Planning Your Learning,** turns the book's hours into a plan for your week, and shows which chapter brings each tool you'll use to test hypotheses.
- **Chapters 10–13** give you the tests: spreadsheets and SQL to count, compare, and break down numbers the way section 5.4 did.
- **Chapter 14, Data Cleaning & Preparation,** handles the "is the data even right?" branch that every issue tree should include.
- **Chapter 22, Statistics Without Fooling Yourself,** shows whether a pattern like "3 of 8 versus 3 of 14" is bigger than chance.
- **Chapter 23, Business Acumen, KPIs & Metrics,** builds full KPI trees for Riverstone and diagnoses a revenue dip with more careful breakdowns.
- **Chapter 24, Requirements, Storytelling & Stakeholders,** turns notes like Meera's into memos and presentations, and covers handling "can you find numbers that support this?"
- **Chapters 30 and 31** test cause and effect properly: experiments, and methods for when experiments aren't possible.
- **Chapters 36 and 40** take on predictive questions like *"What will April's revenue be?"*: the machine learning workflow, and forecasting over time.
- **Interview preparation:** case questions ("revenue fell; why?"), structuring, and hypothesis-driven thinking appear in Chapter 75 (product sense, metrics, and case studies), with model answers; Chapter 76B (the Business Analyst question bank) uses the same structured thinking on requirements and process questions.


# Chapter 6. Planning Your Learning

> **Chapter at a glance**
>
> **You will learn to:** estimate honestly how many hours this book takes, and turn them into weeks at your real pace · build a weekly rhythm you can keep, and recover from a missed week · check whether your computer is ready, and know which chapter brings each tool · read an official page to settle a question for yourself · use AI assistants to learn faster without letting them do your thinking · plan your route and your first 90 days.
>
> **Before you start:** Chapters 1–5, and "How to Use This Book" at the front of the book.
>
> **Time needed:** 2–3 hours, including the exercises and the project.
>
> **Tools:** a notebook or a notes app, and a calendar. No software to install.
>
> **Practice data:** none; you plan with your own week.

---

## Why this matters

From Chapter 10 onward, every chapter asks you to type, run, break, and fix things: formulas, queries, scripts, dashboards. Each of those chapters installs the tool it needs at its start and checks it works with one small first step, so there's nothing to install today.

This chapter sets up the other half: **you**. An honest number of hours, a plan you can keep, a weekly rhythm, a way to use AI assistants that helps you learn instead of replacing the learning, and the habit of checking the official source when two sources disagree. It all decides whether you finish.

---

## In plain English

Think of a cook planning a week of meals. A good cook doesn't buy every utensil in the shop on Sunday and leave them in boxes. They decide what they'll cook each day, check how long each dish takes, and get each utensil when a recipe first calls for it.

Planning to learn is the same:

- **The meal plan** is your study plan: what you'll cook this week, and when.
- **The cooking times** are each chapter's *Time needed* line. Added up, they tell you honestly how long the whole menu takes.
- **The utensils** are the tools: a spreadsheet, a database, Power BI, Python. You get each one when a recipe first needs it.
- **The recipe book** is this book, plus the official documentation for each tool, which is where you look when the recipe is unclear.

You don't need every utensil on day one, only a plan, a rhythm, and the next recipe.

---

## 6.1 How long it really takes

Every chapter's *Time needed* line estimates its **study hours**: the reading, the exercises, and the project together. Adding up those lines for every teaching chapter gives the book's own answer to "how long will this take?":

| | Hours | 6 hours a week | 8 hours a week | 10 hours a week |
|---|---|---|---|---|
| Parts 0 and 1 (<span class="nobr">Chapters 1–9</span>) | <span class="nobr">27–37</span> | 5–6 weeks | 3–5 weeks | 3–4 weeks |
| Part 2 (<span class="nobr">Chapters 10–27</span>) | <span class="nobr">367–451</span> | 61–75 weeks | 46–56 weeks | 37–45 weeks |
| **Job-ready: Parts 0 to 2 (<span class="nobr">Chapters 1–27</span>)** | **<span class="nobr">394–488</span>** | **66–81 weeks, or 15 to 19 months** | **49–61 weeks, or 11 to 14 months** | **39–49 weeks, or 9 to 11 months** |
| Parts 3 to 7 (<span class="nobr">Chapters 28–67</span>) | <span class="nobr">563–705</span> | 1.8 to 2.3 years | 1.4 to 1.7 years | 1.1 to 1.4 years |
| **All of it (<span class="nobr">Chapters 1–67</span>)** | **<span class="nobr">957–1193</span>** | **3.1 to 3.8 years** | **2.3 to 2.9 years** | **1.8 to 2.3 years** |

These are reading-and-exercise hours. Fluency takes more practice on top (Chapter 9).

**Read the bold job-ready row first.** Parts 0 to 2, the **job-ready path**, are what a first analyst job asks for. Parts 3 to 7 are the rest of a career, and they're optional branches: Chapter 8 shows which of them each role needs.

**To turn the table into your own plan, divide.** Weeks = hours ÷ your hours a week. At 6 hours a week, the job-ready path is 394 ÷ 6 = 65.7, about 66 weeks, at the low end and 488 ÷ 6 = 81.3, about 81 weeks, at the high end: fifteen to nineteen months. Months are weeks × 12 ÷ 52, so 66 weeks is about 15 months and 81 weeks is about 19. The same arithmetic works for any number of hours; use the hours you really have, not the hours you wish you had.

That's longer than many courses promise, and it's honest. A plan built on the real number survives a bad month; a plan built on a hopeful one fails in week three and takes your confidence with it.

**One more thing about Parts 0 and 1.** Each of their nine chapters has a project, and together they're more than a month's work if you do them all at once. Do three of them properly as you go: Chapter 1's spending log (it runs for a week while you read on), this chapter's plan, and Chapter 8's door plan. Start Chapter 9's learning system and carry it alongside the book for its twelve weeks. Come back to the others (Chapters 2, 3, 4, 5, and 7) in a review week. Their hours are already in the table, so doing them later doesn't change your total.

---

## 6.2 A weekly rhythm you can keep

The book is long. The difference between finishing and stopping is rarely intelligence; it's a plan, a rhythm, and a way of keeping going after a missed week.

![A week of about 8 hours, one bar per day: Monday 1 hour reading a new section, Tuesday 1 hour of exercises, Wednesday 1 hour reading the next section, Thursday 1 hour of exercises, Friday 30 minutes of review from memory, Saturday 2.5 hours of project or lab work, and Sunday 1 hour redoing missed exercises and planning the next week](figures/fig6-1-weekly-rhythm.svg)

*Figure 6.1 — Short, regular sessions, one longer session for projects, and a review built into the week.*

Figure 6.1 adds up to 8 hours: 1 + 1 + 1 + 1 + 0.5 + 2.5 + 1. Three ideas are built into it:

- **Alternate reading and doing.** A section read on Monday gets practiced on Tuesday, while it's fresh but no longer in front of you.
- **Review from memory.** On Friday, close the book and write down the chapter's key terms and main ideas before checking the recap. Pulling ideas out of your memory strengthens them far more than reading them again. Chapter 9 explains why this works and how expertise forms.
- **Plan at the end of the week.** Ten minutes on Sunday deciding exactly which sections you'll do on which days makes Monday simpler to start.

### When you fall behind

You will miss weeks. Everyone does. When it happens, don't try to catch up by doubling the hours; that's how a missed week becomes a missed month. Instead: **move the plan back a week, do one short review session to reconnect, and start the next section.** Keep a one-line **study log** in your `notes/` folder (date, what you did, one thing you learned), so that when you return, you can see how far you've come.

---

## 6.3 What you'll need, and when

### The computer

You don't need a new or high-end computer to become a data analyst. Almost everything in Parts 0 to 2 runs comfortably on an ordinary laptop from the last five or six years: Windows 10 or 11, or a recent macOS; **8 GB of memory (RAM)** to start, 16 GB to be comfortable; 20 GB of free disk space, 50 GB or more to be comfortable; and an internet connection good enough to download software. A second monitor helps, so the book or the documentation sits next to your work, but a laptop screen is enough.

Three situations need a little planning:

- **A Mac.** Everything in the book runs on a Mac except **Power BI Desktop** and **Excel's Power Pivot**, a data-modelling feature of desktop Excel (Chapter 11, section 11.8), which are Windows only. The usual answer in Microsoft's Q&A forums is to run Windows 11 in a virtual machine, a program that runs Windows in a window on your Mac (for example, Parallels Desktop). The browser version of Power BI can view and interact with reports but can't build the data models Chapter 16 teaches, and it needs a work or school account. You can do everything else on your Mac and handle those two separately.
- **A Chromebook, tablet, or phone.** These can run Google Sheets, Excel for the web, and online SQL practice sites, which is enough for the spreadsheet chapters and some early SQL practice. They can't run Python properly, the databases, or Power BI Desktop. Plan to borrow or buy a laptop before the Python chapters.
- **A work laptop you can't install software on.** Many companies lock their laptops, for good security reasons. Ask your IT team; learning tools like PostgreSQL, Python, and DBeaver are commonly approved. Some tools can be installed without IT's help: Microsoft's documentation notes, for example, that Power BI Desktop from the Microsoft Store doesn't need administrator rights. The story later in this chapter shows one way through.

> **Watch out: Windows 10.** Microsoft stopped regular security updates for Windows 10 in October 2025. It still runs every tool in this book, but a computer that no longer gets security updates is a risk when you start connecting to company data. If you can upgrade to Windows 11, do.

### The tools, and when each arrives

This is the book's **tool timeline**: which tool you'll need, and in which chapter you'll first need it.

| Tool | First needed in | Cost | Runs on |
|---|---|---|---|
| A spreadsheet: Excel or Google Sheets | Chapter 10 | Free on the web | Windows, Mac, browser |
| PostgreSQL and DBeaver (MySQL optional) | Chapter 12 | Free | Windows, Mac, Linux |
| Power BI Desktop | Chapter 16 | Free | Windows only |
| Python, VS Code, and Jupyter | Chapter 17 | Free | Windows, Mac, Linux |
| Git | Chapter 26 | Free | Windows, Mac, Linux |

You'll install each tool at the start of the chapter that first uses it, and check it works with one small first step. Appendix B gathers all the install steps in one place, for when you set up a second computer.

Why wait? A tool installed months before you use it has usually been updated by the time you open it, and a problem is much easier to fix when the chapter in front of you explains what the tool is for. Installing in the chapter that needs it costs nothing and saves an evening.

![Five tool cards along a line of chapters: a spreadsheet, Excel or Google Sheets, first needed in Chapter 10, on Windows, Mac or a browser; the databases, PostgreSQL and DBeaver with MySQL optional, in Chapter 12, on Windows, Mac or Linux; Power BI Desktop in Chapter 16, Windows only; Python with VS Code and Jupyter in Chapter 17, on Windows, Mac or Linux; and Git in Chapter 26, on Windows, Mac or Linux](figures/fig6-2-tool-timeline.svg)

*Figure 6.2 — Five groups of tools cover the whole analyst path, each installed in the chapter that first needs it. Later parts add their own tools when you reach them.*

A few words on these choices. **Free tools only**, so nobody is locked out. **PostgreSQL and MySQL both**, because between them they cover most databases an analyst meets. **DBeaver**, because one app works with both databases. **Power BI**, because it's widely used and free to start with. **Python with VS Code**, because it's free, runs everywhere, and the same editor serves you from your first script to production code.

---

## 6.4 Reading documentation

Every tool in this book has **official documentation**: the manual written by the people who make it. When a tutorial, a colleague, and an AI assistant disagree, the documentation settles it. You'll use it in every tool chapter. You can practise the habit today, on a page you already have: the official page for your phone plan, or your bank's page of fees and charges.

You don't read an official page front to back. You go in with a question and look for five things:

1. **The exact rule**: the name of the thing you're asking about, and what it applies to. On a phone plan's page, that might be the line headed *Daily data*.
2. **The description, every word**: what the rule says, in one or two sentences. Read every word; the small details are usually the point. "2 GB per day" and "2 GB per day, unused data does not carry forward" are different plans.
3. **An example**: many pages show one, such as what happens on a day you use 2.5 GB. Work through it yourself before relying on it.
4. **The exceptions**: often in a box, a footnote, or the small print at the bottom. This is where "except on international roaming" or "after the fair-usage limit, speed drops" lives.
5. **The date or version**: official pages change, and old copies stay online. Check the "last updated" date or the plan's name and version, and make sure it's the one you're actually on.

If the page doesn't answer it, try the organization's official help pages or support, then a well-asked search.

Tools disagree with each other more often than you'd expect. For example, spreadsheets, databases, and Python don't all round a number that ends in exactly .5 the same way. Each tool's documentation says exactly which rule it uses, and you'll check it for yourself when you meet those tools.

---

## 6.5 Learning with AI assistants without letting them think for you

AI assistants can explain a concept five different ways, spot the typo in a query, and describe what an error message means. Used well, they make you learn faster. Used badly, they let you finish every exercise without learning anything, and you find out in an interview, or in your first week at work, when the assistant isn't the one being asked.

### Rules that keep the learning yours

1. **Try first.** Spend real effort on an exercise before asking for help: at least fifteen to twenty minutes, or until you can say exactly where you're stuck. The struggle is where the learning happens.
2. **Ask for explanations, not answers.** *"Why does my query return 21 rows instead of 19?"* teaches you something. *"Write the query for exercise 14"* teaches you nothing.
3. **Check everything against a source you trust.** Assistants can be fluent and wrong at the same time. Section 6.4's method is how you check: find the official page and read the exact rule. A good test: ask an assistant what your phone plan does when you pass your daily data limit, then check the plan's own page.
4. **Never paste data you don't own.** Company data, customer names, invoices, and passwords don't belong in a chat with an outside service unless your employer has explicitly approved that tool for that data (Chapter 2, section 2.9, goes deeper). Practice data like Riverstone's is fine.
5. **Explain it back.** After the assistant helps, close the chat and explain the idea in your own words, or redo the exercise from a blank page. If you can't, you haven't learned it yet.
6. **Use it as a tutor, not a crutch.** Good requests: *"Quiz me on percentage points versus percent change"*, *"Give me a harder version of this exercise"*, *"Explain this error message; don't fix it"*.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Planning with the hours you wish you had | behind by week three; the plan quietly abandoned | Plan with last week's real hours and section 6.1's table |
| Doubling the hours to catch up after a missed week | a missed week becomes a missed month | Move the plan back a week, review once, start the next section |
| Installing every tool now "to get it out of the way" | forgotten passwords and out-of-date versions by the time you need them | Install each tool at the start of the chapter that first uses it |
| Trusting a tutorial or AI over the official source | answers that differ, unexplained | Check the official page, for the right date or version |
| Letting an AI assistant do the exercises | you can follow solutions but can't write them | Try first; ask for explanations; redo from a blank page |
| Reading answers before attempting exercises | answers "make sense" but skills don't stick | Write something first, always |

---

## In the real world: Meera makes a plan

Meera Iyer has done analyst work for months without the title: the customer counts in Chapter 1, the January reconciliation in Chapter 3, the board slide in Chapter 4. Along the way she has picked up some spreadsheet formulas and a little SQL on the job. Now she wants to go further: to learn it properly, from the ground up, and fill the gaps she knows are there. She has two computers to do it with. Neither is ideal.

**Her work laptop** runs Windows 11 and is locked: she can't install software. **Her home laptop** is a MacBook Air from 2020 with 8 GB of memory.

**1. Which tool lives where.** She reads section 6.3 and makes a list. She doesn't install anything today; she decides which tools will live on which computer when she reaches them. The Mac can run everything except Power BI Desktop and Power Pivot. The work laptop is where Power BI would be most useful, since the company already uses Microsoft 365. So: the book's tools go on the Mac at home, each at the start of its chapter; Power BI Desktop goes on the work laptop, if IT agrees. She puts a reminder in her calendar to ask IT two weeks before she reaches Chapter 16, with the request already written: *"I'd like to install Power BI Desktop from the Microsoft Store for learning and for building sales reports. It doesn't need admin rights. I won't connect it to any company data without approval."*

**2. The 8 GB question.** 8 GB is enough to start. When the Mac slows down later, with a database app, an editor, twenty browser tabs, and a video call all open, the fix will cost nothing: close what she isn't using while studying.

**3. The hours.** She has about 6 hours a week: an hour on three weekday evenings after work, and three hours on Sunday morning. Ninety days is about 13 weeks, so 6 × 13 = 78 hours. She adds up the *Time needed* lines from Chapter 7 onward, using the high end of each range so that one slow week doesn't break the plan:

| Chapters | Hours (high end) | Running total |
|---|---|---|
| 7, 8 (with its project), and 9 | 3 + 7 + 3 = 13 | 13 |
| 10 | 22 | 35 |
| 11 | 43 of its 45 hours | 78 |

She writes her first 90 days in `notes/plan.md`. By day 30, about 26 hours: Chapters 7 to 9 and more than half of Chapter 10. By day 60, about 51 hours: about a third of the way through Chapter 11 (16 of its 45 hours). By day 90, 78 hours: Chapter 11 all but finished, with 2 of its hours left. At the top of the plan she writes the whole path, from the job-ready row of section 6.1: 394 to 488 hours, which at 6 hours a week is 15 to 19 months. At work, she'll rebuild the January reconciliation from Chapter 3 in a spreadsheet as her month 2 practice project, using the practice data rather than company files, so nothing sensitive leaves the company's systems.

**4. The AI rule.** She sets herself one rule, taped to the edge of her screen: *"Try for 20 minutes. Ask why, not what. Never paste Riverstone's real data."*

She matched tools to computers without installing anything yet, turned hours into dates with arithmetic, and wrote a plan for her real week, not an ideal one.

---

## Project: plan your route and your first 90 days

**Goal:** a study plan you can keep, built from arithmetic, not hope.

### Tools you'll need

- **A notebook or a notes app** for your plan (`notes/plan.md`) and your study log. A plain text file is enough.
- **A calendar**, paper or on your phone, for your study sessions as named appointments.
- **Each chapter's *Time needed* line**, which is where the hours in section 6.1 come from.

**Step 1. Count your hours.** Write down the hours you really studied, or could have studied, last week. Using section 6.1's table, work out how many weeks the job-ready path takes at that pace, and the month you expect to finish Part 2. Show your division.

**Step 2. Put your rhythm in a calendar.** Adapt Figure 6.1 to your hours and your days, and put each session in your calendar as a named appointment for the next four weeks.

**Step 3. Set up your folder.** Create the `analyst-to-architect` folder described in "How to Use This Book", with `companion/`, `work/`, and `notes/` inside it, and download the companion files into `companion/` (Appendix E gives the address).

**Step 4. Write your AI rule.** One or two lines, like Meera's, somewhere you'll see them.

**Step 5. Read one official page.** Pick one rule that affects you (your phone plan's data limit, a bank fee) and find its official page. Write down the exact rule, one example, one exception, and the date or version (section 6.4).

**Step 6. Match tools to chapters.** Using section 6.3, write which chapter you'll install each tool in, and on which computer.

**Step 7. Write your 90-day plan** in `notes/plan.md`:

- how many hours a week you can study, and on which days and times;
- which chapters you'll finish by day 30, day 60, and day 90, counted from the *Time needed* lines;
- one practice project for each month, using practice data;
- your rule for using AI assistants;
- what you'll do when you miss a week.

**Step 8. Start your study log** with today's entry.

**Deliverable:** `notes/plan.md` with your hours calculation, your 90-day plan, your tool-and-computer list, and your AI rule; your calendar with the next four weeks booked; and your notes on one official page.

---

## Recap

- **The book's hours are known.** Parts 0 to 2, the job-ready path, are 394 to 488 hours; the whole book is 957 to 1,193. At 6 hours a week, job-ready is 15 to 19 months.
- **Divide to plan.** Weeks = hours ÷ your hours a week. Use the hours you really have. Chapter hours are reading-and-exercise hours; fluency takes more practice on top.
- **A rhythm finishes books.** Short regular sessions, one longer project session, and a weekly review from memory. A missed week moves the plan back; it never doubles the load.
- **You don't need a high-end computer.** 8 GB of memory is enough to start, 16 GB is comfortable. Power BI Desktop and Power Pivot are Windows only; Chromebooks cover spreadsheets and online SQL practice, not Python or Power BI.
- **Each tool arrives in the chapter that first uses it:** a spreadsheet in Chapter 10, the databases in 12, Power BI in 16, Python in 17, and Git in 26. Nothing needs installing before then.
- **Official sources settle disagreements.** Go in with a question and find the exact rule, every word, an example, the exceptions, and the date or version.
- **AI assistants are tutors, not substitutes:** try first, ask why, check against sources, never paste data you don't own, and explain it back.
- **Attempt every exercise before reading its answer**, and redo the ones you missed.

---

## Key terms

study hours · job-ready path · weekly rhythm · review from memory · study log · study plan · RAM (memory) · tool timeline · official documentation · AI assistant

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I know how many hours the job-ready path takes, and how many weeks that is at my real weekly hours.
- [ ] My finish date comes from arithmetic, not hope.
- [ ] I have a weekly rhythm in my calendar, and I know what I'll do when I miss a week.
- [ ] I know whether my computer can run each tool, and I have a plan for any it can't.
- [ ] I know which chapter I'll install each tool in.
- [ ] I can find the exact rule, an example, the exceptions, and the date on an official page.
- [ ] I have rules for using AI assistants that keep the learning mine, and I never paste data I don't own.
- [ ] I have a written 90-day plan.
- [ ] I attempt exercises before reading the answers.

---

## Exercises

### Warm-up

1. For each computer, say which chapters you could do on it, and what the owner should do about the rest: (a) a Windows 11 laptop with 8 GB of memory; (b) a MacBook with 16 GB of memory; (c) a Chromebook; (d) a locked-down work laptop running Windows 11.
2. Sort these requests to an AI assistant into "helps you learn" or "does the learning for you", and rewrite the ones that don't help: (a) "Solve Chapter 4, exercise 6." (b) "Explain why averaging monthly growth rates overstates growth." (c) "My query returns 21 rows instead of 19. What kinds of mistake cause extra rows?" (d) "Write my 90-day plan."
3. Without looking back, name the chapter in which you'll install each of these: a spreadsheet, a database, Power BI Desktop, Python, and Git. Then check your answers against section 6.3.

### Core

4. You can study 5 hours a week. Adapt Figure 6.1's weekly rhythm to 5 hours, keeping reading, exercises, review, and project work. Then use section 6.1's table to estimate how long the job-ready path would take at that pace.
5. Your company uses a customer list with names, phone numbers, and outstanding balances. You want an AI assistant's help writing a formula that flags overdue customers. Describe how you'd get the help without sharing the real data.
6. Using the table in section 6.1 and the hours you really studied last week, write the month you expect to finish Part 2. Show your division.
7. Find the official page for one rule that affects you (your phone plan's data limit, a bank fee) and write down the exact rule, one example, one exception, and the date or version.

### Stretch

8. Write a first version of your 90-day plan using the checklist in the project, with specific chapters for days 30, 60, and 90, and a plan for a missed week.
9. A friend plans to install all five groups of tools this weekend "to get it out of the way". Using section 6.3, give two reasons to wait, and one useful thing they could do this weekend instead.

### Think about it (no calculation needed)

10. Why does this book recommend free tools, even though many companies use paid ones? What might you still need to learn on the job?
11. A friend says, "I'll skip the exercises and read the answers; it's faster." What would you tell them, using "How to Use This Book"?
12. When is it reasonable to ask an AI assistant for a complete answer, rather than an explanation? Give one example where it's fine and one where it isn't.

---

## Answers

**1.** (a) Every chapter, including Power BI Desktop in Chapter 16; 8 GB is enough to start, and closing unused apps helps. (b) Every chapter except the Power BI parts of Chapter 16 and the Power Pivot section of Chapter 11; for those, run Windows 11 in a virtual machine, or use a Windows computer at work or college. (c) Parts 0 and 1, the spreadsheet chapters with Google Sheets or Excel for the web, and some early SQL practice on online practice sites; plan to use a laptop before the Python chapters and for the databases and Power BI. (d) Parts 0 and 1 straight away, since they need no software; for later chapters, nothing until IT approves. Ask for Power BI Desktop from the Microsoft Store (no admin rights needed) and for the other tools as you reach their chapters, and meanwhile use a home computer or the web tools with practice data.

**2.** (a) Does the learning for you. Better: *"I got a different answer for Chapter 4, exercise 6. Here's my working; where did my reasoning go wrong?"* (b) Helps you learn. (c) Helps you learn. (d) Does the planning for you. Better: *"Here's my 90-day plan and my available hours. What's unrealistic about it?"*

**3.** A spreadsheet in Chapter 10; the databases (PostgreSQL and DBeaver, with MySQL optional) in Chapter 12; Power BI Desktop in Chapter 16; Python, with VS Code and Jupyter, in Chapter 17; Git in Chapter 26.

**4.** One way: Monday 1 hour reading, Wednesday 1 hour exercises, Friday 30 minutes review from memory, Saturday 2 hours project, Sunday 30 minutes redoing missed exercises and planning: 1 + 1 + 0.5 + 2 + 0.5 = 5 hours. The job-ready path is 394–488 hours; 394 ÷ 5 = 78.8, about 79 weeks, and 488 ÷ 5 = 97.6, about 98 weeks. That's 79–98 weeks, or about 18 to 23 months (79 × 12 ÷ 52 = 18.2; 98 × 12 ÷ 52 = 22.6).

**5.** Describe the structure, not the data: *"I have a table with a customer name column, a due date column, and a balance column. How do I flag rows where the due date is before today and the balance is above zero?"* Or build a small made-up sample (three fake customers with invented numbers) and share that. Test the formula on the fake data, then apply it to the real file on your own computer. If your company has approved an AI tool for internal data, follow its rules instead.

**6.** Answers vary. A worked example: last week you studied 5 hours, and you've finished Chapters 1 to 6. What's left is Chapters 7 to 9 (9–13 hours, from their *Time needed* lines) plus Part 2 (367–451 hours): 376–464 hours. 376 ÷ 5 = 75.2, about 75 weeks; 464 ÷ 5 = 92.8, about 93 weeks. In months, 75 × 12 ÷ 52 = 17.3 and 93 × 12 ÷ 52 = 21.5: about 17 to 21 months. If you start Chapter 7 in October, you'd finish Part 2 between March and July of the year after next. A good answer shows the division and gives a range, not a single hopeful date.

**7.** Answers vary. A complete answer names the rule exactly as the page does (for example, "Daily data: 2 GB"), gives one example worked from the page (what happens on a day you use 2.5 GB), quotes one exception or piece of small print (for example, that unused data doesn't carry forward, or that roaming is charged separately), and records the page's "last updated" date or the plan's name and version.

**8.** Answers vary. A good plan names specific hours ("Tuesday and Thursday, 8–9 p.m.; Saturday, 9–11 a.m."), specific chapters for each checkpoint, counted from the *Time needed* lines as Meera did, one project a month on practice data, an AI rule, and a concrete plan for a missed week ("move the plan back a week; do one review session; start the next section").

**9.** Reasons to wait: a tool installed months early has usually been updated by the time it's used, so the versions and the steps may no longer match; problems are much easier to fix when the chapter in front of you explains what the tool is for; and passwords set months before they're needed get forgotten. Something useful instead: work through this chapter's project (count the hours, book the sessions, set up the folder and download the companion files), and start Chapter 7.

**10.** Nobody is locked out by cost, and PostgreSQL, MySQL, Python, and Git are widely used at work anyway. The ideas transfer: most SQL runs elsewhere, and Power BI's concepts map to other tools such as Tableau and Looker. On the job you may still need to learn a company's own data systems, its BI tool, its data definitions, and its security rules.

**11.** Reading answers you haven't attempted feels like learning because the answers make sense, but it doesn't build the skill of producing them. The exercises are where most of the learning happens, especially the core group. Suggest a compromise: attempt every warm-up and core exercise, even partially, before reading its answer, and redo the missed ones at the end of the week.

**12.** It's reasonable when the task isn't the skill you're trying to learn, or when you already understand it and are saving time, and you'll check the result. Fine: asking for a list of keyboard shortcuts for an app you use, or for a first version of an IT request that you then edit. Not fine: asking for the answer to a SQL exercise while you're learning SQL, because producing that answer is exactly the skill you need.

---

## Where this leads

- **Chapter 7, The Data Landscape,** and **Chapter 8, The Career Tree,** show where the skills you're planning for lead, and which roles use which tools.
- **Chapter 9, How Expertise Actually Forms,** explains the learning science behind section 6.2 (practice, review from memory, and feedback), and why chapter hours are not fluency hours.
- **The chapters that bring each tool:** Chapter 10 (a spreadsheet), Chapter 12 (the databases and DBeaver), Chapter 16 (Power BI Desktop), Chapter 17 (Python, VS Code, and Jupyter), and Chapter 26 (Git, and AI assistants in a professional setting). Each starts by installing its tool.
- **Chapter 83, The Long Game,** returns to the same hours at the end of the book, and to the pace that survives a bad month.
- **Appendix B** gathers every install step in one place.
- **Interview preparation:** Chapter 81 (behavioral, HR, and offer conversations) covers how to talk about how you learned and what you've built, and Chapter 68 explains how data hiring works.
