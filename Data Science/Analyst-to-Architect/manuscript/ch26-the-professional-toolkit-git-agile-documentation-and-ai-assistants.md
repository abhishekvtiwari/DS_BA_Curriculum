# Chapter 26. The Professional Toolkit: Git, Agile, Documentation & AI Assistants

*Part 2 — The Analyst*

> **Chapter at a glance**
>
> **You will learn to:** use the terminal with confidence: move around, make and copy files, read any command, chain commands, and set environment variables · explain what version control solves, and why "final_v3_REALLY_FINAL.xlsx" is a symptom · create a repository and record work in it with `git add`, `git commit`, and `git log` · read `git status` and `git diff` and say exactly what each line means · keep secrets and generated files out of a repository with `.gitignore` and a `.env` file · undo the four things that go wrong, and know which of the four you are in before you type anything · use a branch to try something without breaking what works, and resolve a conflict · push to GitHub, open a pull request, and review someone else's · add one automated check that runs on every push · write a README that lets a stranger run your work · keep a SQL pattern library and documentation that people can still find in six months · work inside Scrum and Kanban, and read a Jira board without being told · use an AI assistant at work: what to delegate, how to check what it gives you, and what must never be pasted into one.
>
> **Before you start:** Chapter 17, section 17.0 (you have opened a terminal, moved around in it, and run Python from it). Chapters 12 and 13 (the SQL you will be versioning), Chapters 17 and 18 (the Python scripts), Chapter 20 (the automated report), and Chapter 25 (user stories and business rules, which sections 26.9 and 26.10 refer to). This chapter installs Git. Nothing here needs a paid account.
>
> **Time needed:** 9–11 hours, including the exercises and the project, in three sittings: sections 26.0 to 26.6, the terminal and Git on your own computer (3–4 hours, typing along); sections 26.7 to 26.9, GitHub, the automated check, and the README (2–3 hours); sections 26.10 and 26.11 and the project (3–4 hours).
>
> **Tools:** Git 2.23 or later (for `git switch` and `git restore`), a free GitHub account, and VS Code from Chapter 17. Every command in this chapter was run on Git 2.43.0 on Linux; the commands are identical on macOS and in Git Bash on Windows.
>
> **Practice data:** none new. You will version the work you have already done in Part 2: the queries from Chapters 12 and 13, the scripts from Chapters 17, 18, and 20. The worked example is one SQL file, `monthly_revenue.sql` in the companion folder `ch26/`, built from nothing to a small shared repository.

---

## Why this matters

Chapter 2 introduced Imran's Friday file: one spreadsheet, on one laptop, that only one person knew how to update, and that stopped when he took leave. Every chapter since has quietly added to the same pile. By now you have queries in Chapter 12, a pattern library in Chapter 13, workbooks in Chapters 10 and 11, cleaning queries and workbooks in Chapter 14, cleaning code in Chapter 18, a report script in Chapter 20, and a dashboard in Chapter 16.

Where are they?

If the honest answer is "in a folder, some of them with a date in the name", then you have the Friday file problem at a larger scale. This chapter fixes it, and it fixes three other things at the same time, because they are the same problem wearing different clothes:

- **Nobody can run your work but you.** A repository with a README is the difference between a script and a thing your colleague can use on Monday.
- **Nobody can see how the team is doing.** Agile, and the board it runs on, is how data work gets planned in most companies you will join.
- **Nobody can check what an AI assistant produced.** You will use one. The skill is not prompting; it is knowing what to hand over and how to verify what comes back.

This is the chapter that turns a person who can analyze data into a person who can be hired to do it on a team. Nearly twenty chapters of this book point here, which is a fair signal of how much of the day-to-day it covers.

---

## In plain English

Version control is a laboratory notebook for files.

A scientist does not erase yesterday's page and write over it. They write today's entry underneath, dated and signed, with a note saying what changed and why. Every page is kept. If Thursday's experiment was wrong, you turn back to Wednesday and see exactly what was different. If two people work on the same project, each writes in their own notebook and they reconcile the pages afterward.

Git is that notebook for files. It does not save every keystroke. It saves **the snapshots you decide are worth keeping**, each with a note from you saying what changed. And because it keeps them all, you can go back, compare two days, or undo a change made three weeks ago without losing anything made since.

The reason people find it hard is not the idea. It is that Git keeps files in **three places at once**, and almost every confusing error message is Git telling you which of the three it is talking about.

Git is a program you type commands to, in a terminal. So the chapter starts there.

---

## 26.0 The terminal in 20 minutes

Chapter 17, section 17.0, gave you the minimum terminal: open one, see where you are with `pwd`, list with `ls` (and `ls -a` for hidden names), move with `cd` and `cd ..`, use Tab, the up arrow, and `Ctrl+C`, and run a program such as `python check_setup.py`. This section adds everything else this chapter types. Reading it takes about twenty minutes; with the install and the drill at the end, allow an hour.

### Step 0. Install Git

Git is free and comes from its official website, git-scm.com.

- **Windows:** download **Git for Windows** and run the installer. Accept the defaults on every page except two. On *Choosing the default editor used by Git*, the default is Vim, an editor that is hard to leave if you've never used it; choose **Use Visual Studio Code as Git's default editor** (or Nano). On *Adjusting the name of the initial branch in new repositories*, choose **Override the default branch name for new repositories** and type `main`. Leave Git Credential Manager ticked: it handles signing in to GitHub in section 26.7. The installer also installs **Git Bash**, the terminal this chapter uses on Windows.
- **macOS:** open Terminal and run `xcode-select --install`, which installs Apple's command line tools, Git among them. Apple's Git is a little older than the newest release, and every command in this chapter runs on it. (If you use Homebrew, `brew install git` gets the newest one.)
- **Linux:** install your distribution's `git` package; on Ubuntu, `sudo apt install git`.

Then check it, in a new terminal:

```
# terminal
$ git --version
git version 2.43.0
```

Yours may show a newer number: the current release is Git 2.56, from 27 September 2026. Anything from 2.23 on runs every command in this chapter.

### Which terminal

| Your computer | The terminal for this chapter |
|---|---|
| macOS | Terminal. Its shell is **zsh**, and everything here works in it |
| Linux | your usual terminal. Its shell is usually **bash** |
| Windows | **Git Bash**, from the Start menu, or inside VS Code (below). It runs **bash**, the same shell as Linux |

A **shell** is the program inside the terminal window that reads your commands and runs them; bash and zsh are two shells that agree on everything in this chapter. In VS Code, open the built-in terminal (`` Ctrl+` ``), click the small arrow next to the `+` at the top of the terminal panel, and choose **Git Bash**; *Terminal: Select Default Profile* in the command palette makes it the one that opens every time.

Why not PowerShell, which Chapter 17 used on Windows? It runs every `git` command in this chapter, but several of the other commands are written differently in it, so the book's pages won't match your screen. For the record, Microsoft's PowerShell documentation gives these equivalents:

| To do this | bash (macOS, Linux, Git Bash) | Windows PowerShell |
|---|---|---|
| list hidden files too | `ls -a` | `ls -Force` |
| set an environment variable | `export NAME=value` | `$env:NAME = "value"` |
| the last program's exit code | `echo $?` | `$LASTEXITCODE` (`$?` is only `True` or `False`) |
| run the next command only if this one worked | `&&` | `&&` in PowerShell 7; not in Windows PowerShell 5.1 |
| activate a virtual environment | `source .venv/Scripts/activate` (Git Bash) | `.venv\Scripts\Activate.ps1` |

### How to read the book's terminal blocks

You saw the format in Chapter 17. In full:

- **`$ `** at the start of a line is the prompt: type what comes after it, not the `$`.
- **Lines without `$`** are the output. If a command prints nothing, the next line is the next `$`.
- **The first line, starting with `# terminal`,** says where the session runs. It is a label, not something to type.
- **Words in angle brackets,** such as `<file>`, `<hash>`, `<url>`, or `<branch>`, are placeholders: replace them, brackets and all, with your own value.
- **Your output will differ in small ways**: your user name and folders, dates, and the **hashes** Git gives each snapshot (section 26.2). Copy those from your own screen, never from the book.

### Reading a command

Every command has the same shape: the **program** to run, then **options** that change how it works, then **arguments** that say what to work on.

![The command git log --oneline -n 2 broken into its parts: git is the program, log is the subcommand, --oneline is a long option, -n 2 is a short option with a value, and a note that an argument such as a file name would come last](figures/fig26-1-anatomy-of-a-command.svg)

*Figure 26.1 — A program, then options, then arguments. Git adds one layer: the word after `git` says which of its commands to run.*

- **Short options** are one dash and one letter: `-m`, `-n 2`, `-a`. Some take a value, written after them (`-n 2`: two commits).
- **Long options** are two dashes and a word: `--oneline`, `--staged`, `--global`. They say the same kind of thing more readably.
- **Arguments** come last. **Put quotes around anything with spaces**: `git commit -m "Add monthly revenue query"` is one message, not four words.
- **Commands are case-sensitive**: `git Log` is not `git log`, and on Linux `Exports` is a different folder from `exports`.

### Folders and files

A **path** says where something is. `/home/meera/riverstone-analysis` is **absolute**: it starts at `/`, the top of the whole disk. `sql/reports` is **relative**: it starts from the folder you're in. Three shorthands: **`~`** is your home folder, **`..`** is the folder above, and **`.`** is this folder (as in `git add .`, "everything here"). Folders are separated by `/`. In Git Bash on Windows, your `C:` drive is `/c`, so `C:\Users\Meera` is `/c/Users/Meera`.

Practise in a throwaway folder in your home folder, so nothing you care about is at risk:

```
# terminal
$ cd ~

$ mkdir terminal-drill

$ cd terminal-drill

$ pwd
/home/meera/terminal-drill

$ mkdir -p sql/reports

$ touch notes.txt

$ ls
notes.txt
sql
```

- **`mkdir terminal-drill`** makes a folder (*make directory*). **`mkdir -p sql/reports`** makes a folder inside a folder in one go; `-p` also makes any missing folder on the way, and doesn't complain if it already exists.
- **`touch notes.txt`** makes an empty file. It's the easiest way to make a file whose name starts with a dot, such as `.gitignore`, which Windows Explorer resists.

Now put some text in a file, look at it, copy it, move it, and delete it:

```
# terminal
$ echo "scratch" > notes.txt

$ cat notes.txt
scratch

$ cp notes.txt notes_copy.txt

$ mv notes_copy.txt sql/reports/

$ ls sql/reports
notes_copy.txt

$ rm sql/reports/notes_copy.txt

$ ls sql/reports
```

- **`echo "scratch"`** prints its text, and **`>`** (Chapter 17) sends that into `notes.txt` instead of the screen, replacing whatever was in the file.
- **`cat notes.txt`** prints a file. For anything longer than a screen, **`less notes.txt`** shows it a page at a time: Space for the next page, `q` to quit.
- **`cp`** copies (`cp from to`). **`mv`** moves, and also renames: `mv old.sql new.sql`. Moving into a folder keeps the name.
- **`rm`** deletes. **There is no recycle bin and no undo.** Run `ls` on the same name first, look at what it lists, then change `ls` to `rm`. The same rule covers whole folders: never delete a repository folder whose work you haven't pushed (section 26.7).

Files whose names start with a dot are **hidden**: plain `ls` skips them, and `ls -a` shows them. Git's own files are all dot-files (`.git`, `.gitignore`, `.github`), and so is `.env` (section 26.4).

```
# terminal
$ touch .env

$ ls
notes.txt
sql

$ ls -a
.
..
.env
notes.txt
sql
```

(`.` and `..` in the list are this folder and the one above; every folder lists them.)

### When the terminal seems stuck

- **A long output stops with a `:` at the bottom.** Git shows long logs and diffs through `less`: Space pages on, `q` quits.
- **A command is still running and you want it gone:** `Ctrl+C`.
- **Git opened an editor and is waiting.** Some Git commands ask you to type a message. If you chose VS Code in the installer (or in section 26.2), a tab opens: type the message, save, and close the tab. If you see a screen full of `~` signs, you are in **Vim**: press `Esc`, then type `:q!` and Enter to leave without saving, or `:wq` and Enter to save and leave. In **nano**, the keys are at the bottom: `Ctrl+O` then Enter saves, `Ctrl+X` leaves.
- **The screen is cluttered:** `clear`.

### Chaining commands, and exit codes

Every command ends with an **exit code**, a number the terminal keeps: **0 means it worked**, anything else means it failed. `$?` holds the last one, and `echo` prints it:

```
# terminal
$ ls sql
reports

$ echo $?
0

$ ls nothing-here
ls: cannot access 'nothing-here': No such file or directory

$ echo $?
2
```

`ls` exits with 2 when it can't find what you asked for. You'll rarely type `echo $?`, but programs read these numbers all the time: section 26.8's automated check fails exactly when one of its commands exits with something other than 0. **`&&`** uses them too. It runs the next command only if the one before it worked:

```
# terminal
$ cd sql && ls
reports

$ cd ..
```

### Environment variables

An **environment variable** (Chapter 17) is a named value the terminal hands to every program it starts. `echo` shows one when you put `$` in front of its name, and **`export`** sets one for this terminal session:

```
# terminal
$ echo $HOME
/home/meera

$ export REPORT_MONTH=2026-01

$ echo $REPORT_MONTH
2026-01
```

No spaces around the `=`. A variable set with `export` lasts until you close the terminal. Chapters 18 and 20 kept settings like the database address in a **`.env`** file instead, one `NAME=value` per line. Python reads that file with python-dotenv's `load_dotenv()` (Chapter 18); bash reads it with one line, the one Chapter 20 used in its crontab:

```
# terminal
$ echo "REPORT_MONTH=2026-02" > .env

$ set -a; . ./.env; set +a

$ echo $REPORT_MONTH
2026-02
```

- **`. ./.env`** runs the file's lines in this terminal, so `REPORT_MONTH=2026-02` sets the variable. (`.` here is a command, "read this file"; `./.env` is the file in this folder.)
- **`set -a`** first switches on "export everything I set", so the programs you start see the variables too; **`set +a`** switches it off again. The `;` separates commands on one line.

Programs you run pick up variables like these. Running a program is what Chapter 17 taught: `python check_setup.py`, or a script with arguments after its name, such as `python monthly_report.py 2025-12` for Chapter 18's report. (`python --version` in an activated environment; `python3` on macOS and Linux before you activate one.)

### The drill, and where this chapter starts

Clean up the drill folder, then make the folder this chapter works in and put the chapter's one file in it. On Windows, remember that `~` is your home folder in Git Bash.

```
# terminal
$ cd ~

$ rm -r terminal-drill

$ mkdir riverstone-analysis && cd riverstone-analysis

$ cp ~/analyst-to-architect/companion/ch26/monthly_revenue.sql .

$ ls -a
.
..
monthly_revenue.sql

$ cat monthly_revenue.sql
-- Monthly net revenue (sales_lines excludes cancelled orders)
SELECT date_trunc('month', order_date) AS mon,
       SUM(net_revenue)                AS revenue
FROM   sales_lines
GROUP  BY mon
ORDER  BY mon;
```

- **`rm -r`** deletes a folder and everything inside it (`-r` for *recursive*). Same warning, doubled.
- **`cp … .`** copies the file into `.`, the folder you're in.

`monthly_revenue.sql` is a PostgreSQL query on Chapter 13's `sales_lines` view (section 13.2): net revenue by month. `date_trunc('month', order_date)` turns each date into the first of its month; on MySQL, line 2 becomes `DATE_FORMAT(order_date, '%Y-%m-01')` (Chapter 13, section 13.8). The first line is a comment saying what the query answers, a habit this chapter will keep asking for.

**Checkpoint.** You can say what `pwd`, `ls -a`, `cd ..`, `mkdir -p`, `touch`, `cp`, `mv`, `rm`, `cat`, `echo … >`, `&&`, `export`, and `echo $?` do, and your terminal is in `riverstone-analysis` with one file in it.

> **Try it: load the full dataset from the terminal.** Chapter 14 loaded the full Riverstone dataset through DBeaver, with scripts of `INSERT` statements. The companion folder `full/terminal/` has faster versions that read the CSV files directly (its `README.md` explains them). From the companion's `full` folder:
>
> ```
> # terminal
> $ cd ~/analyst-to-architect/companion/full
>
> $ psql -U postgres -d riverstone_full -f terminal/riverstone_full_setup_postgresql.sql
> DROP VIEW
> DROP TABLE
> CREATE TABLE
> …
> COPY 116194
> COPY 209006
> …
> CREATE VIEW
> ANALYZE
> ```
>
> `psql` is PostgreSQL's command-line program, installed with the server in Chapter 12, section 12.3. `-U postgres` logs in as the `postgres` user, so it first asks for that password; `-d` names the database and `-f` the file of SQL to run. It prints one line per statement: `COPY 116194` is 116,194 orders loaded, and `COPY 209006` the order lines (the `…` marks lines left out here). The first time, it also prints a few `NOTICE` lines saying there were no tables yet to drop; that's fine. If Git Bash says `psql: command not found`, type its full path in quotes instead of `psql`, for example `"/c/Program Files/PostgreSQL/16/bin/psql"` (change `16` to your version). The MySQL version is `mysql --local-infile=1 -u root -p < terminal/riverstone_full_setup_mysql.sql`; it needs local file loading allowed on the server too (`SET GLOBAL local_infile = 1;`, run once as root), and it **deletes and rebuilds the whole `riverstone_full` database**, including tables you added to it in later chapters. The same idea loads Chapter 14's raw exports: from `companion/ch14`, `psql -d riverstone_full -f sql/terminal/ch14_load_postgresql.sql`.

---

## 26.1 The three places a file lives

Before any Git commands, the mental model. It is the whole of Git's difficulty and it takes two minutes.

![Three boxes, working directory, staging area, and repository, with the commands that move a file between them and the commands that inspect each](figures/fig26-2-three-places.svg)

*Figure 26.2 — Every Git command you will use in this chapter moves a file between two of these, or shows you the difference between two of them.*

| Place | What it holds | How to see it |
|---|---|---|
| **The working directory** | the files as they are on your disk right now, including edits you have not recorded | open the file, or `git diff` |
| **The staging area** | the changes you have chosen to include in the *next* snapshot | `git diff --staged`, or `git status` |
| **The repository** | every snapshot you have ever recorded, with its note and its author | `git log` |

`git add` moves a change from the working directory into the staging area. `git commit` turns everything in the staging area into a permanent snapshot in the repository.

**Why staging exists at all**, because this is the part beginners find fussy: it lets you record *some* of your changes. You fixed a query and, while you were in there, changed a comment in a different file. Those are two different things, and a history where each snapshot does one thing is a history you can read later. Staging is how you separate them.

---

## 26.2 Your first repository

**The question:** I have a SQL file I care about. How do I start keeping its history?

**The plan, in words.** Tell Git who you are, once. Make the folder a repository. Ask Git what it can see. Choose the file for the next snapshot. Take the snapshot with a note. Then look at the history.

### One-time setup

Git stamps every snapshot with a name and an email address, so it needs yours before the first one. Five settings, typed once per computer, in the `riverstone-analysis` folder from section 26.0 (or anywhere):

```
# terminal, in ~/riverstone-analysis
$ git config --global user.name "Meera Iyer"

$ git config --global user.email "meera@riverstone.example"

$ git config --global init.defaultBranch main

$ git config --global core.editor "code --wait"

$ git config --global pull.rebase false

$ git config --global --list
user.name=Meera Iyer
user.email=meera@riverstone.example
init.defaultbranch=main
core.editor=code --wait
pull.rebase=false
```

**How it works:**

- **`git config`** changes Git's settings. **`--global`** means "for every repository on this computer", stored in a file called `.gitconfig` in your home folder. Without it, a setting applies to the current repository only.
- **`user.name`** and **`user.email`** are stamped on every commit you make. Use your own. Once you push to GitHub they are visible to anyone who can see the repository, so use the email address of your GitHub account (or the private "no-reply" address GitHub offers in its email settings).
- **`init.defaultBranch main`** makes new repositories start on a branch called `main`, the name GitHub uses (branches are section 26.6). Without it, Git 2.43 calls the first branch `master`, and section 26.7's `git push -u origin main` fails. If you already made a repository on `master`, `git branch -m master main` renames it.
- **`core.editor "code --wait"`** makes VS Code the editor Git opens when it needs you to type a message. **`--wait`** tells Git to wait until you close that tab. On macOS, run *Shell Command: Install 'code' command in PATH* from VS Code's command palette first, so the terminal can find `code`. (If you prefer nano, use `"nano"`.)
- **`pull.rebase false`** tells `git pull` (section 26.7) to merge other people's work into yours. Since Git 2.33, a pull stops and asks when both sides have new work, unless this is set.
- **`git config --global --list`** prints every global setting, one per line, so you can check what you typed.

### Make the folder a repository

```
# terminal, in ~/riverstone-analysis
$ git init
Initialized empty Git repository in /home/meera/riverstone-analysis/.git/

$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	monthly_revenue.sql

nothing added to commit but untracked files present (use "git add" to track)
```

**How it works:**

- **`git init`** creates a hidden folder called `.git` inside your current folder. That folder is the repository: the entire history lives there. Deleting it deletes the history and leaves your files alone.
- **`git status`** is the command you will type more than any other. It answers "what does Git see right now?" Read its three parts every time.
- **`On branch main`** names the line of history you are working on. Section 26.6 explains branches; for now, `main` is the only one.
- **`No commits yet`** means the repository is empty. You have a notebook with no pages.
- **`Untracked files`** means Git can see `monthly_revenue.sql` but is not watching it. Git never records a file until you tell it to, which is deliberate: your folder is full of things that should not be in the history.

Now choose the file and record it.

```
# terminal
$ git add monthly_revenue.sql

$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   monthly_revenue.sql

$ git commit -m "Add monthly revenue query"
[main (root-commit) 7cd29f8] Add monthly revenue query
 1 file changed, 6 insertions(+)
 create mode 100644 monthly_revenue.sql
```

**How it works:**

- **`git add monthly_revenue.sql`** moves that file's contents into the staging area. It prints nothing, which is Git's way of saying it worked.
- The heading changed from *Untracked files* to **`Changes to be committed`**. That is the staging area, and the file is now in it.
- **`git commit`** takes everything staged and writes it into the repository as one snapshot, called a **commit**.
- **`-m "Add monthly revenue query"`** attaches the note. Without `-m`, Git opens the editor you set above and waits for you to type the note there, save, and close it (section 26.0 has the way out of Vim, if that's what appears).
- **The first line of the reply** is the confirmation: the branch, the fact that this is the first commit in the repository (`root-commit`), and the commit's short **hash**, a unique name Git generates from the content. Yours will differ, because the hash includes the author and the time. Always copy a hash from your own screen.
- **`1 file changed, 6 insertions(+)`** counts lines, not files. Six lines were added.
- **`create mode 100644`** says a new file entered the history as a normal file, not a program to run. You can ignore it.

### The settings on `git commit`

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `-m "…"` | the note attached to this snapshot | `"Add monthly revenue query"` | leave it out and Git opens your editor and waits for you to type the note there |
| `-a` | stage every already-tracked file that changed, then commit | not used here | saves a `git add` step, but silently includes edits you may not have meant to include. New files are still not added |
| `--amend` | replace the previous commit instead of adding a new one | not used here | fixes a bad message or a forgotten file. Never use it on a commit you have already pushed: section 26.5 explains why |
| `--no-verify` | skip checks set up to run before each commit (called *hooks*; the pre-commit tool in the project's Tools table sets them up) | not used here | commits even when a check would have failed. Reach for it only when you know which check you are skipping and why |

### What a commit message should say

A commit message is written for the person who reads it in eight months, which is usually you.

| Instead of | Write |
|---|---|
| `update` | `Fix month grouping: revenue was landing in the wrong month for orders on the 1st` |
| `fixes` | `Exclude cancelled orders from the monthly report script` |
| `asdf` | *anything that says what changed* |

The shape that works: a short line saying what changed, in the present tense, specific enough to be useful in a list of fifty. If the *why* cannot be read from the change itself, put it in a second paragraph after a blank line.

---

## 26.3 Reading the history, and reading a change

Two commands, and the two questions they answer.

**The question:** what has been recorded, and what exactly did I change since the last snapshot?

```
# terminal
$ git log --oneline
7cd29f8 Add monthly revenue query
```

That is the whole history: one commit, shown as its short hash and its message (`--oneline`; section 26.6 shows what the other settings of `git log` do, once there is more history to look at). Now make a change, and look at it before recording it. Open `monthly_revenue.sql` in VS Code (`code monthly_revenue.sql`) and add one line after the `FROM` line, restricting the query to 2025 onward:

```sql
WHERE  order_date >= DATE '2025-01-01'
```

Save the file.

<!-- The edit above, made by the chapter's check (not printed):
```
# terminal
$ cp ~/analyst-to-architect/companion/ch26/steps/1_limit_2025.sql monthly_revenue.sql
```
-->

```
# terminal
$ git diff
diff --git a/monthly_revenue.sql b/monthly_revenue.sql
index 220551a..25ec8e0 100644
--- a/monthly_revenue.sql
+++ b/monthly_revenue.sql
@@ -2,5 +2,6 @@
 SELECT date_trunc('month', order_date) AS mon,
        SUM(net_revenue)                AS revenue
 FROM   sales_lines
+WHERE  order_date >= DATE '2025-01-01'
 GROUP  BY mon
 ORDER  BY mon;
```

**How it works:**

- **`git diff`** shows what changed in the working directory that is **not yet staged**. This is the single most useful habit in this chapter: run it before every commit and read what you are about to record.
- **`--- a/…`** is the file before, **`+++ b/…`** is the file after.
- **`@@ -2,5 +2,6 @@`** says this block starts at line 2 and was 5 lines long before, and starts at line 2 and is 6 lines long now.
- A line starting with **`+`** was added. A line starting with **`-`** was removed. A line starting with a space is unchanged and is shown for context.
- **`index …`** names the file's content before and after. You will rarely need it.

Now stage the change, and watch where it goes:

```
# terminal
$ git add monthly_revenue.sql

$ git diff

$ git diff --staged
diff --git a/monthly_revenue.sql b/monthly_revenue.sql
index 220551a..25ec8e0 100644
--- a/monthly_revenue.sql
+++ b/monthly_revenue.sql
@@ -2,5 +2,6 @@
 SELECT date_trunc('month', order_date) AS mon,
        SUM(net_revenue)                AS revenue
 FROM   sales_lines
+WHERE  order_date >= DATE '2025-01-01'
 GROUP  BY mon
 ORDER  BY mon;
```

`git diff` now prints nothing, and **`git diff --staged`** shows the change. They answer two different questions: `git diff` compares your files with the staging area, and `git diff --staged` compares the staging area with the last commit. That is why a change seems to vanish from `git diff` the moment you `git add` it: it has moved one place along. Record it:

```
# terminal
$ git commit -m "Limit the revenue query to 2025 onward"
[main 6705aff] Limit the revenue query to 2025 onward
 1 file changed, 1 insertion(+)
```

---

## 26.4 What must never go into a repository

A repository is public by default in your head, whatever its setting on GitHub. Two categories of file must stay out, and one of them will get someone fired eventually if this habit is not automatic.

**Secrets.** Passwords, API keys, connection strings, tokens. Chapter 18's report script reads the database address, password included, and Chapter 20's email step reads a mail password. These go in a file called **`.env`**, which stays on your machine, and the code reads them from there.

**Generated output.** Anything a script produces: exported CSVs, built workbooks, rendered charts, `__pycache__`. If it can be rebuilt by running the code, versioning it adds noise to every `git diff` and makes the repository large for no benefit.

**The question:** how do I tell Git to ignore these permanently?

Make a `.env` and an exports folder, as a real project has, and see what Git sees when nothing has been told to ignore them:

```
# terminal
$ echo "RIVERSTONE_DB=postgresql+psycopg://postgres:your-password@localhost:5432/riverstone_full" > .env

$ mkdir exports

$ touch exports/jan.csv

$ git status --short
?? .env
?? exports/
```

**`git status --short`** is the compact form: a two-letter code and a file name on each line. The first letter is the staging area, the second the working directory:

| Code | Means |
|---|---|
| `??` | untracked: Git can see it but isn't watching it |
| ` M` (a space, then M) | modified in the working directory, not staged |
| `M ` (M, then a space) | modified and staged |
| `A ` | a new file, staged |
| `MM` | staged, then modified again |

This is the moment where `git add .` would commit your database password.

Now create a file called `.gitignore` in the top of the repository (`code .gitignore`; section 26.0 showed why a dot-file is easiest to make from the terminal or the editor), with these lines:

```
# .gitignore
# Secrets: never commit these
.env

# Generated output: rebuildable, so not worth versioning
exports/
*.xlsx

# Local noise
.venv/
.ipynb_checkpoints/
__pycache__/
```

<!-- The file above, made by the chapter's check (not printed):
```
# terminal
$ cp ~/analyst-to-architect/companion/ch26/steps/2_gitignore.txt .gitignore
```
-->

(The first line, `# .gitignore`, is the book's label for the file; start your file at `# Secrets`.)

```
# terminal
$ git status --short
?? .gitignore
```

**How it works, line by line:**

- **A line beginning with `#`** is a comment. Use them. A `.gitignore` with no explanation becomes a file nobody dares change.
- **`.env`** matches that exact file name anywhere in the repository.
- **`exports/`** with a trailing slash matches a *directory* and everything inside it. Without the slash it would also match a file named `exports`.
- **`*.xlsx`** matches by pattern: every file ending in `.xlsx`, in any folder.
- **`.venv/`** is the virtual environment from Chapter 17: thousands of files, rebuilt from `requirements.txt` whenever it's needed, so it never goes in.
- After adding it, `.env` and `exports/` are gone from `git status`. The only untracked file left is `.gitignore` itself, which **should** be committed, because everyone working on the repository needs the same rules.

To check what a rule is actually doing, ask Git rather than guessing:

```
# terminal
$ git check-ignore -v .env exports/jan.csv
.gitignore:2:.env	.env
.gitignore:5:exports/	exports/jan.csv
```

Each line says which file, at which line number of `.gitignore`, matched which path (line 2 is `.env`; line 5 is `exports/`, counting comments and blank lines). If a file you expected to be ignored is not, this command tells you in one step whether the rule is wrong or whether the file was already tracked before the rule existed. Commit the rules:

```
# terminal
$ git add .gitignore

$ git commit -m "Add gitignore"
[main 3d7f427] Add gitignore
 1 file changed, 11 insertions(+)
 create mode 100644 .gitignore
```

That message is vague, on purpose: section 26.5 fixes it.

**The trap that catches everyone once.** `.gitignore` only affects files Git is **not already tracking**. If you committed `.env` last week and add the rule today, the file stays tracked and keeps being committed. You have to remove it from tracking explicitly with `git rm --cached .env`, commit that, and then change the password, because the old one is in the history and the history is what gets shared. And never use **`git add -f`** on a secret: `-f` forces Git to add a file that `.gitignore` would skip, which is how a password gets committed by someone who has been told once too often that Git is ignoring it.

**How the code reads a secret instead.** Chapter 18's report script does not contain the password. It reads the whole database address from the environment at runtime:

<!-- run: none -->
```python
import os
from dotenv import load_dotenv

load_dotenv()
url = os.environ["RIVERSTONE_DB"]
```

- **`load_dotenv()`** (python-dotenv, Chapter 18) reads the `.env` file in the current folder and puts each line into the environment, unless a variable of that name is already set.
- **`os.environ["RIVERSTONE_DB"]`** reads the variable, and fails loudly with a `KeyError` if it's missing, which is what you want. A missing password should stop the script, not produce a confusing connection error twenty lines later.

A shell script or a scheduled job loads the same file with the line from section 26.0:

```
# terminal
$ set -a; . ./.env; set +a

$ printenv RIVERSTONE_DB
postgresql+psycopg://postgres:your-password@localhost:5432/riverstone_full
```

**`printenv NAME`** prints one environment variable, proof that anything started from this terminal now sees it. (The password here is the placeholder `your-password`. Don't print a real one on a shared screen.)

Commit a **`.env.example`** instead of `.env`, with the names, and a value only where it is safe and the same for everyone (like `localhost`), so a colleague knows what they need to supply:

```
# .env.example
RIVERSTONE_DB=postgresql+psycopg://postgres:your-password@localhost:5432/riverstone_full
SMTP_HOST=localhost
SMTP_USER=
SMTP_PASSWORD=
```


You'll create it, in VS Code, and commit it in section 26.7.

---

## 26.5 Undoing things: which of the four are you in?

Most Git fear is undo fear. There are four situations, and the first thing to do is work out which one you are in, because the command for each is different and using the wrong one is how people lose work.

![Four panels, one per undo situation, each showing where the change currently lives and the single command that reverses it](figures/fig26-3-four-undos.svg)

*Figure 26.3 — Ask where the change is before asking how to undo it.*

### 1. You edited a file and want the last committed version back

The change is in the working directory only. Make a throwaway edit: add a line `-- test` at the end of `monthly_revenue.sql` and save it.

<!-- The edit above, made by the chapter's check (not printed):
```
# terminal
$ echo "-- test" >> monthly_revenue.sql
```
-->

```
# terminal
$ git diff
diff --git a/monthly_revenue.sql b/monthly_revenue.sql
index 25ec8e0..8541337 100644
--- a/monthly_revenue.sql
+++ b/monthly_revenue.sql
@@ -5,3 +5,4 @@ FROM   sales_lines
 WHERE  order_date >= DATE '2025-01-01'
 GROUP  BY mon
 ORDER  BY mon;
+-- test

$ git status --short
 M monthly_revenue.sql

$ git restore monthly_revenue.sql

$ git status --short
```

`git diff` shows exactly what you're about to throw away: always look first. ` M` (with a space before it) is "modified, not staged". The empty output after `git restore` is the point: the working directory matches the last commit again. **`git restore <file>`** overwrites the file on disk with the committed version. It is the one destructive undo in this list, because the edit was never recorded anywhere, so it is gone.

### 2. You staged something you did not mean to

The change is in the staging area. You meant to stage only your query, but typed `git add .` ("everything here") and also staged a scratch file:

```
# terminal
$ echo "scratch" > notes.txt

$ git add .

$ git status --short
A  notes.txt

$ git restore --staged notes.txt

$ git status --short
?? notes.txt
```

The file went from `A ` (a new file, staged) back to `??` (untracked), which is exactly what unstaging means: the file is still on disk, and Git has stopped planning to commit it. **`git restore --staged <file>`** moves a change out of the staging area and leaves the file alone. Nothing is lost. This is the safe undo, and it is the one you will use most. (Delete the scratch file with `rm notes.txt` when you're done.)

<!-- Clean-up, made by the chapter's check (not printed):
```
# terminal
$ rm notes.txt
```
-->

### 3. The last commit was wrong and you have not shared it

Section 26.4's last commit says only "Add gitignore". Replace its message with one that says what the rules do:

```
# terminal
$ git commit --amend -m "Ignore secrets, generated exports, and local noise"
[main 9dc9f0b] Ignore secrets, generated exports, and local noise
 Date: Mon Mar 2 10:23:00 2026 +0530
 1 file changed, 11 insertions(+)
 create mode 100644 .gitignore

$ git log --oneline
9dc9f0b Ignore secrets, generated exports, and local noise
6705aff Limit the revenue query to 2025 onward
7cd29f8 Add monthly revenue query
```

**`--amend`** replaces the previous commit with a new one. The old commit is not edited; it is discarded and a new one takes its place, with a new hash (compare the top line with section 26.4's). It keeps the original's date, which is why Git prints a `Date:` line. That is why the rule is absolute: **amend only a commit nobody else has.** Once a commit is pushed, somebody may have it, and replacing it makes their history and yours disagree in a way that takes an afternoon to sort out.

To add a forgotten file to the last commit rather than change the message: `git add the_file` then `git commit --amend --no-edit`, where `--no-edit` keeps the existing message.

### 4. A commit is already shared and is wrong

Now you cannot rewrite it. You add a new commit that undoes it. Nothing has been pushed yet (that's section 26.7), so pretend the 2025 filter had been; `revert` works the same on a private commit. Copy the filter commit's hash from **your own** `git log --oneline`; here it is the second one down:

```
# terminal
$ git revert --no-edit 6705aff
[main 75b063a] Revert "Limit the revenue query to 2025 onward"
 Date: Mon Mar 2 10:34:00 2026 +0530
 1 file changed, 1 deletion(-)

$ git log --oneline
75b063a Revert "Limit the revenue query to 2025 onward"
9dc9f0b Ignore secrets, generated exports, and local noise
6705aff Limit the revenue query to 2025 onward
7cd29f8 Add monthly revenue query
```

**How it works:**

- **`git revert <hash>`** looks at what that commit changed and creates a **new** commit doing the opposite. The original is still there, second from the bottom, which is the point: shared history is not edited, it is added to.
- **`--no-edit`** accepts the default message, `Revert "…"`, without opening an editor.
- **`Date:`** is when the new commit was made; yours will be today's.
- The history now records both the change and the decision to undo it. Somebody reading it in six months can see that the 2025 filter was tried and reversed, which is more useful than a history where it never happened.

| Where the change is | Command | Is anything lost? |
|---|---|---|
| Working directory only | `git restore <file>` | **yes**, the edit is gone. Run `git diff` first |
| Staging area | `git restore --staged <file>` | no, the file stays on disk |
| Last commit, not pushed | `git commit --amend` | the old commit is replaced. Safe if nobody has it |
| Any commit, already pushed | `git revert <hash>` | no, a new commit undoes it and both remain |

There is a fifth command, `git reset --hard`, which discards commits and working changes in one step. It is not in this table on purpose. Almost every situation where a beginner reaches for it is really situation 1, 2, or 4, and `--hard` is the one that loses work.

---

## 26.6 Branches, and why they are not an advanced topic

A **branch** is a movable label pointing at a commit. That is the whole definition, and it is why branches in Git are cheap enough to make casually.

**The question:** I want to try splitting the revenue query by product category, without breaking the version that currently works.

```
# terminal
$ git switch -c add-category-split
Switched to a new branch 'add-category-split'
```

**`git switch -c add-category-split`** creates a branch and moves onto it. **`-c`** means create; without it, `git switch` moves to a branch that already exists. Now change the file on this branch: add `category,` to the `SELECT` and to the `GROUP BY` and `ORDER BY` lines, so the whole file reads:

<!-- The edit, made by the chapter's check (not printed):
```
# terminal
$ cp ~/analyst-to-architect/companion/ch26/steps/3_category_split.sql monthly_revenue.sql
```
-->

```
# terminal
$ cat monthly_revenue.sql
-- Monthly net revenue (sales_lines excludes cancelled orders)
SELECT date_trunc('month', order_date) AS mon,
       category,
       SUM(net_revenue)                AS revenue
FROM   sales_lines
GROUP  BY mon, category
ORDER  BY mon, category;

$ git diff
diff --git a/monthly_revenue.sql b/monthly_revenue.sql
index 220551a..044e005 100644
--- a/monthly_revenue.sql
+++ b/monthly_revenue.sql
@@ -1,6 +1,7 @@
 -- Monthly net revenue (sales_lines excludes cancelled orders)
 SELECT date_trunc('month', order_date) AS mon,
+       category,
        SUM(net_revenue)                AS revenue
 FROM   sales_lines
-GROUP  BY mon
-ORDER  BY mon;
+GROUP  BY mon, category
+ORDER  BY mon, category;

$ git add monthly_revenue.sql

$ git commit -m "Split monthly revenue by product category"
[add-category-split a2a9885] Split monthly revenue by product category
 1 file changed, 3 insertions(+), 2 deletions(-)

$ git branch
* add-category-split
  main
```

- The diff shows three lines added and two removed: a changed line is always shown as the old line removed and the new one added.
- **`git branch`** lists the branches. The **`*`** marks the one you're on. `main` still points at the working version; your new commit went onto `add-category-split` only.

Now go back to `main`, and look at the file on disk:

```
# terminal
$ git switch main
Switched to branch 'main'

$ cat monthly_revenue.sql
-- Monthly net revenue (sales_lines excludes cancelled orders)
SELECT date_trunc('month', order_date) AS mon,
       SUM(net_revenue)                AS revenue
FROM   sales_lines
GROUP  BY mon
ORDER  BY mon;
```

The category split has gone from the file. It isn't lost: **`git switch main`** changed the files on disk to match `main`, and the new version is safe on the other branch. This is the moment branches make sense. Bring the work across:

```
# terminal
$ git merge add-category-split
Updating 75b063a..a2a9885
Fast-forward
 monthly_revenue.sql | 5 +++--
 1 file changed, 3 insertions(+), 2 deletions(-)

$ git log --oneline
a2a9885 Split monthly revenue by product category
75b063a Revert "Limit the revenue query to 2025 onward"
9dc9f0b Ignore secrets, generated exports, and local noise
6705aff Limit the revenue query to 2025 onward
7cd29f8 Add monthly revenue query
```

- **`git merge add-category-split`** brings that branch's commits into `main`.
- **`Fast-forward`** means `main` had no commits of its own since the branch started, so Git simply moved the label forward. When both branches have moved, Git makes a **merge commit** instead, which joins the two lines of history.

### When both sides changed the same line: a conflict

If both branches changed the same lines differently, Git can't choose, so it stops and asks you. That's a **merge conflict**, and it will happen to you at work, so here is one on purpose. Make a new branch, `git switch -c limit-to-2026`, and on it add a line after `FROM` that limits the query to 2026, `WHERE  order_date >= DATE '2026-01-01'`. Then commit:

<!-- The edit, made by the chapter's check (not printed):
```
# terminal
$ git switch -c limit-to-2026
Switched to a new branch 'limit-to-2026'

$ cp ~/analyst-to-architect/companion/ch26/steps/4_branch_2026.sql monthly_revenue.sql
```
-->

```
# terminal
$ git commit -am "Limit the revenue query to 2026"
[limit-to-2026 71747c9] Limit the revenue query to 2026
 1 file changed, 1 insertion(+)
```

(`-a` stages the changed file for you; the settings table in section 26.2 has the catch.) Now `git switch main`, where someone else has limited the same query to the second half of 2025, adding `WHERE  order_date >= DATE '2025-07-01'` in the same place. Commit that on `main`, and merge the branch in:

<!-- The edit, made by the chapter's check (not printed):
```
# terminal
$ git switch main
Switched to branch 'main'

$ cp ~/analyst-to-architect/companion/ch26/steps/5_main_2025h2.sql monthly_revenue.sql
```
-->

```
# terminal
$ git commit -am "Limit the revenue query to July 2025 onward"
[main 3abb427] Limit the revenue query to July 2025 onward
 1 file changed, 1 insertion(+)

$ git merge limit-to-2026
Auto-merging monthly_revenue.sql
CONFLICT (content): Merge conflict in monthly_revenue.sql
Automatic merge failed; fix conflicts and then commit the result.

$ cat monthly_revenue.sql
-- Monthly net revenue (sales_lines excludes cancelled orders)
SELECT date_trunc('month', order_date) AS mon,
       category,
       SUM(net_revenue)                AS revenue
FROM   sales_lines
<<<<<<< HEAD
WHERE  order_date >= DATE '2025-07-01'
=======
WHERE  order_date >= DATE '2026-01-01'
>>>>>>> limit-to-2026
GROUP  BY mon, category
ORDER  BY mon, category;
```

Git merged everything it could and stopped at the one line both sides changed, marking it in the file:

- **`<<<<<<< HEAD`** starts your side: the version on the branch you're on (`HEAD` means "where you are now", here `main`).
- **`=======`** separates the two sides.
- **`>>>>>>> limit-to-2026`** ends the other side: the version from the branch you're merging in.

To resolve it, edit the file into the version you want and delete all three marker lines. Here the decision is to keep the 2026 limit, so the `WHERE` line becomes `WHERE  order_date >= DATE '2026-01-01'` and the markers go. Then stage the file, which tells Git the conflict is settled, and commit:

<!-- The edit, made by the chapter's check (not printed):
```
# terminal
$ cp ~/analyst-to-architect/companion/ch26/steps/6_resolved.sql monthly_revenue.sql
```
-->

```
# terminal
$ git add monthly_revenue.sql

$ git commit --no-edit
[main af0da72] Merge branch 'limit-to-2026'
```

`--no-edit` keeps the message Git prepared, `Merge branch 'limit-to-2026'`, with a note of which file had the conflict (you'll see it in the log below); without it, the editor opens with that message filled in (save and close it). If you'd rather not resolve a conflict right now, **`git merge --abort`** puts everything back as it was before the merge.

### A measured what-if: the settings of `git log`

Now that the history has some shape, here is what `git log`'s settings actually do. Here are the same two most recent commits, two ways.

```
# terminal
$ git log -n 2
commit af0da72bad44c5beb418985d7aa1acc658ac481b
Merge: 3abb427 71747c9
Author: Meera Iyer <meera@riverstone.example>
Date:   Mon Mar 2 10:50:00 2026 +0530

    Merge branch 'limit-to-2026'
    
    # Conflicts:
    #       monthly_revenue.sql

commit 3abb427b53ce088a660c9240eed7ccddbb57686c
Author: Meera Iyer <meera@riverstone.example>
Date:   Mon Mar 2 10:47:00 2026 +0530

    Limit the revenue query to July 2025 onward

$ git log --oneline -n 2 --stat
af0da72 Merge branch 'limit-to-2026'
3abb427 Limit the revenue query to July 2025 onward
 monthly_revenue.sql | 1 +
 1 file changed, 1 insertion(+)
```

| Setting | What it means in plain words | What happens if you change it |
|---|---|---|
| `--oneline` | one line per commit: short hash and message only | leave it out and you get the full hash, author, date, and message, about five lines per commit |
| `-n 2` | show only the two most recent commits | raise it to see more, leave it out to see all of them |
| `--stat` | add which files changed and how many lines | leave it out and you see the messages only. Useful when you are looking for "which commit touched this file" |
| `--graph` | draw the branch structure as lines down the left | on a history with branches this is how you see what merged into what. On a straight history it adds nothing |
| `-p` | show each commit's full diff | long, but it is how you see exactly what a commit changed, or search old changes for a password (see Common mistakes) |

The first commit of the full log is the merge: `Merge:` lists the two commits it joined. With `--stat`, the merge shows no file list, because its changes came from the two commits it joins. You'll type some version of these settings most days, so give it a short name, an **alias**:

```
# terminal
$ git config --global alias.lg "log --oneline --graph -n 20"

$ git lg
*   af0da72 Merge branch 'limit-to-2026'
|\  
| * 71747c9 Limit the revenue query to 2026
* | 3abb427 Limit the revenue query to July 2025 onward
|/  
* a2a9885 Split monthly revenue by product category
* 75b063a Revert "Limit the revenue query to 2025 onward"
* 9dc9f0b Ignore secrets, generated exports, and local noise
* 6705aff Limit the revenue query to 2025 onward
* 7cd29f8 Add monthly revenue query
```

**`alias.lg`** makes `git lg` mean `git log --oneline --graph -n 20`. The graph shows the conflict's two lines of history joining at the merge commit. (Add `--stat` to the alias if you like the file list.)

**Why bother for solo work?** Because it lets you stop halfway. A branch is a place to leave an unfinished idea without it sitting in your working directory blocking everything else. And because when you join a team, every change will go through one.

**Naming.** `add-category-split`, `fix-cancelled-orders`, `meera/monthly-report`. Short, specific, and readable in a list.

---

## 26.7 GitHub, pushing, and the pull request

Everything so far has been local. Your history lives in `.git` in your folder and nowhere else, which solves the "which version is current" problem but not the "my laptop died" problem or the "Imran is on leave" problem.

**GitHub** is a hosting service for Git repositories. A repository hosted there is called a **remote**. There are others, GitLab and Bitbucket among them, and they work the same way. The rest of this chapter, and the project, need a free GitHub account.

### An account and an empty repository

1. **Sign up** at github.com and verify your email address.
2. **Turn on two-factor authentication** (*Settings → Password and authentication*), with an authenticator app on your phone. GitHub requires it of accounts that contribute code, and it's the right habit anyway.
3. **Create the repository:** the **+** menu at the top right, then *New repository*. Name it `riverstone-analysis`, choose **Private**, and leave **Add README**, **.gitignore**, and **license** all off. Click **Create repository**.
4. **Copy the HTTPS address** GitHub shows on the next page, `https://github.com/<your-user-name>/riverstone-analysis.git`.

Why empty? Your repository already has a history. If GitHub's copy starts with a README commit of its own, the two histories don't match, and your first push is rejected until you merge them.

### The first push

```
# terminal
$ git remote add origin https://github.com/meera/riverstone-analysis.git

$ git push -u origin main
To https://github.com/meera/riverstone-analysis.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

**How it works:**

- **`git remote add origin <url>`** records a nickname for the remote. **`origin`** is the conventional name for "the main place this repository lives". It is not a keyword; you could call it anything.
- **`git push`** sends commits the remote does not have. The last lines say a new branch `main` was created on GitHub.
- **`-u origin main`** sets the default, so that afterward plain `git push` and `git pull` know where to go. You need it once, on the first push.
- In your terminal, Git also shows progress lines while it sends (`Enumerating objects…`, `Writing objects: 100%…`); they don't matter.

**Signing in the first time.** GitHub stopped accepting account passwords for Git in 2021, so the first push needs a proper sign-in. GitHub's documentation ("Caching your GitHub credentials in Git") recommends one of two tools:

- **Windows:** Git Credential Manager, which came with Git for Windows. On the first push a window opens; choose to sign in with your browser, approve it, and you're done. It remembers you.
- **macOS and Linux:** install **GitHub CLI** (`brew install gh` on a Mac; on Linux, the install page at cli.github.com), then run `gh auth login` once and answer its questions: GitHub.com, HTTPS, yes to authenticating Git, and *Login with a web browser*. After that, `git push` just works.

If you're asked for a username and password in the terminal instead, don't type your GitHub password: it will be refused. Set up one of the two tools above.

Three commands cover the rest of normal use:

| Command | What it does |
|---|---|
| `git clone <url>` | copy an existing remote repository onto your machine, history and all |
| `git pull` | fetch what others have pushed and merge it into your branch |
| `git push` | send your commits to the remote |

### Pull before you push

While Meera was working locally, Farah added a README to the repository on GitHub. Meera, meanwhile, created the `.env.example` from section 26.4. She commits it and pushes.

<!-- Meera's .env.example from section 26.4, made by the chapter's check (not printed):
```
# terminal
$ printf 'RIVERSTONE_DB=postgresql+psycopg://postgres:your-password@localhost:5432/riverstone_full\nSMTP_HOST=localhost\nSMTP_USER=\nSMTP_PASSWORD=\n' > .env.example
```
-->

<!-- On github.com, Farah adds a README and commits it (simulated by the chapter's check, not printed):
```
# terminal
$ github-colleague-readme
```
-->

```
# terminal
$ git add .env.example

$ git commit -m "Add .env.example listing the settings to supply"
[main 3397cdb] Add .env.example listing the settings to supply
 1 file changed, 4 insertions(+)
 create mode 100644 .env.example

$ git push
To https://github.com/meera/riverstone-analysis.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/meera/riverstone-analysis.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

The push is **rejected**: GitHub has a commit Meera doesn't (Farah's), and accepting the push would throw it away. The rejection is Git preventing you from silently discarding someone's work. The fix is to **pull** first, which fetches Farah's commit and merges it with yours, then push:

```
# terminal
$ git pull
From https://github.com/meera/riverstone-analysis
   af0da72..d0dc58b  main       -> origin/main
Merge made by the 'ort' strategy.
 README.md | 3 +++
 1 file changed, 3 insertions(+)
 create mode 100644 README.md

$ git push
To https://github.com/meera/riverstone-analysis.git
   d0dc58b..78dc721  main -> main
```

Because both sides had new commits, `git pull` made a merge commit (`pull.rebase false` from section 26.2 is what told it to merge). It may open your editor with the message `Merge branch 'main' of https://github.com/…`: save and close it. Now `git log --oneline` shows Farah's commit, yours, and the merge that joins them.

### The pull request

On a team, nobody pushes straight to `main`. The flow is the same four steps everywhere. Figure 26.4 shows them, and the rest of this section does them for real.

![A branch leaving main, gaining commits, becoming a pull request with review comments and an automated check, then merging back into main](figures/fig26-4-pull-request-flow.svg)

*Figure 26.4 — Branch, commit, push, pull request, merge: the loop behind every change on a team.*

1. **Branch.** Make a branch for one piece of work.
2. **Commit and push.** Your work goes to the remote on that branch.
3. **Open a pull request.** On GitHub, propose merging your branch into `main`. A pull request is a request for review, a place for the conversation, and a record of why the change was made.
4. **Review, then merge.** Somebody reads it, comments, you change things, and it merges.

Steps 1 and 2 in the terminal. The change: add an order count next to the revenue, a `COUNT(DISTINCT order_id) AS orders` line in the `SELECT`.

```
# terminal
$ git switch -c add-order-count
Switched to a new branch 'add-order-count'
```

<!-- The edit, made by the chapter's check (not printed):
```
# terminal
$ cp ~/analyst-to-architect/companion/ch26/steps/7_order_count.sql monthly_revenue.sql
```
-->

```
# terminal
$ git commit -am "Add the number of orders to monthly revenue"
[add-order-count 05242c4] Add the number of orders to monthly revenue
 1 file changed, 1 insertion(+)

$ git push -u origin add-order-count
To https://github.com/meera/riverstone-analysis.git
 * [new branch]      add-order-count -> add-order-count
branch 'add-order-count' set up to track 'origin/add-order-count'.
```

`git push -u origin add-order-count` creates the branch on GitHub too. (GitHub also prints a few lines starting `remote:`, with a link to open a pull request.)

Step 3, on github.com, as GitHub's "Quickstart for pull requests" describes it:

1. Open the repository. A yellow banner shows your recently pushed branch: click **Compare & pull request**.
2. Check the two branches at the top: **base: main** (where the change goes) and **compare: add-order-count** (the change).
3. Write a title and a description (below), and click **Create pull request**.
4. The reviewer reads the **Files changed** tab, which shows the same diff as `git diff`, and comments on lines.

Step 4, on github.com: when the review is done, click **Merge pull request**, then **Confirm merge**, and then **Delete branch** to tidy up GitHub's copy of it.

<!-- On github.com, the pull request is merged (simulated by the chapter's check, not printed):
```
# terminal
$ github-merge-pr 1 add-order-count "Add the number of orders to monthly revenue"
```
-->

The merge happened on GitHub, so your own `main` doesn't have it yet. Bring it down, and delete your local copy of the finished branch:

```
# terminal
$ git switch main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.

$ git pull
From https://github.com/meera/riverstone-analysis
   78dc721..0248045  main       -> origin/main
Updating 78dc721..0248045
Fast-forward
 monthly_revenue.sql | 1 +
 1 file changed, 1 insertion(+)

$ git branch -d add-order-count
Deleted branch add-order-count (was 05242c4).
```

- **`git pull`** on `main` fetches the merge GitHub made (`Merge pull request #1 …`) and moves your `main` forward to it: a fast-forward, because you had nothing new of your own.
- **`git branch -d`** deletes a branch that has been merged. It refuses if the branch has work that isn't merged anywhere, which makes it safe to type.

**What a good pull request description contains**, and this matters more for data work than for most code: what changed, **why**, and how you checked it. "Fixed the revenue query" is not reviewable. "The monthly report script reads `orders` and `order_items` directly, not the `sales_lines` view, so cancelled orders were being counted. Excluded them. January 2026 drops from ₹1,16,210 to ₹1,04,210, the ₹12,000 of cancelled order 5004, which now matches the finance figure" is a description a reviewer can actually verify.

**What to look for when reviewing someone else's query**, which you will be asked to do:

- Does it answer the question in the description?
- Is the **grain** right? One row per what?
- Are cancelled, test, and internal records handled, or silently included?
- Do the numbers reconcile with something known?
- Would you be able to change this in six months?

---

## 26.8 One automated check on every push

A repository can run a check automatically whenever someone pushes. On GitHub this is called **GitHub Actions**, and the smallest useful version is worth the twenty minutes it takes to set up: it catches the broken thing before a reviewer wastes time on it. The check is described in a file written in **YAML**, so first, the three rules of YAML.

### YAML in two minutes

**YAML** is a plain-text format for settings, designed to be easy to read.

```yaml
name: checks                 # key: value, with a space after the colon
on: [push, pull_request]     # [a, b] is a list written on one line
jobs:                        # a key whose value is the indented block below it
  check:
    steps:
      - run: echo first      # "- " starts one item of a list
      - run: echo second
        with:                # belongs to the item above: indented further
          python-version: "3.14"   # quotes keep it as text
```

- **`key: value`** on each line, with a space after the colon. Everything after `#` is a comment.
- **Indentation is meaning.** A block indented under a key belongs to that key. Use **two spaces per level, never tabs**: YAML refuses tabs, and a wrong indent silently moves a line into the wrong block.
- **`- `** (a dash and a space) starts an item in a list; everything indented under it belongs to that item.
- **Quotes** keep a value as text. Unquoted, YAML reads `3.10` as the number 3.1.

### The workflow file

GitHub looks for workflow files in a folder called `.github/workflows` at the top of the repository. Make it with section 26.0's `mkdir -p`, then create the file in VS Code:

```
# terminal
$ mkdir -p .github/workflows

$ code .github/workflows/checks.yml
```

```yaml
name: checks
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.14"
      - run: python -m pip install -r requirements.txt
      - run: python -m compileall -q scripts
      - run: python scripts/monthly_report.py --help
```

**How it works, line by line:**

- **`name: checks`** is what appears on the pull request. Any name will do.
- **`on: [push, pull_request]`** is the trigger. This runs on every push and on every pull request.
- **`jobs:` then `check:`** declares one job named `check`. A workflow can have several, running in parallel.
- **`runs-on: ubuntu-latest`** asks GitHub for a fresh Linux machine. It is created for this run and destroyed afterward, which is why the next steps have to install everything.
- **`steps:`** run in order. A step is either a prepared action (`uses:`) or a command (`run:`).
- **`uses: actions/checkout@v7`** copies your repository onto that machine. Without it the machine is empty. The `@v7` pins the **major version** of the action, which is the difference between a workflow that keeps working and one that breaks when the action changes. Pin a major version, and update it about once a year, when GitHub announces that an old one is being retired. (Version 7 of both actions is current in September 2026; if you meet `@v4` or `@v5` in older workflows, they are the same actions, older.)
- **`actions/setup-python@v7` with `python-version: "3.14"`** installs that Python, the version Chapter 17 installed. Quote it, as above.
- **`run: python -m pip install -r requirements.txt`** installs your packages on the fresh machine, as Chapter 17 did on yours.
- **`run: python -m compileall -q scripts`** reads every `.py` file in `scripts/` and turns it into Python's internal form without running it, so it fails on any **syntax error**, such as a missing bracket. `-q` (quiet) prints only problems.
- **`run: python scripts/monthly_report.py --help`** starts Chapter 18's report script and asks for its help message. The script reads its arguments before it touches the database, so this proves it imports its packages and starts, without needing a password on GitHub's machine.
- **Red or green.** Each `run:` line is a command, and it ends with an exit code (section 26.0). If any command exits with anything other than 0, the check fails and the pull request shows a red cross; if all exit with 0, a green tick.

**Keep `requirements.txt` short.** Chapter 17 wrote it with `pip freeze`, which lists every package in your environment. A frozen list from a Windows computer includes Windows-only packages (`pywin32`, which Jupyter needs there) that cannot install on GitHub's Linux machine, so the check fails at the install step. For a repository, write `requirements.txt` by hand with just the packages your scripts import: for Chapter 18's report, `pandas`, `sqlalchemy`, `psycopg[binary]`, `python-dotenv`, and `xlsxwriter`, one per line, and add `matplotlib` when Chapter 20's Flash joins it.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `on:` | when the workflow runs | `[push, pull_request]` | narrow it to `[pull_request]` and pushes to your own branch stop burning minutes; add `schedule:` to run it nightly |
| `runs-on:` | which machine | `ubuntu-latest` | `windows-latest` or `macos-latest` cost more minutes. Use Linux unless you need otherwise |
| `python-version:` | which Python | `"3.14"` | set it to the version you actually develop on, or the check passes here and fails on your machine |
| `@v7` | which major version of the prepared action | pinned | leave the version off and you get whatever is newest, which changes under you without warning |

**What to put in this check for a data repository**, in order of value: does the Python import and run, do the tests pass, does a linter accept the SQL, and does a small query against a test database still return the expected number of rows. Chapter 29 extends this check to run your tests once you have some, Chapter 47 turns the last idea into proper data-quality testing, and Chapter 52 takes the whole workflow further into deployment.

---

## 26.9 A repository a stranger can run

The test: hand the URL to a colleague who has never seen it, say nothing, and see whether they get an answer within fifteen minutes. Everything in this section exists to pass that test.

### Structure

```
riverstone-analysis/
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── .github/
│   └── workflows/
│       └── checks.yml       ← section 26.8
├── sql/
│   ├── patterns/            ← the Chapter 13 pattern library, one file per pattern
│   │   ├── top_n_per_group.sql
│   │   ├── running_total.sql
│   │   └── gaps_and_islands.sql
│   └── reports/
│       └── monthly_revenue.sql
├── scripts/
│   ├── monthly_report.py    ← Chapter 18
│   └── daily_flash.py       ← Chapter 20
├── notebooks/
│   └── 2026-02-churn-exploration.ipynb
└── docs/
    └── metrics.md           ← the definitions from Chapter 23
```

Two things to copy. **One file per SQL pattern**, each with a comment at the top saying what question it answers, because a pattern library you cannot search is a file you rewrite. And **dates at the front of exploratory notebooks**, `2026-02-…`, so they sort in time order, the habit from Chapter 2. To get there from this chapter's flat folder, use section 26.0's commands: `mkdir -p sql/reports`, then `git mv monthly_revenue.sql sql/reports/`, which is `mv` that also tells Git the file moved.

### Files Git cannot diff

Git stores any file you give it, but it can only *show you the change* in a text file. A `.sql` file, a `.py` file, a `.md` file, a `.yml` file: all text, all diffable. An `.xlsx` workbook, a `.pbix` Power BI file, a `.docx`, a PNG: all binary. Git will happily version them, and every commit stores a whole new copy, so the repository grows and `git diff` tells you only "Binary files differ".

Three workable answers, in order of preference:

| File | What to do |
|---|---|
| Power BI | save in the **`.pbip` project format** instead of `.pbix`. It writes the model and the report as text files, which diff properly. Chapter 16 introduced it |
| Excel macros and VBA | **export the modules** (`.bas`, `.cls`, `.frm`) into a `vba/` folder and commit those, the habit from Chapter 19. The workbook itself stays out, or goes in as a single dated copy |
| A workbook or document that must be versioned as a whole | commit it, but accept that history is a chain of copies. Keep a `CHANGELOG.md` beside it saying what changed in each version, because Git cannot tell you |

And the blunt one: **data files do not belong in a repository at all.** A CSV export is regenerable, often large, and sometimes confidential. Commit the query that produces it.

### Markdown in ten lines

README files, `docs/metrics.md`, and `CHANGELOG.md` are written in **Markdown**: plain text with a few symbols that GitHub turns into formatting. GitHub shows a repository's `README.md`, formatted, on its front page.

| Type this | To get |
|---|---|
| `# Title`, `## Section` | a heading, and a smaller one |
| a blank line | a new paragraph |
| `- item` | a bullet point |
| `1. step` | a numbered step |
| `` `monthly_revenue.sql` `` | code in the middle of a sentence |
| three backticks on the lines before and after | a block of commands, shown exactly as typed |
| `[the metric definitions](docs/metrics.md)` | a link |
| `\| a \| b \|`, then `\|---\|---\|`, then rows | a table |

### The README

Six headings. This is the whole thing, and it takes twenty minutes:

| Heading | What goes in it |
|---|---|
| **What this is** | one paragraph. What question this repository answers, for whom |
| **What you need** | Python version, database, any account. Be specific: "PostgreSQL 16" not "a database" |
| **Setup** | the exact commands, in order, that take someone from clone to running. Copy them from a terminal where you actually ran them |
| **How to run it** | the command for the main thing, with an example of the output |
| **How the data is defined** | the grain, the filters, and the metric definitions, or a link to `docs/metrics.md` |
| **Who to ask** | a name. A repository with no owner is a repository nobody maintains |

As a Markdown skeleton, before you fill it in:

````markdown
# Riverstone analysis

## What this is
Monthly revenue queries and report scripts for the Riverstone sales team.

## What you need
- Python 3.14, PostgreSQL 16 with the `riverstone_full` database

## Setup
```
python -m venv .venv
```

## How to run it
## How the data is defined
See [the metric definitions](docs/metrics.md).

## Who to ask
Meera Iyer
````

**The test for the setup section:** push first, then clone the repository into a *different* folder and follow your own instructions there, without using anything you remember: `cd ~`, then `git clone <url> readme-test`, then `cd readme-test` and your steps. Everybody's instructions are missing a step; this is how you find which one. Delete the `readme-test` folder afterwards. Never delete your working folder to test this: anything not yet pushed would be gone.

### Documentation that survives

Most documentation fails for one of three reasons, and each has a fix that costs nothing:

| Why it fails | Fix |
|---|---|
| It lives somewhere nobody looks | put it next to the thing it describes: the README in the repository, the definition in the model, the comment in the query |
| It goes stale and nobody trusts it | date it, and write the parts least likely to change. A metric definition lasts; a screenshot does not |
| It explains what rather than why | the code already says what. Write down why cancelled orders are excluded and who decided |

For a data team the highest-value documentation is not a wiki. It is three things: the **metric definitions** from Chapter 23, the **business rules** you wrote as a BA in Chapter 25, and a one-line comment at the top of every query saying which question it answers.

---

## 26.10 How the work is actually planned

You will join a team that runs some version of Agile. Here is enough to be useful in your first week.

**Agile** is a preference, not a process: working in short cycles, showing something real at the end of each one, and changing the plan when what you learn says the plan was wrong. Two ways of organizing it dominate.

**Scrum** runs in fixed cycles called **sprints**, usually two weeks, and has four meetings, which the Scrum Guide calls **events** (many teams say "ceremonies"; the Guide counts the sprint itself as a fifth event).

| Event | When | What happens |
|---|---|---|
| Sprint planning | first day | the team picks what it will finish in this sprint from the backlog |
| Daily standup | every morning, 15 minutes | each person: what I did, what I am doing, what is blocking me |
| Sprint review | last day | show the working thing to the people who asked for it |
| Retrospective | last day | what to change about how we work, not about what we built |

**Kanban** has no sprints. Work flows across a board continuously, and the discipline is a **work-in-progress limit**: no more than *n* items in the "in progress" column at once, so that finishing beats starting.

**Which suits data work.** Analysis requests arrive unpredictably and vary enormously in size, which fits Kanban. Building a pipeline or a dashboard is a project with a shape, which fits Scrum. Most data teams end up with a mix: a board with WIP limits for requests, and sprint-like cycles for the bigger builds.

**Reading a Jira board.** Jira is the tool most companies use for this. Four things to know:

- An **issue** is one unit of work, with a key like `DATA-118`. That key belongs in your branch name and your pull request title, so a year later somebody can trace the code back to the request.
- **Epic, story, task, bug** are sizes and kinds. A story is a user-visible piece of work, the Chapter 25 shape; a task is a piece of it; an epic groups many.
- **Story points** estimate relative size, not hours. A 5 is bigger than a 3. Teams argue about this more than it deserves.
- The **backlog** is everything not yet started, in priority order. If your work is not in it, it does not exist to the people planning.

**The honest part.** Every one of these can become theatre: standups that are status reports to a manager, retrospectives where nothing changes, estimates treated as commitments. The practices are worth what the team makes of them. What is worth defending, whatever the process is called, is the short cycle and the working thing at the end of it.

---

## 26.11 Working with an AI assistant

You will use one. Most data teams already do. The skill that matters is not prompting. It is knowing what to hand over, and how to check what comes back.

### What to delegate, and what not to

| Delegate | Keep |
|---|---|
| boilerplate you have written before: a connection block, argument parsing, a chart's formatting | deciding what the question is |
| translating between dialects: this PostgreSQL query in MySQL | choosing the grain and the filters |
| explaining an error message or an unfamiliar function | judging whether a number is plausible |
| a first draft of a docstring, a README section, a regular expression | anything where being wrong is expensive and the error would be invisible |
| generating test data or edge cases you had not thought of | the final read of the numbers before they go to somebody |

The pattern: **delegate the typing, keep the judgment.** An assistant is good at things with a known right answer and poor at things that depend on context it cannot see, which for data work is most of what matters.

### How to check what it gives you

The failure mode is not nonsense. Nonsense is quick to spot. The failure mode is code that looks right, runs, and returns a number that is wrong.

1. **Run it on data where you know the answer.** Chapter 12's mini database has twelve orders. If a generated query cannot get January right on twelve rows, it will not get it right on two hundred thousand.
2. **Read it line by line before running it.** If you cannot explain every line, you cannot maintain it, and you certainly cannot defend the number it produced. This is the same standard this book applies to its own code.
3. **Check the joins and the filters specifically.** These are where generated SQL goes wrong: a join that fans out and doubles the revenue, a `WHERE` clause that quietly drops NULLs, a missing exclusion of cancelled orders.
4. **Reconcile.** Compare the total against something already known, exactly as Chapter 25, section 25.10, does for a data product.
5. **Never paste an error you do not understand back and accept the next answer.** Two rounds of that and you have code nobody understands, including the assistant.

### What must never be pasted into one

This is a rule, not a preference, and breaking it is a disciplinary matter in many companies.

- **Real customer data.** Names, contact details, addresses, anything identifying a person.
- **Credentials.** Passwords, keys, tokens, connection strings.
- **Anything covered by a contract or a law.** Under India's Digital Personal Data Protection Act 2023, and under the GDPR where it applies, personal data pasted into a tool your employer has no contract with is a disclosure your employer is responsible for, not the tool; an approved tool with a data-processing agreement is a different case (below). Chapter 64 covers the governance side in full.
- **Unreleased financials, or anything a competitor would like.**

The safe habit: **work on the schema, not the rows.** Paste the table structure, the column names, and a made-up row or two. An assistant helping you write a query has no use for real data, and Riverstone's own data in this book is invented for exactly this reason.

If your company has an approved assistant with a data-processing agreement, the rules may be looser. Find out what they are before you need them, not afterward.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Committing a secret | a password or key appears in `git log -p` (every commit's full diff), and now it is in everyone's clone | `git rm --cached`, commit, and then **change the password**. Removing the file does not remove the history |
| Commit messages that say "update" | six months later nobody can find when a rule changed | one line saying what changed and, where it is not obvious, why |
| One giant commit on Friday | the history is useless for finding a mistake, because every change is in the same snapshot | commit each finished piece of work as you finish it |
| Committing generated files | every `git diff` is full of noise; the repository is large | put exports, `__pycache__`, and built workbooks in `.gitignore` |
| Committing a notebook with its outputs | huge diffs over a rerun that changed nothing but a timestamp | clear outputs before committing, or use a tool that strips them |
| Working only on `main` | a half-finished change is sitting in the one branch people use | a branch per piece of work, however small |
| Copying a `git reset --hard` from a forum post | uncommitted work is gone, with no undo | decide which of the four undos you are in first. `restore`, `restore --staged`, `--amend`, `revert` cover almost everything |
| Amending or force-pushing a shared commit | a colleague's `git pull` fails, or silently loses work | amend only what you have not pushed. Shared history is undone with `revert` |
| Not pulling before starting | a conflict every time, on work you did not need to redo | `git pull` before you branch, and before you push |
| Branch names like `test2` | nobody, including you, can tell what is in them | `fix/duplicate-invoice-rows`, or the issue key: `DATA-118-late-file-handling` |
| A repository with no README | the work is technically shared and practically private | six headings, twenty minutes, today |
| Setup instructions written from memory | a colleague cannot get past step 3 | clone it fresh into a new folder and follow your own instructions |
| Absolute paths in scripts | it runs on your laptop and nowhere else | paths relative to the repository, and configuration in `.env` |
| A failing check on `main` that nobody fixes | the red cross stops meaning anything and the check is ignored | fix it or delete it. A check people ignore is worse than no check |
| Running a command in the wrong folder | *No such file or directory*, or *not a git repository* | `pwd` first, then `cd` to the right folder; Tab completion stops you typing a path that doesn't exist |
| Git opens Vim and you can't get out | a screen of `~` signs that ignores your typing | `Esc`, then `:q!` and Enter; then set `core.editor` (section 26.2) |
| Pushing to a GitHub repository created with a README | the first push is rejected | create it empty; or `git pull`, then push |
| Typing your GitHub password when `git push` asks | authentication failed | sign in through Git Credential Manager or `gh auth login` (section 26.7) |
| Pasting real customer data into an AI assistant | a disclosure you cannot take back, and possibly a legal one | work on the schema and made-up rows, never the real ones |
| Accepting generated SQL because it runs | a number that is wrong and looks right | read every line, check the joins and filters, reconcile against something known |

---

## In the real world: the rule nobody could date

In February 2026 Meera Iyer was asked a question she could not answer.

Vikram Singh, comparing the January sales report against his own notes, found the revenue figure lower than he expected by ₹12,000. Meera checked. The report excluded cancelled orders, and ₹12,000 was exactly cancelled order 5004. That was correct, and it was what the finance team wanted. But Vikram's copy of the December report, sitting in his inbox, had included them.

So the rule had changed somewhere between December and January. The question he asked was reasonable and she could not answer it: **when did it change, and who decided?**

The script lived in a folder on her laptop, next to `monthly_report_old.py` and `monthly_report_v2_working.py`. The file dates told her only when she had last saved each one. There was no record of what she had changed, and no record of the conversation that caused it. She had made the change, she was fairly sure, after a conversation with the finance assistant in early January. She could not prove it, and she could not prove anything else either.

The report was re-run three times that week while two teams argued about which number was right. The rule turned out to be correct all along. What cost the week was not the rule. It was that nothing recorded the decision.

The repository she set up the following Monday was small and unglamorous: four SQL files, two Python scripts, a `.gitignore`, and a README with six headings. The habit that mattered was the one that felt like overhead at the time. Every commit message that changed a business rule said who asked for it and when. The first one she wrote recorded the rule that had cost the week, now with the proof she had since found: *Exclude cancelled orders from the monthly report script (agreed with finance on 8 Jan; confirmed by email, 9 Feb)*.

Six weeks later the same question came up about a different rule, from a different person. It took forty seconds.

There was one other thing she got wrong first, which is worth saying because almost everyone does it once. Her first push included the `.env` file with the database password in it. Farah spotted it while looking at the repository on GitHub. Meera deleted the file and committed the deletion, which felt like a fix and was not: the password was still in the history, visible to anyone with access to the repository, and it stayed there. The real fix took ten minutes with the IT contractor: **change the password**. Then add `.env` to `.gitignore`, then commit `.env.example` so the next person knows what to supply.

The lesson is not that Git is complicated. It is that a repository remembers everything, which is exactly why it is useful and exactly why a secret in it is not a mistake you can quietly undo.

---

## Project: one repository for everything you have built

### Tools you'll need

| Tool | What it is for | Notes |
|---|---|---|
| **Git** | the version control system itself | Free, runs locally, works with no internet. Installed in section 26.0; `git --version` checks it |
| **GitHub** | the hosting service most teams and most portfolios use | Free accounts include unlimited public and private repositories. This is where a portfolio lives |
| **GitLab, Bitbucket, Azure Repos** | the same job at companies that do not use GitHub | The commands are identical. Only the website changes |
| **The Git panel in VS Code** | staging, committing, and branching without the terminal | Useful. Learn the commands first, so that you can read what it is doing and fix it when it stops working |
| **GitHub Desktop, Sourcetree, Fork** | graphical Git clients | Same caveat. A graphical client is a convenience, not a substitute for the model in section 26.1 |
| **GitHub Actions** | running checks automatically on every push | Free for public repositories, with a monthly allowance for private ones. Chapter 52 goes further |
| **GitHub CLI** (`gh`) | signing in to GitHub from the terminal, and pull requests without the website | Section 26.7 uses `gh auth login` on macOS and Linux |
| **pre-commit** | running checks *before* a commit is created, on your machine | Catches the formatting and the stray secret before they reach the history |
| **gitleaks, git-secrets** | scanning a repository for credentials | Worth adding to any repository that touches a database |
| **nbstripout** | clearing notebook outputs automatically on commit | Solves the single worst diff problem in data work |
| **Jira, Azure Boards, Linear, Trello** | the board the work is planned on | You will not choose this. Learn to read whichever one you are given |
| **Markdown** | what README files and most documentation are written in | Plain text with a few symbols (section 26.9). An hour to learn, used for the rest of your career |
| **MkDocs, Docusaurus, GitHub Pages** | turning a folder of Markdown into a browsable site | Useful once the documentation outgrows one README |
| **Confluence, Notion, SharePoint** | company wikis | Fine for decisions and context. Poor for anything that must match the code, because it drifts |
| **AI coding assistants** | drafting, translating, and explaining code | Section 26.11. Delegate the typing, keep the judgment |

By now Part 2 has produced a folder of work. This project turns it into one repository a stranger could run, and it is the raw material for Chapter 27's portfolio. Budget two hours.

**1. Create the repository.** A new folder (not this chapter's practice one), `git init`, and a first commit containing only a `.gitignore` (section 26.4's, `.venv/` included) and an empty `README.md` (`touch README.md`). Starting with `.gitignore` is deliberate: the rules exist before anything can be committed by accident.

**2. Move the work in, organized.** Use the structure from section 26.9: `mkdir -p sql/patterns sql/reports scripts notebooks docs`, then `cp` your files in. At minimum, bring in the pattern library from Chapter 13 (one file per pattern, each with a comment saying what question it answers), the report scripts from Chapters 18 and 20, and the metric definitions from Chapter 23 as `docs/metrics.md`. Run `git status` before each `git add`, and check that nothing from `.venv` or `exports` appears. Commit in several commits, grouped by what they are, not all at once.

**3. Make the secrets safe.** Anything holding a password becomes `os.environ[...]`, read from `.env` with `load_dotenv()`. Write a `.env.example` with the names, and values only where they are safe and the same for everyone. Run `git check-ignore -v .env` and confirm it is being ignored by the rule you think it is.

**4. Write the README.** Six headings, from the table in section 26.9. Push, then apply the test: clone the repository into a new folder somewhere else (`git clone <url> readme-test`), and follow your own setup instructions without using anything you remember. Fix what is missing. Commit the fix, and delete the test folder.

**5. Do one full cycle on a branch.** Pick one real improvement, however small: a filter that should have been there, a comment at the top of a query, a metric definition that is vague. Branch, change, commit, push, open a pull request against your own `main`, write the description as though a reviewer who has not seen the change will read it, then merge it. Read your own diff before you merge. This is the loop you will run every working day for the rest of your career.

**6. Add one check.** The workflow from section 26.8, with a short, hand-written `requirements.txt`. Then push a deliberate failure: delete a closing bracket in `scripts/monthly_report.py`, commit, push, and watch the check go red on GitHub's *Actions* tab (`compileall` fails on the syntax error). Put the bracket back, commit, push, and watch it go green. A check you have never seen fail is a check you do not know works.

**Stretch.** Review someone else's repository, from a study group or from a public one, and write three comments: one question about something you did not understand, one thing you would do differently and why, and one thing that was well done. Reviewing badly is the most common way new team members make a poor first impression, and it is entirely avoidable.

**What "done" looks like:** a URL you could put on a CV, where a stranger can read what the work is, see how it was built, and run it.

---

## Recap

The terminal is a program, its options, and its arguments, typed in a folder you can always check with `pwd`. `mkdir -p`, `touch`, `cp`, `mv`, `rm` (with no undo), `cat`, and `echo … >` cover the file work; `&&` runs the next command only if the last one worked, every command leaves an exit code in `$?` (0 means it worked), and `export` or `set -a; . ./.env; set +a` hands settings to the programs you start. Git is installed from its official source, and `git --version` checks it.

Git keeps a file in three places: the working directory where you edit, the staging area where you choose what belongs in the next snapshot, and the history where snapshots are permanent. Nearly every confusing Git message becomes clear once you ask which of the three it means.

The daily loop is small: `git status` to see where you are, `git add` to choose, `git commit -m` to record, `git log` to read. A commit message says what changed and, when the code cannot show it, why. That second half is the part that pays back, because the code can always tell you what.

Five settings, typed once per computer, tell Git who you are, name the first branch `main`, choose an editor you can leave, and make `git pull` merge. Secrets and generated files stay out, through a `.gitignore` written before the first commit. Code reads credentials from the environment, and a committed `.env.example` tells the next person what to supply. A secret that reaches the history is not fixed by deleting the file. It is fixed by changing the credential.

There are four undos, and choosing between them is the whole skill: `git restore` for an edit you have not staged, `git restore --staged` for something staged by mistake, `git commit --amend` for the last commit if you have not shared it, and `git revert` for anything already shared. Branches are not advanced; they are how you try something without risking what works. When two branches change the same line, Git marks the conflict in the file, and you choose.

GitHub adds the shared copy, the pull request, and the review; pull before you push, and pull `main` again after a merge on GitHub. A good pull request is small and has a description that tells the reviewer what to look for. A good review asks questions before it makes demands. One automated check on every push turns a promise into a fact, and checks that people ignore are worse than no checks.

A repository a stranger can run needs structure, a six-heading README, and setup instructions you have tested by following them in a fresh clone. Documentation survives when it lives next to what it describes, carries a date, and records why rather than what. Files Git cannot diff, such as Power BI and Excel workbooks, need a text-based format or exported modules instead.

Work is planned in short cycles. Scrum has sprints and four meetings it calls events; Kanban has a continuous flow and a work-in-progress limit; most data teams mix them. Read the board you are given, put the issue key in your branch name, and remember that the practices are worth exactly what the team makes of them.

You will work with an AI assistant. Delegate the typing: boilerplate, translation between dialects, first drafts, explanations. Keep the judgment: the question, the grain, the filters, and the final read of the numbers. Check what comes back on data where you know the answer, read every line before you run it, look hardest at joins and filters, and reconcile. Never paste real customer data, credentials, or anything covered by a contract or a law. Work on the schema, not the rows.

---

## Key terms

terminal · shell · Git Bash · path (absolute, relative) · home folder · hidden file · option · argument · exit code · `&&` · environment variable · `export` · version control · repository · working directory · staging area · commit · commit hash · `git config` · `git init` · `git status` · `git add` · `git commit` · `git log` · `git diff` · untracked file · tracked file · `.gitignore` · `git check-ignore` · `git rm --cached` · `.env` · `.env.example` · environment variable · `git restore` · `git restore --staged` · `git commit --amend` · `git revert` · branch · `git switch` · `git branch` · `git merge` · fast-forward · merge commit · alias · remote · `git push` · `git pull` · clone · pull request · code review · merge conflict · continuous integration · workflow · YAML · README · Markdown · two-factor authentication · Git Credential Manager · Agile · sprint · Scrum · standup · retrospective · backlog · Kanban · work-in-progress limit · issue key · story point · AI assistant

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- You can open a terminal, say where you are, make, copy, move, and delete files and folders, and read any command as a program, options, and arguments.
- `git --version` prints a version, and `git config --global --list` shows your name, email, `main`, your editor, and `pull.rebase=false`.
- You can name the three places a file lives in Git and say which one a given error message is talking about.
- You commit your work in pieces that make sense, with messages that would help a colleague, or you, in a year.
- Your `.gitignore` exists before your first commit, and you know why `git rm --cached` is needed when it does not.
- You know that deleting a committed secret does not remove it, and that the fix is to change the credential.
- Given something that went wrong, you can say which of the four undos applies before you type a command.
- You work on a branch without being told to, and your branch names say what is in them.
- You can open a pull request whose description a reviewer can act on, and review someone else's without either rubber-stamping it or being unpleasant.
- You can read a `git diff` and say what changed, line by line.
- You have one repository whose README lets a stranger run your work in fifteen minutes.
- You can read a Jira board and say what the team is doing this sprint.
- You use an AI assistant for the typing and not for the judgment, and you can list what must never be pasted into one.

---

## Exercises

### Warm-up

1. Name the three places a file lives in Git, and say what `git add` and `git commit` each move it between.
2. You run `git status` and see a file listed under "Changes not staged for commit". What has happened to it, and what has not?
3. Write three commit messages for these changes, each one line: (a) you added a filter excluding cancelled orders, after finance asked for it; (b) you renamed a column in a query from `amt` to `order_value`; (c) you fixed a join that was double-counting orders with more than one line.
4. Which of these belong in `.gitignore`, and why: `monthly_report.py`, `.env`, `exports/january.csv`, `README.md`, `__pycache__/`, `sales_data.xlsx`, `requirements.txt`, `.venv/`?

### Core

5. For each situation, say which of the four undos you would use and why: (a) you edited a query, made it worse, and have not staged anything; (b) you ran `git add .` and it picked up a 40 MB export; (c) you committed with the message "asdf" two minutes ago and have not pushed; (d) you pushed a commit on Tuesday that dropped the date filter, and two colleagues have pulled since.
6. **Predict before running.** You have committed a file, then edited it, then run `git add` on it, then edited it again. Write down what you expect `git status` to show for that one file, and how many entries it will have. Then do it and check.
7. Write a `.gitignore` for a repository containing Python scripts, SQL files, a Jupyter notebook, a `.env`, and an `exports/` folder that fills with `.xlsx` and `.csv` files. Comment each line.
8. You are reviewing a colleague's pull request. It changes a query's `JOIN` from `LEFT` to `INNER` and the title is "fix query". Write three comments you would leave, in the order you would leave them.
9. A generated query gives you last quarter's revenue as ₹94,32,000. List four specific checks you would run before putting that number in an email, in the order you would run them.
10. Write a README "What you need" and "Setup" section for the Chapter 18 report script, assuming the reader has a laptop and nothing else. Be specific enough that a version number appears at least twice.

### Stretch

11. Section 26.8's workflow runs on every push. Describe two changes you would make to it for a repository where the tests take twenty minutes and most pushes are to branches nobody is reviewing yet, and say what each change costs you.
12. Your team's board has fourteen items in the "in progress" column and three people. Write what you would say in the retrospective, and what you would propose changing. Name the Kanban idea you are appealing to.
13. A colleague pastes a production customer table into an AI assistant to get help writing a query, and the output is good. Write what you would say to them, and then write the policy line you would propose for the team, in one sentence each.

### Think about it (no calculation needed)

14. The chapter says a commit message should record **why** rather than what. But the "why" usually lives in a conversation with someone outside the team, which is not in the repository. What practical habits close that gap, and what does that suggest about where the issue key belongs?
15. An AI assistant will write a correct-looking query faster than you can write a wrong one. If that is true, what exactly is the analyst being paid for, and how should that change what you spend your learning time on?

---

## Answers

**1.** The **working directory** (the files as you see them), the **staging area** (what you have selected for the next commit), and the **history** (commits, permanent). `git add` moves a change from the working directory to the staging area. `git commit` moves everything staged into the history, as one snapshot with a message.

**2.** The file has been **edited in the working directory** and those edits have **not been staged**. Git knows the file, is tracking it, and can see it differs from the last commit. Nothing about it will be in the next commit unless you run `git add` on it first.

**3.** (a) `Exclude cancelled orders from monthly revenue (agreed with finance, 8 Jan)`: the why is the half that matters, and the date and the requester make it findable. (b) `Rename amt to order_value in the revenue query`, which is self-explanatory, so no why is needed. (c) `Fix duplicate rows from order_items join in revenue query`, which names the cause rather than only the symptom, so the next person recognizes the same bug elsewhere.

**4.** In `.gitignore`: `.env` (a secret), `exports/january.csv` (generated), `__pycache__/` (generated), `.venv/` (the virtual environment, rebuilt from `requirements.txt`), and `sales_data.xlsx` (data, and probably regenerable; if it is source data that cannot be regenerated, it still usually belongs somewhere other than a repository). Committed: `monthly_report.py`, `README.md`, `requirements.txt`, all of them text, and all needed to run or understand the work.

**5.** (a) `git restore <file>`: the change is unstaged, so restoring from the last commit costs nothing but the bad edit. (b) `git restore --staged <file>`: unstage it; the file itself is untouched, and this is also the moment to add it to `.gitignore`. (c) `git commit --amend -m "…"`: the commit is the last one and has not been shared, so rewriting it is safe. (d) `git revert <hash>`: it is shared, so the history must not be rewritten. `revert` adds a new commit that undoes it, and everyone's `git pull` works normally.

**6.** `git status` shows the file **twice**: once under "Changes to be committed" (the first edit, staged) and once under "Changes not staged for commit" (the second edit, not staged).

<!-- The two edits, made by the chapter's check on its repository (not printed):
```
# terminal
$ echo "-- first edit" >> monthly_revenue.sql

$ git add monthly_revenue.sql

$ echo "-- second edit" >> monthly_revenue.sql
```
-->

```
# terminal
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   monthly_revenue.sql

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   monthly_revenue.sql
```

In the short form it is one line with two status letters, `MM`: modified in the staging area, and modified again in the working directory.

```
# terminal
$ git status --short
MM monthly_revenue.sql
```

<!-- Clean-up (not printed):
```
# terminal
$ git restore --staged monthly_revenue.sql

$ git restore monthly_revenue.sql
```
-->

This is the clearest single demonstration that the staging area is a real, separate place: Git is holding two different versions of one file, and only the staged one would go into the commit.

**7.** For example:

```
# .gitignore
# Secrets
.env

# Generated exports, whatever the format
exports/

# Belt and braces: spreadsheets and CSVs anywhere in the repository
*.xlsx
*.csv

# Python and notebook noise
.venv/
__pycache__/
.ipynb_checkpoints/
```

The `exports/` rule alone would cover the files in that folder; the `*.xlsx` and `*.csv` lines also catch the copy somebody inevitably saves in the wrong place. Nothing here excludes `.sql` or `.py` or the notebook itself, which are the work.

**8.** (1) *"What was the reason for the join change? If some orders have no line items, this will now drop them from the report, and I want to check that is intended."* The question comes first, because you may be wrong. (2) *"Could the title say what the fix is? Something like 'Exclude orders with no line items from revenue'. It will matter when someone searches the history."* (3) *"Is there a case in the January data where this changes the total? If so, that number is worth putting in the description so the reviewer can check it."* Ordering matters: question, then the cheap fix, then the request for evidence.

**9.** (1) **Read every line** and say what each does, particularly the joins and the `WHERE` clause. (2) **Run it on the twelve-row mini database** from Chapter 12, where you can count the answer by hand. (3) **Check the grain**: does one row mean one order or one order line, and is the join fanning out? (4) **Reconcile** the total against something already trusted, such as the ERP figure or last quarter's report, and explain any difference before sending it.

**10.** A model answer:

> **What you need.** Python 3.14 (any version from 3.11 works) · PostgreSQL 16, with the `riverstone_full` database loaded (the setup scripts in the book's companion files, Appendix E) · the packages in `requirements.txt` · a `.env` file with `RIVERSTONE_DB`, copied from `.env.example`.
>
> **Setup.**
> 1. `git clone <url> && cd riverstone-analysis`
> 2. `python -m venv .venv && source .venv/bin/activate` (Windows, Git Bash: `source .venv/Scripts/activate`; PowerShell: `.venv\Scripts\Activate.ps1`)
> 3. `python -m pip install -r requirements.txt`
> 4. `cp .env.example .env` and put your database password into the `RIVERSTONE_DB` line
> 5. `python scripts/monthly_report.py 2025-12`

Two version numbers appear because "a recent Python" is not a setup instruction. The test of this section is not whether it reads well; it is whether it works in a fresh clone.

**11.** Two reasonable changes. (1) **Run the full suite only on pull requests and on pushes to `main`**, and run a faster subset on other branches. The cost is that a broken branch may stay broken for longer, until the pull request is opened. (2) **Cache the dependency installation** between runs, which usually takes the largest fixed cost out of a twenty-minute job without changing what is tested. The cost is a small risk of a stale cache hiding a dependency problem, which is why the cache key includes `requirements.txt`. A third answer, running the slowest tests on a schedule overnight instead of on every push, is also defensible: it trades immediate feedback for throughput, and it is only safe if somebody actually reads the overnight result.

**12.** "We have fourteen things in progress and three people, so on average each of us is holding four or five open items and finishing none of them quickly. Everything is started and nothing is done, which is why the requesters think we are slow even though we are busy. I would propose a **work-in-progress limit** of two per person: nothing new starts until something moves out of the column. We should expect the first week to feel worse, because some of us will have nothing to start, which is the point: the right response to a blocked item is to help finish someone else's, not to pick up a fifteenth."

**13.** To the colleague: *"That table has real customer names in it, so pasting it counts as a disclosure under our data protection obligations, whatever the tool's own policy says. It is not about whether the answer was good. Use the schema and a couple of made-up rows instead; you will get the same query."* The policy line: *"Schema, column names, and invented sample rows may be shared with approved AI assistants; real personal data, credentials, and unreleased financials may not, in any tool, including approved ones."*

**14.** The gap is real: the reason for a rule usually lives in a meeting, an email, or a conversation at someone's desk. Three habits close it cheaply. **Put the issue key in the branch name and the pull request title**, so the commit leads back to the ticket, which leads back to the request and the discussion on it. **Write the requester and the date into the commit message** when a business rule changes, as Meera did. And **keep the rule itself in `docs/metrics.md`**, dated, so the current answer is findable without reading history at all. The deeper point is that the repository is one of several records and does not have to hold everything. It has to hold the **link** to wherever the decision lives, because links survive people leaving and memories do not.

**15.** The analyst is paid for the part that cannot be delegated: knowing which question is worth asking, knowing what the data means and where it lies, and being accountable for a number that someone will act on. Speed of typing was never the scarce thing; it only looked like the job because it took most of the hours. For learning time, that argues for spending less of it memorizing syntax you can now generate, and more on the three things an assistant cannot do for you: **domain knowledge** (what a cancelled order means at this company), **verification** (how to tell a plausible number from a right one), and **judgment about the question** (Chapters 5, 23, and 25). It also argues for keeping the ability to read code fluently, since checking is now a larger share of the work than writing, and you cannot check what you cannot read.

---

## Where this leads

- **Chapter 27, the capstone,** turns this repository into a portfolio that a hiring manager will actually open.
- **Chapter 29, Python as Software,** adds the things a repository like this grows into: a package layout, tests, and type hints. It extends the check of section 26.8 so that it runs your tests for you.
- **Chapter 32, dbt,** puts your SQL transformations under the same discipline, with version control and automated tests as the default rather than an addition.
- **Chapter 34, the command line,** goes further with the terminal: pipes and text tools, permissions, `PATH`, shell scripts, SSH, and networking.
- **Chapter 44** builds an end-to-end data science project, which is a repository with the same requirements as this one and more moving parts.
- **Chapter 47** turns the "check on every push" idea into data quality tests and contracts that run against the data rather than the code.
- **Chapter 52** takes continuous integration to deployment: containers, cloud, and infrastructure defined as text files in a repository.
- **Chapter 56, MLOps,** versions models and the data they were trained on, because a model with no record of what produced it cannot be debugged.
- **Chapter 64** covers the governance side of what must never leave the building, including what an AI assistant counts as.
- **Chapter 82** includes take-home assignments, which are graded on exactly the repository standards in section 26.9.
