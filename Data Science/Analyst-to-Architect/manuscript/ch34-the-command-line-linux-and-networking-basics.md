# Chapter 34. The Command Line, Linux & Networking Basics

*Part 3 — Advanced Analytics & Analytics Engineering*

> **Chapter at a glance**
>
> **You will learn to:** combine small tools with pipes and redirection to answer questions in seconds · search text with `grep`, and count and summarize it with `wc`, `sort`, `uniq`, `cut`, and `awk` · find files by name, age, and size · read and set file permissions · use environment variables and understand `PATH` · write a shell script that takes arguments, fails safely, and returns a meaningful exit code · connect to a server with SSH keys and copy files to it · explain IP addresses, DNS, ports, and HTTP, and test a web server with `curl`.
>
> **Before you start:** Chapter 26, section 26.0 (the terminal: moving around, making and copying files, reading a command, `&&`, environment variables, and `echo $?`) and Chapter 2 (files, formats, and what an API is). Chapter 20's scheduled jobs are useful background, and Chapter 14's regular expressions help with `grep -E`.
>
> **Time needed:** 9–12 hours over two weeks, in three sittings (sections 34.0–34.4; 34.5–34.7; 34.8–34.9 and the project), most of it typing commands rather than reading.
>
> **Tools:** a terminal running **bash**. On Windows, **WSL** (the Windows Subsystem for Linux), which section 34.1 installs; Git Bash from Chapter 26 is enough for sections 34.0 to 34.4 and 34.7, but not for permissions (34.5), `sudo`, `ss`, or the SSH server. On macOS, the Terminal app with `bash` typed first (section 34.1). On Linux, any terminal. Windows and macOS differences are flagged where they matter.
>
> **Practice data:** the companion folder `ch34/`, which builds a `practice/` folder from Riverstone's 2025 sales: 61 daily export files for November and December 2025, reference lists, and the daily summary job's log, next to the whole year's sales lines in one file (`sales_lines_2025.csv`). Every command in this chapter was run, and every output shown is the real output.

---

## Why this matters

You've been typing commands since Chapter 17: `python` and `pip` there, and `git` in Chapter 26. The rest of the book adds more: `uv` and `pytest` (Chapter 29) are commands, and so is `dbt` (Chapter 32). Scheduled jobs (Chapter 20) are commands the machine runs at 3 a.m. with nobody watching. Cloud servers and containers (Chapter 52) have no desktop at all: a terminal is the only way in. Chapter 26 gave you enough terminal to use Git. This chapter turns "I can type the command I was given" into "I can find my way around a machine I've never seen".

There's a second reason, and it shows up sooner. A surprising share of daily data work is faster in the terminal than anywhere else:

- *"How many rows are in these 61 files, and which ones are empty?"* One command.
- *"The pipeline failed last night. What did it say?"* `grep ERROR` on the log, in the time it takes a log viewer to load.
- *"This 2 GB CSV crashes Excel and takes five minutes to load in pandas. I only need the rows for Pune."* `grep Pune` finishes before pandas has started.
- *"Which of these 400 files contains the customer id we're arguing about?"* `grep -rl`.

You don't need to memorize the manual. You need about thirty commands, a clear picture of how they fit together, and the confidence to look up the rest.

---

## In plain English

**The terminal is a kitchen counter with a lot of small, sharp knives.**

A graphical program is a food processor: one machine, a lid, a few buttons, and whatever it does is what you get. The terminal's tools each do one small thing, and you connect them. One tool finds lines; one counts them; one sorts them; one adds up a column. Alone they're almost too simple to be worth having. Connected with **pipes**, they answer questions that no single program on your machine can answer.

The counter has a few other fixtures:

- **A current folder.** Every command runs somewhere. Half of all early mistakes are "I was in the wrong place".
- **Three channels.** Every command takes **input**, produces **output**, and has a separate channel for **errors**, so you can keep the results and read the complaints separately.
- **A verdict.** Every command ends with a number: 0 means it worked. That number is how scheduled jobs know whether to raise an alarm.
- **Labels on the drawers.** **Environment variables** are named notes the shell hands to every program it starts: where to find things, which database to use, your API key.
- **A telephone line to other kitchens.** **SSH** gives you the same counter on a machine in another building, or another country.

---

## 34.0 Where Chapter 26 left you

Chapter 26, section 26.0, taught the terminal you needed for Git. This chapter starts from there. Here is that section on one screen; every line should look familiar.

| Command or key | What it does | Example |
|---|---|---|
| `pwd` | print the folder you're in | `pwd` |
| `ls`, `ls -a` | list what's here; `-a` includes hidden names that start with a dot | `ls -a` |
| `cd` | move into a folder; `..` is the folder above; `~` is your home folder | `cd sql`, `cd ..`, `cd ~` |
| `mkdir -p` | make a folder, with any missing folders on the way | `mkdir -p sql/reports` |
| `touch` | make an empty file | `touch notes.txt` |
| `cp`, `mv` | copy; move or rename | `cp .env.example .env` |
| `rm` | delete, with no recycle bin and no undo | `rm notes.txt` |
| `cat`, `less` | print a file; page through a long one (`q` quits) | `cat .gitignore` |
| `echo "…" > file` | write text into a file, replacing what was there | `echo "scratch" > notes.txt` |
| Tab, ↑, `Ctrl+C` | complete a name; bring back the last command; stop a command | |
| `&&` | run the next command only if this one worked | `cd sql && ls` |
| `export NAME=value` | set an environment variable for this terminal | `export REPORT_MONTH=2026-01` |
| `echo $?` | the exit code of the last command: 0 means it worked | `echo $?` |

If any of these feels unfamiliar, redo the drill at the end of section 26.0 before going on: the rest of this chapter builds on every line.

Three more keys, now that you'll be typing more. `history` lists the commands you've typed, numbered. `Ctrl+R` searches them: press it, type a few letters of an old command, and press Enter to run it again. `Ctrl+D` means "no more input"; in a terminal on its own, it closes the shell, like typing `exit`.

One way of printing commands is new here. A long command doesn't fit on one line of this book, so it's split with a **backslash** at the very end of a line:

```
$ curl --silent --output /dev/null \
    --write-out "%{http_code}\n" \
    http://127.0.0.1:8034/health
```

A backslash as the last character of a line means "the command continues on the next line". You can type it exactly as printed, pressing Enter after each backslash, or type it all on one line without the backslashes; bash runs the same command either way.

**What's new in this chapter:**

- **Pipes and redirection:** connecting small tools so the output of one becomes the input of the next (section 34.2).
- **Text tools:** `head`, `tail`, `find`, `grep`, `wc`, `sort`, `uniq`, `cut`, and `awk`, which count, search, and add up files without opening them (sections 34.3 and 34.4).
- **Linux itself:** permissions, `sudo`, and `PATH`, which decide who can do what and which program a name runs (sections 34.5 and 34.6).
- **Shell scripts:** saving commands in a file that takes arguments and fails safely (section 34.7).
- **Other machines:** SSH, and the four networking ideas behind every connection (sections 34.8 and 34.9).

---

## 34.1 Setting up for this chapter

Chapter 26's terminal was enough for Git. This chapter needs a real Linux shell, because half of it is about how Linux itself works.

| Your computer | What to use for this chapter | Why |
|---|---|---|
| Linux | your usual terminal (`Ctrl+Alt+T` on most desktops) | it already runs **bash** |
| macOS | the Terminal app, then type `bash` and press Enter | Terminal starts **zsh**, which differs from bash in a few places this chapter uses. macOS includes an older bash, 3.2, which runs every script here |
| Windows | **WSL**, the Windows Subsystem for Linux (steps below) | gives you a real Ubuntu Linux inside Windows |
| Windows, for now | Git Bash, from Chapter 26 | fine for sections 34.0 to 34.4 and 34.7; not for permissions (34.5), `sudo`, `ss`, or the SSH server (34.8) |

The **shell** is the program that reads what you type and runs it. Bash and zsh are both shells; this chapter uses bash, the one on almost every Linux server.

### Windows: install WSL

WSL runs a real Linux, Ubuntu by default, next to Windows. Microsoft's instructions ("How to install Linux on Windows with WSL", Microsoft Learn) come down to five steps. They need administrator rights on the computer, and a restart:

1. Open **PowerShell as administrator**: press the Windows key, type *PowerShell*, right-click it, and choose *Run as administrator*.
2. Type `wsl --install` and press Enter. It turns on the Windows features WSL needs and downloads Ubuntu.
3. **Restart** the computer when it finishes.
4. Open **Ubuntu** from the Start menu. The first start takes a minute, then asks you to create a **UNIX username and password**. They are for Linux only and don't need to match your Windows ones. Remember the password: `sudo` asks for it (section 34.5), and nothing on the screen moves while you type it, which is normal.
5. Bring Ubuntu's software list up to date: `sudo apt update`, then your new password.

Two habits make WSL behave. **Work inside your Linux home folder** (`cd ~`), not in your Windows folders: Windows drives appear under `/mnt/c/…`, and there permissions don't behave as Linux expects and everything runs slower (Microsoft recommends the same, in "Working across Windows and Linux file systems"). And **open VS Code from Ubuntu**: with VS Code's **WSL** extension installed, typing `code .` in the Ubuntu terminal opens the current Linux folder in VS Code.

### Build the practice folder

Copy the companion folder `ch34` into your home folder, go into the copy, and run its generator. On macOS and Linux, the companion files are where Chapter 17 put them:

```
# terminal, in your home folder
$ cp -r ~/analyst-to-architect/companion/ch34 ~/ch34

$ cd ~/ch34

$ python3 make_ch34_data.py
practice folder ready: 326 order lines, 23 customers, 61 daily export files
```

`cp -r` copies a folder and everything inside it (`-r` for *recursive*). In WSL, your Windows files are under `/mnt/c/Users/`, so the first command becomes something like `cp -r /mnt/c/Users/Meera/analyst-to-architect/companion/ch34 ~/ch34` (with your Windows user name). The generator is plain Python, so `python3` from Ubuntu or macOS runs it without a virtual environment; on a fresh WSL, `sudo apt install python3` first if `python3 --version` says it isn't there.

Throughout this chapter, `$` marks a line you type and everything after it is the output, as in Chapter 26. Your prompt shows your own name and folder.

---

## 34.2 Pipes, redirection, and exit codes

This is the idea that makes everything else worth learning.

Every command has three channels: **standard input** (where it reads from), **standard output** (where results go), and **standard error** (where complaints go). By default input comes from your keyboard, and both output channels go to the screen. And every command, when it finishes, leaves an **exit code**: 0 for success, anything else for failure.

![A command in the middle, with standard input flowing in from the left, standard output and standard error flowing out to the right as two separate channels, and the exit code below it, 0 for success and anything else for failure](figures/fig34-1-anatomy-of-a-command.svg)

*Figure 34.1 — Every command reads one channel, writes two, and leaves an exit code behind.*

You can point the channels somewhere else:

| Symbol | Meaning |
|---|---|
| `command > file` | send output to a file, replacing it (section 26.0) |
| `command >> file` | append output to the end of a file |
| `command 2> errors.txt` | send only errors to a file |
| `command > out.txt 2>&1` | send output and errors to the same file |
| `command < file` | read input from a file |
| `command1 \| command2` | send command1's output straight into command2: a **pipe** |

The first pipe, and the question from the start of the chapter: how many daily files are there?

```
# terminal, in ~/ch34
$ cd practice

$ ls exports | wc -l
61
```

`ls exports` lists the folder's files, one per line; the `|` sends that list into `wc -l`, which counts lines (*word count*, `-l` for lines) and prints only the count. Neither program knows the other exists; the shell connects them.

```
# terminal, in ~/ch34/practice
$ head -1 exports/orders_2025-12-16.csv > /tmp/header.csv

$ cat /tmp/header.csv
order_id,order_date,customer_id,customer_name,city,segment,product_id,product_name,category,quantity,net_revenue,sales_rep

$ ls missing_folder 2> /tmp/errors.txt

$ cat /tmp/errors.txt
ls: cannot access 'missing_folder': No such file or directory
```

`head -1` prints a file's first line, and `>` saved it in `/tmp`, the system's folder for throwaway files. Notice the third command printed nothing: the error went to the file instead of the screen. That's why a scheduled job writes `>> job.log 2>&1`: everything, results and complaints, ends up in one file with nothing lost. **Order matters** in that last one: redirect the output first, then `2>&1`, which means "send errors wherever output is going now". Written the other way round, `2>&1 > job.log`, the errors still go to the screen.

**`tee`** does both at once: it shows its input on the screen *and* writes it to a file. `-a` appends instead of replacing. Section 34.7 uses it to keep a log of a script's runs.

### Exit codes

The shell keeps the last exit code in `$?`, which section 26.0 printed with `echo $?`. **`test`** checks a condition and says the answer only through its exit code:

```
# terminal, in ~/ch34/practice
$ test -f exports/orders_2025-12-16.csv; echo $?
0

$ test -f exports/orders_2026-01-05.csv; echo $?
1
```

`test -f` asks "is this an existing file?" and prints nothing; the answer is the exit code. The file for 16 December exists (0); the one for 5 January 2026 hasn't been published (1). The `;` runs the second command whatever happened to the first. A scheduler reads exactly this number to decide whether a job failed.

Exit codes also chain commands:

- `command1 && command2` runs the second **only if** the first succeeded (section 26.0).
- `command1 || command2` runs the second **only if** the first failed.
- `command1 ; command2` runs both regardless.

```
# terminal, in ~/ch34/practice
$ test -f exports/orders_2025-12-16.csv && echo "file is there"
file is there

$ test -f exports/orders_2026-01-05.csv || echo "not published yet"
not published yet
```

---

## 34.3 Looking inside files, and finding them

`ls` has a long form that you'll need for permissions in section 34.5:

```
# terminal, in ~/ch34/practice
$ ls
archive
exports
incoming
logs
reference

$ ls -l reference
total 8
-rw-r--r-- 1 meera meera 877 Jan  5  2026 customers.csv
-rw-r--r-- 1 meera meera 259 Jan  5  2026 products.csv
```

- **`ls -l`** is the long form: permissions, owner, group, size in bytes, when it last changed, and the name. Section 34.5 reads it column by column. **`ls -lh`** prints human-readable sizes (`4.0K`, `12M`).
- Options combine: `ls -lha` is `-l`, `-h`, and `-a` together. Most commands also accept long forms (`ls --all`), which are clearer in scripts.
- `cd -` goes back to the folder you were in before the last `cd`, which saves typing when you're switching between two places.

Names are **case-sensitive** on Linux: `Exports` and `exports` are different folders. That's one of the most common surprises when a script written on a Mac or Windows machine runs on a Linux server for the first time.

### Looking inside files without opening an editor

```
# terminal, in ~/ch34/practice
$ head -2 exports/orders_2025-12-16.csv
order_id,order_date,customer_id,customer_name,city,segment,product_id,product_name,category,quantity,net_revenue,sales_rep
10168,2025-12-16,5,Metro Mart,Mumbai,Retail,101,Storage Box 10L,Storage,35,15050.00,Rahul Mehta

$ tail -2 exports/orders_2025-12-16.csv
10170,2025-12-16,21,Kitchen Kraft,Bengaluru,Retail,101,Storage Box 10L,Storage,35,15050.00,Rahul Mehta
10170,2025-12-16,21,Kitchen Kraft,Bengaluru,Retail,104,Food Container Set,Kitchen,35,21700.00,Rahul Mehta

$ wc -l exports/orders_2025-12-16.csv
8 exports/orders_2025-12-16.csv
```

- **`head`** shows the first lines (10 by default), **`tail`** the last. `tail -f somefile.log` *follows* a file as it grows, which is how you watch a job while it runs; `Ctrl+C` stops following.
- **`wc -l`** with a file name prints the count and the name. Eight lines is seven order lines plus the header row.
- **`less`** (section 26.0) can search: inside it, type `/Pune` and Enter to jump to the next match, `n` for the one after, and `q` to quit. Use `less` for anything longer than a screen.

### Wildcards

The shell expands patterns *before* the command runs:

```
# terminal, in ~/ch34/practice
$ ls exports/orders_2025-12-0*.csv
exports/orders_2025-12-01.csv
exports/orders_2025-12-02.csv
exports/orders_2025-12-03.csv
exports/orders_2025-12-04.csv
exports/orders_2025-12-05.csv
exports/orders_2025-12-06.csv
exports/orders_2025-12-07.csv
exports/orders_2025-12-08.csv
exports/orders_2025-12-09.csv

$ ls exports/orders_2025-12-1?.csv | wc -l
10
```

`*` matches any number of characters, `?` matches exactly one, and `[12]` matches either character listed. This is called **globbing**, and it's the shell's work, not the command's: `ls` only ever sees the list of names the shell found.

### Finding files

`find` searches a folder tree by name, age, size, or type:

```
# terminal, in ~/ch34/practice
$ find . -name "orders_2025-12-2*.csv" | sort | head -3
./exports/orders_2025-12-20.csv
./exports/orders_2025-12-21.csv
./exports/orders_2025-12-22.csv

$ find . -type f -size +8k
./logs/report.log
```

- **`find .`** starts at `.`, the current folder, and looks in every folder below it.
- **`-name "…"`** matches the file name against a pattern. The quotes matter: they stop the shell expanding the `*` itself, so `find` gets the pattern.
- **`-type f`** keeps only files (`-type d`, only folders), and **`-size +8k`** keeps those bigger than 8 kilobytes.
- `find` lists files in whatever order it meets them, so `| sort` puts them in order, and `head -3` keeps the first three.

`find . -type f -mtime -1` lists files changed in the last day, which is how you answer *"did the export actually run last night?"*. `find . -name "*.tmp" -delete` cleans up, and is worth running once without `-delete` first, to see what it would delete.

---

## 34.4 Searching and summarizing text

Six small tools cover most data questions. The practice files hold one row per order line, with the same columns you know from the `sales_lines` view: order id, date, customer, city, segment, product, category, quantity, net revenue, and sales rep.

### grep: find lines

```
# terminal, in ~/ch34/practice
$ grep -c "Pune" ../sales_lines_2025.csv
42

$ grep "Food Container Set" exports/orders_2025-12-16.csv
10169,2025-12-16,18,Evergreen Mart,Indore,Retail,104,Food Container Set,Kitchen,30,18600.00,Rahul Mehta
10170,2025-12-16,21,Kitchen Kraft,Bengaluru,Retail,104,Food Container Set,Kitchen,35,21700.00,Rahul Mehta

$ grep -i "sharma" ../sales_lines_2025.csv | head -2
10007,2025-01-24,1,Sharma Hardware,Mumbai,Retail,101,Storage Box 10L,Storage,45,19350.00,Neha Kulkarni
10007,2025-01-24,1,Sharma Hardware,Mumbai,Retail,102,Storage Box 25L,Storage,20,15000.00,Neha Kulkarni

$ grep -rl "Metro Mart" exports | sort | head -3
exports/orders_2025-11-26.csv
exports/orders_2025-12-16.csv
```

**`grep`** prints every line that contains the text you give it. `../sales_lines_2025.csv` is the year's file, one folder up (`..`).

| Option | Meaning |
|---|---|
| `-c` | count matching lines instead of printing them |
| `-i` | ignore case |
| `-v` | show lines that **don't** match |
| `-r` | search a whole folder tree |
| `-l` | print only the names of files that contain a match |
| `-n` | show line numbers |
| `-w` | match whole words only |
| `-q` | quiet: print nothing, only set the exit code |
| `-E` | use extended regular expressions (Chapter 14's patterns) |

The last `grep` found "Metro Mart" in two files, so `head -3` had only two to show.

`grep` also answers through its exit code, like `test` in section 34.2: 0 when it found something, 1 when it didn't. With `-q` it prints nothing at all, which is what a script wants when it only needs the yes or no:

```
# terminal, in ~/ch34/practice
$ grep -q "Mumbai" reference/customers.csv; echo $?
0

$ grep -q "Kathmandu" reference/customers.csv; echo $?
1
```

### wc, sort, uniq, cut: count and group

```
# terminal, in ~/ch34/practice
$ cut -d, -f5 ../sales_lines_2025.csv | tail -n +2 | sort | uniq -c | sort -nr | head -5
     74 Mumbai
     42 Pune
     34 Bengaluru
     28 Delhi
     21 Kochi
```

**How it works**, one stage at a time:

1. **`cut -d, -f5`** takes field 5 of each line, using a comma as the delimiter: the city.
2. **`tail -n +2`** starts from line 2, dropping the header.
3. **`sort`** puts identical cities next to each other, because…
4. **`uniq -c`** collapses *adjacent* identical lines and counts them. Forgetting the `sort` before `uniq` is the classic mistake: it silently gives wrong counts.
5. **`sort -nr`** sorts numerically (`-n`), largest first (`-r`).
6. **`head -5`** keeps the top five.

![Five boxes left to right: cut keeps column five, 327 lines; tail drops the header, 326 lines; sort groups identical cities, 326 lines; uniq -c counts them down to 16 lines, one per city; sort -nr puts the biggest first, with the resulting counts beside them](figures/fig34-2-pipeline-stages.svg)

*Figure 34.2 — A pipeline is five small programs, each reading what the one before it wrote.*

Mumbai leads with 74 order lines, and Pune's 42 matches the `grep -c "Pune"` count above. ✓ That is Chapter 13's "group by city and count" written with five tiny programs instead of one query, and it works on a file that no database has ever seen. How many cities are there? Swap the last three stages for a count of the distinct values:

```
# terminal, in ~/ch34/practice
$ cut -d, -f5 ../sales_lines_2025.csv | tail -n +2 | sort -u | wc -l
16
```

`sort -u` sorts and keeps one copy of each line (*unique*), so `wc -l` counts cities, not order lines.

> **Watch out: `sort` sorts text unless you tell it otherwise.** Without `-n`, `10` comes before `9`, because it compares character by character. And sort order depends on your language settings, which is why, if your counts come out in a different order from the book's, `LC_ALL=C sort` gives the plain byte order that everyone's machine agrees on.

### awk: arithmetic on columns

`awk` reads a file line by line, splits each line into fields, and runs your rules on each one. It's a small language of its own; four steps cover nearly everything an analyst needs. Start by printing one column of one day:

```
# terminal, in ~/ch34/practice
$ awk -F, '{ print $11 }' exports/orders_2025-12-16.csv
net_revenue
15050.00
2300.00
10212.50
18600.00
6887.50
15050.00
21700.00
```

- **`-F,`** sets the field separator to a comma. Fields are then `$1`, `$2`, …, and `$0` is the whole line. Field 11 is `net_revenue`.
- The program is inside single quotes, so the shell passes it to `awk` untouched. **`{ print $11 }`** is an **action**, and with nothing in front of it, it runs on every line, including the header, which is why `net_revenue` is printed first.

Now add the day up, skipping the header:

```
# terminal, in ~/ch34/practice
$ awk -F, 'NR > 1 { total += $11 } END { print total }' exports/orders_2025-12-16.csv
89800
```

- **`NR > 1`** is a **condition** in front of the action: `NR` is the line number (the *number of the record*), so the action runs only from line 2 on.
- **`total += $11`** adds field 11 to a running total. A variable in awk starts at 0 without being declared.
- **`END { … }`** runs once, after the last line: here it prints the total. ₹89,800 is the day's revenue.

Now the whole month, 31 files at once, printed with two decimals:

```
# terminal, in ~/ch34/practice
$ awk -F, 'NR > 1 { total += $11 } END { printf "%.2f\n", total }' exports/orders_2025-12-*.csv
439823.50
```

- **`exports/orders_2025-12-*.csv`** is a wildcard, so awk reads all 31 December files one after another, as if they were one long file.
- **`printf "%.2f\n", total`** prints with a format, like Python's `f"{total:.2f}"` in Chapter 17: `%.2f` means a number with two decimals, and `\n` starts a new line (plain `print` adds one for you; `printf` doesn't).

The total is right, but only by luck. Group the same month by category and the luck runs out:

```
# terminal, in ~/ch34/practice
$ awk -F, 'NR > 1 { revenue[$9] += $11 } \
    END { for (c in revenue) printf "%-12s %12.2f\n", c, revenue[c] }' \
    exports/orders_2025-12-*.csv | sort -k2 -nr
Storage         220363.50
Kitchen         142180.00
Industrial       77280.00
category             0.00
```

- **`revenue[$9] += $11`** uses an **associative array**, awk's version of a Python dictionary: one running total per category (field 9), built in one pass.
- **`for (c in revenue)`** loops over the array's keys, in no particular order, hence the `sort` at the end.
- **`%-12s`** prints text left-aligned in 12 characters, and **`%12.2f`** a number with two decimals, right-aligned in 12, so the columns line up.
- **`sort -k2 -nr`** sorts on the 2nd whitespace-separated field (`-k2`, the revenue), numerically, largest first.

The first three lines are right; the fourth is a bug worth seeing: an extra line, `category 0.00`. Each of the 30 files after the first starts with a header row, and `NR > 1` skipped only the first one, because **`NR` counts lines across all the files**. So each later header's column 9, the word `category`, became a key, and its revenue, the word `net_revenue`, counted as 0. That's also why the monthly total above was right: awk treats text as 0 in arithmetic, which is exactly the kind of silent nonsense to watch for. **`FNR`** restarts at 1 in each file, so `FNR > 1` skips all 31 headers:

```
# terminal, in ~/ch34/practice
$ awk -F, 'FNR > 1 { revenue[$9] += $11 } \
    END { for (c in revenue) printf "%-12s %12.2f\n", c, revenue[c] }' \
    exports/orders_2025-12-*.csv | sort -k2 -nr
Storage         220363.50
Kitchen         142180.00
Industrial       77280.00
```

Both numbers reconcile with what you already know. December's total, ₹4,39,823.50, is the December 2025 figure of Chapters 10, 11, and 17, and the three categories add up to it: ₹2,20,363.50 + ₹1,42,180.00 + ₹77,280.00 = ₹4,39,823.50. ✓

> **Watch out: these tools don't understand CSV, only text.** `cut -d,` and `awk -F,` split on every comma, including one inside `"Sharma Hardware, Mumbai"`. The practice files have no commas inside fields, so this works, and much real data is the same. When fields may contain commas, quotes, or line breaks, use a real CSV tool: `csvkit` and `xsv`/`qsv` are command-line tools that parse CSV properly, and pandas (Chapter 18) is right there. Use the shell for a quick look and a quick count; use a parser for anything you'll publish.

### Reading logs

This is where `grep` earns its keep. The practice folder has the log of Riverstone's daily summary job for November and December: every morning at 07:00 it summarizes the day before, the job that section 34.7's `daily_summary.sh` imitates. Each log line has a date, a time, a **level** (INFO for normal progress, WARNING for something worth a look, ERROR for a failure), the job's name, and a message.

```
# terminal, in ~/ch34/practice
$ wc -l logs/report.log
187 logs/report.log

$ awk '{ print $3 }' logs/report.log | sort | uniq -c | sort -nr
    149 INFO
     37 WARNING
      1 ERROR

$ grep ERROR logs/report.log
2025-11-09 07:00:04 ERROR daily_summary: database connection refused

$ grep -A1 "connection refused" logs/report.log
2025-11-09 07:00:04 ERROR daily_summary: database connection refused
2025-11-09 07:00:04 INFO daily_summary: exit code 1

$ grep WARNING logs/report.log | head -3
2025-11-01 07:00:04 WARNING daily_summary: no sales lines for 2025-11-01; wrote an empty summary
2025-11-02 07:00:04 WARNING daily_summary: no sales lines for 2025-11-02; wrote an empty summary
2025-11-03 07:00:04 WARNING daily_summary: no sales lines for 2025-11-03; wrote an empty summary
```

- **`awk '{ print $3 }'`** with no `-F` splits on spaces, so field 3 is the level, and the pipeline from before counts each one.
- One **ERROR** in 61 days, on 9 November: the database refused the connection and the job stopped with exit code 1. **`-A1`** shows one line **after** each match (`-B` before, `-C` both), which is how you see what happened next.
- The **WARNING** lines are mostly quiet days: the job ran, found no orders, and wrote an empty summary, which is correct and needs no action. A few are a slow database that answered on the second try.

Finding that in a log viewer takes minutes; here it takes one line, and the same command works on a server over SSH where there is no log viewer at all.

---

## 34.5 Permissions: who can read, write, and run

Every file has an **owner**, a **group**, and nine permission bits. `ls -l` shows them:

```
# terminal, in ~/ch34/practice
$ ls -l reference/customers.csv
-rw-r--r-- 1 meera meera 877 Jan  5  2026 reference/customers.csv
```

Read the first column in four pieces: `-` (a regular file; `d` would be a folder, `l` a link), then three sets of three, for **user** (the owner), **group**, and **others** (everyone else). Each set is `r` read, `w` write, `x` execute, or `-` for "not allowed". So `rw-r--r--` means the owner can read and write, and everyone else can only read. The `1` after the permissions is the number of links to the file: ignore it. Then come the owner (`meera`), the group (a group of one, also called `meera`), the size in bytes, the date, and the name.

![An ls -l line with callouts for the file type and the user, group, and others permission sets, and a table of the common modes 644, 755, 600, and 700](figures/fig34-3-permissions.svg)

*Figure 34.3 — Nine bits, three audiences, and four numbers worth memorizing.*

Each set is also a digit, adding read 4, write 2, and execute 1:

| Number | Means | Common use |
|---|---|---|
| `644` | owner read and write; everyone else read | data files, documents |
| `755` | owner everything; everyone else read and run | scripts, folders |
| `600` | owner read and write; nobody else anything | SSH private keys, `.env` files with passwords |
| `700` | owner everything; nobody else anything | private folders such as `~/.ssh` |

**On a folder**, the bits mean something slightly different: `r` lists the names inside, `w` creates and deletes entries, and `x` lets you go into it or reach anything within it. A folder with no `x` is a locked cabinet: you can't get at the files even if their own permissions would allow it.

Watch a script go from unrunnable to runnable. First, write a two-line script into a file:

```
# terminal, in ~/ch34/practice
$ printf '#!/usr/bin/env bash\necho "the export ran"\n' > run_export.sh

$ cat run_export.sh
#!/usr/bin/env bash
echo "the export ran"
```

**`printf`** is like `echo`, but it understands `\n` as "new line", so one command writes both lines. The first line, `#!/usr/bin/env bash`, tells the system to run the file with bash (section 34.7 explains it); the second is the script's only command. Now try to run it:

```
# terminal, in ~/ch34/practice
$ ls -l run_export.sh
-rw-rw-r-- 1 meera meera 42 Sep 29 02:34 run_export.sh

$ ./run_export.sh
bash: ./run_export.sh: Permission denied

$ chmod +x run_export.sh

$ ls -l run_export.sh
-rwxrwxr-x 1 meera meera 42 Sep 29 02:34 run_export.sh

$ ./run_export.sh
the export ran
```

`./run_export.sh` means "the file `run_export.sh` in this folder": the shell doesn't look in the current folder for programs unless you say so (section 34.6 explains why). The first attempt fails because the file has no `x`; after `chmod +x`, every `-` in an `x` position becomes `x`, and the script runs. Your group bits may show `r--` instead of `rw-`: new files get their starting permissions from a setting called the **umask**, which differs between systems. Your dates will be today's.

`chmod` (*change mode*) sets permissions, either by adding and removing (`chmod +x`, `chmod g-w`, `chmod o-rwx`) or by number (`chmod 755 run_export.sh`). `chown` changes the owner, and usually needs administrator rights.

### sudo, and when to be careful

`sudo` runs one command as the **superuser** (`root`), the account that can do anything: `sudo apt install rsync`. Use it for installing software and editing system files, never out of habit. If a command fails with *Permission denied*, the first question is *"should I be allowed to do this?"*, not *"how do I force it?"*. On a shared server, the answer is often that the file belongs to a service account and your script should be writing somewhere else.

> **Watch out: SSH refuses keys that other people can read.** If your private key is `644`, `ssh` prints *WARNING: UNPROTECTED PRIVATE KEY FILE!* and refuses to use it. `chmod 600 ~/.ssh/id_ed25519` fixes it. The same logic applies to a `.env` file holding a database password (Chapter 26, section 26.4): `chmod 600`, and keep it out of Git.

---

## 34.6 Environment variables and PATH

An **environment variable** is a named value the shell hands to every program it starts. Chapter 26 used them to keep a database password out of the code (section 26.4); here's what's actually happening.

```
# terminal, in ~/ch34/practice
$ export RIVERSTONE_OUTPUT_DIR=/tmp/reports

$ echo "$RIVERSTONE_OUTPUT_DIR"
/tmp/reports

$ python3 -c 'import os; print(os.environ["RIVERSTONE_OUTPUT_DIR"])'
/tmp/reports

$ env | grep RIVERSTONE
RIVERSTONE_OUTPUT_DIR=/tmp/reports
```

`python3 -c '…'` runs a one-line Python program given in quotes, a quick way to show that a program started from this shell sees the variable.

- **`export NAME=value`** sets a variable and passes it to programs the shell starts. Without `export`, it stays in the shell itself.
- No spaces around `=`. `NAME = value` runs a command called `NAME`.
- **`$NAME`**, or better `"$NAME"` with quotes, reads it. The quotes matter: an unquoted value containing spaces is split into several arguments.
- **`env`** lists everything currently set; `unset NAME` removes one.
- Variables set this way last until you close the terminal. To make them permanent, put the `export` lines in `~/.bashrc` (bash) or `~/.zshrc` (zsh), which the shell reads when it starts. On a server, the scheduler or service manager supplies them instead.

### PATH

`PATH` is the list of folders the shell searches, in order, when you type a command name:

```
# terminal, in ~/ch34/practice
$ echo "$PATH" | tr ':' '\n' | head -4
/usr/local/sbin
/usr/local/bin
/usr/sbin
/usr/bin

$ which python3 grep
/usr/local/bin/python3
/usr/bin/grep

$ type cd
cd is a shell builtin
```

`PATH` is one long line with the folders separated by colons; **`tr ':' '\n'`** *translates* every colon into a new line, so each folder gets a line of its own. Yours will list different folders.

`which` shows which file would run. This is the answer to the two most common "but it works in my terminal" mysteries: a virtual environment puts its own folder at the front of `PATH` (that's the heart of what `activate` does; it also changes your prompt), and a scheduled job runs with a much shorter `PATH` than your interactive shell, which is why `cron` jobs should call `/usr/bin/python3` or a full path to the environment rather than trusting `python3` to be found.

`type` explains what a name is: a file, a **built-in** command of the shell itself (like `cd`), an **alias**, or a function.

> **Watch out: never put secrets in your shell history.** Typing `export DB_PASSWORD=hunter2` writes the password into `~/.bash_history`, which is readable by anyone with your account and is often backed up. Keep secrets in a `.env` file with `600` permissions, or in a **secrets manager** (a service that stores passwords and hands them only to the programs allowed to have them), and load them with `set -a; . ./.env; set +a` (section 26.0: `set -a` exports everything the file defines) or a library such as python-dotenv (Chapter 18).

---

## 34.7 Shell scripts

A **shell script** is a file of commands. Anything you can type, you can save and run again, which is how a sequence of clever one-liners becomes something a colleague or a scheduler can use.

The companion folder has `daily_summary.sh`, one folder above `practice/`. Read it before running it; this is the whole file:

```bash
#!/usr/bin/env bash
# Analyst to Architect · Chapter 34 · summarize one day's export.
# Usage: ./daily_summary.sh 2025-12-16      Exit codes: 0 done, 2 no export for that day.
set -euo pipefail

DAY="${1:?usage: $0 YYYY-MM-DD}"
FILE="exports/orders_${DAY}.csv"

if [[ ! -f "$FILE" ]]; then
    echo "no export for $DAY" >&2
    exit 2
fi

ORDER_LINES=$(( $(wc -l < "$FILE") - 1 ))
REVENUE=$(awk -F, 'FNR > 1 { total += $11 } END { printf "%.2f", total + 0 }' "$FILE")
CUSTOMERS=$(awk -F, 'FNR > 1 { seen[$4] = 1 } END { print length(seen) }' "$FILE")

echo "$DAY: order lines $ORDER_LINES, customers $CUSTOMERS, revenue $REVENUE"
```

```
# terminal, in ~/ch34/practice
$ cp ../daily_summary.sh .

$ chmod +x daily_summary.sh

$ ./daily_summary.sh 2025-12-16
2025-12-16: order lines 7, customers 3, revenue 89800.00

$ ./daily_summary.sh 2025-12-25
2025-12-25: order lines 0, customers 0, revenue 0.00

$ ./daily_summary.sh 2026-01-05; echo "exit code $?"
no export for 2026-01-05
exit code 2

$ ./daily_summary.sh; echo "exit code $?"
./daily_summary.sh: line 6: 1: usage: ./daily_summary.sh YYYY-MM-DD
exit code 1
```

**How it works:**

- **`#!/usr/bin/env bash`**, the **shebang**, is the first line of every script: it tells the system which program runs the file. `env bash` finds bash wherever it's installed. It must be the very first line, before any comment.
- **Lines starting with `#`** after it are comments, as in Python.
- **`set -euo pipefail`** belongs at the top of every script you write:
  - `-e` stop at the first command that fails, instead of carrying on with bad data,
  - `-u` treat an unset variable as an error, so a typo doesn't silently become an empty string (see the Watch out below),
  - `-o pipefail` make a pipeline fail if **any** stage fails, not just the last one.
- **`"${1:?message}"`** takes the first argument, or exits with that message if it wasn't given. `$1`, `$2`, … are the arguments, `$0` is the script's name, and `"$@"` is all of them.
- **`$( … )`** is **command substitution**: run the command and use its output as text. `$(( … ))` is arithmetic.
- **`[[ ! -f "$FILE" ]]`** is a test: *is this not a regular file?* Others: `-d` folder, `-s` non-empty file, `-z` empty string, `=` and `!=` for strings, `-eq` and `-lt` for numbers.
- **`>&2`** sends the message to standard error, so it doesn't pollute the script's real output when someone pipes it.
- **`exit 2`** returns a code that says *which* problem occurred: 0 success, 1 general failure, and your own numbers for the cases a caller might want to treat differently.
- **Always quote your variables**: `"$FILE"`, not `$FILE`. Without quotes, a path containing a space becomes two arguments, which is the single most common bug in shell scripts.
- **Name your variables so they can't collide with the system's.** ALL-CAPS names such as `PATH`, `HOME`, `USER`, and `LINES` (bash's own record of the terminal's height) already mean something, which is why this script says `ORDER_LINES`, not `LINES`. A prefix or lowercase names keep you safe.
- The last line prints `customers 1` rather than `1 customers`: a label before the number never needs a plural.

> **Watch out: `rm -rf` with a variable.** Never run `rm -rf` with a variable that might be empty. If `$DIR` is unset, `rm -rf $DIR/` becomes `rm -rf /`, a command that has destroyed more than one production system. `set -u` turns the unset variable into an error before `rm` runs; `"${DIR:?}"` (as in `DAY` above) does the same for one variable. Before any `rm` with a pattern, run `ls` with the same pattern and read what it lists.

### Loops

```
# terminal, in ~/ch34/practice
$ for day in 2025-12-15 2025-12-16 2025-12-17; do ./daily_summary.sh "$day"; done
2025-12-15: order lines 0, customers 0, revenue 0.00
2025-12-16: order lines 7, customers 3, revenue 89800.00
2025-12-17: order lines 2, customers 1, revenue 37628.00
```

**`for day in …; do …; done`** runs the commands between `do` and `done` once for each word in the list, with `$day` set to that word. Loop over a wildcard instead of a list, and you get one run per file:

```
# terminal, in ~/ch34/practice
$ for file in exports/orders_2025-12-2*.csv; do \
    lines=$(( $(wc -l < "$file") - 1 )); \
    [[ $lines -eq 0 ]] && echo "$file is empty"; \
  done
exports/orders_2025-12-20.csv is empty
exports/orders_2025-12-22.csv is empty
exports/orders_2025-12-24.csv is empty
exports/orders_2025-12-25.csv is empty
exports/orders_2025-12-26.csv is empty
exports/orders_2025-12-27.csv is empty
exports/orders_2025-12-28.csv is empty
exports/orders_2025-12-29.csv is empty
```

A `for` loop over a wildcard is the workhorse of file processing: one command per file, in a predictable order. Inside it, `[[ $lines -eq 0 ]] && echo …` prints only when the test passes, the `&&` of section 34.2.

When the list is in a file, one item per line, **`while read`** reads it a line at a time:

```
# terminal, in ~/ch34/practice
$ printf '2025-12-16\n2025-12-17\n2025-12-18\n' > /tmp/days.txt

$ while read -r day; do ./daily_summary.sh "$day"; done < /tmp/days.txt
2025-12-16: order lines 7, customers 3, revenue 89800.00
2025-12-17: order lines 2, customers 1, revenue 37628.00
2025-12-18: order lines 2, customers 1, revenue 23850.00
```

`read -r day` reads one line into the variable `day` (`-r` keeps any backslashes as they are), and `< /tmp/days.txt` feeds the file to the loop's standard input. The loop stops when there are no lines left.

To keep a record of what a script said while still watching it, send its output through **`tee -a`** (section 34.2):

```
# terminal, in ~/ch34/practice
$ ./daily_summary.sh 2025-12-16 | tee -a run.log
2025-12-16: order lines 7, customers 3, revenue 89800.00

$ cat run.log
2025-12-16: order lines 7, customers 3, revenue 89800.00
```

### Three more tools for the project

The project at the end of this chapter needs three commands you haven't met. A **checksum** is a long number calculated from every byte of a file: change one byte, and it changes completely. `sha256sum` prints one:

```
# terminal, in ~/ch34/practice
$ sha256sum exports/orders_2025-12-16.csv
861504c535d42b08c99d34cb273d3d191758487454e3d7b6bc5687afee18e65d  exports/orders_2025-12-16.csv
```

A sender publishes the checksum next to the file; the receiver calculates it again and compares, which proves the download arrived intact. **`gzip`** compresses a file, and **`zcat`** reads a compressed one without unpacking it:

```
# terminal, in ~/ch34/practice
$ gzip -k ../sales_lines_2025.csv

$ ls -l ../sales_lines_2025.csv ../sales_lines_2025.csv.gz
-rw-r--r-- 1 meera meera 34350 Sep 29 02:34 ../sales_lines_2025.csv
-rw-r--r-- 1 meera meera  3992 Sep 29 02:34 ../sales_lines_2025.csv.gz

$ zcat ../sales_lines_2025.csv.gz | head -2
order_id,order_date,customer_id,customer_name,city,segment,product_id,product_name,category,quantity,net_revenue,sales_rep
10001,2025-01-02,2,Patel Kitchenware,Ahmedabad,Retail,108,Stackable Bin,Storage,10,2900.00,Neha Kulkarni

$ rm ../sales_lines_2025.csv.gz
```

`gzip -k` keeps the original (`-k`) and writes `sales_lines_2025.csv.gz` beside it; without `-k`, the original is replaced by the compressed file. And **`date`** prints the date and time in any format you ask for: `date +%F` prints today's date as `YYYY-MM-DD` (`%F`), and `date '+%F %T'` adds the time (`%T`), which is how the project stamps its log lines.

> **Watch out: shell scripts stop being the right tool sooner than you think.** They're ideal for gluing commands together: fetch a file, check it, move it, call a program. Once you need data structures, CSV parsing, arithmetic with decimals, error handling with retries, or tests, write Python (Chapters 17 and 18; Chapter 29 turns a script into a proper tool). A 300-line bash script that nobody dares to change is a common and avoidable mess.

---

## 34.8 SSH: working on another machine

**SSH** (secure shell) gives you a terminal on a remote machine over an encrypted connection. It's how you reach the report server, a cloud database host, or a container.

To practise, you need a machine that accepts SSH connections, an **SSH server**. A real one belongs to your company's platform team; for learning, your own computer can play the part. None of the three systems runs an SSH server until you turn one on.

### Set up a practice server (10 minutes)

- **Ubuntu, and WSL on Windows:** install and start the server, `sudo apt install openssh-server` then `sudo service ssh start`.
- **macOS:** System Settings → General → Sharing, and turn on **Remote Login**.

Then connect to your own machine, by the name `localhost` (section 34.9), and come straight back:

<!-- run: none -->
```
# terminal, anywhere
$ ssh localhost
$ exit
```

The first time, `ssh` shows the server's key fingerprint and asks *Are you sure you want to continue connecting (yes/no/[fingerprint])?*. Type `yes`. The fingerprint is the server's identity card: `ssh` remembers it in `~/.ssh/known_hosts`, and if it ever changes it warns you loudly, because a different fingerprint can mean a different machine pretending to be yours. Then it asks for your login password, gives you a prompt on "the server", and `exit` brings you home.

### Keys, not passwords

An **SSH key pair** is two matching files: a **private key** (`~/.ssh/id_ed25519`) that never leaves your machine, and a **public key** (`~/.ssh/id_ed25519.pub`) that you give to the server. The server uses the public key to check that you hold the private one. Nothing secret crosses the network, and there's no password to guess or reuse.

<!-- run: none -->
```
# terminal, on your own machine (run once)
$ ssh-keygen -t ed25519 -C "meera@laptop"
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/meera/.ssh/id_ed25519):
Created directory '/home/meera/.ssh'.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/meera/.ssh/id_ed25519
```

- **`-t ed25519`** chooses the key type, a modern and short one; **`-C "meera@laptop"`** is a comment stored with the public key, so you can tell your keys apart later.
- Press Enter at the first question to keep the usual file name. The last lines, a fingerprint and a small picture made of symbols, follow; you can ignore them.
- Choose a **passphrase**: it encrypts the private key, so a stolen laptop isn't a stolen server. As with `sudo`, nothing appears while you type it. `ssh-agent` remembers it for the session so you type it once a day.

Now give the server a short name. Create the file `~/.ssh/config` in your editor (`nano ~/.ssh/config`, or `code ~/.ssh/config`) with these four lines, using your own user name, and make it private:

```text
Host reportserver
    HostName 127.0.0.1
    User meera
    IdentityFile ~/.ssh/id_ed25519
```

<!-- run: none -->
```
# terminal, on your own machine
$ chmod 600 ~/.ssh/config

$ ssh-copy-id reportserver
```

- `~/.ssh/config` gives a short name to a host, its address, the user, and which key to use, so `ssh reportserver` replaces `ssh -i ~/.ssh/id_ed25519 meera@127.0.0.1`. `127.0.0.1` is this machine (section 34.9); on a real job the platform team gives you the server's address, for example `10.4.2.17`, and your user name there.
- **`ssh-copy-id reportserver`** copies your public key to the server, asking for your login password this one time. From then on, the key does the work.

### Connecting and running commands

<!-- run: none -->
```
# terminal, in ~/ch34/practice
$ ssh reportserver "hostname; ls /home/meera/ch34/practice/exports | wc -l"
vm
61
```

- **`ssh host "command"`** runs one command on the server and returns, which is exactly what a scheduled job or a deployment script needs. Here the server's name is `vm` (yours prints your computer's name), and it sees the same 61 files, because "the server" is your own machine. Without a command, you get an interactive shell; `exit` (or `Ctrl+D`) comes home.

### Copying files

<!-- run: none -->
```
# terminal, in ~/ch34/practice
$ scp exports/orders_2025-12-16.csv reportserver:/tmp/

$ ssh reportserver "wc -l /tmp/orders_2025-12-16.csv"
8 /tmp/orders_2025-12-16.csv
```

**`scp`** copies one file or folder, like `cp` with a machine name and a colon in front of the path. The other direction works the same way: `scp reportserver:/var/log/report.log .` brings a file back.

For a whole folder, **`rsync`** is better: it copies only what differs, which matters when the folder is large or the connection is slow. It works between two folders on one machine exactly as it does between machines, so try it locally first. The trailing slash matters: `exports/` means "the contents of `exports`", while `exports` without it means "the folder itself", which would land as `exports_copy/exports`. And always do a **dry run** first:

```
# terminal, in ~/ch34/practice
$ rsync -anv --delete exports/ /tmp/exports_copy/ | head -4
sending incremental file list
created directory /tmp/exports_copy
./
orders_2025-11-01.csv

$ rsync -a --delete exports/ /tmp/exports_copy/

$ ls /tmp/exports_copy | wc -l
61
```

- **`-a`** (*archive*) copies folders inside folders and keeps permissions and timestamps.
- **`-n`** is the dry run: list what *would* happen, and do nothing. **`-v`** (*verbose*) prints each file, which is what makes the dry run useful. `head -4` shows only the start of the list of 61 files.
- **`--delete`** makes the destination match the source exactly, deleting anything in it that the source doesn't have. That's why the dry run comes first, every time: with the wrong folder or a missing slash, it deletes the wrong things.

To copy to the server, only the destination changes: `rsync -anv --delete exports/ reportserver:/tmp/exports_copy/`, then the same without `-n` and `-v`.

> **Watch out: tunnels and ports.** `ssh -L 5433:localhost:5432 reportserver` forwards your local port 5433 to the server's PostgreSQL. DBeaver on your laptop then connects to `localhost:5433` and reaches a database that isn't exposed to the internet at all. It's a common and legitimate pattern, and it's also something many companies audit, so use it with your platform team's blessing.

---

## 34.9 Networking in plain English

Four ideas cover most of what a data person needs.

### IP addresses: which machine

An **IP address** identifies a machine on a network, like `142.250.183.4` (IPv4) or a longer IPv6 address. Some ranges are **private**, used inside company networks and never routed on the public internet: `10.x.x.x`, `172.16–31.x.x`, and `192.168.x.x`. And `127.0.0.1`, called **localhost**, always means *this machine*: this chapter's practice server listens there, which is why nothing it does leaves your computer.

### DNS: names into addresses

Typing an address is unworkable, so the **Domain Name System** translates names into addresses. Your machine asks a DNS server *"what is the address of `api.example.com`?"* and caches the answer for a while.

```
# terminal, in ~/ch34/practice
$ getent hosts localhost
127.0.0.1       localhost
```

**`getent hosts`** asks the system to look a name up the way every program does, and prints the address it gets. (macOS has no `getent`: `dscacheutil -q host -a name localhost` does the same.) `dig api.example.com` or `nslookup api.example.com` does a full DNS lookup and prints the result; macOS has both, and on Ubuntu you install them first with `sudo apt install bind9-dnsutils`. DNS is the reason a database connection can fail with *"could not translate host name"*: the name, not the database, is the problem. It's also how a company points `warehouse.internal` at a new server without changing a single connection string.

### Ports: which program on that machine

One machine runs many services, so each listens on a numbered **port**. Some numbers are conventions: 22 SSH, 80 HTTP, 443 HTTPS, 5432 PostgreSQL, 3306 MySQL, 8080 and 8000 for test servers.

```
# terminal, in ~/ch34/practice
$ python3 ../daily_file_server.py > /tmp/server.log 2>&1 &

$ sleep 1; cat /tmp/server.log

$ ss -ltn | grep 8034
LISTEN 0      5          127.0.0.1:8034       0.0.0.0:*          
```

The first command starts the companion's small web server, `daily_file_server.py`, which serves the practice exports the way a partner's file server would. **`&`** at the end runs it in the **background** and gives you the prompt back; its messages go to `/tmp/server.log`, and `sleep 1` waits a second for it to start. `jobs` lists background jobs, `fg` brings one forward, and `kill %1` stops the first one.

`ss -ltn` lists listening TCP sockets (`-l` listening, `-t` TCP, `-n` numbers, not names). On macOS, which has no `ss`, `lsof -iTCP -sTCP:LISTEN -n -P` answers the same question. (Older Linux systems have `netstat -ltn`.) An address of `127.0.0.1:8034` means only this machine can connect; `0.0.0.0:8034` would mean anyone who can reach the machine. When something "can't connect", this command answers the first question: is anything listening at all?

### HTTP: asking for something

**HTTP** is the language of web requests: a **method** (GET to read, POST to send), a path, headers, and a body. The answer has a **status code**, a three-digit number: 200 means OK, 404 means not found, 401 means you must say who you are, 500 and above mean the server failed. It usually comes with a body. **`curl`** speaks HTTP from the command line. The practice server from the ports example is still running in the background, so ask it for things.

```
# terminal, in ~/ch34/practice
$ curl --silent http://127.0.0.1:8034/health
ok

$ curl --silent --output /dev/null --write-out "%{http_code}\n" \
    http://127.0.0.1:8034/exports/orders_2025-12-16.csv
200

$ curl --silent --output /dev/null --write-out "%{http_code}\n" \
    http://127.0.0.1:8034/exports/orders_2026-01-05.csv
404

$ curl --silent --head http://127.0.0.1:8034/exports/orders_2025-12-16.csv \
    | grep -i "^content-"
Content-Type: text/csv
Content-Length: 826

$ curl --silent http://127.0.0.1:8034/exports/orders_2025-12-16.csv | wc -l
8

$ kill %1
```

![A curl command split into protocol, address, port, and path, followed by four steps: DNS lookup, connecting to the port, sending the request, and reading the status code and body](figures/fig34-4-http-request.svg)

*Figure 34.4 — What a URL contains, and what happens after you press Enter.*

- `--silent` hides the progress meter; `--output file` saves the body; `--write-out "%{http_code}"` prints just the status.
- **`/dev/null`** is the system's bin: output sent there disappears. `--output /dev/null` throws the body away, because only the status code is wanted.
- `--head` asks for the headers only, which tells you the type and size before downloading 2 GB. `grep -i "^content-"` keeps the lines that start with `content-` in any case: **`^`** means "at the start of the line", as in Chapter 14's regular expressions. (The other headers, including the date, are filtered out so the output is the same every time.)
- `--fail` makes curl return a non-zero exit code on a 4xx or 5xx status, which is what a script needs. `--max-time 30` sets a timeout. Both are in this chapter's project.
- For an API that needs a key: `curl -H "X-API-Key: demo-key" …`, and `-d '{"json": "body"}' -H "Content-Type: application/json"` for a POST.

The `404` means the file for 5 January 2026 hasn't been published, and no amount of retrying will change that today; a 500-range code, by contrast, is worth retrying later. Chapter 29 writes a Python client that makes exactly this distinction for an API.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Running a command in the wrong folder | *No such file or directory* for a file you can see in Finder or Explorer | `pwd` first; use Tab completion so wrong paths can't be typed (section 26.0) |
| Forgetting that Linux is case-sensitive | A script that worked on your laptop fails on the server | Match the case exactly; keep file names lowercase |
| `rm` with a wildcard, or `rm -rf $DIR/` | Files gone, with no recycle bin | Run `ls` with the same pattern first; `set -u` in scripts so an empty variable is an error |
| Unquoted variables in scripts | A path with a space becomes two arguments and half a file name disappears | Always `"$VAR"` |
| `uniq` without `sort` | Counts too low, silently | `sort \| uniq -c` |
| `sort` on numbers without `-n` | 9 comes after 10 | `sort -n`, or `sort -k2 -nr` for a numeric column |
| `cut -d,` or `awk -F,` on real CSV | Wrong columns when a field contains a comma or a quote | Check the data; use `csvkit`, `qsv`, or pandas for anything published |
| `NR > 1` with several files in awk | Every file's header counted after the first | `FNR > 1` |
| Writing output over the input file (`sort f.csv > f.csv`) | An empty file | Write to a new name, then `mv` |
| Scheduled job "runs" but does nothing | Works by hand, not in cron | The job's `PATH` and environment are minimal: use full paths, set variables in the script |
| Missing shebang or execute bit | *Permission denied*, or the file opens as text | `#!/usr/bin/env bash` on line 1, and `chmod +x` |
| `rsync --delete` without a dry run, or with a missing `/` | Files deleted on the destination, or copied one folder too deep | `rsync -anv --delete` first; `exports/` means the folder's contents |
| Working under `/mnt/c/…` in WSL | Permissions that don't change, and slow commands | Work in your Linux home folder (`cd ~`) |
| No `set -euo pipefail` | The script carries on after a failure and writes a wrong file | Put it at the top of every script |
| Private key readable by others | *WARNING: UNPROTECTED PRIVATE KEY FILE!* and SSH refuses | `chmod 600 ~/.ssh/id_ed25519` |
| `curl` without `--fail` in a script | A 404 or 500 page saved as if it were data | `--fail --show-error --max-time N`, then check the exit code |
| Secrets typed on the command line | Passwords in `~/.bash_history` and in process lists | Use a `.env` file with `600`, or a secrets manager |
| Growing a shell script past a page or two | Nobody dares change it; no tests | Move to Python as soon as there's real logic (Chapter 29 shows how to make it a proper tool) |
| Assuming the shell parsed your pattern | `find . -name *.csv` fails oddly | Quote patterns for `find`: `find . -name "*.csv"` |

---

## In the real world: the disk that filled up at 2 a.m.

At 07:40 on a Tuesday, Meera's phone shows an alert from the report server, the small Linux machine that runs Riverstone's scheduled jobs: the monthly report job exited with code 1. The log line is one she hasn't seen before: *ERROR riverstone_report: could not write reports/riverstone_monthly_2026-01.xlsx: No space left on device*.

The report server has no desktop. Everything below happens over SSH, and takes four minutes.

<!-- run: none -->
```
# terminal, on Meera's laptop
$ ssh reportserver
$ df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        40G   40G     0 100% /

$ du -h --max-depth=1 /var/riverstone | sort -h | tail -4
1.2G    /var/riverstone/exports
2.1G    /var/riverstone/reports
34G     /var/riverstone/incoming
38G     /var/riverstone

$ ls -lh /var/riverstone/incoming | tail -3
-rw-r--r-- 1 reportjob reportjob 412M Feb  1 02:00 orders_2026-01-30.csv
-rw-r--r-- 1 reportjob reportjob 412M Feb  2 02:00 orders_2026-01-31.csv
-rw-r--r-- 1 reportjob reportjob 412M Feb  3 02:00 orders_2026-02-01.csv

$ ls /var/riverstone/incoming | wc -l
84
```

| Command | What it answers |
|---|---|
| `df -h /` | how full is the disk? (*disk free*; `-h` for human-readable sizes, `/` for the disk the system runs from) |
| `du -h --max-depth=1 /var/riverstone` | how big is each folder directly inside this one? (*disk usage*) |
| `sort -h` | sort human-readable sizes correctly, so `34G` comes after `2.1G` |
| `ls -lh … \| tail -3` | the newest files and their sizes (the names sort by date) |

Eighty-four daily files of 412 MB each, one for every day since the download job was switched on, on 10 November. These aren't the small practice exports: each is the ERP's full daily extract, every order line with its history plus audit columns. The download step ran every night; nothing ever moved the files out or deleted them. The archive folder the original script was supposed to use is empty, because that line was never written.

She clears just enough to let the report run, checking before deleting:

<!-- run: none -->
```
# terminal, on the report server
$ find /var/riverstone/incoming -name "orders_2025-*.csv" | wc -l
52
$ find /var/riverstone/incoming -name "orders_2025-*.csv" -print0 \
    | xargs -0 du -ch | tail -1
21G     total
$ find /var/riverstone/incoming -name "orders_2025-*.csv" -delete
$ df -h / | tail -1
/dev/vda1        40G   20G   21G  48% /
```

- The first `find` counts the 2025 files before touching anything: 52, from 10 November to 31 December.
- **`-print0 | xargs -0 du -ch`** hands the file names to `du` safely, even if a name contained a space: `-print0` ends each name with an invisible zero byte instead of a new line, and `xargs -0` reads them that way and runs `du` on them. `du -ch` adds a grand **total** line (`-c`), which `tail -1` keeps.
- Only then does `-delete` run, with exactly the same pattern. `df` confirms the disk is at 48%.

The report runs by hand and goes out at 08:20. Then she fixes the cause, in the project below: a script that downloads the day's file, checks it, compresses it into the archive, and deletes the raw copy, with a monthly clean-up of archives older than a year. She adds one more line to the job's crontab: a weekly check that emails her when the disk is more than 80% full.

**What she tells the data engineer:** *"The job only ever added files. Downloads now get checked, compressed into the archive, and removed from `incoming`; compressed CSV is many times smaller (usually 5 to 10 times with gzip, and our practice sales file shrinks about 8 times). There's a disk check on Mondays. And we should give `incoming` its own volume, so a runaway download can't take the whole server down with it."*

Three things made this fixable in minutes rather than a day: the failure was loud and had a reason (an exit code and an ERROR line with the cause), the machine was reachable by SSH with a key, and `df`, `du`, `find`, and `ls` answer "what is filling the disk?" faster than any console.

---

## Project: a daily file that looks after itself

**Goal:** a script that fetches one day's export, proves it arrived intact, archives it, logs what it did, and tells its caller what happened.

### Tools you'll need

These are the versions used for this chapter, checked in September 2026.

- **bash 5.2** on **Ubuntu 24.04**. **macOS:** Terminal runs zsh, so type `bash` first (macOS includes bash 3.2, which runs every script here). A few Linux tools differ on a Mac: use `lsof -iTCP -sTCP:LISTEN -n -P` for `ss -ltn`, `dscacheutil -q host -a name localhost` for `getent hosts`, and `date -v-1d` for `date -d yesterday` (or `brew install coreutils` and use `gdate`).
- **Windows: WSL 2** with Ubuntu, installed with `wsl --install` from an administrator PowerShell (section 34.1). Git Bash is enough for the text tools, not for permissions, `ss`, or the SSH server; PowerShell is a different language.
- **curl 8.5**, **OpenSSH 9.6**, **rsync 3.2**, **iproute2** (for `ss`), all standard on Ubuntu.
- **Python 3** (any version Chapter 17's rule allows) for the practice data generator and the local file server; neither needs a virtual environment.
- **Companion files** in `ch34/`: `make_ch34_data.py` (builds `practice/` from `sales_lines_2025.csv`), `daily_file_server.py` (the local file server), `daily_summary.sh` and `fetch_daily.sh` (the scripts), and `weekly_summary.sh` (exercise 10's answer).
- **Worth adding later:** `jq` for JSON on the command line, `ripgrep` (`rg`) as a faster `grep`, `fzf` for searching history, `tmux` for sessions that survive a dropped connection, and `qsv` or `csvkit` for proper CSV parsing.

**Option A: your own data.** A file your team downloads, exports, or receives every day. Work in a folder you own, and keep credentials in environment variables, not in the script.

**Option B: Riverstone.** Use the companion `daily_file_server.py` as the partner's server, and write the script yourself before comparing with `fetch_daily.sh`.

**What it must do:**

1. Take the day as an argument, and reject anything that isn't `YYYY-MM-DD` with exit code 1.
2. Download `exports/orders_<day>.csv`, with a timeout, failing on a 404 rather than saving the error page. Exit 2 when the file isn't published yet.
3. Download the matching `.sha256` file and verify the download with `sha256sum --check`. Exit 3 on a mismatch, leaving the file for inspection.
4. Report what arrived: the number of order lines and the day's revenue (`wc -l` and `awk`).
5. Compress the file into `archive/` and remove the raw copy from `incoming/`.
6. Log every step, with a timestamp, to both the screen and `logs/fetch_daily.log`.
7. Exit 0 only when all of that worked.

Start the server in one terminal, then run the script in another:

```
# terminal, in ~/ch34/practice
$ cp ../fetch_daily.sh . && chmod +x fetch_daily.sh

$ python3 ../daily_file_server.py > /tmp/server.log 2>&1 &

$ sleep 1; ./fetch_daily.sh 2025-12-16 | cut -d' ' -f3-
INFO downloading orders_2025-12-16.csv from http://127.0.0.1:8034
INFO orders_2025-12-16.csv passed its checksum: 7 order lines, revenue 89800.00
INFO archived archive/orders_2025-12-16.csv.gz

$ ./fetch_daily.sh 2026-01-05 | cut -d' ' -f3-; echo "exit code ${PIPESTATUS[0]}"
curl: (22) The requested URL returned error: 404
INFO downloading orders_2026-01-05.csv from http://127.0.0.1:8034
ERROR could not download orders_2026-01-05.csv (not published yet, or the server is unreachable)
exit code 2

$ ls archive
orders_2025-12-16.csv.gz

$ ls incoming

$ zcat archive/orders_2025-12-16.csv.gz \
    | awk -F, 'FNR > 1 { total += $11 } END { printf "%.2f\n", total }'
89800.00

$ kill %1
```

*(`cut -d' ' -f3-` drops the date and time from each log line so the output is the same every time. `${PIPESTATUS[0]}` is the exit code of the first command in the pipeline, not of `cut`; it's a bash feature, one more reason this chapter runs bash on macOS. The `curl:` line comes first because curl writes it to standard error, which doesn't go through `cut`, so it appears on the screen as soon as curl writes it.)*

The compressed archive holds the same ₹89,800.00 the summary reported, so nothing was lost on the way in. ✓

### The reference script

Here is `fetch_daily.sh`, the companion's answer. Compare it with yours once yours runs.

```bash
#!/usr/bin/env bash
# Analyst to Architect · Chapter 34 · the project: download one day's export, check it, archive it.
# Usage: ./fetch_daily.sh 2025-12-16 [base_url]
# Exit codes: 0 done, 1 bad arguments, 2 file not published yet, 3 checksum mismatch.
# Tested on: bash 5.2.21, curl 8.5, Ubuntu 24.04.
set -euo pipefail

DAY="${1:-}"
BASE_URL="${2:-http://127.0.0.1:8034}"
INCOMING="incoming"
ARCHIVE="archive"
LOG="logs/fetch_daily.log"

log() { printf '%s %s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" "$2" | tee -a "$LOG"; }

if [[ ! "$DAY" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "usage: $0 YYYY-MM-DD [base_url]" >&2
    exit 1
fi

mkdir -p "$INCOMING" "$ARCHIVE" "$(dirname "$LOG")"
NAME="orders_${DAY}.csv"
log INFO "downloading $NAME from $BASE_URL"

if ! curl --silent --show-error --fail --max-time 30 \
        --output "$INCOMING/$NAME" "$BASE_URL/exports/$NAME"; then
    log ERROR "could not download $NAME (not published yet, or the server is unreachable)"
    rm -f "$INCOMING/$NAME"
    exit 2
fi

curl --silent --show-error --fail --max-time 30 \
     --output "$INCOMING/$NAME.sha256" "$BASE_URL/exports/$NAME.sha256"

if ! (cd "$INCOMING" && sha256sum --check --status "$NAME.sha256"); then
    log ERROR "checksum mismatch for $NAME; leaving it in $INCOMING for inspection"
    exit 3
fi

ROWS=$(( $(wc -l < "$INCOMING/$NAME") - 1 ))
REVENUE=$(awk -F, 'NR > 1 { total += $11 } END { printf "%.2f", total + 0 }' "$INCOMING/$NAME")
log INFO "$NAME passed its checksum: $ROWS order lines, revenue $REVENUE"

gzip --force "$INCOMING/$NAME"
mv "$INCOMING/$NAME.gz" "$ARCHIVE/"
rm -f "$INCOMING/$NAME.sha256"
log INFO "archived $ARCHIVE/$NAME.gz"
```

**How it works:**

1. **Arguments.** `DAY="${1:-}"` takes the first argument, or an empty string if there is none (`:-` gives a default instead of stopping, so the script can print its own usage line). The second argument, the server's address, defaults to the practice server.
2. **`log()`** is a **function**, a named group of commands, like a Python function. It prints the date and time (`date '+%Y-%m-%d %H:%M:%S'`), the level, and the message, and `tee -a` writes the same line to the screen and to the log file.
3. **The date check.** `[[ ! "$DAY" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]` is true when the argument does *not* match the pattern four digits, dash, two digits, dash, two digits (`=~` compares with a regular expression, as in Chapter 14). Then the script prints its usage to standard error and exits 1.
4. **`mkdir -p`** makes the three folders if they're missing, so the first run on a new machine works.
5. **The download.** `curl --silent --show-error --fail --max-time 30 --output …` saves the file, shows an error if there is one, returns a non-zero exit code on a 404 or 500 instead of saving the error page, and gives up after 30 seconds. `if ! curl …; then` runs the block when curl fails: log, delete any half-written file, exit 2.
6. **The checksum.** A second `curl` fetches `orders_<day>.csv.sha256`, and `sha256sum --check --status` recomputes the checksum and compares it, saying nothing and answering only with its exit code. It runs inside `( cd "$INCOMING" && … )`: the brackets run the commands in a separate copy of the shell, so the `cd` doesn't change the script's own folder. A mismatch logs an error and exits 3, leaving the file for inspection.
7. **The report.** `wc -l` and `awk` count the order lines and add up the revenue, as in section 34.4.
8. **The archive.** `gzip --force` compresses the file in place (`--force` overwrites an old copy), `mv` moves the `.gz` into `archive/`, and `rm -f` removes the checksum file (`-f`: no complaint if it's already gone).
9. **The exit code.** A script that reaches its last line ends with the exit code of its last command, 0 here. With `set -euo pipefail`, any unexpected failure on the way stops the script with a non-zero code.

**Deliverables:** the script, a run of each outcome (success, not published, bad checksum), and the log file.

**Stretch goals:**

- Add `--force` to re-fetch a day that's already archived, and refuse without it.
- Add a weekly clean-up that deletes archives older than 365 days (`find archive -name "*.gz" -mtime +365 -delete`), after running it once without `-delete`.
- Schedule it with `cron`: `crontab -e`, then `15 7 * * * cd /var/riverstone && ./fetch_daily.sh "$(date -d yesterday +\%F)" >> logs/cron.log 2>&1`. Remember that cron's `PATH` is minimal (section 34.6), and that `%` must be escaped in a crontab.
- Make the script fetch a range of days and keep going after a failure, reporting a summary at the end.
- Rewrite it in Python with `requests` (Chapter 18) and compare: which parts got simpler, which got longer? Chapter 29 shows how to turn that into a tool with tests.

---

## Recap

- Recap of section 26.0: `pwd`, `ls`, `cd`, `cp`, `mv`, `rm`, and friends. New here: `head`, `tail -f`, searching in `less`, `find`, and wildcards. Linux is case-sensitive, and **globbing** (`*`, `?`) is done by the shell before the command runs.
- Every command has **standard input**, **standard output**, **standard error**, and an **exit code**. `>`, `>>`, `2>`, `<`, and `|` connect them; `&&` and `||` chain on success and failure.
- **grep** finds lines; **wc**, **sort**, **uniq -c**, and **cut** count and group; **awk** does arithmetic on columns (`FNR > 1` skips each file's header). These tools see text, not CSV.
- **Permissions** are user, group, and others, each with read, write, and execute: `644` data, `755` scripts, `600` secrets. `chmod` changes them.
- **Environment variables** pass settings to programs; `PATH` decides which program a name runs; scheduled jobs get a minimal environment.
- **Shell scripts** start with a **shebang** and `set -euo pipefail`, quote every variable, take arguments, and exit with a meaningful code. Move to Python when logic grows.
- **SSH** uses a key pair; `~/.ssh/config` names hosts; `scp` and `rsync` copy files; keys must be `600`.
- **Networking**: an **IP address** is a machine, **DNS** turns names into addresses, a **port** is a program on that machine, and **HTTP** is the request and its **status code**. `ss -ltn` shows what's listening; `curl` makes the request.

---

## Key terms

shell · bash · zsh · WSL · globbing · standard input · standard output · standard error · redirection · pipe · `tee` · exit code · `test` · `grep` · `wc` · `sort` · `uniq` · `cut` · `awk` · `NR` and `FNR` · field separator · associative array · `printf` · `head` · `tail` · `less` · `find` · `chmod` · permission bits · owner · group · others · `sudo` · superuser · environment variable · `export` · `PATH` · shell built-in · shebang · `set -euo pipefail` · command substitution · function · quoting · `for` loop · argument (`$1`, `$@`) · background job · SSH · SSH server · host key fingerprint · `known_hosts` · key pair · public key · private key · passphrase · `~/.ssh/config` · `scp` · `rsync` · dry run · port forwarding · IP address · localhost · private address range · DNS · port · HTTP · method · status code · `curl` · `ss` · `cron` · checksum · `sha256sum` · `gzip`

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can find my way around a strange Linux server with `pwd`, `ls`, `cd`, and `find`.
- [ ] I can answer "how many rows, which files, which values" with a pipeline of small tools.
- [ ] I know where output and errors go, and how to send them where I want.
- [ ] I check exit codes, and my scripts return meaningful ones.
- [ ] I can search a log for errors and see the lines around them.
- [ ] I can read `ls -l` permissions and fix them with `chmod`.
- [ ] I know what `PATH` is, and why a cron job can't find a command my terminal finds.
- [ ] I can write a script that takes arguments, uses `set -euo pipefail`, quotes its variables, and fails safely.
- [ ] I can connect to a server with an SSH key and copy files both ways.
- [ ] I can explain IP, DNS, port, and HTTP status codes to a colleague, and test an API with `curl`.

---

## Exercises

Work in `companion/ch34/practice`. Predict each answer before you run it.

### Warm-up

1. How many daily export files are there for November 2025, and how many lines do they hold in total (including headers)?
2. Which export file is the largest, and how many order lines does it hold?
3. Show the first two order lines of 26 November 2025 without opening an editor.
4. How many lines of `../sales_lines_2025.csv` mention Bengaluru, and how many mention `unassigned`?

### Core

5. List the ten customers with the most order lines in 2025, with their counts, using `cut`, `sort`, and `uniq`.
6. Total 2025 revenue from `../sales_lines_2025.csv` with `awk`, and check it against the ₹43,35,471 Chapter 13 reports.
7. Revenue by segment for December 2025, largest first.
8. Which days in December have no orders? Answer it twice: once with a `for` loop, once with `find` and `-size`.
9. Save the report job's `WARNING` lines to `/tmp/warnings.txt` and count them, without the count including the file name.
10. Write `weekly_summary.sh`, which takes a Monday's date and prints one line per day of that week using `daily_summary.sh`, then a total.

### Stretch

11. Use `awk` to find the three order lines with the highest revenue in 2025, printing date, customer, product, and revenue.
12. Count the `curl` status codes you get for the first five days of January 2026 from the local file server, using a loop.
13. `scp` November's exports to `reportserver:/tmp/nov/`, then verify on the server that the line counts match, in a single `ssh` command.
14. A colleague's script runs `cd $DIR && rm -rf *`. Explain, precisely, what happens when `DIR` is unset, and rewrite the two lines safely.

### Think about it (no commands needed)

15. Your Python script works in your terminal, with your virtual environment active, and fails in cron with *`ModuleNotFoundError: No module named 'pandas'`*. What's happening, and give two fixes.
16. When is `grep` on a CSV the right tool, and when is it a trap? Give one example of each from this chapter's data.

---

## Answers

**1.**

```
# terminal, in ~/ch34/practice
$ ls exports/orders_2025-11-*.csv | wc -l
30

$ cat exports/orders_2025-11-*.csv | wc -l
65
```

30 files, 30 headers plus 35 order lines. `wc -l exports/orders_2025-11-*.csv | tail -1` gives the same total with a `total` label, and also shows each file.

**2.**

```
# terminal, in ~/ch34/practice
$ ls -S exports | head -2
orders_2025-11-16.csv
orders_2025-12-16.csv

$ wc -l exports/orders_2025-11-16.csv
8 exports/orders_2025-11-16.csv
```

`ls -S` sorts by size, largest first. The file for 16 November is the biggest of the two months. (`du -h exports/* | sort -h | tail -2` is the more general form, since it works on folders too.)

**3.**

```
# terminal, in ~/ch34/practice
$ head -3 exports/orders_2025-11-26.csv | tail -2
10155,2025-11-26,3,Green Leaf Hotels,Pune,Hospitality,107,Lunch Box Set,Kitchen,10,3610.00,Farah Khan
10156,2025-11-26,5,Metro Mart,Mumbai,Retail,101,Storage Box 10L,Storage,15,6450.00,Rahul Mehta
```

`head -3` takes the header and the first two order lines; `tail -2` drops the header.

**4.**

```
# terminal, in ~/ch34/practice
$ grep -c Bengaluru ../sales_lines_2025.csv
34

$ grep -c unassigned ../sales_lines_2025.csv
16
```

34 lines mention Bengaluru, and 16 order lines have no sales rep recorded, which is Chapter 13's data-quality finding (11 orders, 10 of them not cancelled) seen at the line level.

**5.**

```
# terminal, in ~/ch34/practice
$ cut -d, -f4 ../sales_lines_2025.csv | tail -n +2 | sort | uniq -c | sort -nr | head -10
     32 Sharma Hardware
     32 Green Leaf Hotels
     29 Metro Mart
     25 Northgate Distributors
     25 Fresh Bowl Kitchens
     21 Harbour Traders
     21 Coastal Foods
     20 Deccan Packaging
     16 Spice Route Restaurants
     16 Evergreen Mart
```

Field 4 is the customer name. The same warning as before: this works because no customer name contains a comma.

**6.**

```
# terminal, in ~/ch34/practice
$ awk -F, 'FNR > 1 { total += $11 } END { printf "%.2f\n", total }' ../sales_lines_2025.csv
4335471.00
```

₹43,35,471.00, matching Chapter 13's total for 2025 to the rupee. ✓

**7.**

```
# terminal, in ~/ch34/practice
$ awk -F, 'FNR > 1 { revenue[$6] += $11 } \
    END { for (s in revenue) printf "%-12s %12.2f\n", s, revenue[s] }' \
    exports/orders_2025-12-*.csv | sort -k2 -nr
Wholesale       205238.50
Hospitality     131080.00
Retail          103505.00
```

The three segments add up to December's ₹4,39,823.50. ✓

**8.**

```
# terminal, in ~/ch34/practice
$ for f in exports/orders_2025-12-*.csv; do \
    [[ $(wc -l < "$f") -eq 1 ]] && basename "$f"; \
  done | head -5
orders_2025-12-02.csv
orders_2025-12-03.csv
orders_2025-12-06.csv
orders_2025-12-07.csv
orders_2025-12-09.csv

$ find exports -name "orders_2025-12-*.csv" -size -125c | sort | wc -l
17
```

In the loop, `basename` strips the folder from a path, leaving the file name. A file with only a header is 1 line and 123 bytes (122 characters and the line ending), so `-size -125c` (smaller than 125 bytes) finds them, and no file with an order in it is that small. The loop is clearer; the `find` version is shorter and depends on knowing the header's exact length, which is the kind of assumption that breaks when a column is added.

**9.**

```
# terminal, in ~/ch34/practice
$ grep WARNING logs/report.log > /tmp/warnings.txt

$ wc -l < /tmp/warnings.txt
37
```

`wc -l < file` reads from standard input, so `wc` never learns the file's name and prints only the number. `wc -l /tmp/warnings.txt` would print `37 /tmp/warnings.txt`, which is awkward inside `$( … )`.

**10.**

```bash
#!/usr/bin/env bash
# weekly_summary.sh 2025-12-15
set -euo pipefail

MONDAY="${1:?usage: $0 YYYY-MM-DD (a Monday)}"
TOTAL=0

for offset in 0 1 2 3 4 5 6; do
    DAY=$(date -d "$MONDAY + $offset days" +%F)      # macOS: date -j -v+"$offset"d -f %Y-%m-%d "$MONDAY" +%F
    LINE=$(./daily_summary.sh "$DAY")
    echo "$LINE"
    REVENUE=${LINE##*revenue }
    TOTAL=$(awk -v a="$TOTAL" -v b="$REVENUE" 'BEGIN { printf "%.2f", a + b }')
done

echo "week of $MONDAY: revenue $TOTAL"
```

```
# terminal, in ~/ch34/practice
$ cp ../weekly_summary.sh . && chmod +x weekly_summary.sh

$ ./weekly_summary.sh 2025-12-15
2025-12-15: order lines 0, customers 0, revenue 0.00
2025-12-16: order lines 7, customers 3, revenue 89800.00
2025-12-17: order lines 2, customers 1, revenue 37628.00
2025-12-18: order lines 2, customers 1, revenue 23850.00
2025-12-19: order lines 1, customers 1, revenue 5750.00
2025-12-20: order lines 0, customers 0, revenue 0.00
2025-12-21: order lines 1, customers 1, revenue 2755.00
week of 2025-12-15: revenue 159783.00
```

`date -d "$MONDAY + $offset days" +%F` works out each day of the week (`-d` gives `date` a date to use instead of today; on macOS, the `date -j -v` form in the comment does the same). `${LINE##*revenue }` strips everything up to the last "revenue ", one of the shell's parameter expansions, leaving the number. `awk -v a="$TOTAL"` hands a shell variable to awk as the awk variable `a`, and `BEGIN { … }` runs before any input is read, so awk works as a calculator. The total uses `awk` because bash's arithmetic is whole numbers only, which is a good sign that anything more complicated belongs in Python.

**11.**

```
# terminal, in ~/ch34/practice
$ awk -F, 'FNR > 1 { printf "%12.2f  %s  %-20s %s\n", $11, $2, $4, $8 }' \
    ../sales_lines_2025.csv | sort -nr | head -3
    56700.00  2025-09-13  Deccan Packaging     Industrial Crate
    51520.00  2025-12-08  Northgate Distributors Industrial Crate
    51520.00  2025-10-13  Harbour Traders      Industrial Crate
```

Printing the sort key first and sorting numerically is the usual shell pattern for a top-N. The largest single order line is ₹56,700: 45 Industrial Crates to Deccan Packaging on 13 September. (Chapter 13's biggest *order*, ₹86,615 on 22 November, is several lines added together, which is the grain difference from Chapter 28 showing up in a shell pipeline.)

**12.**

```
# terminal, in ~/ch34/practice
$ python3 ../daily_file_server.py > /tmp/server.log 2>&1 &

$ sleep 1; for d in 01 02 03 04 05; do \
    curl --silent --output /dev/null --write-out "%{http_code}\n" \
    "http://127.0.0.1:8034/exports/orders_2026-01-$d.csv"; \
  done | sort | uniq -c
      5 404

$ kill %1
```

All five are 404: the server only has November and December 2025. A script that didn't check the status would have saved five files containing the words "not found".

**13.**

<!-- run: none -->
```
# terminal, in ~/ch34/practice
$ ssh reportserver "mkdir -p /tmp/nov"

$ scp exports/orders_2025-11-*.csv reportserver:/tmp/nov/

$ ssh reportserver "cat /tmp/nov/*.csv | wc -l"
65

$ cat exports/orders_2025-11-*.csv | wc -l
65
```

Both 65, so nothing was lost. For many files or a slow connection, `rsync -a exports/orders_2025-11-*.csv reportserver:/tmp/nov/` is the better tool, and the same command with `-anv` shows what it would do first.

**14.** With `DIR` unset, `cd $DIR` expands to plain `cd`, which succeeds and moves to the home folder. The `&&` then runs `rm -rf *` there, deleting everything the user owns. Two changes make it safe:

<!-- run: none -->
```bash
set -euo pipefail                 # -u makes an unset variable an error
cd "${DIR:?DIR is not set}" && rm -rf -- ./*
```

`"${DIR:?message}"` stops with a message if `DIR` is empty or unset, the quotes handle spaces, and `--` stops a file named like an option from being read as one. Better still, delete by pattern (`rm -f ./*.tmp`) rather than everything.

**15.** Cron runs with a minimal environment: a short `PATH` (often just `/usr/bin:/bin`), no `~/.bashrc`, no activated virtual environment, and a different current folder. So `python3` in the crontab is the system's Python, which doesn't have the packages you installed into `.venv`. Two fixes: call the environment's Python by its full path (`/home/meera/analyst-to-architect/.venv/bin/python report.py`, as Chapter 20's crontab does), or set `PATH=` at the top of the crontab or the script so the environment's `bin` folder comes first. A third, often best: have cron run a small wrapper script that sets the environment explicitly, so the job doesn't depend on anyone's login setup.

**16.** `grep` is right for a quick look and a quick count on data you trust: *"how many of these 61 files mention Metro Mart, and which ones"* took one command and no parsing. It's a trap when the answer has to be correct in a published number and the data can contain commas, quotes, or newlines inside fields, or when the match could appear in the wrong column: `grep -c Storage ../sales_lines_2025.csv` counts lines where *any* field contains "Storage", including a product name and a category, which is not the same as "order lines in the Storage category". For that, use `awk -F, '$9 == "Storage"'`, or pandas.

---

## Where this leads

- **Chapter 29, Python as Software, Not Scripts,** takes over when a shell script grows logic: it runs with the same exit codes, environment variables, and HTTP ideas you've just used.
- **Chapter 32, Analytics Engineering with dbt,** is a command-line tool end to end.
- **Chapter 46, Pipelines & Orchestration,** and **Chapter 49, Storage, Warehouses & Lakehouses,** run on machines you reach only this way.
- **Chapter 52, The Cloud, Containers & Infrastructure as Code,** builds on IP addresses, ports, and SSH keys for virtual machines and networks.
- **Chapter 77, Data Engineering & Data System Design Bank,** asks about permissions, exit codes, and debugging a failed job.
- **Looking back:** Chapter 20's `cron` lines and Chapter 26's Git commands are commands you now understand end to end.
