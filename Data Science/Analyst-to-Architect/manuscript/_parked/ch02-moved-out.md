# Parked: text moved out of Chapter 2 (Part 0 + I build, 28 Sep 2026)

Not a book chapter and not built. Each block below was removed from Chapter 2 by the Part 0/I fix instructions (table "Chapter 2", items 2.1, 2.7, 2.9, 2.10, 2.11, 2.15) and is kept here verbatim, labelled with its destination. The destination part's build pulls the block into its chapter (rewritten there to the book's code-cell standard where it contains program output), then deletes it from this file.

---

## Block 1 → Ch 17 (Python from Zero), its section on numbers (fix 2.1, finding 0.5)

**Landed** in Ch 17 §17.3 (0.1 + 0.2 and the exact `Decimal` version) (Part 2/3 build).

Removed from Ch 2 §2.1 "How numbers are stored". In Ch 17 the result must be produced by a code cell the reader can see and run (`0.1 + 0.2`, then the exact-decimal version with `decimal.Decimal`), with the real output pasted and each line explained. Ch 2 now says it in plain words only.

> Whole numbers are stored exactly, as binary. Numbers with decimals are trickier. Most programs store them in a format called **floating point**, which is fast but can only store most decimals *approximately*. Ask Python to add 0.1 and 0.2:
>
> ```
> 0.30000000000000004
> ```
>
> The tiny error is invisible in most charts, but it's why `0.1 + 0.2 = 0.3` can come out as *false* in a program, and why financial systems store money in exact decimal types instead (you'll meet `NUMERIC` in Chapter 12). Asked to add the same numbers as exact decimals, Python gives `0.3`.

---

## Block 2 → Ch 49 (Storage, Warehouses & Lakehouses) (fix 2.7, finding 0.6)

**Landed** in Ch 49 §49.2 "The same test across formats, with timing" (the test re-run on the chapter's sensor data; the old 500,000-row numbers could not be reproduced) (Part 5 build).

Removed from Ch 2 §2.5: the longer Parquet explanation, the 500,000-row format test and the compression numbers from that test. Ch 2 keeps a short Parquet paragraph, Figure 2.2 (row vs column storage) and a short Compression note (lossless vs lossy). Ch 2's §2.2 sentence that pointed to the test file was also removed (last paragraph of this block). The timings were measured on "a small two-processor cloud computer"; re-run them in Ch 49 with the code shown before reusing the numbers.

> **Parquet** is a format built for analyzing large datasets, and it's the standard format of cloud data platforms (Part 5). You can't read it as text: the file begins with the four letters `PAR1`, and the rest is compressed binary data. What makes it special is how it's laid out.
>
> A CSV stores **row by row**: order 1's date, customer, product, quantity; then order 2's. Parquet stores **column by column**: all the dates together, then all the customers, then all the quantities. Two big benefits follow. To total the quantity column, a program reads only that column and skips the rest. And values in one column are similar to each other (a column of dates, a column of product IDs), so they **compress** very well. Parquet also stores each column's **type**, so dates come back as dates.
>
> For four orders, Parquet's advantages are invisible: the file is **4,872 bytes**, bigger than the CSV, because of the information it stores about its own structure. Its advantages appear at scale.
>
> ### The same test at scale
>
> To see the differences properly, the same 500,000 sales lines, with 8 columns, were saved in each format and read back with Python on a small two-processor cloud computer:
>
> | Format | File size | Time to read everything | Time to read one column |
> |---|---|---|---|
> | CSV | 24.1 MB | 0.23 s | 0.10 s |
> | CSV, compressed with gzip | 4.7 MB | — | — |
> | JSON | 82.6 MB | 1.43 s | — |
> | Excel (.xlsx) | 18.3 MB | 31.4 s | — |
> | **Parquet** | **4.3 MB** | **0.02 s** | **0.003 s** |
>
> Exact times depend on the computer, but the pattern holds everywhere. **Parquet was the smallest file, and about ten times faster than CSV to read in full.** Excel took more than a hundred times longer than CSV to read, because every cell has to be unpacked from zipped XML. JSON was the largest, because it repeats all eight column names on every one of the 500,000 rows.
>
> ### Compression
>
> **Compression** makes files smaller by writing repeated patterns more efficiently. Zipping the CSV cut it from 24.1 MB to 4.7 MB, because a column like `status` repeats the same few words half a million times.
>
> (From the old answer 12:) Ledgers compress very well anyway, because columns such as status, product, and customer repeat the same values many times: the 24.1 MB CSV in section 2.5 zipped to 4.7 MB with nothing lost.
>
> (From §2.2:) Riverstone's test file of 500,000 sales lines, which you'll meet in section 2.5, is 24 MB as a CSV.
>
> (From Figure 2.1, MB row:) 500,000 sales lines as CSV: 24 MB

Also removed from the "Choosing a format" table in §2.5: the column "Opens in Excel?" (CSV: yes (import carefully) · Excel: yes · JSON: with Power Query · XML: with Power Query · PDF: no · Parquet: no (Power BI and Python can read it)). Destination: Ch 49 or Ch 18 if wanted.

---

## Block 3 → Ch 52 (The Cloud, Containers & Infrastructure as Code) (fix 2.10, finding 0.6)

**Landed** in Ch 52 §52.1 (the IaaS/PaaS/SaaS table, with an "At Riverstone" column) (Part 5 build).

Removed from Ch 2 §2.7 "The cloud". Ch 2 now keeps two sentences and names SaaS only. The term **region** (in the paragraph after the table, which stays in Ch 2 unbolded) left Ch 2's key terms.

> Businesses rent at three levels, depending on how much they want to manage themselves:
>
> | Level | You rent… | You still manage… | Examples |
> |---|---|---|---|
> | **IaaS** (infrastructure as a service) | virtual computers, storage, and networks | the operating system, software, and data | a virtual server to run your own database |
> | **PaaS** (platform as a service) | a ready-to-use platform, such as a managed database | your data and how you use it | a cloud PostgreSQL service that handles backups and updates for you |
> | **SaaS** (software as a service) | a finished application, used through a browser | your data and your settings | Gmail, Google Drive, Microsoft 365, CRM and accounting software |

---

## Block 4 → Ch 18 §18.14 (Calling an API) (fix 2.9, finding 0.6)

**Landed** in Ch 18 §18.14 (its status-code table; the demo-API wording became Ch 18's own `api_demo.py`) (Part 2/3 build).

Removed from Ch 2 §2.8's status-code table. Ch 2 keeps 200, 401, 404, 429 and 500, and the "first digit" rule.

> | Code | Meaning | What to do |
> |---|---|---|
> | `201 Created` | a new record was created | note the new record's ID |
> | `400 Bad Request` | the request is malformed | check what you sent |
> | `403 Forbidden` | you're recognized, but not allowed to do this | ask for the right permission |

Also from §2.8 (fix 2.8, 2.13, R1): Ch 2 no longer names the `curl` tool or `api_demo.py`. The removed wording, for Ch 18 to reuse when the reader runs the demonstration API: "The companion files include a tiny demonstration API for Riverstone that runs on your own computer (Appendix E)." · "Here's the full reply to a request for order 5009, sent with the `curl` command-line tool:" · Tools bullet: "and `api_demo.py`, the demonstration API used in section 2.8, which you'll run yourself in Chapter 18."

---

## Block 5 → Ch 45 (Data Ingestion & Integration), where hashes detect changed files (fix 2.11, finding 0.5)

**Landed** in Ch 45 §45.5, "What a hash is" (Part 5 build).

Removed from Ch 2 §2.9 "Integrity checks: fingerprints for files". Ch 2 keeps the idea in three sentences with the fingerprints cut to 12 characters and doesn't name SHA-256. In Ch 45 the hashes must be produced by code the reader can see.

> How do you know a file hasn't been changed, even by one character? Computers calculate a **hash**: a fixed-length "fingerprint" of the data. The same data always gives the same hash, and the smallest change gives a completely different one. Here are the SHA-256 hashes of two payment instructions that differ only in the order of two digits:
>
> ```
> Text:    Pay Rs 14,700 to Riverstone Supplies
> SHA-256: f4251ff3fb7191f7e79677f3b1871db06c0935c3cc08164496995f1f909f6f71
>
> Text:    Pay Rs 17,400 to Riverstone Supplies
> SHA-256: 9d2f842c50110e140abd578e7e8460d1f6f2bbca7eba341ce1e5bee43566d0fa
> ```
>
> Nothing about the second fingerprint resembles the first. Software uses hashes to check that downloads arrived undamaged, that backups match the original, and that passwords are stored safely (systems store a hash of your password, not the password itself). Data pipelines use them to detect whether a file has changed since yesterday (Chapter 45).

---

## Block 6 → no fixed destination; offer to Ch 34 (Linux and networking) (fix 2.15, finding 0.6)

Removed from Ch 2 §2.7 with the key term "packet" (fix 2.15 removes the term, so its paragraph went too).

> Data on the internet travels in small **packets**, each finding its own route, then reassembled at the other end. You never see that, but it's why a large file arrives in pieces and why a slow connection affects everything at once.

---

## Block 7 → no destination needed (fix 2.2, finding 0.6); kept for the record

Removed from Ch 2 §2.1. Ch 2 keeps one sentence on lossy compression of photos and music in §2.5. The old exercise 12 and its answer were rewritten (fix 2.14).

> ### How pictures and sound are stored
>
> A digital photo is a grid of tiny dots called **pixels**. Each pixel stores three numbers, for how much red, green, and blue light it has, usually one byte each. A 12-megapixel phone photo has 12 million pixels, so before compression it takes 12,000,000 × 3 = **36 MB**. The file on your phone is usually only a few megabytes, because it has been **compressed** (section 2.5). Sound is stored in a similar way: thousands of measurements of the sound wave every second.
>
> (Old exercise 12:) A 12-megapixel photo is 36 MB before compression, but the file on the phone is 3 MB. Could a sales ledger be compressed the same way? Explain using the terms lossless and lossy.

Also removed from §2.2 (fix 2.3), replaced by a three-sentence Watch out box without binary unit names:

> ### Why your 1 TB drive shows 931 GB
>
> There are two ways to count, and both are in use:
>
> - **Decimal (the SI standard):** 1 KB = 1,000 bytes, 1 MB = 1,000,000 bytes, 1 GB = 1,000,000,000 bytes. Drive makers and most network speeds use this.
> - **Binary:** 1 "KB" = 1,024 bytes (2¹⁰), 1 "MB" = 1,024 × 1,024 bytes, and so on. Windows, and some older software, count this way.
>
> The binary units have their own proper names, **KiB, MiB, GiB** (kibibyte, mebibyte, gibibyte), though few people use them in conversation. The difference grows with size. A drive sold as 1 TB holds 1,000,000,000,000 bytes. Divide by 1,024³ (the binary gigabyte) and you get **931.3**, which is the "GB" Windows displays. No space is missing; it's the same number of bytes counted in a different unit.
