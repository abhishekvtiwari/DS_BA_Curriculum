# Chapter 17. Python from Zero

*Part 2 — The Analyst*

> **Chapter at a glance**
>
> **You will learn to:** use a terminal for the handful of commands Python needs · install Python, VS Code, and Jupyter on Windows, macOS, or Linux, and run your first notebook · create a virtual environment and install packages into it · say what a program is and when Python beats a spreadsheet or SQL · work with variables, strings, numbers, and booleans · use lists, tuples, dictionaries, and sets, and know which to reach for · write conditions and loops, and read a comprehension · write functions with arguments, defaults, and return values · read and write CSV, JSON, and text files with `pathlib` and the standard library · read a traceback, handle errors on purpose, and debug · turn a notebook experiment into a script someone else can run · get unstuck without waiting for anyone.
>
> **Before you start:** Chapters 1–16. Chapter 14 matters most (what cleaning involves), and this chapter keeps comparing Python with the spreadsheet formulas of Chapters 10–11 and the SQL of Chapters 12–13. No programming experience is assumed, and you don't need anything installed yet: section 17.0 installs everything, starting with the terminal.
>
> **Time needed:** 28–32 hours over three to four weeks: about 2 hours to set up (section 17.0), then five sittings of five or six hours, each best split over two or three evenings. The "Stop here" notes mark the sittings. Programming is learned by typing, not by reading.
>
> **Tools:** Python 3.14, VS Code, and JupyterLab, all free; section 17.0 installs them. A laptop or desktop computer: phones and tablets aren't enough from this chapter on.
>
> **Practice data:** `companion/ch17/`: `sales_exports/` (twelve monthly CSV files of the 24 key accounts' 2025 order lines, plus a README so your code has to ignore non-CSV files), `products.json`, `targets_2025.csv`, `broken_export.csv` for the error-handling section, and `check_setup.py`, which checks your setup in section 17.0.

---

## Why this matters

You can already do a great deal without programming. Chapters 10 and 11 made spreadsheets do real work; Chapters 12 and 13 made a database answer questions no spreadsheet could; Chapter 16 turned the answers into a report that refreshes itself.

Python is for the things those tools can't do, and for the things they can do only once.

- **Anything the tool can't do at all:** call an API, read a folder of 200 files, rename 5,000 images, scrape a page, fit a model, run a simulation.
- **Anything you'd otherwise repeat:** the monthly cleaning in Chapter 14 was already a recorded pipeline; a Python script does the same job, runs on a schedule, logs what it did, and emails the result (Chapters 18 and 20).
- **Anything that needs to be exact and reviewable:** code in a file can be read, versioned (Chapter 26), and tested. A sequence of clicks can't.

It also changes what you're allowed to say yes to. "Can you check every branch export for the last three years?" is a week of clicking or twenty minutes of Python. That difference is most of the distance between an analyst and a senior analyst, and all of the distance toward the analytics, data-science, and data-engineering work in Parts 3 to 5.

The chapter starts from zero: how to open a terminal, what a variable is, what a loop is, why your program says `IndentationError`. If you've programmed before, do section 17.0, then skim to section 17.9 and do the exercises.

---

## In plain English

A recipe is a program. It has **ingredients** (data), **steps in order** (statements), and **instructions that depend on something** ("if the dough is sticky, add flour" is a condition; "knead for ten minutes" is a loop). It has **names** for things ("the sauce" is a variable), and **sub-recipes** you can reuse ("make the dough" is a function).

The difference is that a cook fills in the gaps and a computer doesn't. Tell a cook "add the milk" and they'll use the milk on the counter. Tell a computer to add the milk and it will ask which milk, in what amount, and stop if it can't find it. That's not the computer being stupid; it's the computer being exact, which is the whole reason it can do the same job on 200 files without getting bored or making a typo in row 4,000.

So programming is mostly two skills:

1. **Saying exactly what you mean**, in an order that works.
2. **Reading the complaint** when you didn't. Error messages are not failure; they're the computer telling you which step confused it.

Everything else in this chapter is vocabulary.

---

## 17.0 Setting up Python, the terminal and Jupyter

Before any Python, you need three things on your computer: **Python** itself, **VS Code** (the editor you'll type code into), and **Jupyter** (notebooks, where code and its output sit together). Installing them takes a few typed commands, so this section starts with the smallest possible introduction to the terminal. Allow about two hours. Chapter 26 teaches the terminal properly; here you learn only what Python needs.

Work through the steps in order. Each one ends with something you can see, so a problem shows up at once, not three sections later.

### Step 1. The terminal: the minimum

A **terminal** is a window where you type **commands** instead of clicking. You type a command, press Enter, and the computer prints its reply underneath. Open one:

- **Windows:** press the Windows key, type *Terminal* (or *PowerShell* on older Windows 10), and press Enter.
- **macOS:** press `Cmd+Space`, type *Terminal*, and press Enter.
- **Linux:** press `Ctrl+Alt+T` on most desktops, or find *Terminal* in your applications.

The line waiting for you is the **prompt**. It usually ends with `$` or `%` on macOS and Linux, and looks like `PS C:\Users\Meera>` in Windows PowerShell. The prompt tells you the terminal is ready, and often which folder you're in. In this book, a terminal session is shown with `$ ` in front of each command you type (don't type the `$`), and the reply underneath. The first line, starting with `#`, says where the session runs; it isn't something to type either.

First, make the book's folder the way the front section ("How to Use This Book") described, with your file manager: `analyst-to-architect` in your home folder, holding `companion` (the downloaded companion files, unchanged), `work`, and `notes`. Then copy the folder `companion/ch17` and paste it inside `work`, so you have `work/ch17` to practise in, and the original stays untouched.

Every terminal is always "in" one folder, called the **working folder** (or current directory). Commands look for files there. Four commands move you around; try each one:

```
# terminal, in your home folder
$ pwd
/home/meera

$ ls
analyst-to-architect

$ cd analyst-to-architect

$ ls
companion
notes
work

$ cd work/ch17

$ pwd
/home/meera/analyst-to-architect/work/ch17

$ cd ..

$ pwd
/home/meera/analyst-to-architect/work
```

What each command does:

- **`pwd`** (print working directory) prints the folder you're in. `/home/meera` is Meera's home folder on Linux; on a Mac it looks like `/Users/meera`, and on Windows like `C:\Users\Meera`.
- **`ls`** (list) lists what's in the folder. Your home folder holds more than this; that's fine.
- **`cd`** (change directory) followed by a folder name moves you into it. `cd work/ch17` goes two levels down in one command. A command that works silently prints nothing: no news is good news.
- **`cd ..`** moves up one level. `..` always means "the folder above this one".

**On Windows**, the same four commands work in PowerShell: `pwd`, `ls`, `cd`, and `cd ..` are built-in short names for PowerShell's own commands (`Get-Location`, `Get-ChildItem`, `Set-Location`). The replies look different: `pwd` prints a small table with the heading `Path`, and `ls` prints a table with dates and sizes. Paths use `\` instead of `/`, but PowerShell accepts either when you type them.

Four habits make the terminal much less tiring:

- **Tab completes names.** Type `cd wo` and press Tab: the terminal fills in `work/`. It also catches typos, because it only completes names that exist.
- **The up arrow (↑) brings back your last command**, to run again or edit.
- **`Ctrl+C` stops a command** that is running too long (on a Mac too: it's `Ctrl`, not `Cmd`).
- **Put quotes around a folder name with spaces:** `cd "My Documents"`. Without them, the terminal reads two separate words.

### Step 2. Install Python

- **Windows:** python.org recommends the **Python install manager**, available from the python.org downloads page or from the Microsoft Store (the two are the same tool). It installs for your own user, so it usually doesn't need administrator rights. After installing it, open a new terminal and run `py install 3.14`, which installs Python 3.14. (If you skip this, the first `python` command installs the latest version for you.) The commands `python` and `py` then both start Python.
- **macOS:** download the macOS installer from python.org and run it. When it finishes, open the new *Python 3.14* folder in *Applications* and double-click **Install Certificates.command**, which lets Python download packages securely. The `python3` that may already be on a Mac is older and belongs to the system: don't build on it.
- **Linux:** most distributions include a recent Python 3. On Ubuntu or Debian, `sudo apt install python3 python3-venv python3-pip` adds the parts you need (`sudo` runs a command as administrator and asks for your password).

Check it. On macOS and Linux the command is `python3`; on Windows it's `python`:

```
# terminal
$ python3 --version
Python 3.14.7
```

`--version` is an **option**: extra words after a command that change what it does. Here it asks Python for its version number and nothing else.

**Which version?** Install **Python 3.14**, the current release (September 2026; 3.14.7 came out on 5 August 2026). Python 3.15 is due on 1 October 2026, and it will run everything in this book too. Any Python from 3.11 on runs every example in the book; this chapter's code was run and checked on Python 3.14.7 and 3.11.15. Later chapters don't repeat this: the rule is set here.

> **Watch out: `python` versus `python3`.** On macOS and Linux, `python` may not exist until you're inside a virtual environment (step 4); use `python3` until then. On Windows, `python` is right, and `py -3.14` picks a version when several are installed. Once your environment is active, `python` works on all three, and that's what the rest of the chapter writes.

**A locked work laptop?** Many companies lock laptops for good security reasons. Ask your IT team; Python and VS Code are commonly approved for learning. Until then, a cloud notebook such as Google Colab runs every cell in sections 17.1 to 17.11 in a browser.

### Step 3. Install VS Code and its two extensions

Install **VS Code** from its official website, code.visualstudio.com. Open it, click the *Extensions* icon on the left (four small squares), and install two **extensions** (add-ons) published by Microsoft: **Python** and **Jupyter**.

Then use **File → Open Folder** and open your `analyst-to-architect` folder, so VS Code sees the whole book folder. Three shortcuts to learn on day one:

| Action | Windows and Linux | macOS |
|---|---|---|
| Open or close the built-in terminal | `` Ctrl+` `` | `` Ctrl+` `` |
| Command palette (search every command) | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Run the selected notebook cell and move to the next | `Shift+Enter` | `Shift+Enter` |

The built-in terminal (**View → Terminal**) opens in the folder VS Code has open, which saves a `cd`. It's the same terminal as in step 1.

### Step 4. A virtual environment for the book

A **package** is code someone else wrote that you can install and use: JupyterLab is one, and Chapter 18 adds `pandas` for tables. The trap is installing everything into the one Python on your computer: two projects that need different versions of the same package fight, and one day something that worked stops working.

A **virtual environment** is a private copy of Python's package list for one project. The book uses one environment, in a folder called `.venv` inside `analyst-to-architect`. The dot at the start of the name is a convention that hides the folder in normal listings.

Create it, from the book folder:

```
# terminal
$ cd ..

$ python3 -m venv .venv

$ ls -a
.
..
.venv
companion
notes
work
```

How it works:

- `cd ..` moves up from `work` to `analyst-to-architect`, where the environment belongs.
- **`python3 -m venv .venv`** creates the environment. Read it in three parts: `python3` starts Python; **`-m venv`** tells it to run its built-in module `venv` (`-m` means "run this module as a program"); and `.venv` is the name of the folder to create. It prints nothing when it works, and takes a few seconds.
- **`ls -a`** lists *all* names, including the hidden ones that start with a dot. The `-a` option is how you see that `.venv` is really there. (`.` is this folder and `..` the one above; every folder lists them.)

On Windows, the create command is `python -m venv .venv`, and PowerShell's `ls` shows `.venv` without needing `-a`.

Next, **activate** the environment. Activating changes the terminal session, not the computer: from now until you close this terminal, `python` means the Python inside `.venv`, and packages install there.

```
# terminal
$ source .venv/bin/activate

$ python --version
Python 3.14.7
```

The command differs by system, because each terminal program runs a different kind of activation script (the Python documentation lists them):

| Terminal | Activate the environment |
|---|---|
| macOS or Linux (bash, zsh) | `source .venv/bin/activate` |
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |

When it's active, the prompt starts with `(.venv)`, for example `(.venv) PS C:\Users\Meera\analyst-to-architect>` in PowerShell. Run the activate command again each time you open a new terminal to work on the book. To leave the environment, type `deactivate`; the `(.venv)` disappears.

> **Watch out: "running scripts is disabled on this system".** On many Windows computers, PowerShell refuses to run `Activate.ps1` the first time, with an error that says running scripts is disabled on this system. That's PowerShell's **execution policy**, a safety setting that blocks script files; on Windows it blocks them all until someone changes it. The Python documentation's fix is to run this once, in PowerShell:
>
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
>
> Answer `Y` if it asks, then activate again. `RemoteSigned` lets scripts written on your own computer run, while scripts downloaded from the internet still need a signature; `-Scope CurrentUser` changes it for your account only, so it doesn't need administrator rights. If your company doesn't allow the change, use Command Prompt and `activate.bat` instead.

Now install JupyterLab into the environment. With `(.venv)` showing:

<!-- run: none -->
```
# terminal
$ python -m pip install jupyterlab
Collecting jupyterlab
  Downloading jupyterlab-4.6.4-py3-none-any.whl.metadata (16 kB)
Collecting async-lru>=1.0.0 (from jupyterlab)
  Downloading async_lru-2.3.0-py3-none-any.whl.metadata (7.6 kB)
...
Successfully installed MarkupSafe-3.0.3 anyio-4.15.1 argon2-cffi-25.1.0 ...
```

That output is trimmed: the real one is 283 lines. How it works:

- **`pip`** is Python's package installer. It downloads packages from **PyPI**, the Python Package Index, the public library of Python packages.
- **`python -m pip`** runs pip *through the Python you're using*, so the package lands in that Python's environment. Plain `pip install` sometimes belongs to a different Python; `python -m pip` never does.
- JupyterLab needs other packages to work, so pip collects and installs those too: about ninety in all, including **ipykernel**, the part that lets VS Code run notebook cells with this Python. The last line lists everything installed, with version numbers. Yours will be the same or newer.

Record what's installed, so a colleague (or you, next year, on another computer) can rebuild the same environment:

```
# terminal
$ python -m pip freeze > requirements.txt
```

`pip freeze` lists every installed package with its exact version. The **`>`** sends a command's output into a file instead of the screen, so the command prints nothing and `requirements.txt` appears in the folder. Open it in VS Code; its first lines look like this:

```text
anyio==4.15.1
argon2-cffi==25.1.0
argon2-cffi-bindings==26.1.0
```

`python -m pip install -r requirements.txt` installs the same list into a new environment. When you meet Git (Chapter 26), you'll save `requirements.txt` with your work but never the `.venv` folder itself, which can always be rebuilt.

Finally, tell VS Code to use the environment: open the command palette, type **Python: Select Interpreter**, and choose the one inside `.venv`. New VS Code terminals then activate it for you.

> **Tool note: other environment managers.** `conda` (Anaconda or Miniconda) manages environments and non-Python software too, and is common in science teams and on locked-down corporate machines. `uv` and `poetry` are newer and faster. They all solve the same problem; learn `venv` first, because it's built in and most explanations you'll read online assume it.

### Step 5. Check your setup

The companion script `check_setup.py` checks everything so far in one go. You aren't expected to understand its code yet; by the end of the chapter you will. From the book folder, go to your practice folder and run it:

```
# terminal
$ cd work/ch17

$ python check_setup.py
Python          3.14.7      OK
Environment     .venv       OK
JupyterLab      4.6.4       OK
Practice files  12 CSVs     OK
Python in use: /home/meera/analyst-to-architect/.venv/bin/python
Setup OK: you're ready for section 17.1.
```

`python check_setup.py` is how you run any Python file: `python`, then the file's name. Each line checks one thing: the Python version, whether the environment is active, whether JupyterLab is installed, and whether the terminal is in the folder that holds the twelve practice files. The last lines name the Python that ran the script (the one inside `.venv`) and give the verdict.

Here's what a problem looks like. `deactivate` leaves the environment, and `python3` then runs the computer's own Python:

```
# terminal
$ deactivate

$ python3 check_setup.py
Python          3.14.7      OK
Environment     none        FIX 1
JupyterLab      missing     FIX 2
Practice files  12 CSVs     OK
Python in use: /opt/python3.14/bin/python3
Fix these, in order, then run the script again:
  1. Activate the environment (section 17.0, step 4), then run this again.
  2. With the environment active, run:  python -m pip install jupyterlab

$ source ../../.venv/bin/activate
```

The report names each problem and its fix, in the order to do them. Both problems here have one cause, a missing activation, so the last command fixes both: `../..` means "up two levels", from `work/ch17` back to the book folder, where `.venv` lives. (On Windows, `..\..\.venv\Scripts\Activate.ps1`.)

**Meera's setup.** Meera set up her own laptop at home on a Sunday, to keep going beyond work. `check_setup.py` said JupyterLab was missing, although she'd installed it an hour earlier. She had installed it in a terminal where she hadn't activated `.venv`, so it went into the other Python. One `python -m pip install jupyterlab`, with `(.venv)` showing this time, and the script said *Setup OK*.

### Step 6. Your first notebook

In VS Code, with the `analyst-to-architect` folder open:

1. **File → New File…** and choose **Jupyter Notebook**. A notebook opens with one empty **cell**, a box for code.
2. Click **Select Kernel** at the top right and choose the environment in `.venv`. The **kernel** is the Python that runs the notebook's cells.
3. Type this into the cell, then press **Shift+Enter**:

<!-- run: none -->
```python
print("Hello, Riverstone")
```

```
Hello, Riverstone
```

The output appears under the cell, and a new empty cell opens below. `print()` writes whatever is in its brackets to the output; the quotes mark `Hello, Riverstone` as text rather than a command.

4. In the second cell, type this and press Shift+Enter:

<!-- run: none -->
```python
2 + 2 * 10
```

```
22
```

There's no `print()` this time, and the answer still appears: a notebook shows the value of a cell's last line. Python did the multiplication first, 2 × 10 = 20, then added 2, the order of operations from Chapter 4.

5. Save the notebook (**File → Save**) as `first_notebook.ipynb` in `work/ch17`. The folder a notebook is saved in becomes its working folder, which is why every notebook for this chapter goes in `work/ch17`: that's where its files are.

A notebook also holds notes. Hover between two cells, click **+ Markdown**, type a sentence such as `My first notebook, for Chapter 17`, and press Shift+Enter: it shows as formatted text. That's how analysts explain their working next to the code.

(If you prefer a browser, `jupyter lab` in the activated terminal opens the same notebooks in JupyterLab. Everything in this chapter works in either.)

**Checkpoint.** `check_setup.py` says *Setup OK*, and your notebook shows `Hello, Riverstone` and `22`.

### When installation fights back

| Symptom | Cause | Fix |
|---|---|---|
| `python: command not found` or `'python' is not recognized` | Python isn't installed, or the terminal can't find it | Install it as in step 2, then open a *new* terminal; on macOS and Linux use `python3` |
| `can't open file … check_setup.py: [Errno 2] No such file or directory` | The terminal is in the wrong folder | `pwd` to see where you are, then `cd` into `work/ch17` |
| `check_setup.py` says JupyterLab is missing, but you installed it | It went into a different Python, because the environment wasn't active | Activate `.venv`, then `python -m pip install jupyterlab` |
| "Running scripts is disabled on this system" (Windows) | PowerShell's execution policy | The `Set-ExecutionPolicy` line in step 4, or Command Prompt |
| The wrong Python version runs | Several Pythons installed | On Windows, `py -3.14`; in VS Code, check **Python: Select Interpreter** and the notebook's kernel |
| `Permission denied` when installing | Installing into the system's Python | Use the virtual environment (never `sudo pip install`) |
| Company laptop blocks the installer | IT policy | Ask IT; meanwhile use a cloud notebook such as Google Colab |

> **Stop here: sitting 1 of 6.** You have a terminal you can move around in, Python 3.14, VS Code, a virtual environment, and a notebook that runs. Everything from here is Python itself.

---

## 17.1 What a program is, and when to use one

A **program** is a set of instructions a computer follows. **Python** is a language for writing them: it reads almost like English, it's the most common language in data work, and it comes with a large collection of ready-made tools.

### Where Python fits next to what you know

| Job | Best tool | Why |
|---|---|---|
| Look at a few hundred rows, try a formula | Spreadsheet | Immediate, visual, no setup |
| Aggregate millions of rows that live in a database | SQL | The database is built for it |
| A report several people read every month | Power BI | Model once, refresh forever |
| Clean and combine 40 files with different formats | **Python** | Repeatable, and it scales past one machine's patience |
| Anything on a schedule with logging and alerts | **Python** | Scripts can run unattended (Chapter 20) |
| Statistics, forecasting, machine learning | **Python** | The libraries are there (Chapters 21–22, 30–31, and Part 4) |
| Call an API, scrape a page, talk to another system | **Python** | Nothing else in the analyst's kit can |

Python doesn't replace the others. Most real work is a chain: SQL pulls, Python cleans and combines, Power BI or Excel presents.

![Three cards: the REPL for trying one thing, a notebook for exploring data and showing your working, and a script for anything repeated, shared, or scheduled, with an arrow from the notebook card to the script card labelled "when it works, move it into a script"](figures/fig17-1-three-ways-to-run.svg)

*Figure 17.1 — Explore in a notebook, deliver a script.*

### The three ways you'll run Python

1. **The REPL** (type `python` in a terminal): a prompt where each line runs as you press Enter. Good for trying one thing. REPL stands for read, evaluate, print, loop, which is what it does.
2. **A notebook** (Jupyter, or a `.ipynb` file in VS Code): cells of code with their output underneath, mixed with notes. Good for exploring data and for showing your working. You made one in section 17.0.
3. **A script** (a `.py` file you run with `python script.py`): the whole thing, top to bottom, every time. Good for anything repeated, scheduled, or shared. `check_setup.py` is one.

Analysts explore in a notebook and deliver a script. Section 17.12 shows the move from one to the other.

---

## 17.2 Your first Python

Start with the REPL. In the terminal, with `(.venv)` showing, type `python` and press Enter. Python prints a line or two about its version, then the prompt `>>>`, which means "type a line of Python". Type the two lines below, pressing Enter after each:

```text
>>> print("Hello, Riverstone")
Hello, Riverstone
>>> 2 + 2 * 10
22
>>> exit()
```

The lines after `>>>` are what you type; the others are Python's replies. Like a notebook, the REPL shows the value of anything you type, so `2 + 2 * 10` answers `22` without a `print()`. **`exit()`** leaves the REPL and gives you the terminal back.

A script is different: in a `.py` file, only `print()` shows anything. A line that says `2 + 2 * 10` on its own in a script calculates 22 and then throws it away. That surprises everyone once.

From here on, every block of code in this chapter is a **notebook cell**. Open a new notebook in `work/ch17` (or keep using `first_notebook.ipynb`), type each cell, run it with Shift+Enter, and compare your output with the output shown under it. The cells use `print()` even where a notebook would show the value anyway, so the same code works when you move it into a script. **Before you run a cell, predict its output**; the ones you get wrong are the ones that teach you something.

`print()` can show text, a number, or several values at once:

```python
print("Riverstone Supplies")
print(14)
print("Orders this year:", 14)
```

```
Riverstone Supplies
14
Orders this year: 14
```

How it works:

- **`print(...)`** is a **function**, a named, ready-made piece of code, like a spreadsheet function. What goes inside the brackets is its **argument**, the value it works on, just as `A1` was the argument of `ROUND(A1,0)` in Chapter 10.
- **Text goes in quotes**; numbers don't. A piece of text in quotes is called a **string**.
- **Separate several values with commas**, and `print()` puts a space between them in the output.

---

## 17.3 Variables and types

A **variable** is a name for a value: `orders = 14` means "from now on, `orders` refers to 14". The `=` is **assignment**, not equality (equality is `==`, in section 17.5). The name goes on the left, and the value on the right.

```python
customer = "Metro Mart"
orders = 14
print("Customer:", customer)
print("Orders this year:", orders)
```

```
Customer: Metro Mart
Orders this year: 14
```

Where the code says `customer`, Python uses the value the name refers to. No quotes around `customer` in the `print()`: with quotes it would print the word *customer*.

Every value has a **type**, and the type decides what you can do with it. `type()` tells you a value's type:

```python
name = "Metro Mart"          # str: text
orders = 14                  # int: whole number
revenue = 284530.50          # float: number with decimals
is_key_account = True        # bool: True or False
rep = None                   # NoneType: "no value"

print(type(name))
print(type(orders))
print(type(revenue))
print(type(is_key_account))
print(type(rep))
```

```
<class 'str'>
<class 'int'>
<class 'float'>
<class 'bool'>
<class 'NoneType'>
```

- **`#` starts a comment.** Everything after it on that line is for humans, and Python ignores it. The comments here name each type.
- **`str`** (string) is text, **`int`** (integer) a whole number, **`float`** (floating-point number) a number with a decimal point, **`bool`** (Boolean) one of the two values `True` and `False`, and **`None`** means "no value", like a blank cell or SQL's `NULL`.
- `<class 'str'>` is Python's way of saying "this value is of type `str`".

### What a type lets you do

Numbers do arithmetic:

```python
print(orders * 2)
print(revenue / orders)
```

```
28
20323.60714285714
```

`*` multiplies and `/` divides. Division always gives a `float`, and Python shows every digit it stores, which is why 284,530.50 ÷ 14 prints as a long number. You'll format it for people with an f-string, below.

Text has its own tools. `name.upper()` gives the text in capital letters:

```python
print(name.upper())
```

```
METRO MART
```

`upper()` is a **method**: a function that belongs to a value, called with a dot after the value. Read `name.upper()` as "take `name`, and apply its `upper` method". The empty brackets mean it needs no argument. Strings have dozens of methods; you'll meet the useful ones next.

A `bool` can be turned around with `not`:

```python
print(not is_key_account)
```

```
False
```

### Your first script

Back to `orders`. Dividing by 12 gives the orders per month:

```python
print(orders / 12)
```

```
1.1666666666666667
```

That's more decimals than anyone wants to read. An **f-string** puts values into text and formats them on the way:

```python
print(f"about {orders / 12:.1f} a month")
```

```
about 1.2 a month
```

How it works:

- **The `f` before the opening quote** makes it an f-string.
- **Anything in `{curly brackets}`** is calculated, and its value goes into the text.
- **`:.1f` after the value is a format:** the `:` means "format it as", `.1` means one decimal place, and `f` means fixed-point (an ordinary decimal number). Change it to `:.2f` and you get `1.17`; the rounding happens only in what's shown.

Now put the pieces into a script. In VS Code, **File → New File…**, choose **Python File**, and save it in `work/ch17` as `hello.py`:

```python
# hello.py: my first script
customer = "Metro Mart"
orders = 14
print("Customer:", customer)
print("Orders this year:", orders)
print(f"{customer} placed {orders} orders, about {orders / 12:.1f} a month.")
```

```
Customer: Metro Mart
Orders this year: 14
Metro Mart placed 14 orders, about 1.2 a month.
```

Run it in the terminal, from `work/ch17` with the environment active, with `python hello.py`; or press the ▶ button at the top right of VS Code, which does the same. The three lines above appear. Every line of the file ran, top to bottom, and only the `print()` lines showed anything.

### Naming

Names may use letters, digits, and underscores, and can't start with a digit. The convention is `lower_case_with_underscores`. Good names save more time than any other habit: `net_revenue` beats `nr`, and `customers_without_city` beats `list2`.

### Strings

A string's methods are Chapter 14's cleaning, one value at a time. Start with a name that arrived with spaces around it:

```python
customer = "  metro mart  "
clean = customer.strip()
print(len(customer), len(clean))
```

```
14 10
```

`strip()` removes spaces from both ends, and **`len()`** counts the characters: 14 before, 10 after, so four spaces went. `strip()` is like the spreadsheet's `TRIM` for the ends, but it doesn't collapse double spaces in the middle, which `TRIM` does.

```python
print(clean.title())
print(customer.strip().title())
```

```
Metro Mart
Metro Mart
```

`title()` capitalizes each word. The second line **chains** two methods: Python runs them left to right, so `strip()` goes first and `title()` works on its result.

Three questions you can ask a string:

```python
clean = "Metro Mart"
print(clean.replace("Mart", "Market"))
print(clean.startswith("Metro"))
print("Mart" in clean)
```

```
Metro Market
True
True
```

`replace(old, new)` is the spreadsheet's `SUBSTITUTE`. `startswith()` answers `True` or `False`. **`in`** asks whether one string appears inside another.

```python
parts = "2025-01-15".split("-")
print(parts)
print("/".join(parts))
```

```
['2025', '01', '15']
2025/01/15
```

`split("-")` cuts the text at every `-`, like Text to Columns, and gives back a **list** of the pieces (the square brackets; section 17.4 explains lists). `"/".join(parts)` does the reverse: it glues the pieces together with `/` between them.

### Numbers

```python
quantity = 45
unit_price = 430
discount_pct = 5
net = quantity * unit_price * (1 - discount_pct / 100)
print(net)
```

```
18382.5
```

Brackets work as in Chapter 4: `1 - 5 / 100` is worked out first, giving 0.95. Then 45 × 430 × 0.95 = 18,382.5.

Three more operators:

```python
print(quantity // 10)
print(quantity % 10)
print(2 ** 10)
```

```
4
5
1024
```

- **`//` is whole-number division**: 45 items fill 4 full cartons of 10.
- **`%` is the remainder**: 5 items are left over.
- **`**` is power**: 2 to the power 10.

**Converting between types.** `int()` turns text into a whole number, `float()` into a decimal number, and `str()` turns anything into text. And `+` on two strings joins them:

```python
print(int("45") + 5)
print(float("430.50"))
print("Metro" + " Mart")
print(str(net) + " rupees")
```

```
50
430.5
Metro Mart
18382.5 rupees
```

`str(net)` is needed because Python won't join text to a number: `"rupees" + 5` is an error, not a guess. The conversions refuse to guess too: `int("twenty")` fails, which is exactly what you want in a cleaning script.

### Numbers with decimals are approximate

Chapter 2 said that most programs store decimal numbers in **floating point**, which can hold most decimals only approximately. Here it is:

```python
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print(round(0.1 + 0.2, 2) == 0.3)
```

```
0.30000000000000004
False
True
```

`0.1` and `0.2` are each stored a hair away from their true value, so their sum is `0.30000000000000004`, and **`==`** (equals, as a question) says it isn't 0.3. **`round(value, 2)`** rounds to two decimal places, and after rounding the comparison is `True`. A spreadsheet stores numbers the same way, and hides the tail by rounding what it displays.

When a value must be exact, Python has a **decimal** type, which stores decimals exactly, like `NUMERIC` in Chapter 12:

```python
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))
```

```
0.3
```

`from decimal import Decimal` loads one tool, `Decimal`, from Python's standard library (section 17.11 explains `import`). Give it the number as a string, in quotes, so it never passes through a float. Accounting and tax systems work this way. For analysis, the rule is simpler: round when you present, and compare with a tolerance rather than `==`.

### How does 2.5 round?

Chapter 10's first formula came with a promise: Python rounds 2.5 to 2. Here it is, with two more:

```python
print(round(2.5))
print(round(3.5))
print(round(2.675, 2))
```

```
2
4
2.67
```

A spreadsheet gives `3` for `=ROUND(2.5,0)` and `2.68` for `=ROUND(2.675,2)`. Who's right? The Python documentation for `round()` settles it: *"if two multiples are equally close, rounding is done toward the even choice"*. So a half goes to the even neighbour: 2.5 to 2, 3.5 to 4. That's **banker's rounding**, which you met in Chapter 12's `double precision` values. The spreadsheet's `ROUND` sends halves away from zero instead.

`round(2.675, 2)` is a different effect, and the documentation has a note on it: *"`round(2.675, 2)` gives `2.67` instead of the expected `2.68`. This is not a bug"*. 2.675 can't be stored exactly as a float, and the stored value is a hair below 2.675, so it rounds down.

Neither rule is wrong. What's wrong is not knowing which one your tool uses, and then wondering why a Python report and an Excel report differ by a rupee.

> **Stop here: sitting 2 of 6.** You can run Python three ways, and you know values, variables, types, strings, and numbers. Try warm-up exercises 1–3 and 7–8 before the next sitting.

---

## 17.4 Lists and tuples

A **list** holds several values in order. It's the workhorse of Python.

```python
cities = ["Mumbai", "Pune", "Bengaluru", "Delhi"]
print(cities)
print(len(cities))
```

```
['Mumbai', 'Pune', 'Bengaluru', 'Delhi']
4
```

Square brackets make a list, with commas between the items. `len()` counts items, as it counted characters in a string.

Each item has a position, its **index**, counted from 0. Negative numbers count from the end:

| Item | `"Mumbai"` | `"Pune"` | `"Bengaluru"` | `"Delhi"` |
|---|---|---|---|---|
| Index from the start | 0 | 1 | 2 | 3 |
| Index from the end | −4 | −3 | −2 | −1 |

```python
print(cities[0])
print(cities[-1])
```

```
Mumbai
Delhi
```

`cities[0]` is the first item and `cities[-1]` the last, however long the list is.

A **slice** takes several items at once:

```python
print(cities[1:3])
```

```
['Pune', 'Bengaluru']
```

`[1:3]` means "from index 1 up to, but not including, index 3", so items 1 and 2. By hand: start at `"Pune"` (1), take `"Bengaluru"` (2), and stop before `"Delhi"` (3). The start is included and the end isn't. It reads oddly for a day and then becomes natural.

Lists can change. Three methods, one at a time:

```python
cities.append("Kolkata")
print(cities)
```

```
['Mumbai', 'Pune', 'Bengaluru', 'Delhi', 'Kolkata']
```

`append()` adds an item at the end.

```python
cities.insert(0, "Ahmedabad")
print(cities)
```

```
['Ahmedabad', 'Mumbai', 'Pune', 'Bengaluru', 'Delhi', 'Kolkata']
```

`insert(0, ...)` puts an item at index 0, the front, and moves the rest along.

```python
cities.remove("Delhi")
print(cities)
```

```
['Ahmedabad', 'Mumbai', 'Pune', 'Bengaluru', 'Kolkata']
```

`remove()` deletes the first item equal to its argument.

Sorting has two forms, and the difference is a classic beginner bug:

```python
print(sorted(cities))
result = cities.sort()
print(result)
print(cities)
```

```
['Ahmedabad', 'Bengaluru', 'Kolkata', 'Mumbai', 'Pune']
None
['Ahmedabad', 'Bengaluru', 'Kolkata', 'Mumbai', 'Pune']
```

- **`sorted(cities)`** is a function: it gives back a *new*, sorted list and leaves `cities` alone.
- **`cities.sort()`** is a method: it sorts the list *in place* and gives back nothing, which in Python is `None`. So `result` is `None`, while `cities` itself is now sorted. Assigning the result of `.sort()` to a variable is the bug.

Two questions you can ask a list:

```python
print("Pune" in cities)
print(cities.index("Pune"))
```

```
True
4
```

`in` works as it did for strings, and `.index()` gives an item's position: `"Pune"` is at index 4 of the sorted list.

### Numbers in lists

```python
line_values = [2900.0, 20900.0, 12470.0, 6450.0, 38700.0]
print(sum(line_values))
print(max(line_values))
print(min(line_values))
print(round(sum(line_values) / len(line_values), 2))
```

```
81420.0
38700.0
2900.0
16284.0
```

`sum()`, `max()`, and `min()` are the spreadsheet's `SUM`, `MAX`, and `MIN`. The last line is the average: the sum divided by the count, rounded to two decimals.

The three largest values:

```python
ranked = sorted(line_values, reverse=True)
print(ranked[:3])
```

```
[38700.0, 20900.0, 12470.0]
```

`reverse=True` is a **named option**: it tells `sorted()` to go largest first. Section 17.8 explains named (keyword) arguments. `ranked[:3]` is a slice with the start left out, which means "from the beginning": the first three items.

### Tuples

A **tuple** is a list that can't be changed: `("Mumbai", "West")`, in round brackets. Use one for a fixed pair or record, and for a function returning several values (section 17.8). A tuple can be **unpacked** into separate names in one line:

```python
city, region = ("Mumbai", "West")
print(city)
print(region)
```

```
Mumbai
West
```

The first name gets the first item and the second name the second. The counts must match: two names, two items.

---

## 17.5 Conditions: making decisions

A **condition** runs some code only when something is true, like the spreadsheet's `IF`.

```python
net_revenue = 284530.75
target = 250000

if net_revenue >= target:
    status = "above target"
elif net_revenue >= target * 0.9:
    status = "close"
else:
    status = "below target"

print(f"{net_revenue:,.0f} is {status}")
```

```
284,531 is above target
```

Here `net_revenue` is ₹2,84,530.75 and `target` is ₹2,50,000, so the first condition is true: `status` becomes `"above target"`, and Python skips the `elif` and `else`. Change `net_revenue` to `230000` and run it again: 2,30,000 is below the target but above 90% of it (2,25,000), so you get `close`.

The rules:

- **The colon and the indentation are the syntax.** `if` ends with a colon, and the indented lines under it are its body, which runs only when the condition is true. Python has no `END IF`; the indentation *is* the structure. Four spaces is the convention, and VS Code inserts them when you press Tab. Mixing tabs and spaces causes `IndentationError`, which is why editors are set to insert spaces.
- **`elif`** is "else if", and you can have as many as you like. Python checks them in order and runs the first body whose condition is true. **`else`** catches everything left, and is optional.
- **Comparison operators:** `==` equal, `!=` not equal, `<`, `<=`, `>`, `>=`. Each gives `True` or `False`.
- **In the f-string, `:,.0f`** adds a thousands separator (`,`) and shows no decimals (`.0f`). Python's `,` groups digits in thousands, 284,531; this book writes rupee amounts in its text the Indian way, ₹2,84,531, but program output keeps Python's grouping.

Conditions can be combined with **`and`**, **`or`**, and **`not`**:

```python
segment = "Wholesale"
orders = 14

if segment == "Wholesale" and orders > 10:
    print("bulk buyer")
```

```
bulk buyer
```

`and` needs both sides to be true; `or` needs at least one. Use brackets when a mix of `and` and `or` isn't obvious at a glance.

A missing value is `None`, and you test for it with **`is None`**:

```python
city = None

if city is None:
    print("no city on record")
if not city:
    print("no city: empty string, None, and 0 all count as false")
```

```
no city on record
no city: empty string, None, and 0 all count as false
```

- **`is None`**, not `== None`: `is` asks "is this the very same object?", and there is only one `None`.
- **`if not city:`** uses **truthiness**: in a condition, empty and zero values count as false, and everything else as true.

| Value | `""` | `0` | `None` | `[]` (empty list) | `"0"` | `[0]` |
|---|---|---|---|---|---|---|
| In a condition | false | false | false | false | true | true |

Handy, and a trap when `0` is a real value, such as a genuine zero quantity (Chapter 14, section 14.3). When you mean "is missing", say `is None`.

For a small choice, the **conditional expression** fits on one line:

```python
print("large" if orders > 20 else "small")
```

```
small
```

Read it as "`large` if orders are over 20, otherwise `small`": the same as `IF(orders>20, "large", "small")` in a spreadsheet.

---

## 17.6 Loops

A **loop** repeats work. Almost every Python loop is a `for` loop over a collection.

```python
months = ["Jan", "Feb", "Mar"]
for month in months:
    print("processing", month)
```

```
processing Jan
processing Feb
processing Mar
```

**`for month in months:`** takes each item in turn, names it `month`, and runs the indented body once for each. Nothing to count, nothing to increment. The name after `for` is yours to choose.

When you need the position as well, **`enumerate()`** hands you both:

```python
for i, month in enumerate(months, start=1):
    print(i, month)
```

```
1 Jan
2 Feb
3 Mar
```

Each time round, `enumerate()` gives a pair (position, item), and `i, month` unpacks it, as with the tuple in section 17.4. `start=1` counts from 1, like a human, instead of Python's 0.

To walk two lists side by side, **`zip()`** pairs them up:

```python
targets = [77350000, 70000000, 108050000]
for month, target in zip(months, targets):
    print(f"{month}: {target/10000000:.2f} crore")
```

```
Jan: 7.74 crore
Feb: 7.00 crore
Mar: 10.80 crore
```

`zip()` takes the first item of each list, then the second of each, and so on, stopping at the end of the shorter list. Dividing by 1,00,00,000 turns rupees into crore, and `:.2f` shows two decimals.

Notice March: 10.805 crore printed as `10.80`, not `10.81`. It's the float effect from section 17.3: 10.805 is stored as 10.80499999…, which is a hair below the half, so it rounds down.

**`range()`** gives numbers instead of items: `range(5)` is 0, 1, 2, 3, 4, and `range(1, 13)` is the months 1 to 12 (the end is left out, as in a slice). Use it when you need numbers rather than items from a collection.

### Accumulating a result

Most analysis code is a loop that builds up a total, or a list:

```python
line_values = [2900.0, 20900.0, 12470.0, 6450.0, 38700.0]
total = 0
big_lines = []
for value in line_values:
    total += value
    if value > 10000:
        big_lines.append(value)
print(total)
print(big_lines)
```

```
81420.0
[20900.0, 12470.0, 38700.0]
```

`total += value` is short for `total = total + value`: "add this value to the running total". Start with `total = 0` and an empty list, before the loop. Here's what happens on the first three times round:

| Time round | `value` | `total` afterwards | Added to `big_lines`? |
|---|---|---|---|
| 1 | 2,900.0 | 2,900.0 | no |
| 2 | 20,900.0 | 23,800.0 | yes |
| 3 | 12,470.0 | 36,270.0 | yes |

The `if` inside the loop is indented twice: it's part of the loop's body, and its own body is one level deeper.

### `while`, `break`, and `continue`

**`while`** repeats as long as a condition stays true. Analysts need it rarely (retrying a web call, for example); a `for` loop over a collection is safer, because it always finishes.

```python
attempt = 0
while attempt < 3:
    attempt += 1
    print("attempt", attempt)
    if attempt == 2:
        print("worked")
        break
```

```
attempt 1
attempt 2
worked
```

**`break`** leaves the loop at once, so there's no third attempt. Its partner **`continue`** skips the rest of the body and goes straight to the next time round; section 17.10 uses it to skip a bad row.

### List comprehensions

A **comprehension** builds a new list from another collection in one line. You'll read them constantly, so learn to recognize them even before you write them. Here's a loop that keeps the values over 10,000:

```python
values = [2900.0, 20900.0, 12470.0, 6450.0, 38700.0]
big = []
for v in values:
    if v > 10000:
        big.append(v)
print(big)
```

```
[20900.0, 12470.0, 38700.0]
```

The same, as a comprehension:

```python
big = [v for v in values if v > 10000]
print(big)
```

```
[20900.0, 12470.0, 38700.0]
```

Read it from the middle: **for each `v` in `values`** (the middle), **keep it if `v > 10000`** (the right), and **put `v` in the new list** (the left). Two more:

```python
doubled = [v * 2 for v in values]
labels = [f"₹{v:,.0f}" for v in sorted(values, reverse=True)]
print(doubled)
print(labels)
```

```
[5800.0, 41800.0, 24940.0, 12900.0, 77400.0]
['₹38,700', '₹20,900', '₹12,470', '₹6,450', '₹2,900']
```

The left part can be any calculation: `v * 2`, or an f-string that turns each number into a label. The `if` part is optional.

Keep comprehensions to one line and one condition. A comprehension with three nested loops is a puzzle; write the loop out instead.

> **Watch out: looping when the tool can do it for you.** Chapter 18's pandas does whole-column operations without a loop, and a database does them faster still. In plain Python, loops are correct; in pandas, a loop over rows is usually the slow, hard-to-read way. Learn loops first, then learn when not to write them.

> **Stop here: sitting 3 of 6.** Lists, tuples, conditions, and loops: the core of every program. Try warm-up exercises 4–6 before going on.

---

## 17.7 Dictionaries and sets

A **dictionary** maps keys to values: a lookup table, the same idea as XLOOKUP's two columns (Chapter 11) or a mapping table in SQL (Chapter 14, section 14.5).

```python
city_region = {"Mumbai": "West", "Pune": "West", "Bengaluru": "South", "Kolkata": "East"}
print(city_region["Mumbai"])
print(len(city_region))
```

```
West
4
```

Curly brackets make a dictionary, and each entry is `key: value`. `city_region["Mumbai"]` looks up the key `"Mumbai"` and gives its value. `len()` counts the entries.

Looking up a key that isn't there is an error. **`.get()`** asks more politely:

```python
print(city_region.get("Jaipur"))
print(city_region.get("Jaipur", "Unknown"))
```

```
None
Unknown
```

`.get(key)` gives `None` for a missing key, and `.get(key, default)` gives the default you name instead. `city_region["Jaipur"]` would stop with a `KeyError` (section 17.10). In cleaning code, `.get()` with an explicit default is usually what you want.

Adding an entry, or changing one, is an assignment:

```python
city_region["Delhi"] = "North"
print(city_region)
```

```
{'Mumbai': 'West', 'Pune': 'West', 'Bengaluru': 'South', 'Kolkata': 'East', 'Delhi': 'North'}
```

If the key exists, its value is replaced; if not, the entry is added at the end.

**`.items()`** gives each entry as a (key, value) pair, which a `for` loop unpacks:

```python
for city, region in city_region.items():
    print(f"{city:<10} {region}")
```

```
Mumbai     West
Pune       West
Bengaluru  South
Kolkata    East
Delhi      North
```

`:<10` in the f-string pads the city to ten characters, lined up on the left (`<`), so the regions form a neat column. That's how you line up a printed table. `.keys()` and `.values()` give only the keys or only the values.

### Counting with a dictionary

This pattern is behind every "group by" you'll ever write by hand:

```python
statuses = ["Delivered", "Delivered", "Cancelled", "Shipped", "Delivered", "Cancelled"]
counts = {}
for status in statuses:
    counts[status] = counts.get(status, 0) + 1
print(counts)
```

```
{'Delivered': 3, 'Cancelled': 2, 'Shipped': 1}
```

Start with an empty dictionary, `{}`. For each status, `counts.get(status, 0)` gives the count so far (0 the first time the status appears), and `+ 1` adds this one. It's `COUNTIF` for every value at once, or SQL's `GROUP BY status` with `COUNT(*)`.

### Dictionary comprehensions

A dictionary can be built in one line too. Here's the loop version, turning each city into its length:

```python
cities = ["Mumbai", "Pune", "Kolkata"]
name_lengths = {}
for c in cities:
    name_lengths[c] = len(c)
print(name_lengths)
```

```
{'Mumbai': 6, 'Pune': 4, 'Kolkata': 7}
```

And the comprehension:

```python
name_lengths = {c: len(c) for c in cities}
print(name_lengths)
```

```
{'Mumbai': 6, 'Pune': 4, 'Kolkata': 7}
```

It reads like a list comprehension with curly brackets, and `key: value` on the left: for each `c` in `cities`, make an entry with key `c` and value `len(c)`.

### Sets

A **set** holds unique values, with no order, and answers "is it in there?" quickly:

```python
segments = {"Retail", "Wholesale", "Retail", "Hospitality"}
print(len(segments))
print(sorted(segments))
```

```
3
['Hospitality', 'Retail', 'Wholesale']
```

`"Retail"` went in twice and is kept once. A set has no order, so printing one directly gives an order that can change between runs; `sorted()` makes the output predictable.

Two sets can be compared:

```python
a = {"Mumbai", "Pune", "Delhi"}
b = {"Delhi", "Kolkata"}
print(sorted(a & b))
print(sorted(a | b))
print(sorted(a - b))
```

```
['Delhi']
['Delhi', 'Kolkata', 'Mumbai', 'Pune']
['Mumbai', 'Pune']
```

`&` is intersection (in both), `|` is union (in either), and `-` is difference (in the first only). Set difference is the fastest way to answer "which customer codes are in the export but not in the master list?", the Python version of Chapter 12's anti-join.

![A five-row guide: list for ordered, changeable data; tuple for fixed records; dict for lookups from key to value; set for unique values and fast membership; and DataFrame for rows and columns, in Chapter 18. Each row gives a Riverstone example and typical operations](figures/fig17-3-collections.svg)

*Figure 17.2 — The four built-in collections, and where a DataFrame takes over.*

---

## 17.8 Functions

A **function** is a named piece of code you can run again with different inputs. You've used Python's own (`print()`, `len()`, `round()`); now write one.

```python
def net_revenue(quantity, unit_price, discount_pct=0):
    """Return the net value of one order line, after discount."""
    return quantity * unit_price * (1 - discount_pct / 100)

print(net_revenue(45, 430, 5))
print(net_revenue(10, 290))
print(net_revenue(quantity=20, unit_price=1400, discount_pct=12))
```

```
18382.5
2900.0
24640.0
```

- **`def name(parameters):`** defines it. The **parameters** (`quantity`, `unit_price`, `discount_pct`) are the names the function gives its inputs; the values you pass in a call are the **arguments**. The indented block is the body.
- **`return`** sends a value back to whoever called the function. Without `return`, a function gives back `None`.
- **A default value** (`discount_pct=0`) makes an argument optional: the second call leaves it out, so the discount is 0.
- **Keyword arguments** (`quantity=20`) name each value in the call. The call explains itself, and the order no longer matters. `reverse=True` in section 17.4 was one.
- **The docstring**, the string in triple quotes on the first line, is the function's documentation. `help(net_revenue)` prints it.

Why bother, when you could paste the formula three times? Because the formula changes. When Riverstone changes its rebate bands (Chapter 11), you change one function, not eleven places, and you can test it:

```python
def rebate_pct(annual_value):
    """Riverstone's loyalty rebate: 0% standard, 1% from ₹2,50,000, 2% from ₹4,00,000."""
    if annual_value >= 400000:
        return 2
    if annual_value >= 250000:
        return 1
    return 0

for value in [180000, 250000, 399999, 400000]:
    print(f"{value:>7,} → {rebate_pct(value)}%")
```

```
180,000 → 0%
250,000 → 1%
399,999 → 1%
400,000 → 2%
```

How it works:

- **`return` ends the function at once.** A value of ₹4,00,000 or more returns 2 at the first `if`, and the rest never runs. So the second `if` only sees values under ₹4,00,000, and the last line only values under ₹2,50,000.
- **The test values sit on each boundary:** 250,000 and 400,000 exactly, and 399,999 just below. Boundaries are where formulas go wrong.
- **`:>7,`** in the f-string lines the numbers up on the right (`>`) in 7 characters, with a thousands separator (`,`).

Functions have their own **scope**: names created inside a function disappear when it returns, and a function can read names from outside but shouldn't rely on it. Pass what you need in, and return what you produce.

```python
def summarize(values):
    """Return (count, total, average) for a list of numbers."""
    if not values:
        return 0, 0.0, 0.0
    return len(values), sum(values), sum(values) / len(values)

count, total, average = summarize([2900.0, 20900.0, 12470.0])
print(count, total, round(average, 2))
print(summarize([]))
```

```
3 36270.0 12090.0
(0, 0.0, 0.0)
```

A function that returns several values, separated by commas, is really returning one tuple, which you can unpack into three names. `if not values:` catches the empty list (truthiness, section 17.5): handling that case first prevents a `ZeroDivisionError` when a month has no orders.

> **Stop here: sitting 4 of 6.** Dictionaries, sets, and functions. Try core exercise 9 before going on.

---

## 17.9 Files and folders

Analyst code spends most of its life reading files. Python's `pathlib` handles paths, and the standard library reads the formats.

### Where your code is running

Every relative path, such as `"sales_exports"`, is looked up from the **working folder**, the same idea as the terminal's in section 17.0. For a notebook, that's the folder the notebook is saved in; for a script, it's the folder the terminal is in when you run it. So keep this chapter's notebooks in `work/ch17`, and run its scripts from there.

```python
from pathlib import Path

print(Path.cwd())
```

```
/home/meera/analyst-to-architect/work/ch17
```

- **`from pathlib import Path`** loads one tool, `Path`, from the standard library's `pathlib` module. An **`import`** makes code from a module available in yours; section 17.11 says more.
- **`Path.cwd()`** gives the current working folder, like `pwd` in the terminal. Yours will start differently (on Windows, `C:\Users\…`), but it must end in `work/ch17`. If it doesn't, you'll get `FileNotFoundError` on the first file: move the notebook into `work/ch17`.

### Paths

```python
folder = Path("sales_exports")
print(folder.exists())
print(folder.is_dir())
```

```
True
True
```

`Path("sales_exports")` makes a **path object**: an address that knows how to answer questions about itself. `.exists()` asks whether anything is there, and `.is_dir()` whether it's a folder.

```python
files = sorted(folder.glob("*.csv"))
print(len(files))
print(files[0])
```

```
12
sales_exports/riverstone_2025_01.csv
```

**`glob("*.csv")`** finds every name in the folder that matches a pattern. `*` is a **wildcard**: it stands for any characters, so `*.csv` means "anything ending in `.csv`". That's how the `README.txt` in the folder stays out of your way. `glob()` doesn't promise an order, so `sorted()` puts the files in name order. (On Windows, the path prints with `\`.)

A path's parts are **attributes**: values attached to it, written after a dot with no brackets. A method (with brackets) does something; an attribute just is something.

```python
first = files[0]
print(first.name)
print(first.stem)
print(first.suffix)
```

```
riverstone_2025_01.csv
riverstone_2025_01
.csv
```

`.name` is the file's name, `.stem` the name without its extension, and `.suffix` the extension itself.

```python
print(first.stat().st_size)
```

```
1439
```

`.stat()` is a method that asks the computer about the file, and `.st_size` is the size in bytes from its answer.

```python
names = [f.name for f in files[:3]]
print(names)
```

```
['riverstone_2025_01.csv', 'riverstone_2025_02.csv', 'riverstone_2025_03.csv']
```

A comprehension (section 17.6) over the first three paths, keeping each one's name.

**`/` joins paths**, whatever the computer:

```python
january = folder / "riverstone_2025_01.csv"
print(january)
print(january.exists())
```

```
sales_exports/riverstone_2025_01.csv
True
```

`folder / "riverstone_2025_01.csv"` works on Windows, macOS, and Linux alike, with the right separator for each. Never build paths by gluing strings with `\` or `/`.

### Text files

```python
readme = Path("sales_exports/README.txt")
text = readme.read_text(encoding="utf-8")
lines = text.splitlines()
print(len(lines))
print(lines[0])
```

```
2
Monthly order-line exports for Riverstone's 24 key accounts, 2025.
```

- **`read_text()`** reads the whole file into one string.
- **`encoding="utf-8"`** says how the file's bytes turn into characters. Always pass it. Without it, Python uses the computer's default, which differs between Windows and everything else, and Indian names with accents or a `₹` sign then read as gibberish on someone else's laptop.
- **`splitlines()`** cuts the text into a list of lines. In the file, each line ends with an invisible line-break character, written `\n` in Python; `splitlines()` cuts there.

Writing a file:

```python
with open("scratch.txt", "w", encoding="utf-8") as f:
    f.write("first line\n")
    f.write("second line\n")
```

How it works, part by part:

- **`open(name, mode, encoding=...)`** opens a file. The mode says what for: `"r"` read (the default), `"w"` write (which replaces the file if it exists), and `"a"` append (add to the end).
- **`with ... as f:`** names the open file `f` for the indented block, and closes it automatically when the block ends, even if something fails. Always open files with `with`.
- **`f.write(...)`** writes a string. It doesn't add a line break, so each string ends with `\n`.

There's no output: writing a file prints nothing. Open `scratch.txt` in VS Code to see its two lines, or read it back line by line:

```python
with open("scratch.txt", encoding="utf-8") as f:
    for line_no, line in enumerate(f, start=1):
        print(line_no, line.strip())
```

```
1 first line
2 second line
```

A `for` loop over an open file gives one line at a time, and `enumerate()` numbers them. Each line arrives with its `\n` on the end; `.strip()` removes it, along with any spaces.

### CSV files

```python
import csv

with open("sales_exports/riverstone_2025_01.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(len(rows))
```

```
15
```

- **`import csv`** loads the standard library's CSV module; its tools are then written `csv.something`.
- **`newline=""`** is an argument, not a mode: it lets the `csv` module handle line breaks itself, which it needs to do correctly.
- **`csv.DictReader(f)`** reads the file one row at a time, and gives each row as a dictionary keyed by the header.
- **`list(reader)`** collects all the rows into a list, so you can use them after the file closes. January has 15 rows.

Here's the first row, one entry per line:

```python
for key, value in rows[0].items():
    print(key, value)
```

```
order_id 10001
order_date 2025-01-02
customer_name Patel Kitchenware
city Ahmedabad
segment Retail
product_name Stackable Bin
quantity 10
unit_price 290
discount_pct 0
status Delivered
net_revenue 2900.0
```

`rows[0]` is a dictionary, so `.items()` walks it (section 17.7). Reading columns by name, `row["net_revenue"]`, is much clearer than by position.

```python
print(rows[0]["net_revenue"])
print(type(rows[0]["net_revenue"]))
```

```
2900.0
<class 'str'>
```

**Every value arrives as text**, exactly as in Chapter 14's staging tables: `'2900.0'` is a string, not a number. Converting is your job, and that's the point: you decide what happens when a value won't convert.

```python
total = 0.0
for row in rows:
    if row["status"] != "Cancelled":
        total += float(row["net_revenue"])
print(f"January net revenue: ₹{total:,.2f} from {len(rows)} lines")
```

```
January net revenue: ₹202,640.00 from 15 lines
```

January's key-account net revenue is ₹2,02,640.00. The same figure appears in the monthly table in section 17.12.

**Writing a CSV.** `csv.DictWriter` writes dictionaries as rows:

```python
summary = [{"month": "2025-01", "lines": len(rows), "net_revenue": round(total, 2)}]
with open("month_summary.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["month", "lines", "net_revenue"])
    writer.writeheader()
    writer.writerows(summary)
```

- **`fieldnames=[...]`** lists the columns, in order; each dictionary's keys must match them.
- **`writeheader()`** writes the header row, and **`writerows()`** writes one row per dictionary in the list.
- **`newline=""`** again, which stops Windows adding a blank line between rows.

Read it back to check:

```python
print(Path("month_summary.csv").read_text(encoding="utf-8").strip())
```

```
month,lines,net_revenue
2025-01,15,202640.0
```

### JSON

**JSON** is the format APIs speak (Chapter 2). It maps onto Python's dictionaries and lists directly.

```python
import json

products = json.loads(Path("products.json").read_text(encoding="utf-8"))
print(len(products))
print(products[0]["name"], products[0]["unit_price"])
```

```
8
Storage Box 10L 430.0
```

**`json.loads()`** reads JSON text into Python objects: here, a list of eight dictionaries, one per product.

A price list from product name to price, first as a loop:

```python
by_name = {}
for p in products:
    by_name[p["name"]] = p["unit_price"]
print(by_name["Industrial Crate"])
```

```
1400.0
```

Then as a dictionary comprehension (section 17.7), which builds the same dictionary:

```python
by_name = {p["name"]: p["unit_price"] for p in products}
print(by_name["Industrial Crate"])
```

```
1400.0
```

And back to JSON text, into a file:

```python
Path("price_list.json").write_text(json.dumps(by_name, indent=2), encoding="utf-8")
print(Path("price_list.json").read_text(encoding="utf-8").splitlines()[:3])
```

```
['{', '  "Storage Box 10L": 430.0,', '  "Storage Box 25L": 750.0,']
```

**`json.dumps()`** turns Python objects into JSON text, and `indent=2` lays it out on several lines, indented by two spaces, for people to read. (`json.load` and `json.dump`, without the `s`, do the same with an open file.)

---

## 17.10 Errors, tracebacks, and debugging

Your program will fail, often, and that's normal. The skill is reading the complaint.

### Reading a traceback

Run this cell:

<!-- run: none -->
```python
values = [1, 2, 3]
print(values[5])
```

```
---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
Cell In[1], line 2
      1 values = [1, 2, 3]
----> 2 print(values[5])

IndexError: list index out of range
```

That's a **traceback**: Python's report of what went wrong and where. Read it **bottom up**:

- **The last line says *what* went wrong:** the error type, `IndexError`, and a message, `list index out of range`. The list has positions 0 to 2, and the code asked for position 5.
- **The lines above say *where*:** in a notebook, `Cell In[1], line 2` (the cell, and the line within it), with an arrow `---->` pointing at the line that failed.

In a script, the traceback also lists the chain of calls that led there, one file, line number, and function at a time. Figure 17.3 shows a longer one, from the script you'll write in section 17.12. In a long traceback, the last line of *your own* code, not a library's, is usually where the problem is.

From now on, only the last line of each traceback is shown.

![An annotated traceback from summarize_exports.py. Numbered markers show the reading order: 1, the last line, ValueError: could not convert string to float: ''; 2, the line of code that failed; 3, the file, line number, and function above it; 4, the chain of calls at the top. A key explains each number, and a box says what this traceback tells you](figures/fig17-2-traceback.svg)

*Figure 17.3 — Read a traceback from the bottom up: what went wrong, then where.*

### The errors you'll meet in your first month

| Error | Means | Usual cause |
|---|---|---|
| `SyntaxError` | Python can't parse it | Missing `:`, unbalanced bracket or quote, `=` instead of `==` |
| `IndentationError` | The blocks don't line up | Mixed tabs and spaces, or a missing indent after `:` |
| `NameError` | No such name | Typo, or using a variable before creating it |
| `TypeError` | Wrong type for the operation | `"5" + 5`, calling something that isn't a function |
| `ValueError` | Right type, impossible value | `int("twenty")`, `float("")` |
| `KeyError` | No such key in a dictionary | A column name that isn't in the CSV header |
| `IndexError` | Position doesn't exist | Off-by-one, or an empty list |
| `AttributeError` | The object has no such method | `list.push()`, or a `None` where you expected an object |
| `FileNotFoundError` | The path is wrong | Relative path from the wrong folder, a typo, or the file isn't there yet |
| `ZeroDivisionError` | Division by zero | An empty group, a month with no orders |
| `ModuleNotFoundError` | Package not installed here | Wrong virtual environment, or you haven't installed it |

Two errors worth meeting on purpose. A blank where a number should be:

```python
row = {"customer_name": "Metro Mart", "net_revenue": ""}
print(float(row["net_revenue"]))
```

```
ValueError: could not convert string to float: ''
```

And a column that isn't there:

```python
print(row["city"])
```

```
KeyError: 'city'
```

Both are Chapter 14 problems in Python form.

### Handling errors on purpose

```python
def to_float(text, default=None):
    """Convert text to a number, or return default when it can't be converted."""
    try:
        return float(text)
    except (ValueError, TypeError):
        return default

print(to_float("430.5"))
print(to_float(""))
print(to_float("twenty", 0.0))
print(to_float(None))
```

```
430.5
None
0.0
None
```

- **`try:` … `except SomeError:`** runs the risky code in the `try` block, and if it fails with one of the named errors, runs the `except` block instead of stopping. Here, `float("")` raises `ValueError`, and `float(None)` raises `TypeError`; both return the default.
- **Catch what you expect**, not everything. A bare `except:` hides typos, interrupts, and real bugs.
- **`else`** (runs when nothing failed) and **`finally`** (runs either way, for closing things) also exist; you'll see them in other people's code.
- **Sometimes the right answer is to stop.** Quietly turning bad data into zero is how wrong reports get published; count the failures and report them, exactly as Chapter 14 quarantined rows.

Here's that in action on `broken_export.csv`, March's file with one bad row planted in it. First, a helper you'll need: **`repr()`** shows a value the way you'd type it in code, quotes and all, so an empty string is visible:

```python
print(repr("twenty"))
print(repr(""))
```

```
'twenty'
''
```

`print("")` would print nothing at all; `repr("")` prints `''`. That's why it's the right way to report a bad value.

Now read the file, keeping a list of rows that won't convert:

```python
bad_rows = []
clean_total = 0.0
with open("broken_export.csv", encoding="utf-8", newline="") as f:
    for line_no, row in enumerate(csv.DictReader(f), start=2):
        value = to_float(row["net_revenue"])
        quantity = to_float(row["quantity"])
        if value is None or quantity is None:
            bad_rows.append((line_no, row["order_id"], row["quantity"], row["net_revenue"]))
            continue
        clean_total += value

print(bad_rows)
```

```
[(7, '10099', 'twenty', '')]
```

How it works:

- **`start=2`** numbers the rows as a text editor would: line 1 of the file is the header, so the first data row is line 2. The report can then say exactly where to look.
- **`to_float()`** converts both columns; `None` means it couldn't.
- **A bad row** is recorded as a tuple of four values (line number, order, and the two raw values), then **`continue`** skips to the next row, so it never reaches the total.
- The result is a list holding one tuple: line 7, order 10099, a quantity of `'twenty'`, and an empty net revenue.

Then the report:

```python
print(f"clean total ₹{clean_total:,.2f}")
print(f"{len(bad_rows)} row(s) could not be read:")
for r in bad_rows:
    print("  line", r[0], "order", r[1], "quantity", repr(r[2]), "value", repr(r[3]))
```

```
clean total ₹278,007.50
1 row(s) could not be read:
  line 7 order 10099 quantity 'twenty' value ''
```

`r[0]` to `r[3]` pick the tuple's items by position. The clean total is March's ₹2,78,007.50, the same as the untouched March file, so nothing else was lost. That's the whole shape of a cleaning script: read, convert defensively, keep a list of what failed, report it.

### Debugging

When code runs but gives the wrong answer, there's no traceback to read, and you have to find the problem yourself. Six habits, in the order to try them.

1. **Print the thing you assume.** `print(type(x), repr(x))` at the point of doubt answers most questions in seconds, and `repr()` shows a trailing space you'd otherwise miss.
2. **Shrink the problem.** Run it on one file, one row, one function. If a function is wrong, call it with a value whose answer you know.
3. **Check your assumptions about the data**, not only the code: is the column named what you think? Is it text? Does it have blanks?
4. **Use the debugger.** In VS Code, click in the margin to set a breakpoint (a red dot), press **F5**, and step through with **F10** while watching variables. Ten minutes learning it saves hours of print statements.
5. **Rubber-duck it.** Explain the code aloud, line by line, to a colleague or an inanimate object. You'll usually find it yourself in the explaining.
6. **Change one thing at a time**, and keep a working version (Chapter 26's version control is the grown-up form of this).

> **Stop here: sitting 5 of 6.** Files and errors: you can now read real exports and survive bad rows. Try core exercises 10, 11, and 17 before the last sitting.

---

## 17.11 The standard library and packages

Python ships with a large **standard library**: modules that need no installation, only an `import`. A **module** is a file of ready-made Python code; `import csv` makes the `csv` module's tools available as `csv.something`, and `from pathlib import Path` takes just one tool out of a module, so you can write `Path` on its own. The modules an analyst uses first:

| Module | For |
|---|---|
| `pathlib` | Paths and folders |
| `csv`, `json` | Reading and writing those formats |
| `datetime` | Dates, times, and differences |
| `statistics` | Mean, median, standard deviation |
| `collections` | `Counter` and `defaultdict`, for counting and grouping |
| `re` | Regular expressions (Chapter 14's patterns) |
| `math` | Rounding, logs, floors |
| `os`, `sys` | The environment, a script's arguments, exit codes |
| `logging` | Messages from a script that runs unattended (Chapter 18) |
| `zipfile`, `shutil` | Archives and file copying |

### Dates

```python
from datetime import date, datetime, timedelta

order_date = datetime.strptime("15-01-2025", "%d-%m-%Y").date()
print(order_date)
print(order_date.year)
print(order_date.strftime("%d %b %Y"))
```

```
2025-01-15
2025
15 Jan 2025
```

- **`strptime`** (string parse time) reads text into a date, using **format codes** to say where each part is: `%d` day, `%m` month, `%Y` four-digit year. `.date()` keeps the date and drops the time of day.
- **`strftime`** (string format time) turns a date back into text, in any layout: `%b` is the short month name.
- These are the same day-first and year-first formats Chapter 14 had to untangle, and the same rule applies: state the format, never let the computer guess.

Dates do arithmetic:

```python
print(order_date + timedelta(days=45))
print((date(2025, 12, 31) - order_date).days)
```

```
2025-03-01
350
```

A **`timedelta`** is a length of time; `days=45` is a keyword argument that sets it to 45 days, so the first line is 45 days after 15 January. Subtracting two dates gives a `timedelta` too, and `.days` is its length in days, like the spreadsheet's `DAYS()`.

### Counting and grouping

```python
from collections import Counter

statuses = ["Delivered", "Delivered", "Cancelled", "Shipped", "Delivered", "Cancelled"]
print(Counter(statuses))
print(Counter(statuses).most_common(2))
```

```
Counter({'Delivered': 3, 'Cancelled': 2, 'Shipped': 1})
[('Delivered', 3), ('Cancelled', 2)]
```

**`Counter`** is the counting dictionary from section 17.7, written for you. `.most_common(2)` gives the two most frequent values, with their counts, as a list of tuples.

```python
from collections import defaultdict

by_city = defaultdict(list)
for city, value in [("Mumbai", 2900), ("Pune", 20900), ("Mumbai", 12470)]:
    by_city[city].append(value)
print(dict(by_city))
print({c: sum(v) for c, v in by_city.items()})
```

```
{'Mumbai': [2900, 12470], 'Pune': [20900]}
{'Mumbai': 15370, 'Pune': 20900}
```

- **`defaultdict(list)`** is a dictionary that creates an empty list the first time you use a new key, so `by_city[city].append(value)` works even for a city it hasn't seen. That's the shortest correct way to group values.
- **`dict(by_city)`** turns it back into an ordinary dictionary for printing.
- The last line is a dictionary comprehension (section 17.7): for each city and its list of values, the total. Together, that's SQL's `GROUP BY city` with `SUM`.

### Statistics

```python
import statistics

values = [2900.0, 20900.0, 12470.0, 6450.0, 38700.0]
print(statistics.mean(values))
print(statistics.median(values))
print(round(statistics.stdev(values), 2))
```

```
16284.0
12470.0
14266.83
```

`mean` is the average and `median` the middle value, as in Chapter 4. `stdev` is the **standard deviation**, a measure of how spread out the values are; Chapter 21 explains it properly.

### Packages beyond the standard library

`pip install` fetches packages from **PyPI** (section 17.0). The ones this book uses:

| Package | For | Chapter |
|---|---|---|
| `pandas` | Tables, the analyst's core tool | 18 |
| `matplotlib`, `seaborn` | Charts | 18 |
| `openpyxl`, `xlsxwriter` | Reading and writing Excel files | 18 |
| `requests` | Calling APIs | 18 |
| `SQLAlchemy`, `psycopg`, `mysql-connector-python` | Talking to databases | 18 |
| `python-dotenv` | Keeping credentials out of code | 18 |
| `scipy` | Statistics and probability distributions | 21 |
| `statsmodels` | Regression tables and statistical tests | 22 |
| `scikit-learn` | Machine learning | 35 |
| `pyspark`, `polars` | Data too big for pandas | 48 |
| `jupyterlab` | Notebooks | this chapter |

Before installing something you found online, check that it's maintained (recent releases, open issues answered), that the name is spelled exactly right (typo-squatting, publishing a harmful package under a near-miss name, is a real attack), and that it goes into your project's virtual environment rather than the computer's own Python.

> **Watch out: don't paste credentials into code.** Database passwords and API keys belong in **environment variables** (named settings that live in the terminal session or the operating system, outside your code) or in a `.env` file that is never shared (Chapters 18 and 26). A password in a script is a password in every copy of that script, forever.

---

## 17.12 From notebook to script

Exploration belongs in a notebook: run a cell, look, adjust. But a notebook is a poor delivery format, because cells can be run out of order, hidden state builds up, and nobody can schedule it. When something works, move it into a script.

A useful script has five properties: it says what it does, takes its inputs as arguments, does the work in functions, reports what happened, and can be run again with the same result. You'll build one in four stages, in a file called `summarize_exports.py` in `work/ch17`, running it in the terminal after each stage. (The finished script is also in `companion/ch17/`, to compare with yours.)

### Stage 1: read one file

In VS Code, **File → New File… → Python File**, save it in `work/ch17` as `summarize_exports.py`, and type:

<!-- run: none -->
<!-- check: summarize_exports.py stage 1 -->
```python
"""Summarize every CSV export in a folder.

Usage:  python summarize_exports.py sales_exports
"""
import csv
from pathlib import Path


def read_rows(path):
    """Return the rows of a CSV file as a list of dictionaries."""
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


rows = read_rows(Path("sales_exports/riverstone_2025_01.csv"))
print(len(rows))
```

How it works:

- **The string at the very top**, in triple quotes, is the script's own docstring: what it does, and how to run it. Anyone who opens the file reads that first.
- **Imports go at the top**, one per line, so a reader sees at once what the script depends on.
- **`read_rows()`** is the CSV reading from section 17.9, as a function: give it a path, and it returns the rows. The `return` inside `with` is fine: the file still closes.
- **The last two lines are a test:** they call the function on January's file and print how many rows came back. Two blank lines between functions is the usual layout; Python doesn't require it, but people read it faster.

Save, and run it from the terminal (in `work/ch17`, with `(.venv)` showing):

<!-- run: none -->
<!-- check: summarize_exports.py stage 1 run -->
```
# terminal
$ python summarize_exports.py
15
```

Fifteen rows, as in section 17.9. Test each piece as soon as it exists; a script built in one go and run once at the end fails in five places at once.

### Stage 2: summarize one file

Add this function below `read_rows()`:

<!-- run: none -->
<!-- check: summarize_exports.py stage 2 -->
```python
def summarize(path):
    """Return one summary dictionary for a CSV export."""
    rows = read_rows(path)
    values = []
    bad = 0
    for row in rows:
        try:
            if row["status"] != "Cancelled":
                values.append(float(row["net_revenue"]))
        except (ValueError, TypeError, KeyError):
            bad += 1
    return {
        "file": path.name,
        "rows": len(rows),
        "lines_counted": len(values),
        "unreadable": bad,
        "net_revenue": round(sum(values), 2),
    }
```

and replace the two test lines at the bottom with one new test:

<!-- run: none -->
<!-- check: summarize_exports.py stage 2 -->
```python
print(summarize(Path("sales_exports/riverstone_2025_01.csv")))
```

How it works:

- **The loop** is section 17.9's January total, keeping the values in a list instead of adding them up, so the function can report both the count and the total.
- **The `try` catches three errors, each for a reason:** `ValueError` for a value that won't convert (a blank, or `'twenty'`); `TypeError` for a row with fewer fields than the header, where the missing values arrive as `None`; and `KeyError` for a file with no `status` or `net_revenue` column at all. A bad row adds 1 to `bad` instead of stopping the script.
- **It returns a dictionary**, one entry per fact, built across several lines for readability. Brackets let a statement run over several lines.

<!-- run: none -->
<!-- check: summarize_exports.py stage 2 run -->
```
# terminal
$ python summarize_exports.py
{'file': 'riverstone_2025_01.csv', 'rows': 15, 'lines_counted': 15, 'unreadable': 0, 'net_revenue': 202640.0}
```

January again: 15 rows, all counted, none unreadable, ₹2,02,640.00.

### Stage 3: every file, as a table

Add `main()` below `summarize()`:

<!-- run: none -->
<!-- check: summarize_exports.py stage 3 -->
```python
def main(folder):
    """Print one line per CSV file in folder, then a total; return an exit code."""
    paths = sorted(Path(folder).glob("*.csv"))
    if not paths:
        print(f"No CSV files found in {folder}")
        return 1
    print(f"{'file':<28}{'rows':>6}{'net revenue':>16}")
    total = 0.0
    for path in paths:
        s = summarize(path)
        total += s["net_revenue"]
        print(f"{s['file']:<28}{s['rows']:>6}{s['net_revenue']:>16,.2f}")
    print(f"{'TOTAL':<28}{'':>6}{total:>16,.2f}")
    return 0
```

and replace the test line with:

<!-- run: none -->
<!-- check: summarize_exports.py stage 3 -->
```python
main("sales_exports")
```

How it works:

- **`if not paths:`** handles the empty case first: no CSV files means a message and `return 1`. The next stage explains the 1.
- **The f-strings line up a table.** Each `{...}` has a width and a direction:

| Format | Means | Used for |
|---|---|---|
| `:<28` | left-aligned in 28 characters | the file name |
| `:>6` | right-aligned in 6 characters | the row count |
| `:>16,.2f` | right-aligned in 16, thousands separators, 2 decimals | the net revenue |

- **`{'file':<28}`** formats a fixed piece of text the same way, for the heading. Inside an f-string written with double quotes, the text uses single quotes, so Python can tell where the f-string ends. `{'':>6}` is an empty string padded to 6 spaces, which keeps the total under its column.
- **`return 0`** at the end means "all went well".

<!-- run: none -->
<!-- check: summarize_exports.py stage 3 run -->
```
# terminal
$ python summarize_exports.py
file                          rows     net revenue
riverstone_2025_01.csv          15      202,640.00
riverstone_2025_02.csv          20      253,664.00
riverstone_2025_03.csv          18      278,007.50
riverstone_2025_04.csv          21      210,281.50
riverstone_2025_05.csv          29      329,358.75
riverstone_2025_06.csv          22      186,928.00
riverstone_2025_07.csv          29      232,692.25
riverstone_2025_08.csv          28      329,282.00
riverstone_2025_09.csv          40      558,314.75
riverstone_2025_10.csv          38      681,070.75
riverstone_2025_11.csv          35      633,408.00
riverstone_2025_12.csv          35      439,823.50
TOTAL                                 4,335,471.00
```

The twelve months add up to ₹43,35,471.00, the key accounts' 2025 revenue from Chapters 10, 11, and 13. That match is how you know the script is right.

### Stage 4: arguments and an exit code

The script still reads only `sales_exports`, because the folder name is written into it. A script should take its inputs as **arguments**: extra words typed after the script's name in the terminal. Python puts them in a list called `sys.argv`. See it with a two-line script, `show_args.py`:

<!-- run: none -->
<!-- check: show_args.py -->
```python
import sys
print(sys.argv)
```

<!-- run: none -->
<!-- check: show_args.py run -->
```
# terminal
$ python show_args.py sales_exports
['show_args.py', 'sales_exports']
```

`sys` is the standard-library module for things about the running Python. `sys.argv` (argument values) is a list: item 0 is the script's own name, and item 1 onward are the words you typed after it.

Now finish `summarize_exports.py`. Add `import sys` below `import csv`, and replace `main("sales_exports")` at the bottom with:

<!-- run: none -->
<!-- check: summarize_exports.py stage 4 -->
```python
if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "sales_exports"
    raise SystemExit(main(folder))
```

How it works:

- **`if __name__ == "__main__":`** means "only when this file is run directly". Python sets the special name `__name__` to `"__main__"` for the file you run; when another script *imports* this one to reuse `summarize()`, the block doesn't run, and nothing prints.
- **`sys.argv[1] if len(sys.argv) > 1 else "sales_exports"`** is a conditional expression (section 17.5): the first argument if there is one, otherwise a sensible default.
- **`raise SystemExit(main(folder))`** runs `main()` and then stops the script, handing `main()`'s return value to the terminal as the **exit code**: a number every program leaves behind when it finishes. `0` means success and anything else means failure. A scheduler (Chapter 20) reads it to know whether the job worked.

Here's the whole file:

<!-- run: none -->
<!-- check: summarize_exports.py stage 4 -->
```python
"""Summarize every CSV export in a folder.

Usage:  python summarize_exports.py sales_exports
"""
import csv
import sys
from pathlib import Path


def read_rows(path):
    """Return the rows of a CSV file as a list of dictionaries."""
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def summarize(path):
    """Return one summary dictionary for a CSV export."""
    rows = read_rows(path)
    values = []
    bad = 0
    for row in rows:
        try:
            if row["status"] != "Cancelled":
                values.append(float(row["net_revenue"]))
        except (ValueError, TypeError, KeyError):
            bad += 1
    return {
        "file": path.name,
        "rows": len(rows),
        "lines_counted": len(values),
        "unreadable": bad,
        "net_revenue": round(sum(values), 2),
    }


def main(folder):
    """Print one line per CSV file in folder, then a total; return an exit code."""
    paths = sorted(Path(folder).glob("*.csv"))
    if not paths:
        print(f"No CSV files found in {folder}")
        return 1
    print(f"{'file':<28}{'rows':>6}{'net revenue':>16}")
    total = 0.0
    for path in paths:
        s = summarize(path)
        total += s["net_revenue"]
        print(f"{s['file']:<28}{s['rows']:>6}{s['net_revenue']:>16,.2f}")
    print(f"{'TOTAL':<28}{'':>6}{total:>16,.2f}")
    return 0


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "sales_exports"
    raise SystemExit(main(folder))
```

Run it with the folder as an argument, then ask the terminal for the exit code:

<!-- run: none -->
<!-- check: final run 1 -->
```
# terminal
$ python summarize_exports.py sales_exports
file                          rows     net revenue
riverstone_2025_01.csv          15      202,640.00
riverstone_2025_02.csv          20      253,664.00
riverstone_2025_03.csv          18      278,007.50
riverstone_2025_04.csv          21      210,281.50
riverstone_2025_05.csv          29      329,358.75
riverstone_2025_06.csv          22      186,928.00
riverstone_2025_07.csv          29      232,692.25
riverstone_2025_08.csv          28      329,282.00
riverstone_2025_09.csv          40      558,314.75
riverstone_2025_10.csv          38      681,070.75
riverstone_2025_11.csv          35      633,408.00
riverstone_2025_12.csv          35      439,823.50
TOTAL                                 4,335,471.00

$ echo $?
0
```

**`echo $?`** prints the exit code of the last command, on macOS and Linux. In PowerShell, type `$LASTEXITCODE` instead. `0`: it worked.

What if the folder name is wrong? **Before you run it, predict the output and the exit code.**

<!-- run: none -->
<!-- check: final run 2 -->
```
# terminal
$ python summarize_exports.py sales_export
No CSV files found in sales_export

$ echo $?
0
```

A typo in the folder name (`sales_export`, no `s`) finds no files, so `main()` prints its message and returns 1. The script didn't crash, and a scheduler would still know it failed.

What makes it a script rather than a pile of code:

- **A docstring at the top** says what it does and how to run it.
- **Functions with one job each**, each with a docstring. `summarize()` can be tested on one file.
- **`if __name__ == "__main__":`**, so another script can import its functions without running it.
- **Arguments** from `sys.argv`, with a sensible default. Nothing is tied to your laptop.
- **An exit code:** `0` for success, non-zero for failure.

A script that runs unattended at 6 a.m. should also write a **log**, timestamped messages saved for later, instead of printing to a screen nobody watches. Chapter 18 does that with the `logging` module, and adds proper command-line options with `argparse`; Chapter 20 puts such a script on a schedule.

> **Tool note: style, so other people can read it.** Python's style guide, **PEP 8**, is worth ten minutes: four-space indents, `snake_case` names, spaces around operators, lines under about 100 characters, imports at the top. Don't memorize it: install a **formatter** (`ruff format` or `black`, which rewrite the layout for you) and a **linter** (`ruff`, which points out likely mistakes), and let them do it. Most teams run them automatically, and consistent code is code you can read at speed.

---

## 17.13 Getting unstuck

Every programmer is stuck several times a day. What separates people is how quickly they get moving again.

1. **Read the error properly.** The last line names the problem; the lines above say where. Half of all "I'm stuck" moments end here.
2. **Check the obvious three:** am I in the right folder, the right environment, and running the file I think I am? (`pwd`, the `(.venv)` in the prompt, and the file name in the command.)
3. **Make the smallest failing example.** Cut everything unrelated. Often the answer appears while cutting.
4. **Search well.** Paste the error type and the meaningful part of the message, not your variable names: `python ValueError could not convert string to float csv` finds the answer; `my code doesn't work` doesn't. Prefer the official documentation and recent, high-voted answers; check the Python version an answer was written for.
5. **Read the documentation.** `help(str.strip)` in the REPL, or the module's page on docs.python.org. Look for the signature (the function's name and what goes in, such as `round(number, ndigits=None)`), the description, the examples, and the notes; that's where `round(2.675, 2)` was explained in section 17.3.
6. **Use an AI assistant like a knowledgeable colleague who can't see your data.** It's excellent at explaining an error, drafting a function, and suggesting an approach. It is confidently wrong often enough that you must run the code, check the numbers against something you trust, and never paste confidential data into it. If you can't explain what the code does, you can't defend the result, and you'll be the one in the meeting.
7. **Ask a human well:** what you're trying to do, what you did, what happened, what you expected, and the smallest example. Half the time you answer your own question while writing it.
8. **Take a break.** A ten-minute walk solves an astonishing share of bugs.

> **Stop here: sitting 6 of 6, done.** That's the whole of Python's core. The project and exercises below are where it becomes yours.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Installing packages without the environment active | "pip installed it, but Python can't find it"; one project breaks another | Activate `.venv`; install with `python -m pip install …` |
| Working in the wrong environment | `ModuleNotFoundError` for something you installed | Check the prompt shows `(.venv)`; **Python: Select Interpreter** and the notebook's kernel in VS Code |
| Running commands in the wrong folder | `No such file or directory`, or `FileNotFoundError` | `pwd` to check where you are, then `cd` |
| Expecting a script to print expressions | A script that "does nothing" | `print()` what you want to see |
| Mixing tabs and spaces | `IndentationError` | Let the editor insert four spaces |
| `=` where `==` belongs | `SyntaxError: invalid syntax` (Python often suggests "Maybe you meant '=='") | `=` assigns, `==` compares |
| Forgetting that CSV values are text | `"430" + 5` fails, or totals join up as text | Convert with `float()`/`int()`, defensively |
| Assuming a column exists | `KeyError` in row 4,000 | `.get()` with a default; check the header first |
| Opening files without an encoding | Gibberish for `₹` and Indian names on another machine | `encoding="utf-8"` every time |
| Building paths by gluing strings | Works on your laptop, fails on the server | `pathlib`, and `/` to join |
| Using `.sort()` and assigning the result | `None` where a list should be | `sorted(x)` returns a new list; `x.sort()` changes `x` |
| Changing a list while looping over it | Items skipped for no visible reason | Build a new list, or loop over a copy |
| Bare `except:` | Typos and interrupts swallowed silently | Catch the specific errors you expect |
| Turning bad data into 0 | A report that looks complete and is wrong | Count and report failures (Chapter 14) |
| Copying a formula into ten places | One of them is out of date within a month | A function, called ten times |
| One giant script with no functions | Impossible to test or reuse | Small functions with docstrings |
| Hard-coded paths and passwords | Runs only on your machine; secrets in every copy | Arguments and environment variables |
| Notebook delivered as the product | Cells run out of order; nobody can schedule it | Move the working code into a script |
| Pasting AI-generated code without reading it | Plausible code, wrong numbers, no explanation | Run it, check against a number you trust, and understand it |

---

## In the real world: the fifteen-minute rescue

Riverstone's operations team sent Meera a folder on a Thursday afternoon: 13 CSV files, one per branch per month for the last quarter plus one more, exported from the old billing system before it was switched off. Finance wanted a single question answered by Monday: how much was invoiced in the quarter, by branch, and did it match the ERP?

Her first instinct was the usual one: open them in Excel, paste them together, pivot. She'd done it before with a dozen files and it had taken an afternoon. This time the columns weren't in the same order in every file.

She wrote fourteen lines of Python instead. The heart of it:

<!-- run: none -->
```python
files = sorted(Path("billing_exports").glob("*.csv"))
rows = []
for path in files:
    with open(path, encoding="utf-8", newline="") as f:
        rows.extend(csv.DictReader(f))
```

`extend()` adds every item from another collection to the list, where `append()` adds one; here, every row of each file. The dictionary reader didn't care about column order, because each row's values are found by column name, which solved the problem that would have cost her the afternoon. The script then converted amounts with a `to_float()` like the one in section 17.10, counted what it couldn't convert, grouped by branch with a `defaultdict`, and printed a table.

It took fifteen minutes to write and two seconds to run. It also found three things the spreadsheet approach would have hidden:

- **Eleven rows had an empty amount.** The script listed them with their file and line number; they turned out to be cancelled invoices the old system exported as blanks.
- **One file, `Mumbai_2025_09 (1).csv`, was an exact duplicate of September's 412 rows**, saved twice. It would have silently added ₹1.4 crore to the quarter.
- **Two branches spelled their own name three ways.** The grouping showed "Kolkata", "kolkata", and "KOL" as separate branches, which is Chapter 14's mapping-table problem in miniature.

The quarter came to ₹1.4 crore less than Finance's first estimate, entirely because of the duplicate. Meera sent the script with the answer, so the next person could rerun it, and the team asked her to run it again for the two quarters before that. That took four seconds.

What made the difference:

- She **chose the tool for the shape of the job**: many files, uneven columns, a question that would be asked again.
- She **wrote defensively**: convert, count failures, report them, instead of letting bad rows vanish.
- She **kept the script**, so the work became reusable rather than a heroic afternoon.
- She'd have been slower on her first day of Python. That's the point of this chapter: the first script is slow, the tenth is faster than the spreadsheet, and the hundredth is a thing colleagues ask for by name.

---

## Project: summarize a folder of exports

**Goal:** a script that reads a folder of CSV files and prints a summary of each, then writes a small report. This is the shape of a hundred real analyst tasks.

### Tools you'll need

- **Python 3.14** in the book's virtual environment, set up in section 17.0 (any Python from 3.11 on works; this chapter's code was checked on 3.14.7 and 3.11.15).
- **VS Code** with the Python and Jupyter extensions, or any editor you like, and **JupyterLab** for notebooks.
- **Standard library only:** this chapter installs nothing except JupyterLab. `pandas` arrives in Chapter 18.
- **Companion files (`companion/ch17/`), copied into `work/ch17/`:**
  - `sales_exports/`: twelve monthly CSVs of the 24 key accounts' 2025 order lines (330 lines in total), plus `README.txt` so your folder code has to filter by extension.
  - `products.json`: the eight products as JSON.
  - `targets_2025.csv`: the key accounts' monthly targets for 2025 (₹42,40,000 for the year).
  - `broken_export.csv`: March's file with one unreadable row added, for section 17.10.
  - `check_setup.py`: the setup checker from section 17.0.
  - `summarize_exports.py`: the finished script from section 17.12, to compare with yours.
- **Optional:** `ruff` (formatter and linter), and the free official tutorial at docs.python.org for a second explanation of anything here.

**Option A: your own data.** A folder of exports you receive regularly (anonymized).

**Option B: Riverstone.** `work/ch17/sales_exports/`.

**Steps**

1. **List the files** with `pathlib`, ignoring anything that isn't a `.csv`.
2. **Read each file** with `csv.DictReader`.
3. **For each file, compute:** row count, the number of lines you could convert, the number you couldn't, net revenue excluding cancelled lines, and the number of distinct customers.
4. **Print a table** with aligned columns and a total row.
5. **Write a report** to `summary.md`: a Markdown table of the same numbers, with today's date and the folder name at the top.
6. **Handle the awkward cases:** an empty folder, a file with no rows, a file missing the `net_revenue` column, and a row whose value can't be converted. Report them; don't crash and don't silently skip them.
7. **Structure it properly:** small functions with docstrings, `if __name__ == "__main__":`, the folder as a command-line argument with a default, and an exit code.
8. **Check it:** the twelve Riverstone files hold **330 lines**, of which **326** are not cancelled, and their net revenue is **₹43,35,471.00**, the same figure as Chapters 10, 11, and 13, which is how you know the script is right.

**Stretch goals**

- Add the targets from `targets_2025.csv` and show attainment per month (the year comes to 102.3% of ₹42,40,000).
- Write the summary as JSON as well, so another script could read it.
- Add a `tests.py` that checks `to_float("")`, `to_float("430.5")`, and `summarize()` on one known file, using `assert` (exercise 28 shows how); a first taste of Chapter 29's testing.

---

## Timed challenge: the folder in forty minutes

Forty minutes, `work/ch17/sales_exports/`, standard library only, no pandas. Answers at the end of the chapter.

- **Level 1:** How many CSV files are in the folder, and how many data rows in total?
- **Level 2:** How many rows are not cancelled, and what is their total net revenue?
- **Level 3:** Which month had the highest net revenue, and how much?
- **Level 4:** What are the top three products by net revenue?
- **Level 5:** How many distinct customers have non-cancelled revenue, and which two bought the most?
- **Level 6:** Count the rows by status.
- **Level 7:** What are the mean, median, and maximum line values (non-cancelled)?
- **Bonus:** Total quantity sold, the largest single line quantity, and the number of cities.

---

## Recap

- **Python earns its place** where a spreadsheet or SQL can't go: many files, APIs, schedules, statistics, and anything you'd otherwise repeat.
- **A terminal needs only a few commands to start:** `pwd`, `ls`, `cd`, and `cd ..`, plus Tab, the up arrow, and `Ctrl+C`.
- **Install it properly:** Python 3.14; VS Code with the Python and Jupyter extensions; a **virtual environment**, activated in each new terminal, with packages installed by `python -m pip install` and recorded in `requirements.txt`. `check_setup.py` confirms it.
- **Types matter:** `str`, `int`, `float`, `bool`, `None`. CSV values arrive as text and must be converted, which is where cleaning bugs live. Floats are approximate, and Python's `round()` sends halves to the even neighbour.
- **Collections:** list (ordered), tuple (fixed), dict (lookup), set (unique and fast membership). Counting and grouping with a dict, or `Counter` and `defaultdict`, is the manual version of a SQL `GROUP BY`.
- **Conditions and loops** need a colon and consistent indentation; `for` over a collection is the normal loop; comprehensions are one-line loops that build a list or a dictionary.
- **Functions** turn a formula into something you can name, reuse, test, and change in one place.
- **Files:** `pathlib` for paths, `with open(...)` for reading and writing, `encoding="utf-8"` always, `csv.DictReader` and `json` for the two formats you'll meet most.
- **Errors are information.** Read the last line first, know the common ten, catch what you expect, and count what you couldn't process instead of hiding it.
- **The standard library** covers dates, counting, statistics, regular expressions, and more before you install anything.
- **A script** has a docstring, functions, arguments, `if __name__ == "__main__":`, and an exit code. That's the difference between a notebook that worked once and a tool the team can run.
- **Getting unstuck is a skill:** read the error, shrink the example, search precisely, use AI as a colleague you check, and ask humans well.

---

## Key terms

terminal · command · prompt · working folder (current directory) · `pwd`, `ls`, `cd` · option · program · Python · Python install manager · REPL · script · notebook · cell · kernel · Jupyter · VS Code · extension · virtual environment (`venv`) · activate · execution policy · package · `pip` · PyPI · `requirements.txt` · module · `import` · standard library · function · argument · string · variable · assignment · type (`str`, `int`, `float`, `bool`, `None`) · comment · method · f-string · format specification · type conversion · floating-point number · `Decimal` · banker's rounding (round half to even) · list · index · slice · tuple · unpacking · condition · `if`/`elif`/`else` · comparison operator · truthiness · conditional expression · loop · `for` · `while` · `range` · `enumerate` · `zip` · `+=` · `break` · `continue` · list comprehension · dictionary · key and value · `get` with default · dictionary comprehension · set · union, intersection, difference · parameter · default value · keyword argument · `return` · scope · docstring · `pathlib` · path object · attribute · `glob` · wildcard · context manager (`with`) · encoding · `csv.DictReader` · `csv.DictWriter` · JSON · traceback · exception · `try`/`except` · `repr` · `datetime` · `strptime`/`strftime` · `Counter` · `defaultdict` · standard deviation · environment variable · `sys.argv` · exit code · `if __name__ == "__main__"` · PEP 8 · linter · formatter

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can open a terminal, see where you are, move between folders, and run a Python file.
- [ ] You can install Python, create and activate a virtual environment, and install a package into it without guessing, and `check_setup.py` says *Setup OK*.
- [ ] You can explain the difference between the REPL, a notebook, and a script, and choose sensibly.
- [ ] You use variables, f-strings, and the basic types without looking them up, and you know why 2.5 rounds to 2 in Python.
- [ ] You choose between a list, a dictionary, a tuple, and a set for a given job.
- [ ] You write conditions and `for` loops, and can read a comprehension aloud.
- [ ] You write small functions with arguments, defaults, a return value, and a docstring.
- [ ] You read and write CSV, JSON, and text files with `pathlib`, always specifying the encoding.
- [ ] You read a traceback, name the common errors, and use `try`/`except` where it's the right answer.
- [ ] You know what's in the standard library before reaching for a package.
- [ ] You can turn a notebook that works into a script someone else can run, with arguments and an exit code.
- [ ] When you're stuck, you have a routine, and it doesn't start with "ask someone".

---

## Exercises

Use `work/ch17/` and the standard library only. Run everything; the point is the typing.

### Warm-up

1. In the REPL, work out: 17 % 5, 17 // 5, 2 ** 8, `int("42") + 8`, and `float("3.5") * 2`. What does `int("42.5")` do, and why?
2. Create variables for a customer name, an order count, and a revenue figure, then print one sentence with an f-string showing revenue to two decimals and orders as a whole number.
3. What's the difference between `"430" + "5"` and `430 + 5`, and how do you get 435 from the first pair?
4. Predict, then check: `bool("")`, `bool("0")`, `bool([])`, `bool([0])`, `None == False`, `1 == True`.
5. Given `cities = ["Mumbai", "Pune", "Bengaluru", "Delhi"]`, write expressions for: the first city, the last, the middle two, the list sorted, the list reversed, and whether "Kolkata" is in it.
6. Explain the difference between a list and a tuple, and give a Riverstone example of each.
7. A friend's terminal shows `python: can't open file '/home/priya/analyst-to-architect/work/check_setup.py': [Errno 2] No such file or directory`. List two likely causes, and how you'd check each.
8. Predict, then check: `round(4.5)` in Python, and `=ROUND(4.5,0)` in a spreadsheet. Explain why they differ.

### Core

9. Write a function `net_line(quantity, unit_price, discount_pct=0)` that returns the line value, and a second function `is_large(value, threshold=25000)` that returns True or False. Test both on three lines you compute by hand.
10. Read `sales_exports/riverstone_2025_01.csv` with `csv.DictReader` and print the first three rows' customer name and net revenue. How many rows are there?
11. Total the non-cancelled net revenue in January. What is it, and how many lines did you count?
12. Loop over all twelve files and count the total number of rows in the folder. How many CSV files are there, and why must you filter by suffix?
13. Compute net revenue by month across the folder, print it as an aligned table, and name the highest and lowest months.
14. Build a dictionary of net revenue by product across the year, and print the top three.
15. Count the rows by status with `Counter`. How many are cancelled?
16. Using a set, list the distinct cities in the folder. How many are there?
17. Write `to_float(text, default=None)` and use it on `broken_export.csv`: how many rows convert, how many don't, and what are the bad values?
18. Read `products.json` and build a dictionary from product name to unit price. Which product is the most expensive, and what does it cost?
19. Read `targets_2025.csv` and calculate attainment per month (revenue ÷ target). In how many months did the key accounts beat their target, and what is the year's attainment?
20. Write a function `summarize(path)` that returns a dictionary with the file name, row count, non-cancelled line count, and net revenue. Run it on three files.
21. Write the folder summary to `summary.csv` with `csv.DictWriter`: one row per file, with a total row at the end.
22. Convert the `order_date` text to a `date` with `strptime`, and find the earliest and latest order dates in the folder.
23. Write a list comprehension that returns the net revenue of every cancelled line in the folder, then explain the same thing as a `for` loop.
24. Trigger each of these on purpose and paste the last line of the traceback: `KeyError`, `ValueError`, `FileNotFoundError`, `ZeroDivisionError`.
25. You installed JupyterLab, but `check_setup.py` still says it's missing. Explain the most likely reason, and write the two commands, for your operating system, that fix it.
26. Find the official documentation page for Python's `round()` (docs.python.org, *Built-in Functions*) for the version you installed. Write down its signature, one example you ran yourself, and its note about `2.675`. Then find one tutorial or video that explains rounding in Python, and say whether it matches the documentation.

### Stretch

27. Write a function that takes the folder and returns a dictionary of customers whose net revenue exceeds a threshold, sorted from largest. Which customers exceed ₹4,00,000?
28. Write three small tests in a `tests.py` for `to_float` and `net_line`, using **`assert`**: `assert condition` does nothing when the condition is true, and stops with an `AssertionError` when it's false. Run the file.
29. Read the folder once into a list of dictionaries, then answer exercises 13, 14, and 15 from that list instead of re-reading the files. Time both with `time.perf_counter()` and explain the difference.

### Think about it

30. When is a notebook the right deliverable, and when is it the wrong one?
31. A colleague sends a script that works on their laptop and fails on yours with `FileNotFoundError` and then `ModuleNotFoundError`. What are the two likely causes, and what would you change in the script so it doesn't happen to the next person?
32. You ask an AI assistant for code to summarize a folder of CSVs. It gives you twenty lines that run and produce a number. What do you check before sending that number to Finance?
33. A Python report and an Excel report of the same invoices show totals that differ by ₹1. Using section 17.3, give one possible explanation, and describe how you'd confirm it.

---

## Answers

**1.** 17 % 5 = 2; 17 // 5 = 3; 2 ** 8 = 256; `int("42") + 8` = 50; `float("3.5") * 2` = 7.0. `int("42.5")` raises `ValueError`: `int()` parses whole numbers only, so convert with `float()` first and then round or truncate deliberately.

**2.** For example: `print(f"{customer} placed {orders:,} orders worth ₹{revenue:,.2f}.")`

**3.** `"430" + "5"` joins the text into `"4305"`; `430 + 5` adds to 435. Convert first: `int("430") + int("5")`.

**4.** `bool("")` False; `bool("0")` **True** (a non-empty string); `bool([])` False; `bool([0])` True (a list with one item); `None == False` False; `1 == True` True (booleans are integers in Python).

**5.** `cities[0]`, `cities[-1]`, `cities[1:3]`, `sorted(cities)`, `cities[::-1]` (or `list(reversed(cities))`), `"Kolkata" in cities`.

**6.** A list can be changed (append, remove, sort in place); a tuple can't. List: the order lines in a file. Tuple: a `(city, region)` pair, or the `(count, total, average)` returned by `summarize()`.

**7.** (1) The terminal is in a different folder from the script: the path in the message ends `work/check_setup.py`, one level above `work/ch17`. Check with `pwd`, then `cd ch17`. (2) The file isn't there, or has a different name: for example `check_setup.py.txt` because file extensions are hidden, or it's still inside a zip file. Check with `ls`, show file extensions, and unzip the download.

**8.** Python gives **4**; the spreadsheet gives **5**. Python's `round()` sends a half to the even neighbour (banker's rounding), and 4 is even; the spreadsheet's `ROUND` sends halves away from zero.

**9.** For example, `net_line(45, 430, 5)` is 18,382.50; `net_line(10, 290)` is 2,900.00; `is_large(18382.5)` is False with the default threshold and True with 15,000.

**10.** January has **15** rows. The first three are Patel Kitchenware (₹2,900.00), Green Leaf Hotels (₹20,900.00), and Metro Mart (₹2,900.00).

**11.** **₹2,02,640.00** across 15 lines (January has no cancelled lines).

**12.** **12** CSV files, **330** data rows. `sales_exports` also contains `README.txt`; `glob("*.csv")` filters by suffix, and reading the README as CSV would produce nonsense rows rather than an error, which is worse.

**13.** Highest **October, ₹6,81,070.75**; lowest **June, ₹1,86,928.00**. (Full year, non-cancelled, to the nearest rupee: Jan 2,02,640 · Feb 2,53,664 · Mar 2,78,008 · Apr 2,10,282 · May 3,29,359 · Jun 1,86,928 · Jul 2,32,692 · Aug 3,29,282 · Sep 5,58,315 · Oct 6,81,071 · Nov 6,33,408 · Dec 4,39,824.)

**14.** Storage Box 25L **₹9,08,212.50**, Storage Box 10L **₹8,60,946.00**, Industrial Crate **₹7,95,830.00**.

**15.** Delivered 322, Cancelled **4**, Shipped 3, Pending 1 (330 rows).

**16.** **16** cities.

**17.** 18 of the file's 19 rows convert; **one** row fails, the planted line with `quantity` `'twenty'` and an empty `net_revenue`. Report both bad values with the line number, as section 17.10 does.

**18.** The most expensive product is the **Industrial Crate at ₹1,400.00**.

**19.** The key accounts beat their target in **6** of 12 months, and the year came to **102.3%** of ₹42,40,000 (₹43,35,471.00), the same figure as Chapter 10.

**20.** For example, January returns `{"file": "riverstone_2025_01.csv", "rows": 15, "lines_counted": 15, "net_revenue": 202640.0}`.

**21.** Use `csv.DictWriter` with `fieldnames=["file", "rows", "lines_counted", "net_revenue"]`, `writeheader()`, a row per file, and a final row with `file="TOTAL"` and the sum, ₹43,35,471.00.

**22.** Earliest **2 January 2025**, latest **23 December 2025**, using `datetime.strptime(row["order_date"], "%Y-%m-%d").date()`.

**23.** `[float(r["net_revenue"]) for r in rows if r["status"] == "Cancelled"]` gives the four cancelled line values. The loop version creates an empty list, loops over `rows`, checks the status, and appends: same result, three more lines, and easier to extend when the condition grows.

**24.** `KeyError: 'city'` · `ValueError: could not convert string to float: ''` · `FileNotFoundError: [Errno 2] No such file or directory: 'nope.csv'` · `ZeroDivisionError: division by zero`. (The exact wording can differ slightly between Python versions.)

**25.** JupyterLab went into a different Python from the one running the script, usually because the virtual environment wasn't active when you installed it. From the `analyst-to-architect` folder: on Windows, `.venv\Scripts\Activate.ps1`, then `python -m pip install jupyterlab`; on macOS or Linux, `source .venv/bin/activate`, then `python -m pip install jupyterlab`. Then run `check_setup.py` again from `work/ch17`.

**26.** Answers vary. A complete answer gives the signature, `round(number, ndigits=None)`; an example you ran, such as `round(2.5)` giving `2`; and the note that `round(2.675, 2)` gives `2.67` "instead of the expected 2.68. This is not a bug". Many tutorials say "Python rounds .5 up", which doesn't match the documentation; noticing that is the point of the exercise.

**27.** Two customers exceed ₹4,00,000 in 2025: **Sharma Hardware ₹5,02,775.00** and **Harbour Traders ₹4,12,680.50**.

**28.** For example: `assert to_float("430.5") == 430.5`, `assert to_float("") is None`, `assert net_line(10, 290) == 2900`. Run with `python tests.py`; silence means they passed, and an `AssertionError` names the failing line.

**29.** Reading once into memory is much faster, because the cost is opening and parsing the files, not the arithmetic. With 330 rows the difference is milliseconds; with 3 million rows, re-reading for every question is the difference between seconds and minutes. It's the same principle as Chapter 13's "let the database do the work once" and Chapter 16's Import mode.

**30.** A notebook is right for exploration, teaching, and showing your working, where the reader wants to see code and output together. It's wrong as a scheduled job, as a thing colleagues run, or as anything whose correctness depends on cells being run in order. Deliver a script (or a report the script produces) and keep the notebook as evidence.

**31.** `FileNotFoundError`: a hard-coded absolute path, or a relative path that assumes a particular working folder. `ModuleNotFoundError`: a package installed in their environment and not in yours, with no `requirements.txt`. Fix both: take paths as arguments with sensible defaults, resolve them with `pathlib`, and ship a `requirements.txt` (and a one-line "how to run" in the docstring).

**32.** Read it line by line and make sure you can explain each one. Check what it excludes (cancelled rows? blank amounts?), what it does with rows it can't parse, and whether it counts files you didn't intend (the README). Then reconcile the output against something you trust: one file totalled by hand, or the same period from the ERP. The number goes to Finance under your name, not the assistant's.

**33.** The two tools may round halves differently: Python's `round()` sends halves to the even neighbour (and a float like 2.675 is stored slightly below the half), while Excel's `ROUND` sends halves away from zero. If each invoice is rounded before the totals are added, small differences can add up to a rupee. To confirm: find invoices whose unrounded values end in exactly half of the rounding unit, compare each line's rounded value in both reports, and check whether the differences add up to ₹1. The lasting fix is to agree on one rule and round at the end (Chapter 4).

**Timed challenge answers.** Level 1: **12** files, **330** rows. Level 2: **326** non-cancelled rows, **₹43,35,471.00**. Level 3: **October, ₹6,81,070.75**. Level 4: Storage Box 25L ₹9,08,212.50 · Storage Box 10L ₹8,60,946.00 · Industrial Crate ₹7,95,830.00. Level 5: **23** customers; **Sharma Hardware ₹5,02,775.00** and **Harbour Traders ₹4,12,680.50**. Level 6: Delivered 322 · Cancelled 4 · Shipped 3 · Pending 1. Level 7: mean **₹13,298.99**, median **₹10,212.50**, maximum **₹56,700.00**. Bonus: **9,475** units, largest line **85** units, **16** cities.

---

## Where this leads

- **Chapter 18, Python for Analysts:** pandas replaces most of the loops in this chapter with whole-table operations, and adds Excel, SQL, APIs, charts, and scripts with logging and command-line options.
- **Chapter 19, Spreadsheet Automation:** the same programming ideas in VBA and Apps Script, for work that has to stay inside a spreadsheet.
- **Chapter 20, Automating Reports & Delivering Insights:** scheduling scripts, sending email, handling failure, and keeping a log file of every run.
- **Chapter 21 and 22:** statistics, with simulations written in Python.
- **Chapter 26, Git:** version control for the scripts you're now writing, and the terminal in more depth.
- **Chapter 29, Python as Software, Not Scripts:** modules, packaging, testing, and type hints, once scripts grow up.
- **Interview preparation:** the Python & pandas Question Bank (Chapter 72) starts with exactly these fundamentals.
