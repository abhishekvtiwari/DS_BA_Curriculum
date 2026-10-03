-- Chapter 12. Databases & SQL Foundations
-- Practice SQL for POSTGRESQL, extracted from the chapter.
--
-- Riverstone Supplies is the worked example throughout the book. Load the database
-- first (companion/riverstone_setup_mini.sql, riverstone_2025_setup.sql, or
-- companion/full/riverstone_full_setup_postgresql.sql), then run these statements in order.
--
-- Each statement keeps the chapter's explanation above it and the chapter's own
-- result below it, marked as the chapter's. Run it yourself to see your own.
-- Source: manuscript/ch12-databases-and-sql-foundations.md


-- A few details are planted on purpose, because real data always has them:

-- - Sunrise Caterers has no city (an empty value, called NULL). - Blue Bay Cafe has never ordered.
-- - The Garden Chair has never sold. - Order 5008 has no sales rep. - Order 5004 was cancelled, so
-- it shouldn't count as revenue. - order_items stores the price actually charged at the time of
-- sale, separately from today's list price in products. Prices change; history shouldn't. -
-- products.unit_cost is the standard cost of making each product, so you can calculate profit, not
-- just revenue. - Invoices are raised when an order ships (the amount is net of discount; tax is
-- left out to keep the numbers simple). Customers often pay in parts: invoices 9002 and 9005 were
-- paid in two instalments, 9003, 9006, and 9008 are only partly paid, and 9007 and 9010 haven't
-- been paid at all. - Throughout the chapter, "today" is 31 March 2026, the end of the quarter.

-- > Why store the price twice? It looks like it breaks "store each fact once", but the two columns
-- are different facts: the list price today, and the price charged on 5 January. If the Industrial
-- Crate goes up to ₹1,600 next month, January's revenue must not change. Spotting that difference
-- is the kind of judgment interviewers look for.

-- ---

-- =============================================================================================
-- 12.3 Setting up your SQL laboratory
-- =============================================================================================

-- You need two things: a database server that stores the data and runs queries, and a client, the
-- app where you type queries and see results.

-- =============================================================================================
-- Which database should you install?
-- =============================================================================================

-- This book teaches with PostgreSQL and shows MySQL alongside it. Both are free, both are used by
-- thousands of companies, and between them they cover most of the databases an analyst meets at
-- work.

-- | | PostgreSQL | MySQL | |---|---|---| | Where you'll meet it | Analytics teams, fintech,
-- government, SaaS products; the base of several cloud warehouses | Web and e-commerce
-- applications, WordPress sites, many startups' production systems, online stores | | Why learn it
-- | Follows the SQL standard closely, so what you learn transfers well | Very likely to be the
-- database behind the app your company runs | | In this book | Every query and result is shown in
-- PostgreSQL | Section 12.16 shows every difference that matters, and the companion files have a
-- tested MySQL version of every query |

-- Recommendation: install PostgreSQL first and work through the chapter with it. If your company
-- uses MySQL, or a job description mentions it, install MySQL as well (it takes twenty minutes)
-- and run the queries in both. Seeing the same question answered in two dialects is the fastest
-- way to learn which parts of SQL are universal and which are local spelling. You can run both
-- servers on one computer at the same time; they use different ports.

-- For both databases you'll use DBeaver Community Edition as the client. It's free, runs on
-- Windows, macOS, and Linux, and connects to almost every database, so you learn one editor, not
-- two.

-- Which versions? Choose the current release of each. In September 2026 that was PostgreSQL 18
-- (supported until November 2030) and MySQL 9.7 LTS. Every query in this chapter was run on
-- PostgreSQL 16 and MySQL 8.0, and uses only features that work the same way in the newer
-- versions. Install every tool from its official website; download sites that repackage installers
-- sometimes bundle unwanted software.

-- =============================================================================================
-- Three words you'll meet while connecting
-- =============================================================================================

-- - localhost means "this computer". The database server runs on your own machine, so that's where
-- DBeaver looks for it. - A port is the numbered door a server listens on. PostgreSQL uses 5432
-- and MySQL 3306, which is why both can run on one computer at once. - A driver is the small
-- connector file DBeaver uses to talk to one kind of database. DBeaver downloads the right one the
-- first time you connect.

-- =============================================================================================
-- Option A: PostgreSQL
-- =============================================================================================

-- 1. Install the server. Download PostgreSQL from the official PostgreSQL website, then follow the
-- steps for your system:

-- - Windows. The website recommends the interactive installer by EDB. Accept the default folders
-- and port 5432. On the Select Components page, untick Stack Builder (you won't need it); pgAdmin,
-- PostgreSQL's own client, is optional, because you'll use DBeaver. Keep Command Line Tools
-- ticked. - macOS. Use the same EDB installer, or Postgres.app, a small app that runs PostgreSQL
-- from the menu bar: drag it to Applications, open it, and click Initialize. - Linux (Ubuntu or
-- Debian). These are terminal commands. If you use Linux you've probably used a terminal; if not,
-- Appendix B has the same steps with screenshots, and an online playground (at the end of this
-- section) needs no install at all. sudo means "run as administrator", apt is Ubuntu's installer,
-- and everything after # is a comment for you, not part of the command.

-- <!-- run: none --> sudo apt update sudo apt install postgresql                 # the server, and
-- the psql client sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'choose-a-password';"

-- The last line gives the postgres user a password, which DBeaver needs. (Ubuntu's own package may
-- be a version or two behind the newest; that's fine for this book.)

-- During setup you choose a password for the postgres user, the database's administrator account.
-- Write it down somewhere safe: without it you can't connect.

-- 2. Install DBeaver Community Edition from the DBeaver website. It includes everything it needs,
-- so there's nothing else to install.

-- 3. Connect. In DBeaver, choose Database → New Database Connection → PostgreSQL, and fill in host
-- localhost, port 5432, database postgres, user postgres, and your password. Click Test
-- Connection; DBeaver offers to download the driver the first time, so accept.

-- 4. Create the database. Open an SQL editor on that connection (the box "Running your first query
-- in DBeaver", below, shows how) and run:

CREATE DATABASE riverstone;


-- CREATE DATABASE makes a new, empty database called riverstone; section 12.13 explains it
-- properly. Now point the connection at it: right-click the connection → Edit Connection → on the
-- Main tab, set Database to riverstone → OK. Then right-click the connection again →
-- Invalidate/Reconnect (or Disconnect, then Connect).

-- 5. Load the data. Open riverstone_setup.sql from the companion files (Appendix E) and run the
-- whole script with Execute SQL Script (not Execute Statement; the box below explains the
-- difference). It creates the seven tables and inserts every row shown in section 12.2.

-- 6. Check it worked. Run this one-line query. COUNT(*) counts rows (section 12.9 teaches it):

SELECT COUNT(*) FROM order_items;

/* The chapter shows:
    count
   -------
       19
   (1 row)
*/


-- In DBeaver you see the same thing as a grid: one column, count, holding 19. Nineteen order
-- lines: the same twelve orders you followed through Chapters 1 to 5.

-- > Troubleshooting PostgreSQL. > - "password authentication failed". The password doesn't match
-- the one set during installation. If you've lost it on a practice computer with nothing you need
-- in it, the simplest fix is to uninstall PostgreSQL, delete its data folder, and install again;
-- Appendix B shows how to reset it without reinstalling. > - The installer says port 5432 is in
-- use. Another PostgreSQL is already installed, often an older one. Use that one, or accept the
-- port the installer suggests (such as 5433) and type the same number in DBeaver. > - "Connection
-- refused". The server isn't running. On Windows, open Services, find the entry that starts with
-- postgresql, and click Start; with Postgres.app, click Start; on Linux, run sudo systemctl start
-- postgresql.

-- =============================================================================================
-- Option B: MySQL
-- =============================================================================================

-- Which version? Install MySQL Community Server, the free edition, and choose the current LTS
-- (Long-Term Support) release. At the time of writing that's MySQL 9.7, released in April 2026 and
-- supported until 2034; 8.4 LTS is also fine. Avoid 8.0, which reached end of life in April 2026,
-- and the short-lived "Innovation" releases, which are aimed at people testing new features. Every
-- MySQL query in this book uses features that work the same way in 8.4 and 9.x.

-- 1. Install the server. Download MySQL Community Server from the official MySQL downloads page,
-- then follow the steps for your system:

-- - Windows. Download the MSI installer for Windows (64-bit). If the installer asks for the
-- Microsoft Visual C++ Redistributable, install that first; the download page links to it. When
-- the MSI finishes, MySQL Configurator opens automatically. Accept the Development Computer
-- configuration, keep port 3306, choose a strong password for the root account and write it down,
-- and leave Configure MySQL Server as a Windows Service and Start the MySQL Server at System
-- Startup ticked. You don't need to create extra user accounts or load the sample databases.
-- (Older guides tell you to use "MySQL Installer for Windows". That tool only installs version 8.0
-- and earlier, so skip it.) - macOS. Download the DMG archive that matches your Mac: ARM for Apple
-- silicon (M-series chips), x86 for older Intel Macs. Open it, run the .pkg installer, and set the
-- root password when asked. MySQL then appears in System Settings, where you can start and stop it
-- and choose whether it starts automatically. The command-line client is installed at
-- /usr/local/mysql/bin/mysql, for later. - Linux (Ubuntu or Debian). As for PostgreSQL, these are
-- terminal commands (sudo, apt-get, and # mean the same as above). Add Oracle's MySQL APT
-- repository by downloading its mysql-apt-config package from the MySQL downloads page, then run:

-- <!-- run: none --> sudo dpkg -i mysql-apt-config_*_all.deb    # installs a downloaded package
-- file; # choose the 9.7 LTS (or 8.4 LTS) series when asked sudo apt-get update
-- # refreshes the list of available packages sudo apt-get install mysql-server          # asks you
-- to set the root password systemctl status mysql                     # should show "active
-- (running)"

-- (Ubuntu's own apt install mysql-server, without the Oracle repository, also works but may give
-- you an older series.) Fedora, Red Hat, and similar systems use Oracle's Yum repository in the
-- same way.

-- 2. Connect with DBeaver. Choose Database → New Database Connection → MySQL, and use host
-- localhost, port 3306, user root, and your password. Leave Database blank for now. Accept the
-- driver download.

-- > Troubleshooting: "Public Key Retrieval is not allowed". This is the most common first-
-- connection error with MySQL 8.4 and later. Modern MySQL protects passwords with an
-- authentication method that needs a public key, and the driver won't fetch it unless you allow
-- it. For a server on your own computer, open the connection's Driver properties tab, set
-- allowPublicKeyRetrieval to true (and useSSL to false if it still complains), and reconnect.
-- Don't copy these settings to a company server; ask the database administrator for the correct
-- secure connection details instead.

-- 3. Load the data. Open riverstone_setup_mysql.sql from the companion files and run the whole
-- script (Execute SQL Script). Unlike the PostgreSQL script, this one creates the riverstone
-- database itself, so there's no separate step. Refresh the connection, and riverstone appears in
-- the navigator. Double-click it to make it the active database; DBeaver shows the active database
-- in the editor's toolbar.

-- > For later (Chapter 26): loading from the command line. Once you've met the terminal, one
-- command does the same job, asking for the root password first: mysql -u root -p <
-- riverstone_setup_mysql.sql. Until then, DBeaver's Execute SQL Script is all you need.

-- 4. Check it worked. In MySQL, USE riverstone; picks the database that the following statements
-- run in. Run it, then the same count as in PostgreSQL:

USE riverstone;
SELECT COUNT(*) FROM order_items;

/* The chapter shows:
   +----------+
   | COUNT(*) |
   +----------+
   |       19 |
   +----------+
*/


-- The same 19 lines. MySQL names the column after the expression, COUNT(*), where PostgreSQL wrote
-- count.

-- > MySQL Workbench, the other client you'll hear about. Oracle's own free client, MySQL
-- Workbench, is common in companies that run MySQL, and many online tutorials use it. It adds
-- visual tools for designing schemas and managing users. It connects the same way (host, port
-- 3306, user, password), and every query in this book runs in it unchanged. Use whichever your
-- team uses; this book's tips use DBeaver because it works with both databases.

-- > Words you'll see during MySQL setup. A schema in MySQL is the same thing as a database: CREATE
-- SCHEMA riverstone and CREATE DATABASE riverstone are identical. (In PostgreSQL a schema is a
-- folder inside a database, which is why the two tools use the word differently.) A collation is
-- the set of rules for comparing and sorting text, including whether 'delivered' equals
-- 'Delivered'. MySQL's default collation ignores capital letters; section 12.16 shows why that
-- matters.

-- =============================================================================================
-- Optional: the one-year database
-- =============================================================================================

-- Chapter 13 works on a full year of Riverstone's sales, the same 2025 data as your Chapter 10 and
-- 11 workbooks. You can load it now while the steps are fresh, or wait until Chapter 13:

-- - PostgreSQL: create a second database, CREATE DATABASE riverstone_2025;, make a connection to
-- it (as in step 4), and run riverstone_2025_setup.sql with Execute SQL Script. - MySQL: run
-- riverstone_2025_setup_mysql.sql; like the mini script, it creates its database for you.

-- On riverstone_2025, SELECT COUNT(*) FROM orders; returns 175. Exercise 30 uses it.

-- > Running your first query in DBeaver. > 1. Right-click the riverstone connection → SQL Editor →
-- New SQL script (or press Ctrl+]; Cmd+] on a Mac). An empty editor opens, connected to that
-- database. > 2. Type SELECT 1;. > 3. Put the cursor anywhere in the statement and press
-- Ctrl+Enter (Cmd+Enter on a Mac). This is Execute Statement: it runs the one statement under the
-- cursor. The result grid opens below the editor, with one column (PostgreSQL calls it ?column?,
-- MySQL 1) holding the value 1. The number of rows fetched is shown at the bottom of the grid. >
-- 4. Alt+X (Option+X on a Mac) is Execute SQL Script: it runs every statement in the editor, one
-- after another, each result in its own tab. Use it for setup scripts, not for everyday queries. >
-- 5. If a statement fails, DBeaver shows the database's error message where the grid would be.
-- Read it: it usually names the problem and the line. > 6. Keep several queries in one editor by
-- ending each with ; and leaving a blank line between them. Ctrl+Enter then runs only the one your
-- cursor is in.

-- > Can't install software on your computer? A Chromebook, or a locked work laptop, can stop you
-- here. On a work laptop, ask your IT team: PostgreSQL and DBeaver are commonly approved for
-- learning, and exercise 33 shows how to ask. Meanwhile, online SQL playgrounds let you paste a
-- setup script and practice in a browser; most offer both PostgreSQL and MySQL. Installation steps
-- and screens change over time; Appendix B keeps current, step-by-step instructions for both
-- databases.

-- > Try it. Before reading on, run SELECT  FROM products; (the  means "every column"; section 12.4
-- explains it). You should see six rows, one per product. If you installed both databases, run it
-- in both.

SELECT * FROM products;

/* The chapter shows:
    product_id |    product_name    |  category  | unit_price | unit_cost
   ------------+--------------------+------------+------------+-----------
           101 | Storage Box 10L    | Storage    |     450.00 |    300.00
           102 | Storage Box 25L    | Storage    |     780.00 |    540.00
           103 | Water Bottle 1L    | Kitchen    |     120.00 |     70.00
           104 | Food Container Set | Kitchen    |     650.00 |    430.00
           105 | Industrial Crate   | Industrial |    1450.00 |   1100.00
           106 | Garden Chair       | Furniture  |    1200.00 |    850.00
   (6 rows)
*/


-- If you see these six products, your laboratory is ready.

-- Good place to stop.

-- ---

-- =============================================================================================
-- 12.4 Your first query: SELECT and FROM
-- =============================================================================================

-- Every query that reads data starts with two clauses:

-- - FROM names the table to read. - SELECT names the columns you want back.

SELECT customer_name, city
FROM customers;

/* The chapter shows:
        customer_name      |   city
   ------------------------+-----------
    Sharma Hardware        | Mumbai
    Patel Kitchenware      | Ahmedabad
    Green Leaf Hotels      | Pune
    Coastal Foods          | Chennai
    Metro Mart             | Mumbai
    Sunrise Caterers       |
    Northgate Distributors | Delhi
    Blue Bay Cafe          | Pune
   (8 rows)
*/


-- Read it aloud: from the customers table, select the name and city.

-- > How results are printed in this book. Results are shown as text, the way PostgreSQL's command-
-- line client, psql, prints them. In DBeaver you'll see the same rows in a grid. Two small
-- differences: the row count ("8 rows") appears at the bottom of DBeaver's grid rather than under
-- the table, and a missing value shows as [NULL] where this book shows a blank (Sunrise Caterers'
-- city, above).

-- A few words you'll meet in every section from now on:

-- - A statement is one complete instruction to the database, ending with ;. The query above is one
-- statement. - A clause is one part of a statement that starts with a keyword, such as the SELECT
-- clause or the FROM clause. - An expression is anything that works out to a value: a column name,
-- a number such as 1.18, or a calculation such as unit_price * 1.18.

-- A few rules of the language, learned once:

-- - Keywords aren't case-sensitive. select, SELECT, and Select all work. The convention in this
-- book, and in most teams, is to write keywords in capitals so they stand out. - The semicolon ;
-- ends a statement. Some tools don't insist on it, but it's a good habit, especially when you run
-- several queries at once. - Line breaks and spaces don't matter to the database. They matter a
-- great deal to the humans who read your query later, including you. - Text values go in single
-- quotes: 'Mumbai'. Double quotes mean something different in most databases (a column or table
-- name), so a beginner who writes "Mumbai" gets a confusing "column does not exist" error. -
-- Comments start with -- and run to the end of the line. Use them to explain why a query does
-- something.

-- =============================================================================================
-- SELECT * — every column
-- =============================================================================================

-- SELECT  returns all columns. You've already run one: SELECT  FROM products; in section 12.3's
-- "Try it" returned all five columns of the six products.

-- It's handy for a quick look at an unfamiliar table. In real work, name your columns: the query
-- is clearer, it runs faster on wide tables, and it won't silently change when someone adds a
-- column to the table next year.

-- =============================================================================================
-- Calculated columns and aliases
-- =============================================================================================

-- SELECT can compute new values, not just return stored ones. Suppose Riverstone must quote prices
-- including an 18% tax. Start with the calculation on its own:

SELECT product_name,
       unit_price,
       unit_price * 1.18
FROM products;

/* The chapter shows:
       product_name    | unit_price | ?column?
   --------------------+------------+-----------
    Storage Box 10L    |     450.00 |  531.0000
    Storage Box 25L    |     780.00 |  920.4000
    Water Bottle 1L    |     120.00 |  141.6000
    Food Container Set |     650.00 |  767.0000
    Industrial Crate   |    1450.00 | 1711.0000
    Garden Chair       |    1200.00 | 1416.0000
   (6 rows)
*/


-- -  between two values means *multiply. (On its own after SELECT it means "every column"; the
-- position tells the database which you mean.) - unit_price  1.18 is worked out for every row:
-- ₹450 × 1.18 = ₹531. The result is a new column in your *result only. Nothing stored in the table
-- changes. - The heading ?column? is PostgreSQL's way of saying "this column has no name". (MySQL
-- uses the expression itself as the heading.) - The extra decimal places appear because unit_price
-- has two decimals and 1.18 has two more; multiplying keeps all four.

-- Give the new column a name with AS:

SELECT product_name,
       unit_price,
       unit_price * 1.18 AS price_incl_tax
FROM products;

/* The chapter shows:
       product_name    | unit_price | price_incl_tax
   --------------------+------------+----------------
    Storage Box 10L    |     450.00 |       531.0000
    Storage Box 25L    |     780.00 |       920.4000
    Water Bottle 1L    |     120.00 |       141.6000
    Food Container Set |     650.00 |       767.0000
    Industrial Crate   |    1450.00 |      1711.0000
    Garden Chair       |    1200.00 |      1416.0000
   (6 rows)
*/


-- AS price_incl_tax gives the calculated column a name, called an alias. The values are the same;
-- only the heading changed.

-- Finally, round the prices to two decimal places:

SELECT product_name,
       unit_price,
       ROUND(unit_price * 1.18, 2) AS price_incl_tax
FROM products;

/* The chapter shows:
       product_name    | unit_price | price_incl_tax
   --------------------+------------+----------------
    Storage Box 10L    |     450.00 |         531.00
    Storage Box 25L    |     780.00 |         920.40
    Water Bottle 1L    |     120.00 |         141.60
    Food Container Set |     650.00 |         767.00
    Industrial Crate   |    1450.00 |        1711.00
    Garden Chair       |    1200.00 |        1416.00
   (6 rows)
*/


-- ROUND is a function: a named operation, written as its name followed by its inputs in brackets.
-- Each input is called an argument, and arguments are separated by commas. ROUND takes two here:
-- the value to round (unit_price * 1.18) and the number of decimal places (2). It's the same idea
-- as =ROUND(A1,0) in your spreadsheet (Chapter 10). Section 12.8 shows how ROUND settles a value
-- that sits exactly halfway, such as 2.5.

-- You can use the usual arithmetic operators: +, -, *, /.

-- > Watch out: integer division. In PostgreSQL and SQL Server, dividing one whole number by
-- another throws away the remainder. When you need a decimal answer, make one side a decimal.

-- Compare the two:

SELECT 7 / 2   AS whole_numbers,
       7 / 2.0 AS with_a_decimal;

/* The chapter shows:
    whole_numbers |   with_a_decimal
   ---------------+--------------------
                3 | 3.5000000000000000
   (1 row)
*/


-- 7 / 2 gives 3, not 3.5. Writing 7 / 2.0 (or 7  1.0 / 2) makes one side a decimal, and the answer
-- keeps its fraction. A SELECT with no FROM simply calculates and shows one row. This quietly
-- breaks percentage calculations in a lot of beginners' reports. (MySQL does the opposite: /
-- always gives a decimal, 3.5000, and DIV gives the whole-number result. Writing 100.0  works
-- correctly in all of them.)

-- ---

-- =============================================================================================
-- 12.5 ORDER BY and LIMIT: sorting, top-N, and unique values
-- =============================================================================================

-- Rows in a table have no guaranteed order. If you don't sort, the database returns rows in
-- whatever order is fastest for it that day, and that order can change. Any time order matters,
-- say so with ORDER BY.

SELECT customer_name, segment, signup_date
FROM customers
ORDER BY segment ASC, signup_date DESC;

/* The chapter shows:
        customer_name      |   segment   | signup_date
   ------------------------+-------------+-------------
    Blue Bay Cafe          | Hospitality | 2026-03-01
    Sunrise Caterers       | Hospitality | 2026-02-03
    Green Leaf Hotels      | Hospitality | 2026-01-08
    Metro Mart             | Retail      | 2026-01-22
    Patel Kitchenware      | Retail      | 2025-12-15
    Sharma Hardware        | Retail      | 2025-11-04
    Northgate Distributors | Wholesale   | 2026-02-17
    Coastal Foods          | Wholesale   | 2025-10-20
   (8 rows)
*/


-- Sorting by several columns works like sorting a phone book: first by segment A→Z (ASC,
-- ascending, the default), then within each segment by newest signup first (DESC, descending).

-- LIMIT keeps only the first n rows. Combined with ORDER BY, it answers "top-N" questions:

SELECT product_name, unit_price
FROM products
ORDER BY unit_price DESC
LIMIT 3;

/* The chapter shows:
      product_name   | unit_price
   ------------------+------------
    Industrial Crate |    1450.00
    Garden Chair     |    1200.00
    Storage Box 25L  |     780.00
   (3 rows)
*/


-- > Dialect note. LIMIT 3 works in PostgreSQL, MySQL, SQLite, Snowflake, and BigQuery. SQL Server
-- uses SELECT TOP 3 ...; the SQL standard (and Oracle) uses FETCH FIRST 3 ROWS ONLY.

-- > Watch out: ties. If two products shared the third-highest price, LIMIT 3 would return one of
-- them arbitrarily. "Top 3 with ties" is a real business requirement and a favorite interview
-- follow-up; Chapter 13 solves it properly with RANK().

-- =============================================================================================
-- DISTINCT — unique values only
-- =============================================================================================

-- Which cities do our customers come from?

SELECT DISTINCT city
FROM customers
ORDER BY city;

/* The chapter shows:
      city
   -----------
    Ahmedabad
    Chennai
    Delhi
    Mumbai
    Pune
   
   (6 rows)
*/


-- DISTINCT removes duplicate rows from the result: Mumbai and Pune each appear once. That empty-
-- looking sixth row is Sunrise Caterers' missing city. Databases mark a missing value as NULL
-- (DBeaver shows it as [NULL]); section 12.7 is all about it.

-- > Dialect note: where NULLs sort. PostgreSQL and Oracle put NULLs last in ascending order, as
-- above; MySQL and SQL Server put them first. Once you've met NULL (section 12.7), you can control
-- this explicitly: ORDER BY city NULLS LAST in PostgreSQL and Oracle. MySQL and SQL Server don't
-- support NULLS LAST; section 12.16 shows the MySQL way.

-- ---

-- =============================================================================================
-- 12.6 WHERE: keeping only the rows you want
-- =============================================================================================

-- WHERE is a filter. The database checks the condition against each row and keeps only the rows
-- where it's true.

SELECT order_id, customer_id, order_date, status
FROM orders
WHERE status = 'Delivered';

/* The chapter shows:
    order_id | customer_id | order_date |  status
   ----------+-------------+------------+-----------
        5001 |           1 | 2026-01-05 | Delivered
        5002 |           4 | 2026-01-09 | Delivered
        5003 |           2 | 2026-01-14 | Delivered
        5005 |           1 | 2026-02-02 | Delivered
        5006 |           5 | 2026-02-06 | Delivered
        5007 |           4 | 2026-02-11 | Delivered
        5008 |           6 | 2026-02-19 | Delivered
        5010 |           3 | 2026-03-03 | Delivered
   (8 rows)
*/


-- =============================================================================================
-- Comparison operators
-- =============================================================================================

-- | Operator | Meaning | Example | |---|---|---| | = | equal to | status = 'Shipped' | | <> or !=
-- | not equal to | status <> 'Cancelled' | | > < | greater / less than | unit_price > 500 | | >=
-- <= | greater / less than or equal | order_date >= '2026-02-01' |

-- > Watch out: text comparisons may be case-sensitive. In PostgreSQL, 'delivered' does not equal
-- 'Delivered'. Other databases may ignore case depending on settings. When you're unsure how a
-- column was typed in, compare in a consistent case: WHERE LOWER(status) = 'delivered'. LOWER()
-- turns text into lower case, so 'Delivered' becomes 'delivered' before the comparison (section
-- 12.8 has the other text functions).

-- =============================================================================================
-- Combining conditions: AND, OR, NOT
-- =============================================================================================

-- - AND: both conditions must be true. - OR: at least one must be true. - NOT: reverses a
-- condition.

-- Here is the classic trap. The sales head asks: "Show me our Retail and Wholesale customers in
-- Mumbai." A beginner writes:

SELECT customer_name, city, segment
FROM customers
WHERE segment = 'Retail' OR segment = 'Wholesale' AND city = 'Mumbai';

/* The chapter shows:
      customer_name   |   city    | segment
   -------------------+-----------+---------
    Sharma Hardware   | Mumbai    | Retail
    Patel Kitchenware | Ahmedabad | Retail
    Metro Mart        | Mumbai    | Retail
   (3 rows)
*/


-- Patel Kitchenware is in Ahmedabad. Why is it here? Because AND is evaluated before OR, just as
-- multiplication comes before addition in arithmetic. The database read the condition as:

-- segment is Retail OR (segment is Wholesale AND city is Mumbai)

-- Every Retail customer passed, wherever they were. Parentheses fix it:

SELECT customer_name, city, segment
FROM customers
WHERE (segment = 'Retail' OR segment = 'Wholesale')
  AND city = 'Mumbai';

/* The chapter shows:
     customer_name  |  city  | segment
   -----------------+--------+---------
    Sharma Hardware | Mumbai | Retail
    Metro Mart      | Mumbai | Retail
   (2 rows)
*/


-- Rule for life: whenever you mix AND and OR, use parentheses, even when you think you don't need
-- them. Notice the wrong query didn't produce an error. It produced a plausible, wrong answer. In
-- analysis, those are the dangerous ones.

-- =============================================================================================
-- IN, BETWEEN, and LIKE
-- =============================================================================================

-- Three shortcuts make filters easier to read.

-- BETWEEN matches a range, and it includes both ends. Which orders were placed in February?

SELECT order_id, order_date
FROM orders
WHERE order_date BETWEEN '2026-02-01' AND '2026-02-28';

/* The chapter shows:
    order_id | order_date
   ----------+------------
        5005 | 2026-02-02
        5006 | 2026-02-06
        5007 | 2026-02-11
        5008 | 2026-02-19
        5009 | 2026-02-25
   (5 rows)
*/


-- '2026-02-01' is text in quotes, but because order_date is a DATE column, the database reads it
-- as a date: 1 February 2026.

-- IN matches any value in a list; it replaces a chain of ORs. Which orders are Delivered or
-- Shipped?

SELECT order_id, status
FROM orders
WHERE status IN ('Delivered', 'Shipped');

/* The chapter shows:
    order_id |  status
   ----------+-----------
        5001 | Delivered
        5002 | Delivered
        5003 | Delivered
        5005 | Delivered
        5006 | Delivered
        5007 | Delivered
        5008 | Delivered
        5009 | Shipped
        5010 | Delivered
        5011 | Shipped
   (10 rows)
*/


-- status IN ('Delivered', 'Shipped') means exactly the same as status = 'Delivered' OR status =
-- 'Shipped', only shorter. The cancelled and pending orders are left out.

-- Now combine the two with AND: February orders that are Delivered or Shipped.

SELECT order_id, order_date, status
FROM orders
WHERE order_date BETWEEN '2026-02-01' AND '2026-02-28'
  AND status IN ('Delivered', 'Shipped');

/* The chapter shows:
    order_id | order_date |  status
   ----------+------------+-----------
        5005 | 2026-02-02 | Delivered
        5006 | 2026-02-06 | Delivered
        5007 | 2026-02-11 | Delivered
        5008 | 2026-02-19 | Delivered
        5009 | 2026-02-25 | Shipped
   (5 rows)
*/


-- All five February orders were Delivered or Shipped, so the second filter removed nothing here.
-- That's worth noticing: a filter that removes nothing today may matter next month.

-- > Watch out: BETWEEN with timestamps. On a DATE column, BETWEEN '2026-02-01' AND '2026-02-28' is
-- fine. On a TIMESTAMP column, '2026-02-28' means midnight at the start of 28 February, so every
-- order placed later that day is silently dropped. The safe habit for any date range is a half-
-- open range: from the first day, up to but not including the first day of the next period. It
-- works for dates and timestamps, and for February in leap years:

SELECT order_id, order_date, status
FROM orders
WHERE order_date >= '2026-02-01'
  AND order_date <  '2026-03-01'
  AND status IN ('Delivered', 'Shipped');

/* The chapter shows:
    order_id | order_date |  status
   ----------+------------+-----------
        5005 | 2026-02-02 | Delivered
        5006 | 2026-02-06 | Delivered
        5007 | 2026-02-11 | Delivered
        5008 | 2026-02-19 | Delivered
        5009 | 2026-02-25 | Shipped
   (5 rows)
*/


-- The same five orders. Chapter 11 filtered a month with SUMIFS criteria ">=" the first day and
-- "<=" the last day; the half-open range does the same job without having to know how many days
-- the month has.

-- LIKE matches text patterns. % stands for "any number of characters (including none)" and _ for
-- "exactly one character".

SELECT product_name, unit_price
FROM products
WHERE product_name LIKE 'Storage%';

/* The chapter shows:
     product_name   | unit_price
   -----------------+------------
    Storage Box 10L |     450.00
    Storage Box 25L |     780.00
   (2 rows)
*/


-- | Pattern | Matches | |---|---| | 'Storage%' | starts with "Storage" | | '%Box%' | contains
-- "Box" anywhere | | '%L' | ends with "L" | | 'Storage Box __L' | "Storage Box ", then exactly two
-- characters, then "L" |

-- > Dialect note. In PostgreSQL, LIKE is case-sensitive; ILIKE ignores case. MySQL (with its
-- default collation) and SQL Server (with its usual settings) ignore case with plain LIKE, and
-- with = too. MySQL has no ILIKE.

-- ---

-- =============================================================================================
-- Real-life example: which products barely make money?
-- =============================================================================================

-- Riverstone's finance manager asks: "Which products earn less than 30% gross margin at list
-- price?" Gross margin is the share of the selling price left after paying for the product: (price
-- − cost) ÷ price.

-- Build it in two steps. First, calculate the margin for every product, with no filter, so you can
-- see all six:

SELECT product_name,
       unit_price,
       unit_cost,
       ROUND(100.0 * (unit_price - unit_cost) / unit_price, 1) AS margin_pct
FROM products
ORDER BY margin_pct;

/* The chapter shows:
       product_name    | unit_price | unit_cost | margin_pct
   --------------------+------------+-----------+------------
    Industrial Crate   |    1450.00 |   1100.00 |       24.1
    Garden Chair       |    1200.00 |    850.00 |       29.2
    Storage Box 25L    |     780.00 |    540.00 |       30.8
    Storage Box 10L    |     450.00 |    300.00 |       33.3
    Food Container Set |     650.00 |    430.00 |       33.8
    Water Bottle 1L    |     120.00 |     70.00 |       41.7
   (6 rows)
*/


-- - (unit_price - unit_cost) / unit_price is the margin as a fraction, such as 0.241. Brackets
-- work as in arithmetic: the subtraction happens first. - 100.0 * turns the fraction into a
-- percentage. Here both columns are NUMERIC, so plain 100 would work too; writing 100.0 is a habit
-- that protects you when the columns are whole numbers (the integer-division Watch out in section
-- 12.4). - ROUND(…, 1) keeps one decimal place, and AS margin_pct names the result. - ORDER BY
-- margin_pct puts the weakest product first. ORDER BY can use the alias; section 12.11 explains
-- why.

-- Now add the filter:

SELECT product_name,
       unit_price,
       unit_cost,
       ROUND(100.0 * (unit_price - unit_cost) / unit_price, 1) AS margin_pct
FROM products
WHERE (unit_price - unit_cost) / unit_price < 0.30
ORDER BY margin_pct;

/* The chapter shows:
      product_name   | unit_price | unit_cost | margin_pct
   ------------------+------------+-----------+------------
    Industrial Crate |    1450.00 |   1100.00 |       24.1
    Garden Chair     |    1200.00 |    850.00 |       29.2
   (2 rows)
*/


-- - WHERE (unit_price - unit_cost) / unit_price < 0.30 filters on a calculation, not a stored
-- column. WHERE can test any expression. - Notice the WHERE repeats the formula instead of writing
-- WHERE margin_pct < 30. That's not laziness: the alias margin_pct doesn't exist yet when WHERE
-- runs. Section 12.11 explains why. - The two rows are exactly the two below 30 in the first
-- result. Running the unfiltered version first let you check the filter by eye.

-- Check one row by hand: the crate sells for ₹1,450 and costs ₹1,100, leaving ₹350, and 350 ÷
-- 1,450 = 24.1%. ✓ Keep this result in mind. In section 12.10 you'll find that the Industrial
-- Crate is also Riverstone's biggest seller, which makes its thin margin a much bigger story.

-- =============================================================================================
-- 12.7 NULL: the value that isn't there
-- =============================================================================================

-- Sunrise Caterers has no city. The cell isn't an empty string or a zero; it holds NULL, SQL's
-- marker for "unknown or missing". NULL causes more wrong reports than any other single thing in
-- SQL, so it gets its own section.

-- =============================================================================================
-- NULL is not equal to anything, not even NULL
-- =============================================================================================

-- Try to find customers with no city the obvious way:

SELECT customer_name
FROM customers
WHERE city = NULL;

/* The chapter shows:
    customer_name
   ---------------
   (0 rows)
*/


-- Zero rows, and no error. Here's why. Asking "is the city equal to unknown?" can't be answered
-- true or false; the answer is itself unknown. SQL uses three-valued logic: a condition can be
-- TRUE, FALSE, or UNKNOWN, and WHERE keeps only rows where it's TRUE. Any comparison with NULL (=,
-- <>, >, and so on) gives UNKNOWN, so nothing passes.

-- To test for NULL, use the special operators IS NULL and IS NOT NULL:

SELECT customer_name
FROM customers
WHERE city IS NULL;

/* The chapter shows:
     customer_name
   ------------------
    Sunrise Caterers
   (1 row)
*/


-- =============================================================================================
-- The silent disappearance
-- =============================================================================================

-- This one fools experienced analysts. List every customer not in Mumbai:

SELECT customer_name, city
FROM customers
WHERE city <> 'Mumbai';

/* The chapter shows:
        customer_name      |   city
   ------------------------+-----------
    Patel Kitchenware      | Ahmedabad
    Green Leaf Hotels      | Pune
    Coastal Foods          | Chennai
    Northgate Distributors | Delhi
    Blue Bay Cafe          | Pune
   (5 rows)
*/


-- Eight customers, two in Mumbai, and only five came back. Sunrise Caterers vanished, because
-- "unknown is not Mumbai" is UNKNOWN, not TRUE. If NULLs should be included, say so explicitly:

SELECT customer_name, city
FROM customers
WHERE city <> 'Mumbai' OR city IS NULL;

/* The chapter shows:
        customer_name      |   city
   ------------------------+-----------
    Patel Kitchenware      | Ahmedabad
    Green Leaf Hotels      | Pune
    Coastal Foods          | Chennai
    Sunrise Caterers       |
    Northgate Distributors | Delhi
    Blue Bay Cafe          | Pune
   (6 rows)
*/


-- Sunrise Caterers is back: six customers, the eight minus the two in Mumbai. With only OR in the
-- condition, no brackets are needed. The moment you add an AND (say, AND segment = 'Retail'),
-- bracket the OR part, as section 12.6 showed.

-- > Real-life example: unknown is not zero. Imagine a blank "discount" box on an order form. It
-- could mean no discount was given, or nobody wrote the discount down. Those are different facts,
-- and a database keeps them apart: 0 means none; NULL means unknown. Riverstone's order 5008 has
-- no sales rep. That doesn't mean nobody sold it; it means the record is incomplete. A report that
-- silently drops it loses ₹23,325 of revenue (you'll meet that exact trap in exercise 6).

-- > Try it. Find the order with the missing sales rep: SELECT order_id FROM orders WHERE
-- sales_rep_id IS NULL; You should get order 5008. Now try = NULL instead and watch it return
-- nothing.

-- =============================================================================================
-- Replacing NULLs with COALESCE
-- =============================================================================================

-- COALESCE(a, b, c, ...) returns the first value in its list that isn't NULL. It's the standard
-- way to show a readable label instead of a blank:

SELECT customer_name,
       COALESCE(city, 'Unknown') AS city
FROM customers
ORDER BY customer_id;

/* The chapter shows:
        customer_name      |   city
   ------------------------+-----------
    Sharma Hardware        | Mumbai
    Patel Kitchenware      | Ahmedabad
    Green Leaf Hotels      | Pune
    Coastal Foods          | Chennai
    Metro Mart             | Mumbai
    Sunrise Caterers       | Unknown
    Northgate Distributors | Delhi
    Blue Bay Cafe          | Pune
   (8 rows)
*/


-- =============================================================================================
-- NULL in arithmetic
-- =============================================================================================

-- Any arithmetic involving NULL gives NULL: 5 + NULL is NULL. If one order line has a missing
-- discount and you compute quantity  unit_price  (1 - discount_pct / 100), that line's revenue
-- becomes NULL. Section 12.9 shows that SUM then skips it, so your total is quietly too low. Where
-- a missing number really means zero, write COALESCE(discount_pct, 0). Where it doesn't, the data
-- needs fixing, and Chapter 14 covers how.

-- > NULL rules to memorize > 1. Test with IS NULL / IS NOT NULL, never = NULL. > 2. WHERE col <>
-- 'x' silently drops rows where col is NULL. > 3. Arithmetic with NULL gives NULL. > 4. Aggregate
-- functions (except COUNT(*)) ignore NULLs (section 12.9). > 5. DISTINCT and GROUP BY treat all
-- NULLs as one group. > 6. Before trusting any filter on a column, ask: can this column be NULL?

-- Good place to stop.

-- ---

-- =============================================================================================
-- 12.8 Transforming values: CASE, dates, and text
-- =============================================================================================

-- =============================================================================================
-- CASE: if-then logic inside a query
-- =============================================================================================

-- CASE works like the spreadsheet IF function from Chapter 10, and like IFS from Chapter 11: it
-- can check many conditions in order. Riverstone's pricing team wants each product labeled by
-- price band:

SELECT product_name,
       unit_price,
       CASE
           WHEN unit_price >= 1000 THEN 'Premium'
           WHEN unit_price >= 500  THEN 'Mid-range'
           ELSE 'Budget'
       END AS price_band
FROM products
ORDER BY unit_price;

/* The chapter shows:
       product_name    | unit_price | price_band
   --------------------+------------+------------
    Water Bottle 1L    |     120.00 | Budget
    Storage Box 10L    |     450.00 | Budget
    Food Container Set |     650.00 | Mid-range
    Storage Box 25L    |     780.00 | Mid-range
    Garden Chair       |    1200.00 | Premium
    Industrial Crate   |    1450.00 | Premium
   (6 rows)
*/


-- CASE checks each WHEN from top to bottom and stops at the first match. The Industrial Crate is
-- also ≥ 500, but it matched >= 1000 first. That's why the order of conditions matters: put the
-- most specific ones first. If nothing matches and there's no ELSE, the result is NULL.

-- CASE is one of the most useful tools you'll learn. You'll use it to group messy categories,
-- build flags (CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END), and, combined with aggregates in
-- the next section, to pivot data into columns.

-- =============================================================================================
-- Working with dates
-- =============================================================================================

-- Business questions are full of time: this month, last quarter, same period last year. Two
-- PostgreSQL functions do most of the work:

-- - EXTRACT(part FROM date) pulls out one part: YEAR, QUARTER, MONTH, DAY, DOW (day of week). -
-- DATE_TRUNC('month', date) rounds a date down to the start of its month (or 'week', 'quarter',
-- 'year'). This is the standard way to group by month.

SELECT order_id,
       order_date,
       EXTRACT(MONTH FROM order_date)        AS month_no,
       DATE_TRUNC('month', order_date)::date AS order_month
FROM orders
WHERE order_id <= 5004;

/* The chapter shows:
    order_id | order_date | month_no | order_month
   ----------+------------+----------+-------------
        5001 | 2026-01-05 |        1 | 2026-01-01
        5002 | 2026-01-09 |        1 | 2026-01-01
        5003 | 2026-01-14 |        1 | 2026-01-01
        5004 | 2026-01-20 |        1 | 2026-01-01
   (4 rows)
*/


-- Why prefer DATE_TRUNC over EXTRACT(MONTH ...) for grouping? Because month number 1 means January
-- of every year. Once your data covers more than twelve months, grouping by month number merges
-- January 2026 with January 2027. DATE_TRUNC keeps the year.

-- The ::date is PostgreSQL shorthand for casting (converting) a value to another type; the
-- standard form is CAST(value AS DATE). DATE_TRUNC returns a date and time (midnight), so ::date
-- keeps only the date part.

-- You can also write a fixed date straight into a query, and subtract one date from another:

SELECT DATE '2026-03-31' - DATE '2026-02-05' AS days;

/* The chapter shows:
    days
   ------
      54
   (1 row)
*/


-- - DATE '2026-03-31' is a date literal: the word DATE followed by the date in quotes, written
-- year-month-day. It tells the database "this text is a date", even where there's no date column
-- to compare it with. - Subtracting two dates gives the number of days between them: 54 days from
-- 5 February to 31 March.

-- > Dialect note. Date functions are where databases differ most. MySQL uses
-- DATE_FORMAT(order_date, '%Y-%m-01') or YEAR()/MONTH() instead of DATE_TRUNC, and DATEDIFF(later,
-- earlier) to count days. Never subtract dates with - in MySQL: it doesn't raise an error, it
-- returns a meaningless number (section 12.16 shows the trap); SQL Server uses DATETRUNC(month,
-- order_date) in recent versions and DATEFROMPARTS(YEAR(d), MONTH(d), 1) in older ones; BigQuery
-- uses DATE_TRUNC(order_date, MONTH). The idea transfers; check your database's documentation for
-- the spelling.

-- =============================================================================================
-- Casting, and two number traps
-- =============================================================================================

-- Casting lets you see, in SQL, two number traps that trip up reports. The first is the one from
-- section 12.1's "money and decimals" Watch out. double precision is PostgreSQL's floating-point
-- type:

SELECT 0.1 + 0.2                                   AS exact_numeric,
       0.1::double precision + 0.2::double precision AS floating;

/* The chapter shows:
    exact_numeric |      floating
   ---------------+---------------------
              0.3 | 0.30000000000000004
   (1 row)
*/


-- 0.1 typed on its own is NUMERIC, an exact decimal, so the sum is exactly 0.3. Cast to double
-- precision, each number is stored as a close binary approximation (Chapter 2, section 2.1), and
-- the tiny errors show up in the sum. That's why money never goes in a floating-point column.

-- > Watch out: how ROUND breaks ties. What does rounding 2.5 to a whole number give? It depends on
-- the number's type:

SELECT ROUND(2.5)                   AS exact_half,
       ROUND(3.5)                   AS exact_three_half,
       ROUND(2.5::double precision) AS float_half,
       ROUND(3.5::double precision) AS float_three_half;

/* The chapter shows:
    exact_half | exact_three_half | float_half | float_three_half
   ------------+------------------+------------+------------------
             3 |                4 |          2 |                4
   (1 row)
*/


-- MySQL gives the same four answers. There, 2.5E0 (scientific notation: 2.5 × 10⁰) is how you
-- write a floating-point number:

SELECT ROUND(2.5)   AS exact_half,
       ROUND(3.5)   AS exact_three_half,
       ROUND(2.5E0) AS float_half,
       ROUND(3.5E0) AS float_three_half;

/* The chapter shows:
   +------------+------------------+------------+------------------+
   | exact_half | exact_three_half | float_half | float_three_half |
   +------------+------------------+------------+------------------+
   |          3 |                4 |          2 |                4 |
   +------------+------------------+------------+------------------+
*/


-- So 2.5 rounds to 3 as an exact decimal and to 2 as a floating-point number. Neither database is
-- broken; each manual says exactly what to expect:

-- - The PostgreSQL manual (round): "For numeric, ties are broken by rounding away from zero. For
-- double precision, the tie-breaking behavior is platform dependent, but 'round to nearest even'
-- is the most common rule." - The MySQL manual (Rounding Behavior): exact-value numbers use the
-- "round half up" rule, which moves a .5 away from zero; "For approximate-value numbers, the
-- result depends on the C library. On many systems, this means that ROUND() uses the 'round to
-- nearest even' rule."

-- Rounding a half to the nearest even number is called banker's rounding. Your spreadsheet's ROUND
-- (Chapter 10) rounds halves away from zero, like NUMERIC. Riverstone's money columns are NUMERIC
-- (DECIMAL in MySQL), so ties round away from zero: that's why ₹124.425 becomes ₹124.43 in section
-- 12.13, and another reason money never goes in a floating-point column. Chapter 17 shows how
-- Python rounds the same values.

-- =============================================================================================
-- Real-life example: which invoices are overdue?
-- =============================================================================================

-- Every business that sells on credit asks this weekly. Finance wants each invoice labelled by how
-- late it is as of 31 March 2026:

SELECT invoice_id,
       due_date,
       CASE
           WHEN due_date >= DATE '2026-03-31'             THEN 'Not yet due'
           WHEN DATE '2026-03-31' - due_date <= 30         THEN 'Overdue 1-30 days'
           WHEN DATE '2026-03-31' - due_date <= 60         THEN 'Overdue 31-60 days'
           ELSE 'Overdue 60+ days'
       END AS due_status
FROM invoices
ORDER BY due_date;

/* The chapter shows:
    invoice_id |  due_date  |     due_status
   ------------+------------+--------------------
          9001 | 2026-02-05 | Overdue 31-60 days
          9002 | 2026-02-09 | Overdue 31-60 days
          9003 | 2026-02-14 | Overdue 31-60 days
          9004 | 2026-03-05 | Overdue 1-30 days
          9005 | 2026-03-09 | Overdue 1-30 days
          9006 | 2026-03-14 | Overdue 1-30 days
          9007 | 2026-03-22 | Overdue 1-30 days
          9008 | 2026-03-28 | Overdue 1-30 days
          9009 | 2026-04-03 | Not yet due
          9010 | 2026-04-10 | Not yet due
   (10 rows)
*/


-- How it works:

-- - DATE '2026-03-31' is the date literal from "Working with dates", and DATE '2026-03-31' -
-- due_date counts the days from each due date to 31 March. In a live report you'd use CURRENT_DATE
-- (today) instead; a fixed date is used here so your results match the book. - The WHEN conditions
-- are checked top to bottom. An invoice 45 days late fails the first two tests and matches the
-- third. Because the first match wins, each condition only has to handle what the earlier ones
-- didn't. - Grouping amounts into bands like 1–30, 31–60, and 60+ days is called ageing, and an
-- ageing report is one of the most common reports in finance.

-- Now look closely at invoice 9001: Overdue 31-60 days. But Sharma Hardware paid it in full on 2
-- February. This query is wrong for the business, even though the SQL is perfect. It knows due
-- dates but not payments. A real overdue report must also look at the payments table, and building
-- it properly is the main event of section 12.15. It's a lesson worth learning early: a
-- technically correct query can still give the wrong business answer if it ignores data that
-- changes the answer.

-- =============================================================================================
-- Working with text
-- =============================================================================================

-- A handful of text functions cover most cleaning and display work:

-- | Function | Does | Example → Result | |---|---|---| | UPPER(s) / LOWER(s) | change case |
-- UPPER('pune') → PUNE | | TRIM(s) | remove spaces at both ends | TRIM('  Pune ') → Pune | |
-- LENGTH(s) | count characters | LENGTH('Pune') → 4 | | SUBSTRING(s FROM 1 FOR 3) | take part of a
-- string | SUBSTRING('Pune' FROM 1 FOR 3) → Pun | | REPLACE(s, 'a', 'b') | swap text |
-- REPLACE('Box 10L', 'L', ' litre') → Box 10 litre | | s1 \|\| s2 or CONCAT(s1, s2) | join text
-- together | 'Riverstone' \|\| ' Supplies' → Riverstone Supplies (in MySQL use CONCAT; there \|\|
-- means OR) |

-- Here are four of them on real rows:

SELECT customer_name,
       UPPER(city)                              AS city_upper,
       LENGTH(customer_name)                    AS name_length,
       SUBSTRING(customer_name FROM 1 FOR 3)    AS short_code,
       customer_name || ' (' || segment || ')'  AS label
FROM customers
ORDER BY customer_id
LIMIT 3;

/* The chapter shows:
      customer_name   | city_upper | name_length | short_code |              label
   -------------------+------------+-------------+------------+---------------------------------
    Sharma Hardware   | MUMBAI     |          15 | Sha        | Sharma Hardware (Retail)
    Patel Kitchenware | AHMEDABAD  |          17 | Pat        | Patel Kitchenware (Retail)
    Green Leaf Hotels | PUNE       |          17 | Gre        | Green Leaf Hotels (Hospitality)
   (3 rows)
*/


-- - LENGTH counts the space too: "Sharma Hardware" is 15 characters. - SUBSTRING(customer_name
-- FROM 1 FOR 3) starts at character 1 and takes 3. - || joins five pieces: the name, the text '
-- (', the segment, and ')'.

-- Now the same functions on Sunrise Caterers, whose city is missing:

SELECT customer_name,
       UPPER(city)                              AS city_upper,
       customer_name || ' (' || city || ')'     AS with_pipes,
       CONCAT(customer_name, ' (', city, ')')   AS with_concat
FROM customers
WHERE customer_id = 6;

/* The chapter shows:
     customer_name   | city_upper | with_pipes |     with_concat
   ------------------+------------+------------+---------------------
    Sunrise Caterers |            |            | Sunrise Caterers ()
   (1 row)
*/


-- UPPER of a missing city is still missing, and || with a NULL gives NULL for the whole label,
-- just like arithmetic with NULL (section 12.7). CONCAT skips NULLs in PostgreSQL, so it keeps the
-- name. (MySQL's CONCAT returns NULL instead; see exercise 21.)

-- You'll use these heavily in Chapter 14, where real-world text is full of extra spaces,
-- inconsistent capitals, and typos.

-- ---

-- =============================================================================================
-- 12.9 Summarizing: aggregate functions, GROUP BY, and HAVING
-- =============================================================================================

-- So far every query has returned individual rows. But business questions are almost always about
-- totals, counts, and averages: How many orders? What's our revenue by city? Which customers buy
-- most? Answering them means collapsing many rows into a few summary rows.

-- =============================================================================================
-- Aggregate functions
-- =============================================================================================

-- An aggregate function takes many values and returns one:

-- | Function | Returns | |---|---| | COUNT(*) | number of rows | | COUNT(column) | number of rows
-- where that column is not NULL | | COUNT(DISTINCT column) | number of different non-NULL values |
-- | SUM(column) | total | | AVG(column) | average (mean) of non-NULL values | | MIN(column) /
-- MAX(column) | smallest / largest; also works on dates and text |

-- Four of them on the invoices table:

SELECT SUM(amount)       AS invoiced,
       AVG(amount)       AS avg_invoice,
       MIN(invoice_date) AS first_invoice,
       MAX(invoice_date) AS last_invoice
FROM invoices;

/* The chapter shows:
    invoiced  |    avg_invoice     | first_invoice | last_invoice
   -----------+--------------------+---------------+--------------
    297710.00 | 29771.000000000000 | 2026-01-06    | 2026-03-11
   (1 row)
*/


-- The ten invoices come to ₹2,97,710, an average of ₹29,771 each; the first was raised on 6
-- January and the last on 11 March. Each function collapsed ten rows into one value. The long run
-- of zeros after the average is PostgreSQL keeping extra decimal places after a division; wrap it
-- in ROUND(AVG(amount), 2) for a report.

-- The three flavors of COUNT answer different questions, and mixing them up is a classic error:

SELECT COUNT(*)                    AS total_orders,
       COUNT(sales_rep_id)         AS orders_with_rep,
       COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;

/* The chapter shows:
    total_orders | orders_with_rep | unique_customers
   --------------+-----------------+------------------
              12 |              11 |                7
   (1 row)
*/


-- - 12 orders in total. - 11 have a sales rep; order 5008's NULL rep was skipped. - They came from
-- 7 different customers; Sharma Hardware's three orders count once, and Blue Bay Cafe has none.

-- > Back to Chapter 11. Exercise 10 there counted 326 order lines but 173 distinct orders in the
-- 2025 data. That's this same trap: COUNT(*) counts rows, COUNT(DISTINCT order_id) counts orders.

-- COUNT(column) skipping NULLs is easy to see on the customers table, where one city is missing:

SELECT COUNT(*)    AS customers,
       COUNT(city) AS with_city
FROM customers;

/* The chapter shows:
    customers | with_city
   -----------+-----------
            8 |         7
   (1 row)
*/


-- Eight customers, but only seven cities to count: Sunrise Caterers' NULL was skipped.

-- > Watch out: AVG ignores NULLs too. If three products had ratings 4, 5, and NULL, AVG(rating)
-- would be 4.5, the average of the two known ratings, not 3 (as if the missing one were zero).
-- Usually that's what you want. Sometimes it isn't. Decide deliberately.

-- Now the most important calculation in this chapter: revenue. Each order line's net revenue is
-- quantity × price charged × (1 − discount). Before adding anything up, look at the formula on a
-- few lines:

SELECT order_id,
       quantity,
       unit_price,
       discount_pct,
       quantity * unit_price * (1 - discount_pct / 100) AS line_revenue
FROM order_items
WHERE order_id IN (5001, 5002);

/* The chapter shows:
    order_id | quantity | unit_price | discount_pct |         line_revenue
   ----------+----------+------------+--------------+------------------------------
        5001 |       20 |     450.00 |         0.00 |  9000.0000000000000000000000
        5001 |       50 |     120.00 |         5.00 |  5700.0000000000000000000000
        5002 |       40 |    1450.00 |        10.00 | 52200.0000000000000000000000
        5002 |       30 |     780.00 |        10.00 | 21060.0000000000000000000000
   (4 rows)
*/


-- - discount_pct / 100 turns a percentage into a fraction: 5.00 becomes 0.05. - 1 - discount_pct /
-- 100 is the share the customer actually pays: 0.95 for a 5% discount. - quantity  unit_price  …
-- multiplies it out: 50 × ₹120 × 0.95 = ₹5,700. - discount_pct is NUMERIC, so / 100 keeps its
-- decimals. If it were a whole-number INTEGER column, 5 / 100 would be 0 (integer division,
-- section 12.4), and every discount would silently vanish. - The long tail of zeros is again
-- PostgreSQL keeping decimal places; ROUND tidies it in a moment.

-- Put the formula inside SUM, and one query adds up every line in the table:

SELECT ROUND(SUM(quantity * unit_price * (1 - discount_pct / 100)), 0) AS net_revenue_all_lines
FROM order_items;

/* The chapter shows:
    net_revenue_all_lines
   -----------------------
                   335930
   (1 row)
*/


-- An aggregate can work on any expression, not only a column. But this total includes the
-- cancelled order 5004 (₹12,000), which shouldn't count as revenue. The status lives in the orders
-- table, not in order_items, so leaving it out needs both tables at once, which is what joins are
-- for (next section).

-- =============================================================================================
-- GROUP BY: one summary row per group
-- =============================================================================================

-- Aggregates over a whole table give one row. GROUP BY gives one row per group:

SELECT status,
       COUNT(*) AS num_orders
FROM orders
GROUP BY status
ORDER BY num_orders DESC, status;

/* The chapter shows:
     status   | num_orders
   -----------+------------
    Delivered |          8
    Shipped   |          2
    Cancelled |          1
    Pending   |          1
   (4 rows)
*/


-- Picture what the database does: it sorts the twelve orders into piles by status, then counts
-- each pile.

-- > Back to Chapter 11: the pivot table. A pivot table and a GROUP BY query are the same idea. The
-- pivot's Filters area is WHERE, its Rows area is GROUP BY, and its Values area is the aggregate
-- (SUM, COUNT). Its Columns area is one SUM(CASE …) column per value, which you'll meet later in
-- this section. Exercise 32 rebuilds Chapter 11's first pivot in SQL.

-- The same works for money. Summing lines per order:

SELECT order_id,
       SUM(quantity * unit_price * (1 - discount_pct / 100)) AS order_revenue
FROM order_items
GROUP BY order_id
ORDER BY order_id
LIMIT 5;

/* The chapter shows:
    order_id |        order_revenue
   ----------+------------------------------
        5001 | 14700.0000000000000000000000
        5002 | 73260.0000000000000000000000
        5003 | 16250.0000000000000000000000
        5004 | 12000.0000000000000000000000
        5005 | 14550.0000000000000000000000
   (5 rows)
*/


-- Order 5001's two lines, ₹9,000 and ₹5,700, became one row of ₹14,700. Now round the total to two
-- decimal places, wrapping SUM in ROUND:

SELECT order_id,
       ROUND(SUM(quantity * unit_price * (1 - discount_pct / 100)), 2) AS order_revenue
FROM order_items
GROUP BY order_id
ORDER BY order_id
LIMIT 5;

/* The chapter shows:
    order_id | order_revenue
   ----------+---------------
        5001 |      14700.00
        5002 |      73260.00
        5003 |      16250.00
        5004 |      12000.00
        5005 |      14550.00
   (5 rows)
*/


-- Check order 5001 by hand: 20 × ₹450 × 1.00 = ₹9,000, plus 50 × ₹120 × 0.95 = ₹5,700, total
-- ₹14,700. ✓ Always hand-check at least one row of any new calculation. It takes a minute and
-- catches most logic errors.

-- =============================================================================================
-- The GROUP BY rule
-- =============================================================================================

-- Once a query has GROUP BY, every column in SELECT must either be in the GROUP BY or be inside an
-- aggregate function. This fails:

SELECT customer_id, order_date, COUNT(*)
FROM orders
GROUP BY customer_id;

/* The chapter shows:
   ERROR:  column "orders.order_date" must appear in the GROUP BY clause
           or be used in an aggregate function
*/


-- And it should fail. Sharma Hardware has three orders on three dates, so which single order_date
-- should appear on its one summary row? The database refuses to guess. Decide what you mean: the
-- first order (MIN(order_date)), the latest (MAX(order_date)), or one row per customer and date
-- (add order_date to GROUP BY).

-- > Dialect note. Modern MySQL rejects this query too, with error 1055 ("…not in GROUP BY clause…
-- incompatible with sql_mode=only_full_group_by"). But very old MySQL versions, and servers where
-- an administrator has switched the ONLY_FULL_GROUP_BY setting off, accept it and silently pick an
-- arbitrary date. That's worse than an error, because the result looks fine. If you ever inherit a
-- MySQL report that "works" with a query like this, treat its numbers with suspicion. Write
-- standard SQL even when your database lets you get away with less.

-- =============================================================================================
-- Conditional aggregation: CASE inside SUM
-- =============================================================================================

-- Put CASE inside an aggregate and you can count or sum only certain rows, side by side in one
-- result. It's how you build pivot-style reports in SQL, and it's the SQL form of Chapter 11's
-- SUMIFS and COUNTIFS: each CASE is the criterion. How many customers in each segment, and how
-- many of those in Mumbai?

SELECT segment,
       COUNT(*)                                        AS customers,
       SUM(CASE WHEN city = 'Mumbai' THEN 1 ELSE 0 END) AS in_mumbai
FROM customers
GROUP BY segment
ORDER BY segment;

/* The chapter shows:
      segment   | customers | in_mumbai
   -------------+-----------+-----------
    Hospitality |         3 |         0
    Retail      |         3 |         2
    Wholesale   |         2 |         0
   (3 rows)
*/


-- - COUNT(*) counts every customer in the segment. - CASE WHEN city = 'Mumbai' THEN 1 ELSE 0 END
-- turns each customer into a 1 (in Mumbai) or a 0 (anywhere else, including a NULL city). - SUM(…)
-- adds those 1s and 0s, so it counts only the Mumbai customers: the two Retail ones, Sharma
-- Hardware and Metro Mart.

-- =============================================================================================
-- HAVING: filtering groups
-- =============================================================================================

-- Which customers have placed more than one order? You can't use WHERE:

SELECT customer_id, COUNT(*) AS num_orders
FROM orders
WHERE num_orders > 1
GROUP BY customer_id;

/* The chapter shows:
   ERROR:  column "num_orders" does not exist
*/


-- WHERE filters individual rows before they're grouped, and at that moment no counts exist yet. To
-- filter the groups after aggregation, use HAVING:

SELECT customer_id, COUNT(*) AS num_orders
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY customer_id;

/* The chapter shows:
    customer_id | num_orders
   -------------+------------
              1 |          3
              3 |          2
              4 |          2
              5 |          2
   (4 rows)
*/


-- | | WHERE | HAVING | |---|---|---| | Filters | rows | groups | | Runs | before GROUP BY | after
-- GROUP BY | | Can use aggregates like COUNT(*)? | No | Yes | | Example | WHERE status <>
-- 'Cancelled' | HAVING SUM(revenue) > 50000 |

-- You can, and often will, use both in one query: WHERE to exclude cancelled orders, then HAVING
-- to keep only customers above a revenue threshold. Filtering with WHERE whenever possible is also
-- faster, because the database groups fewer rows.

-- Good place to stop.

-- ---

-- =============================================================================================
-- 12.10 JOIN: combining tables
-- =============================================================================================

-- This is the concept that separates people who can use a database from people who merely poke at
-- one.

-- Remember why Riverstone's data is split across tables: to store each fact once. But the sales
-- head doesn't want to see "customer 4". She wants "Coastal Foods". A join stitches tables back
-- together by matching a key in one table to a key in another.

-- =============================================================================================
-- INNER JOIN
-- =============================================================================================

SELECT o.order_id,
       c.customer_name,
       o.order_date
FROM orders AS o
INNER JOIN customers AS c
        ON o.customer_id = c.customer_id
ORDER BY o.order_id
LIMIT 4;

/* The chapter shows:
    order_id |   customer_name   | order_date
   ----------+-------------------+------------
        5001 | Sharma Hardware   | 2026-01-05
        5002 | Coastal Foods     | 2026-01-09
        5003 | Patel Kitchenware | 2026-01-14
        5004 | Green Leaf Hotels | 2026-01-20
   (4 rows)
*/


-- Read it aloud: take each order, find the customer whose customer_id matches the order's
-- customer_id, and put them side by side.

-- - AS o and AS c are table aliases, short nicknames so you don't retype full table names. -
-- o.order_id means "the order_id column from the table nicknamed o". When two tables share a
-- column name (both have customer_id), the prefix is required. Use prefixes on every column in a
-- join anyway; readers shouldn't have to guess where a column comes from. - ON states the matching
-- condition. - The word INNER is optional; plain JOIN means INNER JOIN.

-- An inner join keeps only rows that have a match on both sides. Blue Bay Cafe has no orders, so
-- it could never appear in this result.

-- > Spreadsheet link. In Chapter 10 you used XLOOKUP to fetch a customer's name from another
-- sheet, one cell at a time. A join is the same idea done for every row at once, with far stricter
-- rules.

-- =============================================================================================
-- LEFT JOIN: keep everything on the left
-- =============================================================================================

-- Suppose the question is "list every customer and their orders, including customers who haven't
-- ordered."

SELECT c.customer_name,
       o.order_id
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_id;

/* The chapter shows:
        customer_name      | order_id
   ------------------------+----------
    Sharma Hardware        |     5001
    Sharma Hardware        |     5005
    Sharma Hardware        |     5011
    Patel Kitchenware      |     5003
    Green Leaf Hotels      |     5004
    Green Leaf Hotels      |     5010
    Coastal Foods          |     5002
    Coastal Foods          |     5007
    Metro Mart             |     5006
    Metro Mart             |     5012
    Sunrise Caterers       |     5008
    Northgate Distributors |     5009
    Blue Bay Cafe          |
   (13 rows)
*/


-- A left join keeps every row from the left table (the one after FROM), whether or not it has a
-- match. Where there's no match, the right table's columns are filled with NULL. Blue Bay Cafe
-- appears with an empty order_id. (In Chapter 10's terms, it's an XLOOKUP for every row whose "not
-- found" result is NULL.)

-- Notice two more things:

-- 1. Rows multiplied. Sharma Hardware appears three times, once per order. A join produces one
-- output row per matching pair. Eight customers became thirteen rows. Keep this in mind; it causes
-- the biggest trap in this section. 2. The choice between INNER and LEFT is a business decision,
-- not a technical one. "Revenue by customer" can use an inner join. "Customer list with order
-- counts" must use a left join, or your newest customers (the ones sales most wants to chase)
-- silently vanish from the report.

-- Figure 12.3 shows both joins side by side on three customers.

-- Figure 12.3 — The same match, two results. An inner join keeps only matched rows; a left join
-- also keeps unmatched left rows and fills the gaps with NULL.

-- > Real-life example: the attendance register. HR has an employees list and a leave_requests
-- table. "Show leave taken by each employee" with an inner join lists only people who took leave.
-- Anyone with zero days vanishes, and the report can't answer "who hasn't taken a day off all
-- year?", which is often the question HR actually cares about. Whenever the business question
-- contains every, all, or including those with none, reach for a left join.

-- =============================================================================================
-- The anti-join: finding what's missing
-- =============================================================================================

-- A left join plus an IS NULL filter finds rows that have no match. That answers some of the most
-- valuable questions in business: customers who never ordered, products that never sold, invoices
-- never paid.

-- Customers who have never placed an order
SELECT c.customer_name
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

/* The chapter shows:
    customer_name
   ---------------
    Blue Bay Cafe
   (1 row)
*/


-- Products that have never been sold
SELECT p.product_name
FROM products AS p
LEFT JOIN order_items AS oi
       ON p.product_id = oi.product_id
WHERE oi.order_item_id IS NULL;

/* The chapter shows:
    product_name
   --------------
    Garden Chair
   (1 row)
*/


-- This pattern is called an anti-join. It's the SQL version of Chapter 11's Power Query Left Anti
-- merge, which found Home Plus, the one customer with no 2025 sales. Test the IS NULL on a column
-- that can never be NULL in a real match, such as the right table's primary key, so you're only
-- catching the rows that found no partner.

-- =============================================================================================
-- RIGHT JOIN, FULL OUTER JOIN, and CROSS JOIN
-- =============================================================================================

-- - RIGHT JOIN is a left join viewed from the other side: it keeps every row of the right table. A
-- RIGHT JOIN B gives the same rows as B LEFT JOIN A. Most analysts simply write left joins and
-- list the "keep everything" table first; it reads more naturally. - FULL OUTER JOIN keeps every
-- row from both tables, with NULLs wherever either side lacks a match. It's the tool for
-- reconciliation: comparing the sales system's list of invoices with the finance system's, and
-- showing what's missing on either side. (MySQL doesn't support it directly; section 12.16 shows
-- how.) - CROSS JOIN has no matching condition. It pairs every row with every row, as the next two
-- queries show.

-- With 8 customers and 6 products, a cross join gives 8 × 6 = 48 pairs:

SELECT c.customer_name, p.product_name
FROM customers AS c
CROSS JOIN products AS p
ORDER BY c.customer_id, p.product_id
LIMIT 6;

/* The chapter shows:
     customer_name  |    product_name
   -----------------+--------------------
    Sharma Hardware | Storage Box 10L
    Sharma Hardware | Storage Box 25L
    Sharma Hardware | Water Bottle 1L
    Sharma Hardware | Food Container Set
    Sharma Hardware | Industrial Crate
    Sharma Hardware | Garden Chair
   (6 rows)
*/


-- LIMIT 6 shows only Sharma Hardware's six pairs. Count them all:

SELECT COUNT(*) AS pairs
FROM customers AS c
CROSS JOIN products AS p;

/* The chapter shows:
    pairs
   -------
       48
   (1 row)
*/


-- That's useful for building a complete grid (every customer × every product, including pairs with
-- zero sales) that you then left-join real sales onto. To get each segment × category pair once,
-- you first need the distinct lists, a job for subqueries (section 12.12 builds it). A cross join
-- is dangerous by accident: a cross join of two 100,000-row tables produces ten billion rows.

-- =============================================================================================
-- The self-join: a table joined to itself
-- =============================================================================================

-- Riverstone's employees table records each person's manager as another employee_id in the same
-- table. To show each employee next to their manager's name, join the table to itself using two
-- different aliases:

SELECT e.employee_name,
       e.job_title,
       m.employee_name AS manager_name
FROM employees AS e
LEFT JOIN employees AS m
       ON e.manager_id = m.employee_id
ORDER BY e.employee_id;

/* The chapter shows:
    employee_name |    job_title    | manager_name
   ---------------+-----------------+--------------
    Anita Rao     | Sales Head      |
    Vikram Singh  | Sales Manager   | Anita Rao
    Neha Kulkarni | Sales Executive | Vikram Singh
    Rahul Mehta   | Sales Executive | Vikram Singh
    Farah Khan    | Sales Executive | Anita Rao
   (5 rows)
*/


-- Think of e and m as two photocopies of the same list: one read as "employees", the other as
-- "managers". It's a left join so that Anita Rao, who has no manager, still appears. Self-joins
-- turn up in org charts, "customers referred by other customers", and comparing a row to the
-- previous one. (Chapter 13 shows a neater tool for that last case.)

-- =============================================================================================
-- Joining three or more tables
-- =============================================================================================

-- Real questions usually cross several tables. Revenue by city, excluding cancelled orders needs
-- customers (city), orders (status), and order_items (money). Each JOIN adds one table and one
-- matching condition. Build multi-table queries one join at a time, running the query after each
-- step and checking that the row count makes sense before adding the next. Here are the four
-- steps, counting rows only.

-- Start with one table:

SELECT COUNT(*) AS row_count
FROM orders AS o;

/* The chapter shows:
    row_count
   -----------
           12
   (1 row)
*/


-- Add the customers:

SELECT COUNT(*) AS row_count
FROM orders AS o
JOIN customers AS c ON o.customer_id = c.customer_id;

/* The chapter shows:
    row_count
   -----------
           12
   (1 row)
*/


-- Still 12. Each order has exactly one customer, so joining customers adds columns but no rows.
-- Good. Now add the order lines:

SELECT COUNT(*) AS row_count
FROM orders AS o
JOIN customers   AS c  ON o.customer_id = c.customer_id
JOIN order_items AS oi ON o.order_id    = oi.order_id;

/* The chapter shows:
    row_count
   -----------
           19
   (1 row)
*/


-- Nineteen: one row per order line now, not per order. The grain changed, which is expected here
-- (the money lives on the lines), but it's the moment to be careful with counts. Finally, drop the
-- cancelled order:

SELECT COUNT(*) AS row_count
FROM orders AS o
JOIN customers   AS c  ON o.customer_id = c.customer_id
JOIN order_items AS oi ON o.order_id    = oi.order_id
WHERE o.status <> 'Cancelled';

/* The chapter shows:
    row_count
   -----------
           18
   (1 row)
*/


-- Order 5004 had one line, so 19 became 18. Every step's count made sense, so now group and add
-- up:

SELECT COALESCE(c.city, 'Unknown') AS city,
       COUNT(DISTINCT o.order_id)  AS orders,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS revenue
FROM orders AS o
JOIN customers   AS c  ON o.customer_id = c.customer_id
JOIN order_items AS oi ON o.order_id    = oi.order_id
WHERE o.status <> 'Cancelled'
GROUP BY COALESCE(c.city, 'Unknown')
ORDER BY revenue DESC;

/* The chapter shows:
      city    | orders | revenue
   -----------+--------+---------
    Chennai   |      2 |  105885
    Mumbai    |      5 |   81810
    Delhi     |      1 |   76560
    Unknown   |      1 |   23325
    Pune      |      1 |   20100
    Ahmedabad |      1 |   16250
   (6 rows)
*/


-- - COALESCE(c.city, 'Unknown') shows Sunrise Caterers' missing city as "Unknown", in both SELECT
-- and GROUP BY, so it forms its own group instead of a blank one. - COUNT(DISTINCT o.order_id)
-- counts orders, not the lines the join produced. - The six cities add up to ₹3,23,930, the total
-- revenue from non-cancelled orders.

-- =============================================================================================
-- Rebuilding the order slip from Figure 12.2
-- =============================================================================================

-- Section 12.2 promised you'd rebuild order 5001's slip yourself. It needs five tables: the order,
-- its customer, its sales rep, its lines, and each line's product:

SELECT o.order_id,
       c.customer_name,
       e.employee_name AS sales_rep,
       p.product_name,
       oi.quantity,
       ROUND(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100), 2) AS line_value
FROM orders AS o
JOIN      customers   AS c  ON o.customer_id  = c.customer_id
LEFT JOIN employees   AS e  ON o.sales_rep_id = e.employee_id
JOIN      order_items AS oi ON oi.order_id    = o.order_id
JOIN      products    AS p  ON p.product_id   = oi.product_id
WHERE o.order_id = 5001
ORDER BY p.product_id;

/* The chapter shows:
    order_id |  customer_name  |   sales_rep   |  product_name   | quantity | line_value
   ----------+-----------------+---------------+-----------------+----------+------------
        5001 | Sharma Hardware | Neha Kulkarni | Storage Box 10L |       20 |    9000.00
        5001 | Sharma Hardware | Neha Kulkarni | Water Bottle 1L |       50 |    5700.00
   (2 rows)
*/


-- Two rows, one per line on the slip, with ₹9,000 and ₹5,700 calculated, not stored, exactly as
-- Figure 12.2 showed. The sales rep is joined with a left join because order 5008 has no rep: for
-- that order an inner join would drop the whole slip. Add o.order_date, o.status, c.city,
-- oi.unit_price, and oi.discount_pct to the SELECT and you have every piece of the paper slip.

-- =============================================================================================
-- Real-life example: revenue is not profit
-- =============================================================================================

-- Sales teams love revenue. Owners care about profit. With unit_cost you can show both, by
-- category, for all non-cancelled orders:

SELECT p.category,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue,
       ROUND(SUM(oi.quantity * p.unit_cost), 0)                                  AS product_cost,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)
               - oi.quantity * p.unit_cost), 0)                                  AS gross_profit,
       ROUND(100.0 * SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)
               - oi.quantity * p.unit_cost)
             / SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 1) AS margin_pct
FROM order_items AS oi
JOIN orders   AS o ON oi.order_id   = o.order_id
JOIN products AS p ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY net_revenue DESC;

/* The chapter shows:
     category  | net_revenue | product_cost | gross_profit | margin_pct
   ------------+-------------+--------------+--------------+------------
    Industrial |      161385 |       137500 |        23885 |       14.8
    Storage    |       81810 |        57900 |        23910 |       29.2
    Kitchen    |       80735 |        52650 |        28085 |       34.8
   (3 rows)
*/


-- It joins the same three tables as the city query, with products in place of customers, because
-- cost and category live there. Here's what each part does:

-- - net_revenue is the money actually charged: quantity × price charged × (1 − discount). -
-- product_cost is quantity × the product's cost. Cost comes from products, which is why that table
-- is joined in. - gross_profit is revenue minus cost, summed across every line in the category. -
-- margin_pct divides total profit by total revenue. Notice it divides two sums. Averaging each
-- line's margin would give a different, misleading number, because a ₹50 line would count as much
-- as a ₹50,000 one.

-- Now read it as a manager would. Industrial crates bring in half of all revenue (₹1,61,385 of
-- ₹3,23,930) but earn the lowest margin, 14.8%. Kitchen products bring in the least revenue but
-- the most profit. The earlier margin query showed that crates are thin even at list price
-- (24.1%); the 10–12% discounts on crate orders push it down to 14.8%. A sales team rewarded on
-- revenue will keep pushing discounted crates. This one query can start a real conversation about
-- pricing and incentives, which is exactly what analysis is for.

-- > Simplification note. unit_cost here is today's standard cost. Real costs change over time, and
-- serious profit reporting stores the cost at the time of sale, just as order_items stores the
-- price at the time of sale. Chapter 23 covers how businesses define metrics like margin.

-- =============================================================================================
-- The fan-out trap: when joins inflate your numbers
-- =============================================================================================

-- This is the most expensive mistake in beginner SQL, and it rarely produces an error. The
-- question: how many orders has each customer placed? A reasonable-looking query:

SELECT c.customer_name, COUNT(*) AS num_orders
FROM customers AS c
JOIN orders      AS o  ON c.customer_id = o.customer_id
JOIN order_items AS oi ON o.order_id    = oi.order_id
GROUP BY c.customer_name
ORDER BY c.customer_name;

/* The chapter shows:
        customer_name      | num_orders
   ------------------------+------------
    Coastal Foods          |          3
    Green Leaf Hotels      |          3
    Metro Mart             |          4
    Northgate Distributors |          1
    Patel Kitchenware      |          1
    Sharma Hardware        |          5
    Sunrise Caterers       |          2
   (7 rows)
*/


-- Sharma Hardware has three orders, not five. Sunrise Caterers has one, not two. What happened?
-- Joining to order_items created one row per order line, so an order with two products appears
-- twice, and COUNT(*) counted lines, not orders. The data "fanned out" to the finest level of
-- detail in the join.

-- Two fixes. The better one: don't join tables you don't need. This question never needed
-- order_items:

SELECT c.customer_name, COUNT(*) AS num_orders
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
GROUP BY c.customer_name
ORDER BY c.customer_name;

/* The chapter shows:
        customer_name      | num_orders
   ------------------------+------------
    Coastal Foods          |          2
    Green Leaf Hotels      |          2
    Metro Mart             |          2
    Northgate Distributors |          1
    Patel Kitchenware      |          1
    Sharma Hardware        |          3
    Sunrise Caterers       |          1
   (7 rows)
*/


-- One row per order again, so COUNT(*) counts orders. Sometimes you do need the finer table in the
-- same query, for example to add each customer's revenue next to the count. Then use the fallback:
-- count what you mean, with COUNT(DISTINCT o.order_id), which counts each order once however many
-- lines it has:

SELECT c.customer_name, COUNT(DISTINCT o.order_id) AS num_orders
FROM customers AS c
JOIN orders      AS o  ON c.customer_id = o.customer_id
JOIN order_items AS oi ON o.order_id    = oi.order_id
GROUP BY c.customer_name
ORDER BY c.customer_name;

/* The chapter shows:
        customer_name      | num_orders
   ------------------------+------------
    Coastal Foods          |          2
    Green Leaf Hotels      |          2
    Metro Mart             |          2
    Northgate Distributors |          1
    Patel Kitchenware      |          1
    Sharma Hardware        |          3
    Sunrise Caterers       |          1
   (7 rows)
*/


-- The same seven numbers either way.

-- =============================================================================================
-- The same trap with money
-- =============================================================================================

-- Counting too many orders is embarrassing. Counting money twice can be expensive. Finance asks a
-- simple question: how much have we invoiced, how much has been paid, and how much is still owed?
-- Joining invoices to their payments seems natural:

SELECT SUM(i.amount)                   AS total_invoiced,
       SUM(p.amount)                   AS total_paid,
       SUM(i.amount) - SUM(p.amount)   AS outstanding
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id;

/* The chapter shows:
    total_invoiced | total_paid | outstanding
   ----------------+------------+-------------
         385610.00 |  197250.00 |   188360.00
   (1 row)
*/


-- The real total invoiced is ₹2,97,710 (just SELECT SUM(amount) FROM invoices). This query says
-- ₹3,85,610, and it nearly doubles the amount owed to ₹1,88,360. A collections team chasing that
-- number would be chasing money customers have already paid. To see why, look at the joined rows
-- for three invoices:

SELECT i.invoice_id, i.amount AS invoice_amount, p.payment_id, p.amount AS payment_amount
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id
WHERE i.invoice_id IN (9001, 9002, 9007)
ORDER BY i.invoice_id, p.payment_id;

/* The chapter shows:
    invoice_id | invoice_amount | payment_id | payment_amount
   ------------+----------------+------------+----------------
          9001 |       14700.00 |          1 |       14700.00
          9002 |       73260.00 |          2 |       40000.00
          9002 |       73260.00 |          3 |       33260.00
          9007 |       23325.00 |            |
   (4 rows)
*/


-- Invoice 9002 was paid in two parts, so the join produced two rows, each carrying the full
-- invoice amount of ₹73,260. Summing that column counts the invoice twice. The same happens to
-- invoice 9005. Payments aren't affected, because each payment appears once: payments are the
-- finest grain in the join.

-- The fix is to add up the payments for each invoice first, and only then join, so each invoice
-- meets at most one row. That needs one more tool, a query inside a query; section 12.12 shows it,
-- with this exact example.

-- > The grain question. Before writing any join, ask: what does one row of each table represent?
-- One row of orders is one order; one row of order_items is one product line within an order. That
-- "what is one row" is called the table's grain. When you join to a finer grain, your rows
-- multiply. Chapter 28 builds a whole discipline on this idea.

-- =============================================================================================
-- The LEFT JOIN that quietly became an INNER JOIN
-- =============================================================================================

-- Question: list every customer, and show their Pending orders if they have any. Two versions that
-- look almost the same:

-- Version A: condition in ON
SELECT c.customer_name, o.order_id, o.status
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status = 'Pending'
ORDER BY c.customer_id;

/* The chapter shows:
        customer_name      | order_id | status
   ------------------------+----------+---------
    Sharma Hardware        |          |
    Patel Kitchenware      |          |
    Green Leaf Hotels      |          |
    Coastal Foods          |          |
    Metro Mart             |     5012 | Pending
    Sunrise Caterers       |          |
    Northgate Distributors |          |
    Blue Bay Cafe          |          |
   (8 rows)
*/


-- Version B: condition in WHERE
SELECT c.customer_name, o.order_id, o.status
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
WHERE o.status = 'Pending'
ORDER BY c.customer_id;

/* The chapter shows:
    customer_name | order_id | status
   ---------------+----------+---------
    Metro Mart    |     5012 | Pending
   (1 row)
*/


-- Figure 12.5 — You write SELECT first, but the database gets to it fifth.

-- This order explains:

-- - Why WHERE can't use COUNT(*): at step 2, grouping hasn't happened. - Why WHERE can't use a
-- column alias defined in SELECT, like num_orders: at step 2, SELECT hasn't run, so the alias
-- doesn't exist yet. - Why ORDER BY can use an alias: it runs at step 7, after SELECT created it.
-- - Why a LEFT JOIN condition in WHERE removes rows: the join finished at step 1, and WHERE
-- filters its output at step 2.

-- (The real database engine is free to rearrange the physical work for speed, but the result
-- always matches this logical order. Chapter 28 shows how to see what it actually does.)

-- ---

-- =============================================================================================
-- 12.12 Queries inside queries: subqueries and set operations
-- =============================================================================================

-- =============================================================================================
-- Subqueries
-- =============================================================================================

-- A subquery is a query in parentheses used inside another query. Its most common forms:

-- A single value (scalar subquery). Which products are priced above the average price?

SELECT product_name, unit_price
FROM products
WHERE unit_price > (SELECT AVG(unit_price) FROM products)
ORDER BY unit_price;

/* The chapter shows:
      product_name   | unit_price
   ------------------+------------
    Storage Box 25L  |     780.00
    Garden Chair     |    1200.00
    Industrial Crate |    1450.00
   (3 rows)
*/


-- The inner query runs first and returns one number (₹775.00); the outer query compares every
-- product against it. You couldn't write WHERE unit_price > AVG(unit_price), because aggregates
-- can't appear in WHERE.

-- A list of values, with IN. Which customers have bought the Industrial Crate (product 105)?

SELECT customer_name
FROM customers
WHERE customer_id IN (
    SELECT o.customer_id
    FROM orders AS o
    JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE oi.product_id = 105
)
ORDER BY customer_name;

/* The chapter shows:
        customer_name
   ------------------------
    Coastal Foods
    Northgate Distributors
   (2 rows)
*/


-- A yes/no test, with EXISTS. Which customers have at least one order currently Shipped?

SELECT c.customer_name
FROM customers AS c
WHERE EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.customer_id
      AND o.status = 'Shipped'
)
ORDER BY c.customer_name;

/* The chapter shows:
        customer_name
   ------------------------
    Northgate Distributors
    Sharma Hardware
   (2 rows)
*/


-- EXISTS asks only "is there at least one matching row?", so the SELECT 1 inside is a convention;
-- what it selects doesn't matter. Notice the inner query refers to c.customer_id from the outer
-- query. That makes it a correlated subquery: conceptually it re-runs for each customer.

-- A correlated subquery with a real use. For each invoice, show the most recent payment. It's the
-- kind of thing a collections team asks daily: when did we last hear from this customer?

SELECT p.invoice_id, p.payment_date, p.amount
FROM payments AS p
WHERE p.payment_date = (
    SELECT MAX(p2.payment_date)
    FROM payments AS p2
    WHERE p2.invoice_id = p.invoice_id
)
ORDER BY p.invoice_id;

/* The chapter shows:
    invoice_id | payment_date |  amount
   ------------+--------------+----------
          9001 | 2026-02-02   | 14700.00
          9002 | 2026-03-02   | 33260.00
          9003 | 2026-02-20   | 10000.00
          9004 | 2026-03-01   | 14550.00
          9005 | 2026-03-12   |  7640.00
          9006 | 2026-03-10   | 20000.00
          9008 | 2026-03-20   | 30000.00
          9009 | 2026-03-25   | 20100.00
   (8 rows)
*/


-- Read it as: keep a payment if its date equals the latest payment date for the same invoice. The
-- inner query uses p.invoice_id from the outer row, so for payment 2 it finds the latest date
-- among invoice 9002's payments (2 March), and payment 2 (5 February) is dropped. The table uses
-- two aliases, p and p2, for the same payments table, just like the self-join. Invoices 9007 and
-- 9010 don't appear because they have no payments at all. "Latest record per group" is such a
-- common need that Chapter 13 gives it a cleaner tool, ROW_NUMBER().

-- > Watch out: NOT IN and NULLs. WHERE customer_id NOT IN (subquery) returns no rows at all if the
-- subquery's list contains even one NULL, because "x is not in (1, 2, NULL)" can't be confirmed
-- true. For "not in" logic, prefer NOT EXISTS or the anti-join from section 12.10. This is a
-- favorite interview trap, and Riverstone's data has a real case of it.

-- Which employees manage nobody? The obvious query:

SELECT employee_name
FROM employees
WHERE employee_id NOT IN (SELECT manager_id FROM employees);

/* The chapter shows:
    employee_name
   ---------------
   (0 rows)
*/


-- Zero rows, and no error, although three sales executives manage nobody. The subquery's list of
-- manager_id values is (NULL, 1, 2, 2, 1): Anita Rao, the Sales Head, has no manager. For Neha
-- Kulkarni (employee 3), "3 is not in (NULL, 1, 2, 2, 1)" would need "3 is not NULL" to be true,
-- and that comparison is UNKNOWN (section 12.7). So no row can pass. NOT EXISTS asks a different
-- question, "is there no row where this person is the manager?", and NULLs can't spoil it:

SELECT e.employee_name
FROM employees AS e
WHERE NOT EXISTS (
    SELECT 1
    FROM employees AS m
    WHERE m.manager_id = e.employee_id
)
ORDER BY e.employee_id;

/* The chapter shows:
    employee_name
   ---------------
    Neha Kulkarni
    Rahul Mehta
    Farah Khan
   (3 rows)
*/


-- A third option keeps NOT IN but removes the NULL from the list first:

SELECT employee_name
FROM employees
WHERE employee_id NOT IN (SELECT manager_id
                          FROM employees
                          WHERE manager_id IS NOT NULL)
ORDER BY employee_id;

/* The chapter shows:
    employee_name
   ---------------
    Neha Kulkarni
    Rahul Mehta
    Farah Khan
   (3 rows)
*/


-- It works, but only while everyone remembers the extra line. NOT EXISTS is the safer habit.

-- A table (derived table) in FROM or JOIN. A subquery can act as a temporary table you then query
-- or join to. This is how you aggregate at one level and then summarize again.

-- Figure 12.4 — The fix is to bring payments to the invoice's grain (one row per invoice) before
-- joining.

-- Its first job: the money fan-out from section 12.10. Joining invoices to payments counted
-- invoice 9002 twice and inflated the total invoiced to ₹3,85,610. The fix: add up payments per
-- invoice first, in a derived table, and join that one-row-per-invoice result:

SELECT SUM(i.amount)                        AS total_invoiced,
       SUM(COALESCE(p.paid, 0))             AS total_paid,
       SUM(i.amount - COALESCE(p.paid, 0))  AS outstanding
FROM invoices AS i
LEFT JOIN (
    SELECT invoice_id, SUM(amount) AS paid
    FROM payments
    GROUP BY invoice_id
) AS p ON i.invoice_id = p.invoice_id;

/* The chapter shows:
    total_invoiced | total_paid | outstanding
   ----------------+------------+-------------
         297710.00 |  197250.00 |   100460.00
   (1 row)
*/


-- How it works:

-- - The subquery in parentheses runs first and returns one row per invoice with its total paid. AS
-- p names that result so the outer query can join to it like a table. - The left join now matches
-- each invoice to at most one row, so nothing is repeated. - COALESCE(p.paid, 0) turns "no
-- payments" (NULL) into zero, so unpaid invoices still count in full. Without it, i.amount - NULL
-- would be NULL and those invoices would silently drop out of outstanding. - Reconcile: ₹2,97,710
-- invoiced minus ₹1,97,250 paid is ₹1,00,460. The totals now agree with each table summed on its
-- own. ✓

-- There's no SUM(DISTINCT ...) shortcut here, by the way. SUM(DISTINCT i.amount) would add each
-- different amount once, so two separate invoices that happened to be for the same amount would be
-- counted as one. The only reliable fix is to aggregate to the right grain before joining. Chapter
-- 13 shows a tidier way to write these steps, using CTEs.

-- Another use: averages of totals. What's the average order value, excluding cancelled orders?
-- First total each order, then average those totals:

SELECT ROUND(AVG(order_revenue), 2) AS avg_order_value
FROM (
    SELECT o.order_id,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS order_revenue
    FROM orders AS o
    JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY o.order_id
) AS per_order;

/* The chapter shows:
    avg_order_value
   -----------------
           29448.18
   (1 row)
*/


-- Averaging the order lines directly would give the average line value, a different and misleading
-- number. Derived tables solve the fan-out problem from section 12.10 too: aggregate each table to
-- the grain you need, then join the results. Once subqueries nest more than one level deep they
-- become hard to read, and Chapter 13 introduces common table expressions (CTEs), which do the
-- same job with named, top-to-bottom steps.

-- Derived tables with a cross join. Section 12.10 wanted every segment paired with every category,
-- once each. Two derived tables supply the two distinct lists, and CROSS JOIN pairs them: 3
-- segments × 4 categories = 12 pairs, of which LIMIT 5 shows the first five:

SELECT s.segment, p.category
FROM (SELECT DISTINCT segment  FROM customers) AS s
CROSS JOIN
     (SELECT DISTINCT category FROM products)  AS p
ORDER BY s.segment, p.category
LIMIT 5;

/* The chapter shows:
      segment   |  category
   -------------+------------
    Hospitality | Furniture
    Hospitality | Industrial
    Hospitality | Kitchen
    Hospitality | Storage
    Retail      | Furniture
   (5 rows)
*/


-- Left-join real sales onto a grid like this and the combinations with no sales show up as zeros
-- instead of being missing.

-- =============================================================================================
-- Set operations: stacking results
-- =============================================================================================

-- Joins combine tables side by side. Set operations stack results on top of each other. The
-- queries being stacked must return the same number of columns, with compatible types.

-- - UNION stacks results and removes duplicates. - UNION ALL stacks results and keeps everything.

SELECT city FROM customers WHERE segment = 'Retail'
UNION
SELECT city FROM customers WHERE segment = 'Hospitality'
ORDER BY city;

/* The chapter shows:
      city
   -----------
    Ahmedabad
    Mumbai
    Pune
   
   (4 rows)
*/


-- Now the same with UNION ALL:

SELECT city FROM customers WHERE segment = 'Retail'
UNION ALL
SELECT city FROM customers WHERE segment = 'Hospitality'
ORDER BY city;

/* The chapter shows:
      city
   -----------
    Ahmedabad
    Mumbai
    Mumbai
    Pune
    Pune
   
   (6 rows)
*/


-- Six rows: Ahmedabad once, Mumbai twice, Pune twice, and the blank (NULL) city once. Notice that
-- UNION treated NULL like any other value when removing duplicates.

-- UNION ALL is faster, because removing duplicates requires extra work. Use it by default when you
-- know the pieces don't overlap (January's table stacked on February's) or when duplicates are
-- meaningful. Use UNION only when you actually want duplicates removed.

-- Two more set operations: INTERSECT returns rows that appear in both results, and EXCEPT (called
-- MINUS in Oracle) returns rows in the first result but not the second. EXCEPT is a quick
-- reconciliation tool: which product IDs are in the price list but not in the warehouse system? On
-- Riverstone's data: which customers ordered in February but placed no (non-cancelled) order in
-- March?

SELECT c.customer_name
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.order_date >= DATE '2026-02-01'
  AND o.order_date <  DATE '2026-03-01'
EXCEPT
SELECT c.customer_name
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.order_date >= DATE '2026-03-01'
  AND o.order_date <  DATE '2026-04-01'
  AND o.status <> 'Cancelled'
ORDER BY customer_name;

/* The chapter shows:
        customer_name
   ------------------------
    Coastal Foods
    Northgate Distributors
    Sunrise Caterers
   (3 rows)
*/


-- The first query lists February's five customers; EXCEPT removes the ones that also appear in the
-- second (Sharma Hardware and Metro Mart ordered again in March). Like UNION, it removes
-- duplicates, so each name appears once. Section 12.15 uses this result to explain why March's
-- revenue fell.

-- Good place to stop.

-- ---

-- =============================================================================================
-- 12.13 Building and changing a database: CREATE, INSERT, UPDATE, DELETE, ALTER, and DROP
-- =============================================================================================

-- Until now you've only read data that someone else loaded. This section is the other half:
-- creating a database and its tables, putting data in, correcting it, removing it, and changing
-- the structure of a table after it's already full of data. Every step is shown in both PostgreSQL
-- and MySQL, because this is where the two differ most. First time through, do the PostgreSQL
-- blocks only: every block that differs is labelled PostgreSQL: or MySQL:, so you can skip the
-- MySQL ones now and come back to them with the MySQL track.

-- As an analyst you'll mostly read data, and in many companies your account on the live business
-- systems will be read-only. That's a protection, not an insult. But you'll still use everything
-- in this section: to build practice and staging tables, to load a spreadsheet someone emails you,
-- to keep a small tracker for your team, and, as you move toward engineering and architecture
-- roles, to design and change the databases other people rely on.

-- =============================================================================================
-- Three families of SQL statements
-- =============================================================================================

-- | Family | Stands for | Statements | What it changes | |---|---|---|---| | DDL | Data Definition
-- Language | CREATE, ALTER, DROP, TRUNCATE, RENAME | the structure: databases, tables, columns,
-- constraints | | DML | Data Manipulation Language | INSERT, UPDATE, DELETE (and SELECT, which
-- only reads) | the rows inside tables | | TCL | Transaction Control Language | BEGIN / START
-- TRANSACTION, COMMIT, ROLLBACK | whether a group of changes is kept or undone |

-- A fourth family, DCL (Data Control Language: GRANT and REVOKE), controls who may do what.
-- Chapter 64, section 64.3 decides who should get which access and shows GRANT, REVOKE and row-
-- level security in use.

-- > The lab rule: never practice on data that matters. Everything in this section happens in a
-- new, separate database called riverstone_lab, so nothing you do can damage the riverstone
-- database the rest of the chapter uses. At work, follow the same rule: try changes on a copy,
-- never first on the live system.

-- =============================================================================================
-- The brief: a purchasing database
-- =============================================================================================

-- Riverstone's purchasing team tracks its suppliers and purchase orders in a spreadsheet that
-- three people edit. Last month two people typed the same supplier twice, someone entered an order
-- for a supplier that had been removed, and a unit cost of ₹12,050 turned out to be ₹120.50.
-- They've asked you for a small database with two tables:

-- - suppliers: one row per supplier. Every supplier must have a unique name, a rating from 1 to 5
-- if rated, and a date they were onboarded. - purchase_orders: one row per order line. Every order
-- must belong to a real supplier and have a positive quantity.

-- Each of those business rules will become a constraint, a rule the database enforces so bad data
-- can't get in at all. That's the real advantage over the spreadsheet.

-- =============================================================================================
-- Step 1: Create the database
-- =============================================================================================

-- The statement is the same in both databases:

CREATE DATABASE riverstone_lab;


-- Creating a database doesn't switch you into it. The next step depends on the database and the
-- tool:

-- - PostgreSQL in DBeaver: each connection points at one database. Edit the connection (or create
-- a new one) so its Database is riverstone_lab, as in section 12.3, then open an SQL editor on it.
-- (In the psql command-line client, which needs the terminal you'll meet in Chapter 26, the same
-- switch is \c riverstone_lab.) - MySQL: run USE riverstone_lab;. Everything after that happens
-- inside riverstone_lab until you USE another database. In DBeaver you can also double-click the
-- database in the navigator.

-- To see which databases exist, ask PostgreSQL's built-in list. pg_database is a table PostgreSQL
-- keeps about itself, with one row per database; you can query it like any other table.

-- PostgreSQL:

SELECT datname
FROM pg_database
WHERE datname LIKE 'riverstone%'
ORDER BY datname;

/* The chapter shows:
        datname
   -----------------
    riverstone
    riverstone_2025
    riverstone_full
    riverstone_lab
   (4 rows)
*/


-- > Naming. Use lower-case letters, digits, and underscores: riverstone_lab, purchase_orders.
-- Avoid spaces, hyphens, and capital letters. They force you to wrap every name in quotes forever
-- after ("Purchase Orders" in PostgreSQL,  Purchase Orders  in MySQL), and PostgreSQL and MySQL
-- treat capitals in names differently. CREATE DATABASE IF NOT EXISTS riverstone_lab; works in
-- MySQL if you want a script that can safely run twice; PostgreSQL doesn't support IF NOT EXISTS
-- for databases, only for tables and schemas.

-- =============================================================================================
-- Step 2: Design the tables before you type
-- =============================================================================================

-- Five minutes on paper saves hours of ALTER TABLE later. For each column, decide four things: its
-- name, its type, whether it may be empty, and any rule it must follow.

-- | Column | Type | Empty allowed? | Rule | |---|---|---|---| | supplier_id | whole number,
-- numbered automatically | no | primary key | | supplier_name | text up to 100 characters | no |
-- unique | | city | text up to 50 characters | yes | | | contact_email | text up to 100 characters
-- | yes | | | fax_number | text up to 20 characters | yes | copied from the old spreadsheet | |
-- rating | small whole number | yes (not rated yet) | between 1 and 5 | | is_active | true/false |
-- no | defaults to true | | onboarded_on | date | no | |

-- Most types have the same or similar names in both databases. The differences you'll meet most:

-- | You want | PostgreSQL | MySQL | |---|---|---| | Whole number | INTEGER (or INT) | INT (or
-- INTEGER) | | Small whole number (−32,768 to 32,767; enough for a 1–5 rating) | SMALLINT |
-- SMALLINT | | Big whole number | BIGINT | BIGINT | | Exact decimal, e.g. money | NUMERIC(10,2) |
-- DECIMAL(10,2) (NUMERIC also accepted) | | Text with a maximum length | VARCHAR(100) |
-- VARCHAR(100) | | Long text | TEXT | TEXT | | Date | DATE | DATE | | Date and time | TIMESTAMP |
-- DATETIME (or TIMESTAMP, which has a narrower range) | | True/false | BOOLEAN (stored and shown
-- as t/f) | BOOLEAN (really TINYINT(1): stored and shown as 1/0) | | Automatic ID | INTEGER
-- GENERATED ALWAYS AS IDENTITY | INT AUTO_INCREMENT |

-- =============================================================================================
-- Step 3: CREATE TABLE
-- =============================================================================================

-- Here is suppliers.

-- PostgreSQL:

CREATE TABLE suppliers (
    supplier_id    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supplier_name  VARCHAR(100) NOT NULL UNIQUE,
    city           VARCHAR(50),
    contact_email  VARCHAR(100),
    fax_number     VARCHAR(20),
    rating         SMALLINT CHECK (rating BETWEEN 1 AND 5),
    is_active      BOOLEAN NOT NULL DEFAULT TRUE,
    onboarded_on   DATE NOT NULL
);


-- Read it line by line:

-- - CREATE TABLE suppliers ( … ); names the table, then lists its columns inside the parentheses,
-- separated by commas. There's no comma after the last one. - GENERATED ALWAYS AS IDENTITY
-- (PostgreSQL) and AUTO_INCREMENT (MySQL) tell the database to number new rows 1, 2, 3… by itself.
-- You never type an ID. - PRIMARY KEY makes the column the row's identity: unique and never empty
-- (section 12.1). - NOT NULL means the column must always have a value. - UNIQUE means no two rows
-- may have the same value. Here, it stops the "same supplier typed twice" problem. - CHECK (rating
-- BETWEEN 1 AND 5) is a rule every row must pass. An empty rating is still allowed, because a
-- CHECK only rejects values that are definitely false, and NULL is unknown (section 12.7). -
-- DEFAULT TRUE fills in a value when an insert doesn't mention the column.

-- Now purchase_orders, which links to suppliers.

-- PostgreSQL:

CREATE TABLE purchase_orders (
    po_id        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supplier_id  INTEGER NOT NULL,
    po_date      DATE NOT NULL,
    item         VARCHAR(100) NOT NULL,
    quantity     INTEGER NOT NULL CHECK (quantity > 0),
    unit_cost    NUMERIC(10,2) NOT NULL,
    status       VARCHAR(20) NOT NULL DEFAULT 'Open',
    FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id)
);


-- The last line is the foreign key (section 12.1): every supplier_id in this table must exist in
-- suppliers. Two things follow from it. The parent table has to be created first, and, as you'll
-- see, the database will refuse to delete a supplier who still has orders.

-- > Dialect note: write foreign keys on their own line. PostgreSQL also accepts a shorter form
-- inside the column definition: supplier_id INTEGER NOT NULL REFERENCES suppliers (supplier_id).
-- MySQL 8.4 and earlier read that form and silently ignore it: the table is created, but nothing
-- is enforced. MySQL 9.0 and later do enforce it. The separate FOREIGN KEY (…) REFERENCES … line,
-- used above, works correctly in every version of both databases, so it's the habit this book
-- recommends.

-- Check what you built. PostgreSQL stores a description of every table in information_schema, a
-- set of views that most SQL databases provide:

SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'suppliers'
ORDER BY ordinal_position;

/* The chapter shows:
     column_name  |     data_type     | is_nullable | column_default
   ---------------+-------------------+-------------+----------------
    supplier_id   | integer           | NO          |
    supplier_name | character varying | NO          |
    city          | character varying | YES         |
    contact_email | character varying | YES         |
    fax_number    | character varying | YES         |
    rating        | smallint          | YES         |
    is_active     | boolean           | NO          | true
    onboarded_on  | date              | NO          |
   (8 rows)
*/


-- Notice is_active became tinyint(1) with a default of 1: MySQL's BOOLEAN is really a tiny whole
-- number. SHOW CREATE TABLE suppliers; prints the full statement MySQL would use to recreate the
-- table, constraints included. It's the quickest way to see exactly what MySQL built.

-- =============================================================================================
-- Step 4: INSERT: adding rows
-- =============================================================================================

-- Add one supplier. This statement is identical in both databases:

INSERT INTO suppliers (supplier_name, city, contact_email, rating, onboarded_on)
VALUES ('Western Polymers', 'Vapi', 'sales@westernpolymers.example', 4, '2025-06-01');


-- - The column list after the table name says which columns you're filling, and in what order.
-- Always write it. INSERT INTO suppliers VALUES (…) without a list depends on the exact column
-- order, and breaks the day someone adds a column. - supplier_id isn't mentioned, so the database
-- numbers it. is_active isn't mentioned, so it gets its default, TRUE. fax_number isn't mentioned,
-- so it's NULL. - Text and dates go in single quotes; numbers don't.

-- Add several rows in one statement by separating them with commas:

INSERT INTO suppliers (supplier_name, city, contact_email, rating, onboarded_on)
VALUES ('Deccan Cartons',     'Pune',       'sales@deccancartons.example', 3,    '2025-08-15'),
       ('Kaveri Steel Works', 'Coimbatore', NULL,                          5,    '2025-09-10'),
       ('Sagar Labels',       'Mumbai',     'orders@sagarlabels.example',  NULL, '2026-01-05');


-- Writing NULL without quotes records "unknown". (Writing 'NULL' in quotes would store the four
-- letters N-U-L-L, a surprisingly common mistake.)

SELECT supplier_id, supplier_name, city, rating, is_active, onboarded_on
FROM suppliers
ORDER BY supplier_id;

/* The chapter shows:
    supplier_id |   supplier_name    |    city    | rating | is_active | onboarded_on
   -------------+--------------------+------------+--------+-----------+--------------
              1 | Western Polymers   | Vapi       |      4 | t         | 2025-06-01
              2 | Deccan Cartons     | Pune       |      3 | t         | 2025-08-15
              3 | Kaveri Steel Works | Coimbatore |      5 | t         | 2025-09-10
              4 | Sagar Labels       | Mumbai     |        | t         | 2026-01-05
   (4 rows)
*/


-- MySQL shows the same four rows, with 1 instead of t in is_active and the word NULL for Sagar
-- Labels' rating.

-- Now the orders:

INSERT INTO purchase_orders (supplier_id, po_date, item, quantity, unit_cost)
VALUES (1, '2026-03-02', 'Polypropylene granules (kg)', 2000, 118.50),
       (1, '2026-03-16', 'Polypropylene granules (kg)', 1500, 121.00),
       (2, '2026-03-05', 'Cardboard cartons',            800,  22.00),
       (3, '2026-03-09', 'Steel handles',                500,  14.75),
       (4, '2026-03-20', 'Printed labels',              3000,   1.20);


-- Every order gets status = 'Open' from the default.

-- > How do you know it worked? The database reports how many rows each statement changed. DBeaver
-- shows it in the results area as Updated Rows: 5. (The command-line clients say the same thing
-- their own way: psql prints INSERT 0 5, where the 0 is a leftover from old PostgreSQL versions
-- and the 5 is the row count, and the MySQL client prints Query OK, 5 rows affected.) Glance at
-- that number after every change. If you expected 1 and it says 300, stop.

-- =============================================================================================
-- When the database says no
-- =============================================================================================

-- This is where constraints pay for themselves. Try four inserts that the old spreadsheet would
-- have accepted without complaint.

-- A supplier with no name:

INSERT INTO suppliers (city, onboarded_on)
VALUES ('Surat', '2026-02-01');


-- The same supplier twice:

INSERT INTO suppliers (supplier_name, city, onboarded_on)
VALUES ('Deccan Cartons', 'Nashik', '2026-02-01');


-- A rating of 7:

INSERT INTO suppliers (supplier_name, city, rating, onboarded_on)
VALUES ('Gujarat Pigments', 'Ahmedabad', 7, '2026-02-01');


-- An order for a supplier that doesn't exist:

INSERT INTO purchase_orders (supplier_id, po_date, item, quantity, unit_cost)
VALUES (99, '2026-03-21', 'Lids', 100, 9.00);


-- Each rejected row is a problem that never reaches a report. Learn to read these messages: they
-- name the rule (not-null, unique, check, foreign key), the column, and often the offending value.
-- PostgreSQL's messages are usually more detailed; MySQL's error numbers (1062, 1452…) are easy to
-- search for.

-- Now add Gujarat Pigments with a valid rating, and look at the IDs:

INSERT INTO suppliers (supplier_name, city, rating, onboarded_on)
VALUES ('Gujarat Pigments', 'Ahmedabad', 4, '2026-02-01');


SELECT supplier_id, supplier_name
FROM suppliers
ORDER BY supplier_id;


-- Gujarat Pigments is supplier 8 in PostgreSQL and 6 in MySQL. Nothing is broken. The failed
-- inserts used up ID numbers before they were rejected, and the two databases use them up slightly
-- differently. Automatic IDs are labels, not counts. They can have gaps, and they'll differ
-- between systems. Never use the highest ID as "the number of suppliers" (use COUNT(*)), and never
-- assume the next ID will be exactly one more than the last.

-- Getting the ID of the row you just inserted. Programs often need it straight away, for example
-- to add that supplier's first order. PostgreSQL can return it from the insert itself:

INSERT INTO suppliers (supplier_name, city, onboarded_on)
VALUES ('Nilgiri Packaging', 'Ooty', '2026-03-01')
RETURNING supplier_id;

/* The chapter shows:
    supplier_id
   -------------
              9
   (1 row)
*/


-- Loading local files is switched off by default in MySQL for security, so the first attempt
-- usually fails with "Loading local data is disabled; this must be enabled on both the client and
-- server sides". On your own lab server, an administrator setting, SET GLOBAL local_infile = 1;,
-- plus the client option --local-infile=1 (or the allowLoadLocalInfile driver property in DBeaver)
-- enables it. On a company server, ask first.

-- =============================================================================================
-- Step 5: UPDATE: changing rows
-- =============================================================================================

-- An UPDATE has three parts: the table, the new values (SET), and which rows (WHERE).

-- Purchasing has now rated Sagar Labels. Before changing anything, look at exactly the rows your
-- WHERE will touch:

SELECT supplier_id, supplier_name, rating
FROM suppliers
WHERE supplier_name = 'Sagar Labels';

/* The chapter shows:
    supplier_id | supplier_name | rating
   -------------+---------------+--------
              4 | Sagar Labels  |
   (1 row)
*/


-- One row, the right one. Now change it, reusing the same WHERE:

UPDATE suppliers
SET rating = 4
WHERE supplier_name = 'Sagar Labels';


-- DBeaver reports Updated Rows: 1: one row, as the preview promised.

-- Calculated updates. Western Polymers (supplier 1) has raised prices by 5% on orders not yet
-- received. SET can use the column's current value:

UPDATE purchase_orders
SET unit_cost = ROUND(unit_cost * 1.05, 2)
WHERE supplier_id = 1
  AND status = 'Open';


-- The database reports 2 rows changed. Check them: ₹118.50 × 1.05 = ₹124.425, rounded to ₹124.43,
-- and ₹121.00 × 1.05 = ₹127.05.

-- Updating with information from another table. Purchasing decides that open orders from suppliers
-- rated below 4 go on hold until reviewed. The rating lives in suppliers, the status in
-- purchase_orders. This is one of the places where the two databases differ. PostgreSQL adds a
-- FROM clause:

UPDATE purchase_orders AS po
SET status = 'On hold'
FROM suppliers AS s
WHERE po.supplier_id = s.supplier_id
  AND s.rating < 4
  AND po.status = 'Open';


-- Both change one row: the Deccan Cartons order, because Deccan's rating is 3. Finally, the first
-- granules order has arrived:

UPDATE purchase_orders
SET status = 'Received'
WHERE po_id = 1;


SELECT po_id, supplier_id, item, unit_cost, status
FROM purchase_orders
ORDER BY po_id;

/* The chapter shows:
    po_id | supplier_id |            item             | unit_cost |  status
   -------+-------------+-----------------------------+-----------+----------
        1 |           1 | Polypropylene granules (kg) |    124.43 | Received
        2 |           1 | Polypropylene granules (kg) |    127.05 | Open
        3 |           2 | Cardboard cartons           |     22.00 | On hold
        4 |           3 | Steel handles               |     14.75 | Open
        5 |           4 | Printed labels              |      1.20 | Open
   (5 rows)
*/


-- You can set several columns at once, separated by commas: SET status = 'Received', unit_cost =
-- 120.00.

-- > Watch out: UPDATE or DELETE without WHERE. UPDATE purchase_orders SET status = 'Received';
-- marks every order as received. DELETE FROM purchase_orders; removes them all. The database won't
-- ask "are you sure?". Three habits prevent this: run the WHERE as a SELECT first; check the
-- reported row count; and for anything important, work inside a transaction (Step 8) so you can
-- undo it. > > MySQL Workbench helps here. By default it runs in safe updates mode and refuses an
-- UPDATE or DELETE whose WHERE doesn't use a key column, with error 1175 ("You are using safe
-- update mode…"). It's annoying the first time and a lifesaver the tenth. Don't switch it off just
-- to make an error go away; add a proper WHERE instead.

-- =============================================================================================
-- Step 6: DELETE: removing rows
-- =============================================================================================

-- The printed-labels order (order 5) was entered by mistake:

DELETE FROM purchase_orders
WHERE po_id = 5;


-- DBeaver reports Updated Rows: 1 (it uses the same words for deletes). Check what's left:

SELECT COUNT(*) AS orders_left
FROM purchase_orders;

/* The chapter shows:
    orders_left
   -------------
              4
   (1 row)
*/


-- Five orders minus one: MySQL gives the same 4.

-- Now try to remove a supplier who still has orders:

DELETE FROM suppliers
WHERE supplier_name = 'Western Polymers';


-- The foreign key protects the orders from becoming orphans: rows pointing at a supplier who no
-- longer exists. What should happen to a parent's children is a design choice you make when you
-- create the foreign key, by adding ON DELETE … to it:

-- | Foreign key option | When the supplier is deleted… | Use it when | |---|---|---| | (nothing),
-- RESTRICT, or NO ACTION | the delete is refused while orders exist | the history matters: almost
-- always, for business records | | ON DELETE CASCADE | all its orders are deleted too | the child
-- rows mean nothing without the parent, like the lines of a draft basket | | ON DELETE SET NULL |
-- its orders stay, with supplier_id set to NULL | the child should survive, and the column allows
-- NULL |

-- For suppliers, refusing is right. Past purchase orders are financial records, and nobody should
-- be able to wipe them out by removing a supplier. So how do you remove a supplier Riverstone no
-- longer uses? Usually, you don't delete it at all. You mark it inactive, which is called a soft
-- delete:

UPDATE suppliers
SET is_active = FALSE
WHERE supplier_name = 'Nilgiri Packaging';


-- Check it:

SELECT supplier_name, is_active
FROM suppliers
WHERE supplier_name = 'Nilgiri Packaging';


-- f (false) in PostgreSQL, 0 in MySQL: the same fact, in each database's spelling of a true/false
-- value (Step 2). Reports and forms then show only WHERE is_active = TRUE, while the history stays
-- complete. Most business systems work this way.

-- Good place to stop.

-- =============================================================================================
-- Step 7: Insert or update in one statement (upsert)
-- =============================================================================================

-- Every week Deccan Cartons sends an updated contact sheet. For each supplier on it, you want to
-- update the row if the supplier already exists, or insert it if it's new. Doing that in one
-- statement is called an upsert (update + insert), and each database spells it differently. Both
-- rely on a UNIQUE or primary key column to recognize "already exists"; here, supplier_name.

-- PostgreSQL:

INSERT INTO suppliers (supplier_name, city, contact_email, onboarded_on)
VALUES ('Deccan Cartons', 'Pune', 'accounts@deccancartons.example', '2025-08-15')
ON CONFLICT (supplier_name)
DO UPDATE SET contact_email = EXCLUDED.contact_email;


-- - In PostgreSQL, EXCLUDED means "the row you tried to insert". ON CONFLICT (supplier_name) names
-- the unique column to check. - In MySQL, AS new gives the incoming row a name you can refer to.
-- (Older tutorials write VALUES(contact_email) instead; that form still works but is deprecated.)
-- MySQL reports 2 rows affected for an upsert that updated, and 1 for one that inserted.

-- Deccan Cartons already existed, so its email changed and no new row was added:

SELECT supplier_name, city, contact_email, rating, is_active
FROM suppliers
ORDER BY supplier_name;

/* The chapter shows:
      supplier_name    |    city    |         contact_email          | rating | is_active
   --------------------+------------+--------------------------------+--------+-----------
    Deccan Cartons     | Pune       | accounts@deccancartons.example |      3 | t
    Gujarat Pigments   | Ahmedabad  |                                |      4 | t
    Kaveri Steel Works | Coimbatore |                                |      5 | t
    Nilgiri Packaging  | Ooty       |                                |        | f
    Sagar Labels       | Mumbai     | orders@sagarlabels.example     |      4 | t
    Western Polymers   | Vapi       | sales@westernpolymers.example  |      4 | t
   (6 rows)
*/


-- > Real-life example: the nightly supplier sync. Many companies copy a master list, such as
-- suppliers, products, or price lists, from one system into another every night. An upsert is the
-- heart of that job: new suppliers are added, changed details are updated, and running the job
-- twice doesn't create duplicates. Chapter 45 builds this kind of load; Chapter 20 uses the same
-- "safe to run twice" idea for reports.

-- =============================================================================================
-- Step 8: Transactions: the undo button
-- =============================================================================================

-- A transaction groups statements so they're kept or undone together. BEGIN (or START TRANSACTION)
-- starts one, COMMIT keeps every change since then, and ROLLBACK undoes them all.

-- Try a dangerous delete safely. In PostgreSQL:

BEGIN;
DELETE FROM purchase_orders WHERE status = 'Open';
SELECT COUNT(*) AS orders_left FROM purchase_orders;
ROLLBACK;
SELECT COUNT(*) AS orders_left FROM purchase_orders;

/* The chapter shows:
    orders_left
   -------------
              2
   (1 row)
   
    orders_left
   -------------
              4
   (1 row)
*/


-- Inside the transaction the two open orders were gone; after ROLLBACK all four are back. The
-- MySQL version is identical except that it starts with START TRANSACTION;, and gives the same two
-- results.

-- Transactions are why a bank transfer never takes money out of one account without putting it
-- into the other: both changes commit together, or neither does. That guarantee is part of the
-- ACID properties you'll study in Chapter 49.

-- The big difference: structure changes. Try undoing an ALTER TABLE (Step 9 explains the statement
-- itself):

-- PostgreSQL:

BEGIN;
ALTER TABLE suppliers ADD COLUMN notes TEXT;
ROLLBACK;
SELECT COUNT(*) AS notes_column_exists
FROM information_schema.columns
WHERE table_name = 'suppliers' AND column_name = 'notes';

/* The chapter shows:
    notes_column_exists
   ---------------------
                      0
   (1 row)
*/


-- > Dialect note: auto-commit. DBeaver and MySQL Workbench run in auto-commit mode by default:
-- every statement is committed the instant it runs, unless you start a transaction. DBeaver also
-- has a toolbar switch for manual commit mode, where nothing is saved until you press Commit.
-- Check which mode you're in before experimenting.

-- =============================================================================================
-- Step 9: ALTER TABLE: changing the structure
-- =============================================================================================

-- Business requirements change after tables are full of data. Purchasing now wants each supplier's
-- GST number, calls the email column just email, has stopped using fax, and wants the email to be
-- required. You don't recreate the table; you alter it. The data stays where it is.

-- First, take a backup copy. One statement copies both the structure and the rows into a new
-- table, in both databases:

CREATE TABLE suppliers_backup AS
SELECT * FROM suppliers;


SELECT COUNT(*) AS rows_copied FROM suppliers_backup;

/* The chapter shows:
    rows_copied
   -------------
              6
   (1 row)
*/


-- A copy made this way keeps the columns and their types, but not the primary key, defaults, or
-- other constraints. It's a safety net for the data, not a replacement table.

-- Add a column. Same in both:

ALTER TABLE suppliers ADD COLUMN gst_number VARCHAR(15);


-- Existing rows get NULL in the new column (or its default, if you give it one with DEFAULT). Fill
-- in the two numbers purchasing has so far. (These GST numbers are invented, like everything else
-- at Riverstone.)

UPDATE suppliers SET gst_number = '24AAACW1234A1Z5' WHERE supplier_name = 'Western Polymers';
UPDATE suppliers SET gst_number = '27AAACD5678B1Z2' WHERE supplier_name = 'Deccan Cartons';


-- Add a constraint to an existing table. No two suppliers may share a GST number. Give the
-- constraint a name, so error messages are readable and you can remove it later:

ALTER TABLE suppliers
ADD CONSTRAINT uq_suppliers_gst UNIQUE (gst_number);


UPDATE suppliers
SET gst_number = '24AAACW1234A1Z5'
WHERE supplier_name = 'Sagar Labels';


-- Adding a constraint also checks the rows already in the table: if two suppliers had shared a GST
-- number, the ALTER TABLE itself would have failed until you fixed the data.

-- Rename a column. Same in both (MySQL 8.0 and later):

ALTER TABLE suppliers RENAME COLUMN contact_email TO email;


-- Renaming is easy for the database and risky for everything around it: every saved query, report,
-- and dashboard that uses the old name breaks. Search for the old name before you rename.

-- Remove a column. Same in both. The data in it is gone for good:

ALTER TABLE suppliers DROP COLUMN fax_number;


-- A structure change like these two touches no rows, so there's no row count to check. The table
-- description at the end of this step (information_schema.columns, or DESCRIBE in MySQL) shows
-- both changes.

-- Change a column's type or size. Purchasing has a supplier in "Thiruvananthapuram (Technopark
-- Phase III)", which doesn't fit in 50 characters. This is where the two databases differ:

-- PostgreSQL:

ALTER TABLE suppliers ALTER COLUMN city TYPE VARCHAR(80);


-- In PostgreSQL, ALTER COLUMN … TYPE changes only the type, and NOT NULL and the default stay as
-- they were:

ALTER TABLE purchase_orders ALTER COLUMN status TYPE VARCHAR(30);


-- PostgreSQL:

SELECT column_name, character_maximum_length, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'purchase_orders' AND column_name = 'status';

/* The chapter shows:
    column_name | character_maximum_length | is_nullable |      column_default
   -------------+--------------------------+-------------+---------------------------
    status      |                       30 | NO          | 'Open'::character varying
   (1 row)
*/


-- The MySQL rule of thumb: before any MODIFY COLUMN, run SHOW CREATE TABLE and copy the column's
-- full current definition, then change only the part you mean to change.

-- Make a column required. Purchasing wants every supplier to have an email. Try it:

-- PostgreSQL:

ALTER TABLE suppliers ALTER COLUMN email SET NOT NULL;

/* The chapter shows:
   ERROR:  column "email" of relation "suppliers" contains null values
*/


-- Both refuse, because three suppliers have no email yet. A new rule can't be added while existing
-- data breaks it. Fix the data first, then add the rule:

UPDATE suppliers SET email = 'info@kaveristeel.example'      WHERE supplier_name = 'Kaveri Steel Works';
UPDATE suppliers SET email = 'hello@gujaratpigments.example' WHERE supplier_name = 'Gujarat Pigments';
UPDATE suppliers SET email = 'contact@nilgiripack.example'   WHERE supplier_name = 'Nilgiri Packaging';


-- PostgreSQL:

ALTER TABLE suppliers ALTER COLUMN email SET NOT NULL;


-- This time both statements succeed: no row breaks the rule any more. The finished-table
-- description at the end of this step shows email as required.

-- (To make a column optional again: ALTER COLUMN email DROP NOT NULL in PostgreSQL, or MODIFY
-- COLUMN email VARCHAR(100) NULL in MySQL.)

-- Add a CHECK rule for allowed values. Status should only ever be one of four words:

ALTER TABLE purchase_orders
ADD CONSTRAINT chk_po_status
CHECK (status IN ('Open', 'On hold', 'Received', 'Cancelled'));


UPDATE purchase_orders
SET status = 'Shipped'
WHERE po_id = 2;


-- "Shipped" isn't a purchase-order status at Riverstone, so the database refuses it, just as a
-- drop-down list in a form would.

-- Change or remove a default, and remove a constraint. These are written the same way in both
-- databases:

ALTER TABLE purchase_orders ALTER COLUMN status SET DEFAULT 'Open';


-- - ALTER TABLE purchase_orders ALTER COLUMN status DROP DEFAULT; removes a default. - ALTER TABLE
-- purchase_orders DROP CONSTRAINT chk_po_status; removes a named constraint. (MySQL supports DROP
-- CONSTRAINT from version 8.0.19; older tutorials use DROP CHECK, DROP INDEX, or DROP FOREIGN KEY
-- instead.)

-- > Watch out: MySQL won't rename or drop a column that a CHECK rule uses. In MySQL, renaming or
-- dropping a column mentioned in a CHECK constraint fails with error 3959 ("Check constraint …
-- uses column …, hence column cannot be dropped or renamed"). Drop the constraint, change the
-- column, then add the constraint again with the new column name. PostgreSQL updates the
-- constraint for you. Exercise 26 walks through both.

-- Here's the finished suppliers table:

-- PostgreSQL:

SELECT column_name, data_type, character_maximum_length AS max_length, is_nullable
FROM information_schema.columns
WHERE table_name = 'suppliers'
ORDER BY ordinal_position;

/* The chapter shows:
     column_name  |     data_type     | max_length | is_nullable
   ---------------+-------------------+------------+-------------
    supplier_id   | integer           |            | NO
    supplier_name | character varying |        100 | NO
    city          | character varying |         80 | YES
    email         | character varying |        100 | NO
    rating        | smallint          |            | YES
    is_active     | boolean           |            | NO
    onboarded_on  | date              |            | NO
    gst_number    | character varying |         15 | YES
   (8 rows)
*/


-- fax_number is gone, contact_email is now a required email, city is wider, and gst_number is new
-- and unique. The six suppliers and their data came through every change.

-- =============================================================================================
-- Step 10: Rename tables and organize them
-- =============================================================================================

-- Rename a table. Give the backup a name that says when it was taken. Same in both:

ALTER TABLE suppliers_backup RENAME TO suppliers_backup_2026_03_31;


-- (MySQL also offers RENAME TABLE old_name TO new_name;, which can rename several tables at once.)

-- List the tables in the database. PostgreSQL:

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

/* The chapter shows:
            table_name
   -----------------------------
    purchase_orders
    suppliers
    suppliers_backup_2026_03_31
   (3 rows)
*/


-- MySQL: SHOW TABLES; gives the same three names.

-- Schemas: folders for tables. Backup copies clutter the list. The two databases organize tables
-- differently:

-- - In PostgreSQL, a database contains schemas, and schemas contain tables. Every new database
-- starts with a schema called public, which is where your tables have been going. You can create
-- more schemas as folders, such as staging, reporting, or archive, and refer to a table in one as
-- schema_name.table_name. - In MySQL, a schema is a database (section 12.3), so the equivalent
-- folder is simply another database.

-- Move the backup into an archive. PostgreSQL:

CREATE SCHEMA archive;
ALTER TABLE suppliers_backup_2026_03_31 SET SCHEMA archive;
SELECT COUNT(*) AS archived_rows FROM archive.suppliers_backup_2026_03_31;

/* The chapter shows:
    archived_rows
   ---------------
                6
   (1 row)
*/


-- Data warehouses use schemas heavily: raw data lands in one schema, cleaned tables live in
-- another, and reports read from a third. You'll see that layout in Chapter 32.

-- =============================================================================================
-- Step 11: Empty and remove: TRUNCATE, DROP TABLE, DROP DATABASE
-- =============================================================================================

-- Three statements remove data, and they're easy to confuse:

-- | Statement | Removes | Structure afterwards | Can use WHERE? | Speed on big tables | Undo |
-- |---|---|---|---|---|---| | DELETE FROM t WHERE … | the matching rows (all rows without WHERE) |
-- table stays | yes | slow: row by row | inside a transaction, in both databases | | TRUNCATE
-- TABLE t | every row | table stays, empty | no | very fast | PostgreSQL: inside a transaction;
-- MySQL: no (implicit commit) | | DROP TABLE t | the rows and the table itself | gone | no | fast
-- | PostgreSQL: inside a transaction; MySQL: no |

-- TRUNCATE is the tool for staging tables: a table you empty and reload every day with fresh data.
-- Try all three on a throwaway copy. Same in both:

CREATE TABLE po_import_staging AS
SELECT * FROM purchase_orders;


TRUNCATE TABLE po_import_staging;


SELECT COUNT(*) AS rows_left FROM po_import_staging;

/* The chapter shows:
    rows_left
   -----------
            0
   (1 row)
*/


DROP TABLE po_import_staging;


-- Dropping a table that others depend on. Try to drop suppliers:

DROP TABLE suppliers;


-- The foreign key protects you again. You have two options:

-- 1. Drop the child table first, then the parent. This is the clean way, and it works the same in
-- both databases. 2. PostgreSQL only: DROP TABLE suppliers CASCADE; Read the hint carefully:
-- CASCADE drops the dependent objects, which here is the foreign key constraint on
-- purchase_orders, not the purchase_orders table. The orders survive with no link to any supplier,
-- which is rarely what you want. Treat CASCADE as a statement to double-check, never a shortcut to
-- make an error disappear.

-- Take the clean route. IF EXISTS makes a cleanup script safe to run even if a table is already
-- gone:

DROP TABLE IF EXISTS purchase_orders;
DROP TABLE IF EXISTS suppliers;


-- Removing the archive. A PostgreSQL schema must be empty before DROP SCHEMA, unless you add
-- CASCADE, which here really does delete every table inside it:

DROP SCHEMA archive CASCADE;


-- In MySQL it runs from anywhere. In PostgreSQL you can't drop the database you're connected to
-- ("cannot drop the currently open database"), so connect to another database, such as postgres,
-- first. If other sessions are still connected, PostgreSQL 13 and later accept DROP DATABASE
-- riverstone_lab WITH (FORCE);, which disconnects them. On a shared server, that's a statement to
-- run only when you're certain.

-- > Watch out: DROP is instant and final. There's no recycle bin. On a real system, DROP TABLE or
-- DROP DATABASE without a tested backup can mean restoring from last night's backup and losing a
-- day's work, if a backup exists at all. Many companies don't give analysts DROP rights on shared
-- databases for exactly this reason.

-- =============================================================================================
-- Real-life example: changing a live table safely
-- =============================================================================================

-- Six months later, purchasing asks you to add a required payment_terms_days column to the real
-- suppliers table, which the ordering app uses all day. The SQL is one line. The job is the
-- checklist around it:

-- 1. Agree the change in writing: the column name, type, default (say, 30 days), and who asked for
-- it. 2. Find everything that depends on the table: reports, dashboards, the ordering app,
-- scheduled jobs. Tell their owners. 3. Back up the table (a copy or a database backup), and know
-- how you'd restore it. 4. Write the change as a script, including a second "undo" script (for
-- example, DROP COLUMN payment_terms_days), and run both on a copy of the database first. 5. Add
-- columns in a way that doesn't break existing inserts: a new NOT NULL column needs a DEFAULT, or
-- every program that doesn't know about it will start failing. 6. Run it at a quiet time. On very
-- large tables some changes lock the table while they work, and users' screens freeze. How long
-- depends on the change and the database version, so test on a copy of realistic size. 7. Check
-- afterwards: describe the table, count the rows, run the reports. 8. Save the script in version
-- control (Chapter 26). Teams that change databases often use migration tools, which keep every
-- structure change as a numbered, reviewed script and apply them in order to every environment.
-- You'll meet them in Chapter 28.

-- For the lab, Steps 1–11 were enough. For production, the checklist is the skill.

-- =============================================================================================
-- Cheat sheet: building and changing, PostgreSQL vs MySQL
-- =============================================================================================

-- Entries that start with a backslash (\c, \l, \dt, \d, \copy) work only in PostgreSQL's command-
-- line client, psql, which you'll be able to use after Chapter 26; everything else runs in
-- DBeaver.

-- | Task | PostgreSQL | MySQL | |---|---|---| | Create a database | CREATE DATABASE db; | CREATE
-- DATABASE db; (IF NOT EXISTS allowed) | | Switch to it | new connection, or \c db in psql | USE
-- db; | | List databases | SELECT datname FROM pg_database; or \l | SHOW DATABASES; | | List
-- tables | information_schema.tables or \dt | SHOW TABLES; | | Describe a table |
-- information_schema.columns or \d t | DESCRIBE t; / SHOW CREATE TABLE t; | | Automatic ID |
-- INTEGER GENERATED ALWAYS AS IDENTITY | INT AUTO_INCREMENT | | Foreign key | FOREIGN KEY (col)
-- REFERENCES parent (col) | same (use this form; inline REFERENCES is ignored before 9.0) | |
-- Insert rows | INSERT INTO t (cols) VALUES (…), (…); | same | | ID of the new row | … RETURNING
-- id; | SELECT LAST_INSERT_ID(); | | Load a CSV | \copy t FROM 'file.csv' WITH (FORMAT csv, HEADER
-- true) | LOAD DATA LOCAL INFILE 'file.csv' INTO TABLE t … | | Update rows | UPDATE t SET col =
-- val WHERE …; | same | | Update using another table | UPDATE t SET … FROM other WHERE … | UPDATE
-- t JOIN other ON … SET … WHERE … | | Delete rows | DELETE FROM t WHERE …; | same | | Upsert |
-- INSERT … ON CONFLICT (col) DO UPDATE SET col = EXCLUDED.col | INSERT … AS new ON DUPLICATE KEY
-- UPDATE col = new.col | | Start a transaction | BEGIN; | START TRANSACTION; (or BEGIN;) | | Can
-- ROLLBACK undo ALTER/DROP? | yes | no: structure changes commit immediately | | Copy a table with
-- its data | CREATE TABLE copy AS SELECT * FROM t; | same | | Add a column | ALTER TABLE t ADD
-- COLUMN col type; | same | | Rename a column | ALTER TABLE t RENAME COLUMN a TO b; | same (8.0+);
-- drop any CHECK on it first | | Drop a column | ALTER TABLE t DROP COLUMN col; | same | | Change
-- a column's type | ALTER TABLE t ALTER COLUMN col TYPE newtype; | ALTER TABLE t MODIFY COLUMN col
-- newtype NOT NULL DEFAULT …; (restate everything) | | Make required / optional | ALTER COLUMN col
-- SET NOT NULL / DROP NOT NULL | MODIFY COLUMN col type NOT NULL / NULL | | Set / remove a default
-- | ALTER COLUMN col SET DEFAULT val / DROP DEFAULT | same | | Add / drop a constraint | ADD
-- CONSTRAINT name … / DROP CONSTRAINT name | same (DROP CONSTRAINT from 8.0.19) | | Rename a table
-- | ALTER TABLE t RENAME TO new; | same, or RENAME TABLE t TO new; | | Folders for tables | CREATE
-- SCHEMA s; / ALTER TABLE t SET SCHEMA s; | another database / RENAME TABLE db1.t TO db2.t; | |
-- Empty a table | TRUNCATE TABLE t; | same | | Remove a table | DROP TABLE IF EXISTS t; | same | |
-- Rename a database | ALTER DATABASE a RENAME TO b; (nobody connected) | not supported: create
-- new, move tables | | Remove a database | DROP DATABASE IF EXISTS db; (connect elsewhere first) |
-- DROP DATABASE IF EXISTS db; |

-- Good place to stop.

-- ---

-- =============================================================================================
-- 12.14 Writing SQL that humans can read
-- =============================================================================================

-- A query is read far more often than it's written: by your reviewer, by the colleague who
-- inherits your report, by you in six months. Readable SQL is also correct SQL more often, because
-- mistakes have fewer places to hide.

-- Compare:

select c.city,count(distinct o.order_id),sum(oi.quantity*oi.unit_price*(1-oi.discount_pct/100)) from orders o join customers c on o.customer_id=c.customer_id join order_items oi on o.order_id=oi.order_id where o.status<>'Cancelled' group by c.city order by 3 desc


-- with the version in section 12.10. Same logic. One of them you can review in ten seconds.

-- A simple style guide:

-- 1. Capitalize keywords (SELECT, FROM, JOIN); keep table and column names lower-case. 2. One
-- major clause per line, and one column per line when there are more than two or three. 3. Indent
-- join conditions and subqueries. 4. Alias every calculated column with a clear business name
-- (net_revenue, not x or sum). 5. Use meaningful table aliases (c for customers, oi for
-- order_items), and prefix every column in a multi-table query. 6. Name columns in ORDER BY and
-- GROUP BY rather than using position numbers like ORDER BY 3; numbers break silently when someone
-- reorders the SELECT. 7. Comment the why, not the what: -- exclude cancelled orders: finance
-- counts revenue on delivery or shipment. 8. Name tables and columns in snake_case: lower-case
-- words joined by underscores.

-- Teams often adopt a published SQL style guide and enforce it with an automatic formatter
-- ("linter"). You'll meet that in Chapter 32.

-- ---

-- =============================================================================================
-- 12.15 Putting it all together: Tuesday morning with the sales head
-- =============================================================================================

-- It's Tuesday, 31 March 2026, the last day of the quarter. Before the 10 a.m. review, Anita Rao,
-- Riverstone's Sales Head, sends you five questions. None of them mentions SQL. This is what real
-- analysis work looks like, so we'll answer each one the way an experienced analyst would, with a
-- method rather than guesswork.

-- =============================================================================================
-- A six-step method for any business question
-- =============================================================================================

-- 1. Restate the question precisely. What exactly is being counted? As of when? Which records are
-- included or excluded (cancelled orders, unpaid invoices)? Write the business rules down. 2.
-- Decide the shape of the answer. What does one row of the result represent: one customer, one
-- month, one invoice? Which columns will the reader need? 3. Find the tables. Which tables hold
-- each piece? What is the grain (one row = what?) of each? 4. Plan the joins. Which keys connect
-- them? Inner or left join? Will any join multiply rows (fan-out)? 5. Build in small steps. Start
-- with one table, add one join at a time, then filters, then grouping. Run the query after every
-- step and check the row count. 6. Check the answer. Hand-check one row. Reconcile a total to a
-- number you already trust. Then ask: does this make business sense?

-- =============================================================================================
-- Question 1: "Which customers have gone quiet?"
-- =============================================================================================

-- Restate. Customers with no (non-cancelled) order in March 2026, meaning nothing since 1 March.
-- Cancelled orders don't count as activity. Customers who have never ordered must be included,
-- because they're the easiest to miss.

-- Shape. One row per customer: name, segment, last order date, days since that order.

-- Tables and joins. customers and orders. It must be a left join, or never-ordered customers
-- disappear. The "not cancelled" rule goes in the ON clause, for the reason you saw in section
-- 12.10.

-- Filter. "Last order before 1 March" is a condition on MAX(order_date), an aggregate, so it
-- belongs in HAVING, not WHERE.

SELECT c.customer_name,
       c.segment,
       MAX(o.order_date)                     AS last_order_date,
       DATE '2026-03-31' - MAX(o.order_date) AS days_since_last_order
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name, c.segment
HAVING MAX(o.order_date) < DATE '2026-03-01'
    OR MAX(o.order_date) IS NULL
ORDER BY last_order_date NULLS FIRST;

/* The chapter shows:
        customer_name      |   segment   | last_order_date | days_since_last_order
   ------------------------+-------------+-----------------+-----------------------
    Blue Bay Cafe          | Hospitality |                 |
    Patel Kitchenware      | Retail      | 2026-01-14      |                    76
    Coastal Foods          | Wholesale   | 2026-02-11      |                    48
    Sunrise Caterers       | Hospitality | 2026-02-19      |                    40
    Northgate Distributors | Wholesale   | 2026-02-25      |                    34
   (5 rows)
*/


-- How it works. GROUP BY c.customer_id, … makes one group per customer (grouping by the ID as well
-- as the name protects against two customers sharing a name). MAX(o.order_date) finds each
-- customer's latest valid order; for Blue Bay Cafe there are no matching orders, so it's NULL.
-- HAVING … OR MAX(o.order_date) IS NULL keeps the never-ordered customers, because "NULL < 1
-- March" is unknown, not true (section 12.7). NULLS FIRST puts them at the top.

-- Check. Green Leaf Hotels isn't listed. Its January order was cancelled, but it ordered again on
-- 3 March, so it's active. ✓ Sharma Hardware (10 March) and Metro Mart (15 March) are active too.
-- ✓

-- What to tell Anita. Five of eight customers haven't ordered this month. Blue Bay Cafe signed up
-- on 1 March and has never ordered: a warm lead to call today. Patel Kitchenware has gone 76 days,
-- far longer than any other customer.

-- > Back to Chapter 7. Section 7.6 showed a data analyst answering the same question on a full
-- year of data: every customer with no non-cancelled order in the 60 days to 31 December 2025,
-- which found five customers. It was this query with two dates changed, run on the one-year
-- database. Exercise 30 asks you to write it. Chapter 13 then improves the rule itself, comparing
-- each customer's silence with their own usual ordering rhythm (Pattern 6).

-- =============================================================================================
-- Question 2: "How much are discounts costing us?"
-- =============================================================================================

-- Restate. For non-cancelled orders, compare the value of the goods before discount, at the price
-- charged (the gross value), with the discount given, by category. We use the price on the order
-- line, not today's list price in products, for the reason in section 12.2: the price charged is
-- what the customer was offered.

-- Shape. One row per category. Tables: order_items (quantities, prices, discounts), products
-- (category), orders (status). Every join goes from a line to its one order and one product, so
-- nothing fans out.

SELECT p.category,
       ROUND(SUM(oi.quantity * oi.unit_price), 0)                           AS gross_value,
       ROUND(SUM(oi.quantity * oi.unit_price * oi.discount_pct / 100), 0)   AS discount_given,
       ROUND(100.0 * SUM(oi.quantity * oi.unit_price * oi.discount_pct / 100)
             / SUM(oi.quantity * oi.unit_price), 1)                         AS discount_pct_of_gross
FROM order_items AS oi
JOIN orders   AS o ON oi.order_id   = o.order_id
JOIN products AS p ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY discount_given DESC;

/* The chapter shows:
     category  | gross_value | discount_given | discount_pct_of_gross
   ------------+-------------+----------------+-----------------------
    Industrial |      181250 |          19865 |                  11.0
    Storage    |       85050 |           3240 |                   3.8
    Kitchen    |       82850 |           2115 |                   2.6
   (3 rows)
*/


-- Check. Gross value minus discount should equal the net revenue from section 12.10's profit
-- query: for Industrial, ₹1,81,250 − ₹19,865 = ₹1,61,385. ✓

-- What to tell Anita. Riverstone gave away ₹19,865 on crates this quarter, 11% of their value,
-- against under 4% elsewhere. Put that next to the gross profit query from section 12.10: crates
-- earned only ₹23,885 of gross profit. The discounts on crates were worth about 83% of the profit
-- the crates actually made. That's a finding worth a meeting.

-- =============================================================================================
-- Question 3: "Who owes us money, and how late is it?"
-- =============================================================================================

-- This is the classic receivables ageing report, and it pulls together almost everything in this
-- chapter.

-- Restate. As of 31 March 2026, for each customer: the total unpaid balance, split by how overdue
-- it is (not yet due, 1–30, 31–60, 60+ days past the due date). Only invoices with money still
-- owed.

-- Shape. One row per customer, with one column per ageing band.

-- Tables and grain. invoices (one row per invoice), payments (one row per payment, many per
-- invoice), orders (to reach the customer), customers (names). The payments join would fan out, so
-- payments must be summed per invoice first.

-- Build in steps. First, the balance for every invoice:

SELECT i.invoice_id,
       i.amount,
       COALESCE(pay.paid, 0.00)            AS paid,
       i.amount - COALESCE(pay.paid, 0.00) AS balance
FROM invoices AS i
LEFT JOIN (
    SELECT invoice_id, SUM(amount) AS paid
    FROM payments
    GROUP BY invoice_id
) AS pay ON i.invoice_id = pay.invoice_id
ORDER BY i.invoice_id;

/* The chapter shows:
    invoice_id |  amount  |   paid   | balance
   ------------+----------+----------+----------
          9001 | 14700.00 | 14700.00 |     0.00
          9002 | 73260.00 | 73260.00 |     0.00
          9003 | 16250.00 | 10000.00 |  6250.00
          9004 | 14550.00 | 14550.00 |     0.00
          9005 | 14640.00 | 14640.00 |     0.00
          9006 | 32625.00 | 20000.00 | 12625.00
          9007 | 23325.00 |     0.00 | 23325.00
          9008 | 76560.00 | 30000.00 | 46560.00
          9009 | 20100.00 | 20100.00 |     0.00
          9010 | 11700.00 |     0.00 | 11700.00
   (10 rows)
*/


-- Invoice 9001, which section 12.8 wrongly flagged as overdue, now correctly shows a zero balance.
-- Next, wrap that result as a derived table, join it to orders and customers, and use conditional
-- aggregation (section 12.9) to spread balances into ageing columns:

SELECT c.customer_name,
       SUM(inv.balance) AS total_due,
       SUM(CASE WHEN inv.due_date >= DATE '2026-03-31' THEN inv.balance ELSE 0.00 END) AS not_yet_due,
       SUM(CASE WHEN inv.due_date <  DATE '2026-03-31'
                 AND DATE '2026-03-31' - inv.due_date <= 30 THEN inv.balance ELSE 0.00 END) AS overdue_1_30,
       SUM(CASE WHEN DATE '2026-03-31' - inv.due_date BETWEEN 31 AND 60 THEN inv.balance ELSE 0.00 END) AS overdue_31_60,
       SUM(CASE WHEN DATE '2026-03-31' - inv.due_date > 60 THEN inv.balance ELSE 0.00 END) AS overdue_60_plus
FROM (
    SELECT i.invoice_id, i.order_id, i.due_date,
           i.amount - COALESCE(pay.paid, 0) AS balance
    FROM invoices AS i
    LEFT JOIN (SELECT invoice_id, SUM(amount) AS paid FROM payments GROUP BY invoice_id) AS pay
           ON i.invoice_id = pay.invoice_id
) AS inv
JOIN orders    AS o ON inv.order_id  = o.order_id
JOIN customers AS c ON o.customer_id = c.customer_id
WHERE inv.balance > 0
GROUP BY c.customer_id, c.customer_name
ORDER BY total_due DESC;

/* The chapter shows:
        customer_name      | total_due | not_yet_due | overdue_1_30 | overdue_31_60 | overdue_60_plus
   ------------------------+-----------+-------------+--------------+---------------+-----------------
    Northgate Distributors |  46560.00 |        0.00 |     46560.00 |          0.00 |            0.00
    Sunrise Caterers       |  23325.00 |        0.00 |     23325.00 |          0.00 |            0.00
    Coastal Foods          |  12625.00 |        0.00 |     12625.00 |          0.00 |            0.00
    Sharma Hardware        |  11700.00 |    11700.00 |         0.00 |          0.00 |            0.00
    Patel Kitchenware      |   6250.00 |        0.00 |         0.00 |       6250.00 |            0.00
   (5 rows)
*/


-- How it works.

-- - The innermost subquery totals payments per invoice (the fan-out fix). The next layer computes
-- each invoice's balance. The outer query joins balances to customers and aggregates. - WHERE
-- inv.balance > 0 removes fully paid invoices before grouping. - Each SUM(CASE WHEN … THEN
-- inv.balance ELSE 0.00 END) adds up only the balances that fall into one ageing band. Five CASE
-- columns turn one list of invoices into a five-column report, the same result you'd build with a
-- pivot table in Chapter 11. - Each column is its own CASE, so there's no "first match wins"
-- across columns, as there was in section 12.8's single CASE. That's why every band states both
-- its limits (the 1–30 column checks that the invoice is past due and at most 30 days late):
-- otherwise an invoice could be counted in two columns. - ELSE 0.00 (rather than leaving out the
-- ELSE) makes empty bands show zero instead of NULL, which matters when someone totals the columns
-- in Excel. - GROUP BY c.customer_id, c.customer_name groups by the ID as well as the name, as in
-- Question 1.

-- Check. The total_due column adds up to 46,560 + 23,325 + 12,625 + 11,700 + 6,250 = ₹1,00,460,
-- exactly the outstanding total from the fan-out fix in section 12.12. ✓ And each row's bands add
-- up to its total. ✓

-- What to tell Anita. ₹88,760 is overdue, and more than half of it is Northgate Distributors
-- (₹46,560). Northgate is also on the "gone quiet" list from Question 1, so before sales chases
-- them for a new order, finance should chase the old one. Sunrise Caterers hasn't paid anything,
-- has no city recorded, and has no sales rep assigned: a credit risk and a data-quality problem at
-- the same time.

-- =============================================================================================
-- Question 4: "How is each sales rep doing, and who do they report to?"
-- =============================================================================================

-- Restate. For each sales rep: number of orders and net revenue on non-cancelled orders, with
-- their manager's name.

-- Tables and joins. employees twice (the rep, and the rep's manager, a self-join), orders,
-- order_items. The manager join is a left join, so a rep with no manager still appears.

SELECT e.employee_name                         AS sales_rep,
       COALESCE(m.employee_name, '(none)')     AS reports_to,
       COUNT(DISTINCT o.order_id)              AS orders,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue
FROM employees AS e
LEFT JOIN employees   AS m  ON e.manager_id   = m.employee_id
JOIN      orders      AS o  ON o.sales_rep_id = e.employee_id
JOIN      order_items AS oi ON oi.order_id    = o.order_id
WHERE o.status <> 'Cancelled'
GROUP BY e.employee_id, e.employee_name, m.employee_name
ORDER BY net_revenue DESC;

/* The chapter shows:
      sales_rep   |  reports_to  | orders | net_revenue
   ---------------+--------------+--------+-------------
    Rahul Mehta   | Vikram Singh |      4 |      146745
    Farah Khan    | Anita Rao    |      2 |       96660
    Neha Kulkarni | Vikram Singh |      4 |       57200
   (3 rows)
*/


-- How it works. COUNT(DISTINCT o.order_id) avoids the fan-out from joining to order lines. Both
-- names are in GROUP BY because both appear in SELECT, and e.employee_id is there too, so two reps
-- with the same name would stay apart. Anita Rao and Vikram Singh don't appear as reps because
-- they have no orders of their own; the inner join to orders removes them, which is what this
-- question wants.

-- Check. The three reps total ₹3,00,605. Order 5008 has no rep and is worth ₹23,325. 3,00,605 +
-- 23,325 = ₹3,23,930, exactly the total non-cancelled revenue. ✓ Reconciling to a known total is
-- how you prove a report hasn't lost anything. Mention the unassigned ₹23,325 in a footnote so
-- nobody wonders where it went.

-- What to tell Anita. Rahul Mehta leads on revenue with ₹1,46,745, largely from two big Coastal
-- Foods orders. Neha Kulkarni handled as many orders but at a much smaller average size, which is
-- worth understanding before judging performance. Ranking reps, showing each one's share of team
-- revenue, and comparing this quarter with last all need window functions, the headline tool of
-- Chapter 13.

-- =============================================================================================
-- Question 5: "Why did March fall?"
-- =============================================================================================

-- Chapter 5 asked this question and answered it with an issue tree, using numbers from this mini
-- database. Every one of those numbers is a short query you can now write yourself. Here is the
-- walk-through again, as SQL.

-- Restate. Chapter 5 measured billed revenue: invoices, by invoice date. That's a business rule,
-- so write it down. (The monthly report in "In the real world", later in this chapter, uses a
-- different rule, orders by order date. On this data both give ₹31,800 for March, but in general
-- they differ.)

-- Step 1. Split with a formula. Billed revenue = number of invoices × average invoice:

SELECT DATE_TRUNC('month', invoice_date)::date AS month,
       COUNT(*)                                AS invoices,
       SUM(amount)                             AS billed,
       ROUND(AVG(amount), 0)                   AS avg_invoice
FROM invoices
WHERE invoice_date >= DATE '2026-02-01'
GROUP BY DATE_TRUNC('month', invoice_date)
ORDER BY month;

/* The chapter shows:
      month    | invoices |  billed   | avg_invoice
   ------------+----------+-----------+-------------
    2026-02-01 |        5 | 161700.00 |       32340
    2026-03-01 |        2 |  31800.00 |       15900
   (2 rows)
*/


-- February: 5 invoices averaging ₹32,340, ₹1,61,700 in all. March: 2 averaging ₹15,900, ₹31,800.
-- The same numbers as Chapter 5. The split of the ₹1,29,900 fall is arithmetic, done by hand
-- exactly as there: at February's average, March's 2 invoices would have brought ₹64,680, so fewer
-- invoices explain ₹1,61,700 − ₹64,680 = ₹97,020, and smaller invoices the other ₹64,680 − ₹31,800
-- = ₹32,880. ✓ ₹97,020 + ₹32,880 = ₹1,29,900.

-- Step 2. Which customers stopped? Customers invoiced in February, EXCEPT those with a non-
-- cancelled order in March:

SELECT c.customer_name
FROM customers AS c
JOIN orders   AS o ON c.customer_id = o.customer_id
JOIN invoices AS i ON i.order_id    = o.order_id
WHERE i.invoice_date >= DATE '2026-02-01'
  AND i.invoice_date <  DATE '2026-03-01'
EXCEPT
SELECT c.customer_name
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.order_date >= DATE '2026-03-01'
  AND o.order_date <  DATE '2026-04-01'
  AND o.status <> 'Cancelled'
ORDER BY customer_name;

/* The chapter shows:
        customer_name
   ------------------------
    Coastal Foods
    Northgate Distributors
    Sunrise Caterers
   (3 rows)
*/


-- Coastal Foods, Northgate Distributors, and Sunrise Caterers: the three from Chapter 5. ✓ A
-- tempting shortcut gets this wrong. Take away the customers invoiced in March instead:

SELECT c.customer_name
FROM customers AS c
JOIN orders   AS o ON c.customer_id = o.customer_id
JOIN invoices AS i ON i.order_id    = o.order_id
WHERE i.invoice_date >= DATE '2026-02-01'
  AND i.invoice_date <  DATE '2026-03-01'
EXCEPT
SELECT c.customer_name
FROM customers AS c
JOIN orders   AS o ON c.customer_id = o.customer_id
JOIN invoices AS i ON i.order_id    = o.order_id
WHERE i.invoice_date >= DATE '2026-03-01'
  AND i.invoice_date <  DATE '2026-04-01'
ORDER BY customer_name;

/* The chapter shows:
        customer_name
   ------------------------
    Coastal Foods
    Metro Mart
    Northgate Distributors
    Sunrise Caterers
   (4 rows)
*/


-- Four customers, and Metro Mart is wrong: it did order in March; the order just isn't billed yet.
-- "Didn't reorder" is a question about orders, so the second half must look at orders.

-- Step 3. Booked, not billed. Which non-cancelled orders have no invoice? An anti-join (section
-- 12.10), with each order's revenue:

SELECT o.order_id,
       o.order_date,
       o.status,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS order_revenue
FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.order_id
LEFT JOIN invoices AS i ON i.order_id = o.order_id
WHERE i.invoice_id IS NULL
  AND o.status <> 'Cancelled'
GROUP BY o.order_id, o.order_date, o.status;

/* The chapter shows:
    order_id | order_date | status  | order_revenue
   ----------+------------+---------+---------------
        5012 | 2026-03-15 | Pending |         26220
   (1 row)
*/


-- Metro Mart's order 5012, ₹26,220, still Pending. Billed, March would be ₹31,800 + ₹26,220 =
-- ₹58,020, as Chapter 5 said. ✓

-- Step 4. The wholesale mix. How much of February's billing came from wholesale customers?
-- Conditional aggregation (section 12.9):

SELECT SUM(i.amount)                                                   AS billed,
       SUM(CASE WHEN c.segment = 'Wholesale' THEN i.amount ELSE 0 END) AS wholesale,
       ROUND(100.0 * SUM(CASE WHEN c.segment = 'Wholesale' THEN i.amount ELSE 0 END)
             / SUM(i.amount), 1)                                       AS wholesale_pct
FROM invoices AS i
JOIN orders    AS o ON o.order_id    = i.order_id
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE i.invoice_date >= DATE '2026-02-01'
  AND i.invoice_date <  DATE '2026-03-01';

/* The chapter shows:
     billed   | wholesale | wholesale_pct
   -----------+-----------+---------------
    161700.00 | 109185.00 |          67.5
   (1 row)
*/


-- ₹1,09,185 of ₹1,61,700, 67.5%, from two wholesale orders. ✓

-- Step 5. Did they stop ordering, and do they owe money? Reuse Question 3's balance for each
-- invoice, add it up per customer, and add a yes/no column with EXISTS: is there a non-cancelled
-- March order for this customer? An EXISTS (…) in the SELECT list gives true or false for each
-- row; it's the same test you used in WHERE in section 12.12.

SELECT c.customer_name,
       EXISTS (SELECT 1
               FROM orders AS m
               WHERE m.customer_id = c.customer_id
                 AND m.order_date >= DATE '2026-03-01'
                 AND m.status <> 'Cancelled')           AS ordered_in_march,
       COALESCE(SUM(inv.balance), 0.00)                 AS owed,
       SUM(CASE WHEN inv.due_date < DATE '2026-03-31'
                THEN inv.balance ELSE 0.00 END)          AS overdue
FROM customers AS c
JOIN orders AS o ON o.customer_id = c.customer_id
LEFT JOIN (
    SELECT i.order_id, i.due_date,
           i.amount - COALESCE(pay.paid, 0) AS balance
    FROM invoices AS i
    LEFT JOIN (SELECT invoice_id, SUM(amount) AS paid
               FROM payments
               GROUP BY invoice_id) AS pay
           ON i.invoice_id = pay.invoice_id
) AS inv ON inv.order_id = o.order_id
GROUP BY c.customer_id, c.customer_name
ORDER BY overdue DESC, owed DESC, c.customer_name;

/* The chapter shows:
        customer_name      | ordered_in_march |   owed   | overdue
   ------------------------+------------------+----------+----------
    Northgate Distributors | f                | 46560.00 | 46560.00
    Sunrise Caterers       | f                | 23325.00 | 23325.00
    Coastal Foods          | f                | 12625.00 | 12625.00
    Patel Kitchenware      | f                |  6250.00 |  6250.00
    Sharma Hardware        | t                | 11700.00 |     0.00
    Green Leaf Hotels      | t                |     0.00 |     0.00
    Metro Mart             | t                |     0.00 |     0.00
   (7 rows)
*/


-- Chapter 5's seven-row table, row for row. ✓ ordered_in_march shows t (true) or f (false). The
-- joins start from orders, so Blue Bay Cafe, which has never ordered, isn't listed, and SUM(CASE …
-- ELSE 0.00 END) counts a balance as overdue only when its due date has passed.

-- What the data can't answer. As in Chapter 5, the queries stop at what happened. Whether March is
-- always slow needs last year's March, which the mini database doesn't have; whether a competitor
-- is involved needs a phone call. The overdue pattern in step 5 is a hypothesis to test with the
-- customers, not a cause.

-- > Watch out: billed revenue and order revenue are different rules. Billed revenue counts
-- invoices by invoice date; order revenue counts orders by order date and status. An order placed
-- on 28 February and invoiced on 2 March lands in different months under the two rules. Say which
-- one you report, every time.

-- =============================================================================================
-- What just happened
-- =============================================================================================

-- Five questions, a handful of queries, and each answer came with a number and a reason to act.
-- None of the SQL was new; every piece came from sections 12.4 to 12.12. What made the difference
-- was the method: restating the question, knowing the grain of each table, choosing joins
-- deliberately, building in steps, and checking every result against something you already
-- trusted. That habit, far more than syntax, is what makes an analyst trusted.

-- =============================================================================================
-- 12.16 The same SQL in MySQL
-- =============================================================================================

-- Everything you've learned in this chapter works in MySQL: tables and keys, SELECT, WHERE, NULL
-- logic, CASE, aggregates, GROUP BY and HAVING, every kind of join except one, subqueries, UNION,
-- and transactions. The companion file ch12_queries_mysql.sql contains every query in this chapter
-- rewritten for MySQL, and each one was run against riverstone_setup_mysql.sql and checked against
-- the PostgreSQL result: the answers are identical.

-- (Section 12.13 already compared, side by side, the statements that create, change, and remove
-- databases and tables; the table below repeats the most important of those differences.) What
-- changes is a short list of spellings, and a shorter list of behaviors. The spellings are easy:
-- MySQL tells you with an error. The behaviors are the dangerous part, because MySQL quietly
-- returns a different answer. This section covers both.

-- =============================================================================================
-- The differences that matter in this chapter
-- =============================================================================================

-- | Task | PostgreSQL (this chapter) | MySQL | |---|---|---| | Days between two dates | DATE
-- '2026-03-31' - due_date | DATEDIFF(DATE '2026-03-31', due_date) | | Start of the month |
-- DATE_TRUNC('month', order_date)::date | CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) | |
-- Convert a type | value::date or CAST(value AS DATE) | CAST(value AS DATE) only | | Join text | a
-- \|\| b or CONCAT(a, b) | CONCAT(a, b) only | | Case-insensitive match | LOWER(col) = 'x' or
-- ILIKE | = and LIKE already ignore case (default collation) | | Put NULLs first or last | ORDER
-- BY col NULLS FIRST / NULLS LAST | ORDER BY col IS NULL DESC, col / ORDER BY col IS NULL, col | |
-- NULLs in a plain ascending sort | last | first | | 7 / 2 | 3 (whole numbers) | 3.5000 (always
-- decimal); 7 DIV 2 gives 3 | | Keep every row from both tables | FULL OUTER JOIN | not supported;
-- LEFT JOIN … UNION ALL … RIGHT JOIN | | Start a transaction | BEGIN; | START TRANSACTION; (or
-- BEGIN;) | | Undo a structure change with ROLLBACK | works | doesn't: CREATE, ALTER, DROP,
-- TRUNCATE commit immediately | | Automatic ID column | GENERATED ALWAYS AS IDENTITY |
-- AUTO_INCREMENT | | Change a column's type | ALTER COLUMN col TYPE newtype | MODIFY COLUMN col
-- newtype … (restate NOT NULL and DEFAULT) | | Insert or update (upsert) | ON CONFLICT (col) DO
-- UPDATE | ON DUPLICATE KEY UPDATE | | Money type | NUMERIC(10,2) | DECIMAL(10,2) (NUMERIC also
-- accepted) | | Whole numbers | INTEGER | INT (INTEGER also accepted) | | A database vs. a schema
-- | a schema is a folder inside a database | SCHEMA and DATABASE mean the same thing |

-- Everything else in the chapter, including LIMIT, COALESCE, EXTRACT, COUNT(DISTINCT …), EXISTS,
-- UNION, INTERSECT, and EXCEPT (MySQL 8.0.31 and later), is written the same way.

-- =============================================================================================
-- Trap 1: subtracting dates gives a number, not days
-- =============================================================================================

-- In PostgreSQL, subtracting one date from another gives the number of days between them. MySQL
-- accepts exactly the same expression without complaint and returns something else:

SELECT DATE '2026-03-31' - DATE '2026-02-05'         AS looks_like_days,
       DATEDIFF(DATE '2026-03-31', DATE '2026-02-05') AS actual_days;

/* The chapter shows:
   +-----------------+-------------+
   | looks_like_days | actual_days |
   +-----------------+-------------+
   |             126 |          54 |
   +-----------------+-------------+
*/


-- MySQL turned both dates into the numbers 20260331 and 20260205 and subtracted them. There are 54
-- days between 5 February and 31 March, not 126. Imagine this inside the receivables ageing report
-- from section 12.15: invoices only a few weeks late would land in the "60+ days" column, and
-- finance would start chasing customers who aren't seriously late at all.

-- Rule for MySQL: count days with DATEDIFF(later_date, earlier_date), always. Notice the order of
-- the arguments: the later date comes first, just as it does in a subtraction.

-- Here is Question 1 from section 12.15, "Which customers have gone quiet?", in MySQL. Two lines
-- change: DATEDIFF replaces the subtraction, and the sort puts NULLs first by hand, because MySQL
-- has no NULLS FIRST.

SELECT c.customer_name,
       c.segment,
       MAX(o.order_date)                              AS last_order_date,
       DATEDIFF(DATE '2026-03-31', MAX(o.order_date)) AS days_since_last_order
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name, c.segment
HAVING MAX(o.order_date) < DATE '2026-03-01'
    OR MAX(o.order_date) IS NULL
ORDER BY last_order_date IS NULL DESC, last_order_date;

/* The chapter shows:
   +------------------------+-------------+-----------------+-----------------------+
   | customer_name          | segment     | last_order_date | days_since_last_order |
   +------------------------+-------------+-----------------+-----------------------+
   | Blue Bay Cafe          | Hospitality | NULL            |                  NULL |
   | Patel Kitchenware      | Retail      | 2026-01-14      |                    76 |
   | Coastal Foods          | Wholesale   | 2026-02-11      |                    48 |
   | Sunrise Caterers       | Hospitality | 2026-02-19      |                    40 |
   | Northgate Distributors | Wholesale   | 2026-02-25      |                    34 |
   +------------------------+-------------+-----------------+-----------------------+
*/


-- The same five customers, in the same order, with the same day counts as the PostgreSQL version.
-- Two details:

-- - How the sort works. last_order_date IS NULL is 1 (true) for Blue Bay Cafe and 0 (false) for
-- everyone else. Sorting that DESC puts the 1s first. The second sort column then orders the rest
-- by date. - How MySQL shows results. The MySQL command-line client draws borders with +, -, and
-- |, and prints missing values as the word NULL rather than a blank. DBeaver shows [NULL] in both
-- databases. It's still a missing value, not the text "NULL".

-- =============================================================================================
-- Trap 2: MySQL ignores capital letters when comparing text
-- =============================================================================================

-- Run the same query in both databases. PostgreSQL:

SELECT COUNT(*) AS delivered_orders
FROM orders
WHERE status = 'delivered';

/* The chapter shows:
    delivered_orders
   ------------------
                   0
   (1 row)
*/


-- MySQL:

SELECT COUNT(*) AS delivered_orders
FROM orders
WHERE status = 'delivered';

/* The chapter shows:
   +------------------+
   | delivered_orders |
   +------------------+
   |                8 |
   +------------------+
*/


-- PostgreSQL returns 0, because 'delivered' and 'Delivered' are different text. MySQL returns 8.
-- Its default collation (the rules for comparing text, section 12.3) is case-insensitive, and also
-- accent-insensitive, so 'cafe' matches 'Café' too.

-- That's often convenient: a user who types "mumbai" in a search box still finds Mumbai. But it
-- has real consequences:

-- - A query that works in MySQL can silently return nothing when moved to PostgreSQL, Snowflake,
-- or most other warehouses. When a company migrates its reports, this is one of the first things
-- to break. - Duplicate checks behave differently. In MySQL, GROUP BY email treats
-- Ravi@Example.com and ravi@example.com as one group, and a UNIQUE column won't accept both. In
-- PostgreSQL they're two. - When you really need an exact match in MySQL, such as for case-
-- sensitive codes or passwords, ask for a binary comparison, shown below.

-- COLLATE utf8mb4_bin compares the stored characters exactly:

SELECT COUNT(*) AS delivered_orders
FROM orders
WHERE status COLLATE utf8mb4_bin = 'delivered';

/* The chapter shows:
   +------------------+
   | delivered_orders |
   +------------------+
   |                0 |
   +------------------+
*/


-- Zero, like PostgreSQL.

-- Portable habit: match the stored capitalization exactly, or write LOWER(status) = 'delivered',
-- which gives the same answer in every database.

-- =============================================================================================
-- Trap 3: || means OR, not "join text"
-- =============================================================================================

SELECT 'Riverstone' || ' Supplies'      AS pipes,
       CONCAT('Riverstone', ' Supplies') AS concat_result;

/* The chapter shows:
   +-------+---------------------+
   | pipes | concat_result       |
   +-------+---------------------+
   |     0 | Riverstone Supplies |
   +-------+---------------------+
*/


-- In MySQL's default settings, || is an old synonym for OR. MySQL tried to treat both pieces of
-- text as true/false values and returned 0, with only a warning. Recent versions mark this use of
-- || as deprecated, but it still runs. In MySQL, join text with CONCAT, which also works in
-- PostgreSQL, SQL Server, Snowflake, and BigQuery.

-- =============================================================================================
-- Where NULLs sort
-- =============================================================================================

-- Section 12.5's DISTINCT query returns the same six rows in both databases, but PostgreSQL put
-- Sunrise Caterers' missing city last, and MySQL puts it first:

SELECT DISTINCT city
FROM customers
ORDER BY city;

/* The chapter shows:
   +-----------+
   | city      |
   +-----------+
   | NULL      |
   | Ahmedabad |
   | Chennai   |
   | Delhi     |
   | Mumbai    |
   | Pune      |
   +-----------+
*/


-- Neither is wrong; the SQL standard lets each database choose. It matters when a report takes
-- "the first row" or when two people compare exports line by line. To get PostgreSQL's order in
-- MySQL, write ORDER BY city IS NULL, city. Better still, decide where missing values belong and
-- say so explicitly in every database.

-- =============================================================================================
-- No FULL OUTER JOIN: reconciliation the MySQL way
-- =============================================================================================

-- Section 12.10 described FULL OUTER JOIN as the reconciliation tool. Here's a real use in
-- PostgreSQL: which orders have no invoice, and which invoices have no order?

SELECT o.order_id, o.status, i.invoice_id
FROM orders AS o
FULL OUTER JOIN invoices AS i ON o.order_id = i.order_id
WHERE o.order_id IS NULL OR i.invoice_id IS NULL
ORDER BY o.order_id;

/* The chapter shows:
    order_id |  status   | invoice_id
   ----------+-----------+------------
        5004 | Cancelled |
        5012 | Pending   |
   (2 rows)
*/


-- MySQL doesn't support FULL OUTER JOIN. Build it from its two halves: a left join that finds
-- orders with no invoice, stacked on a right join that finds invoices with no order.

SELECT o.order_id, o.status, i.invoice_id
FROM orders AS o
LEFT JOIN invoices AS i ON o.order_id = i.order_id
WHERE i.invoice_id IS NULL
UNION ALL
SELECT o.order_id, o.status, i.invoice_id
FROM orders AS o
RIGHT JOIN invoices AS i ON o.order_id = i.order_id
WHERE o.order_id IS NULL
ORDER BY order_id;

/* The chapter shows:
   +----------+-----------+------------+
   | order_id | status    | invoice_id |
   +----------+-----------+------------+
   |     5004 | Cancelled |       NULL |
   |     5012 | Pending   |       NULL |
   +----------+-----------+------------+
*/


-- The same answer. The cancelled order and the pending order have no invoice, which is correct,
-- and no invoice is orphaned. If an invoice with no matching order ever appeared here, it would
-- mean money billed against an order the sales system doesn't know about: exactly what an audit
-- wants to find.

-- Each half has its own WHERE, so the two halves can never return the same row, which is why UNION
-- ALL is safe (and faster than UNION). If you want all rows from both sides, not just the
-- unmatched ones, remove the first WHERE, keep the second, and still use UNION ALL: the second
-- half then adds only the rows the first half couldn't produce.

-- =============================================================================================
-- Habits that make your SQL portable
-- =============================================================================================

-- You'll probably work with more than one database in your career; many companies run MySQL for
-- their applications and copy the data into a warehouse for analysis. These habits make a query
-- move between them with the fewest surprises:

-- 1. Count days with a function (DATEDIFF in MySQL), never by subtracting dates. 2. Join text with
-- CONCAT. 3. Use CAST(x AS type), not ::. 4. Match text exactly, or use LOWER() on purpose. Never
-- rely on a database ignoring case. 5. Say where NULLs sort whenever the order of rows matters. 6.
-- Write 100.0 * in percentage calculations, so division behaves the same everywhere. 7. Keep every
-- non-aggregated column in GROUP BY, even if a database lets you skip it. 8. Before you trust a
-- result from an unfamiliar database, reconcile one total with a number you already know, exactly
-- as you did throughout section 12.15.

-- > Interview extra point. When asked "Which SQL databases have you used?", don't just list names.
-- Add one concrete difference you've handled: "Mostly PostgreSQL, and MySQL for our application
-- database. The thing I watch for in MySQL is date arithmetic: subtracting dates doesn't give
-- days, so I always use DATEDIFF. And its default collation ignores case, which changes how
-- duplicate checks behave." One specific, correct detail tells the interviewer you've actually
-- worked with the database, not just read its name. Chapter 69 explains this move, and Chapter 71
-- has more dialect questions.

-- ---

-- =============================================================================================
-- Common mistakes
-- =============================================================================================

-- | Mistake | Symptom | Fix | |---|---|---| | Mixing AND/OR without parentheses | Too many rows;
-- results include things you meant to exclude | Always bracket OR groups | | = NULL instead of IS
-- NULL | Zero rows, no error | Use IS NULL / IS NOT NULL | | <> filter on a column with NULLs |
-- Rows silently missing | Add OR col IS NULL, or COALESCE first | | Fan-out from joining a finer-
-- grain table | Counts and sums too high | Ask "what is one row?"; COUNT(DISTINCT); aggregate
-- before joining | | Summing a parent amount after joining to child rows (invoices → payments) |
-- Invoiced or outstanding totals inflated | Aggregate the child table per parent first, then join
-- | | Storing phone numbers, PIN codes, or account numbers as numbers | Leading zeros vanish; +91
-- rejected | Store identifiers as text | | Answering with only part of the relevant data (due
-- dates without payments) | "Overdue" invoices that are already paid | Ask which other tables
-- change the answer, and join them | | Not reconciling totals | A report silently loses a customer
-- or an unassigned order | Compare report totals with a simple SUM on the source table | | Inner
-- join where a left join was needed | Customers or products with no activity vanish | Decide on
-- purpose whether unmatched rows must stay | | Right-table condition in WHERE after LEFT JOIN |
-- Left join behaves like an inner join | Move the condition into ON | | NOT IN with a subquery
-- that can return NULL | Zero rows | Use NOT EXISTS or an anti-join | | Integer division |
-- Percentages come out as 0 | Multiply by 1.0 or 100.0 first | | BETWEEN on timestamps | Last
-- day's records missing | Half-open range: >= start AND < next_start | | Grouping by EXTRACT(MONTH
-- ...) across years | Different years merged | DATE_TRUNC('month', ...) | | Relying on unsorted
-- output | Order changes between runs | Always ORDER BY when order matters | | UPDATE/DELETE
-- without WHERE | Every row changed | Run the WHERE as a SELECT first; use transactions | | No
-- constraints on a table you build | Duplicates, impossible values, and orphan rows creep in |
-- Turn every business rule into NOT NULL, UNIQUE, CHECK, or a foreign key | | Treating automatic
-- IDs as counts | "Highest ID = number of suppliers" is wrong after failed inserts | Count with
-- COUNT(*); expect gaps in IDs | | MySQL MODIFY COLUMN without the full definition | Column
-- silently becomes nullable and loses its default | Copy the definition from SHOW CREATE TABLE,
-- then change one part | | Expecting ROLLBACK to undo ALTER or DROP in MySQL | The change is still
-- there | Back up with CREATE TABLE … AS SELECT before structure changes | | Adding NOT NULL or a
-- constraint while old rows break it | ALTER TABLE fails | Fix the existing data first, then add
-- the rule | | DROP … CASCADE to make an error go away | Constraints, or whole tables in a schema,
-- silently removed | Read what depends on the object; drop children first | | Practicing changes
-- on a real database | Real data changed or lost | Use a lab database or a copy | | Forgetting the
-- database password set during installation | Can't connect to PostgreSQL or MySQL | Write it down
-- during installation, somewhere safe | | Not hand-checking a new calculation | Wrong logic ships
-- in a report | Verify one row or one group by hand, every time |

-- ---

-- =============================================================================================
-- In the real world: Riverstone's monthly sales report
-- =============================================================================================

-- Every month, Riverstone's sales coordinator spends most of a day building the same report. She
-- exports orders from the billing system to Excel, looks up customer names, filters out cancelled
-- orders, adds up line values with discounts, and builds a pivot table by month. When a late
-- correction arrives, she starts again.

-- Here is that report as one query:

-- Monthly sales summary
-- Revenue counts Delivered and Shipped orders (finance policy);
-- Pending and Cancelled orders are excluded.
SELECT DATE_TRUNC('month', o.order_date)::date AS month,
       COUNT(DISTINCT o.order_id)             AS orders,
       COUNT(DISTINCT o.customer_id)          AS active_customers,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue
FROM orders AS o
JOIN order_items AS oi
  ON o.order_id = oi.order_id
WHERE o.status IN ('Delivered', 'Shipped')
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY month;

/* The chapter shows:
      month    | orders | active_customers | net_revenue
   ------------+--------+------------------+-------------
    2026-01-01 |      3 |                3 |      104210
    2026-02-01 |      5 |                5 |      161700
    2026-03-01 |      2 |                2 |       31800
   (3 rows)
*/


-- The same report in MySQL. The report you just built needs one change in MySQL (section 12.16):
-- DATE_FORMAT builds the first day of each month, because MySQL has no DATE_TRUNC.

-- Monthly sales summary (MySQL)
-- Revenue counts Delivered and Shipped orders (finance policy).
SELECT CAST(DATE_FORMAT(o.order_date, '%Y-%m-01') AS DATE) AS month,
       COUNT(DISTINCT o.order_id)                          AS orders,
       COUNT(DISTINCT o.customer_id)                       AS active_customers,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue
FROM orders AS o
JOIN order_items AS oi
  ON o.order_id = oi.order_id
WHERE o.status IN ('Delivered', 'Shipped')
GROUP BY month
ORDER BY month;

/* The chapter shows:
   +------------+--------+------------------+-------------+
   | month      | orders | active_customers | net_revenue |
   +------------+--------+------------------+-------------+
   | 2026-01-01 |      3 |                3 |      104210 |
   | 2026-02-01 |      5 |                5 |      161700 |
   | 2026-03-01 |      2 |                2 |       31800 |
   +------------+--------+------------------+-------------+
*/


-- '%Y-%m-01' is a format pattern: %Y is the four-digit year, %m the two-digit month, and -01 is
-- typed literally, giving text like 2026-02-01. CAST(… AS DATE) turns that text back into a real
-- date, so it sorts and joins like one. The format letters are MySQL's own; %d is the day, %M the
-- month's name, and %b its short name, which is handy for chart labels (DATE_FORMAT(order_date,
-- '%b %Y') gives Feb 2026).

-- The query runs in well under a second, it gives the same answer every time, and a late
-- correction just means running it again. Every idea in this chapter is in it: filtering, a join,
-- aggregates, COUNT(DISTINCT) to avoid fan-out, date truncation, and a comment recording a
-- business rule (which statuses count as revenue).

-- That business rule is the most important line in the query, and SQL can't decide it for you.
-- Does a Shipped order count as revenue, or only Delivered? Does Pending? Finance, sales, and
-- operations may each give a different answer. Your first job on any report is to find out and
-- write it down. Chapter 24 covers how to have that conversation.

-- And once the query is right, nobody should have to run it by hand at all. Chapter 20 takes a
-- query of exactly this kind and turns it into a Daily Sales Flash: an email that lands in every
-- manager's inbox by 7:30 each morning, with the numbers in the body of the email, an alert when
-- something in the data looks wrong, and a warning to you if the job ever fails.

-- ---

-- =============================================================================================
-- Project: rebuild a real report in SQL
-- =============================================================================================

-- Goal: replace one manual report with a single, commented, verified SQL query.

-- =============================================================================================
-- Tools you'll need
-- =============================================================================================

-- - PostgreSQL: a free, professional-grade relational database that follows the SQL standard
-- closely. It's the recommended database for learning and a common choice in industry. - MySQL
-- Community Server (optional second database): the free edition of MySQL, behind a large share of
-- web and e-commerce applications. Install the current LTS release (section 12.3). - DBeaver
-- Community Edition: a free query editor that connects to almost any database, including both of
-- the above. Alternatives: pgAdmin (PostgreSQL's own tool), MySQL Workbench (MySQL's own tool), or
-- the editor built into your company's data warehouse. - The Riverstone practice files (Appendix
-- E): riverstone_setup.sql (the small database used in this chapter) and its MySQL twin
-- riverstone_setup_mysql.sql; riverstone_2025_setup.sql and riverstone_2025_setup_mysql.sql (the
-- one-year database: 24 customers and 175 orders from 2025, for exercise 30 and the project);
-- ch12_queries_postgresql.sql and ch12_queries_mysql.sql (every query in this chapter, in each
-- database's spelling, including Chapter 7's quiet-customer query from exercise 30); and
-- ch12_lab_postgresql.sql and ch12_lab_mysql.sql (every statement from section 12.13 and exercises
-- 23–27, in order). - Later in the book: a cloud data warehouse (Chapter 49), where the same SQL
-- runs on billions of rows.

-- Option A: your own work data. Use a report you actually produce: sales, collections, inventory,
-- attendance, leads. Get permission first, and never copy confidential data to personal devices.
-- Remove or mask names if needed.

-- Option B: the one-year Riverstone database (riverstone_2025_setup.sql, 175 orders from 2025;
-- section 12.3), if you don't have suitable work data.

-- Steps:

-- 1. Pin down the question. Write, in one or two sentences, exactly what the report answers, for
-- whom, and over what period. List every business rule: which statuses count, how discounts and
-- returns are handled, which date defines the month (order date, invoice date, or delivery date?).
-- 2. Map the data. Sketch the tables you need, their keys, and the grain of each (what one row
-- represents). Draw it on paper like Figure 12.1. 3. Load it. Create the tables in PostgreSQL and
-- load the data. (For CSV files, DBeaver's import wizard works; Chapter 45 covers robust loading.)
-- Run COUNT(*) on each table and compare it with the source. 4. Build step by step. Start with
-- SELECT ... FROM one table. Add one join at a time, checking row counts after each. Add filters.
-- Add aggregation last. 5. Reconcile. Compare your SQL totals with the report you trust. They will
-- differ at first. Track down every difference: a cancelled order counted, a join that fanned out,
-- a date boundary, a NULL. Write down what you found. 6. Make it readable. Apply the style guide
-- from section 12.14 and comment every business rule. 7. Save it. Put the query and a short README
-- (what the report is, the rules, and how to run it) in a dated project folder. In Chapter 26
-- you'll put this folder under version control.

-- Stretch goals:

-- - Add a second query for the same report broken down by salesperson or customer segment. - Add a
-- "data checks" query that flags problems: orders with no items, items with zero quantity,
-- customers with no city. - Time how long the manual process took and how long the query takes.
-- That number belongs on your CV. - After Chapter 20, schedule the query and deliver its result
-- automatically by email.

-- ---

-- =============================================================================================
-- Recap
-- =============================================================================================

-- - A relational database stores data in strictly typed tables. Primary keys identify rows;
-- foreign keys link tables; the database enforces both. - Data is split across tables
-- (normalization) to store each fact once. Joins stitch it back together. - SELECT chooses
-- columns, FROM names tables, WHERE filters rows, ORDER BY sorts, LIMIT keeps the top n. - NULL
-- means unknown. Test it with IS NULL; remember that comparisons with NULL are never true, so <>
-- filters silently drop NULL rows. - CASE adds if-then logic; DATE_TRUNC groups by period; text
-- functions clean labels. - Aggregates (COUNT, SUM, AVG, MIN, MAX) plus GROUP BY turn rows into
-- summaries. HAVING filters groups; WHERE filters rows. - INNER JOIN keeps matches only; LEFT JOIN
-- keeps every left row. Anti-joins find what's missing. Self-joins relate a table to itself. -
-- Fan-out from joining to a finer grain inflates counts and sums. Know the grain of every table. -
-- The database runs clauses in the order FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY →
-- LIMIT, which explains most errors. - Subqueries nest queries; NOT EXISTS is safer than NOT IN.
-- UNION ALL stacks results; UNION also removes duplicates. - DDL (CREATE, ALTER, DROP, TRUNCATE)
-- builds and changes structure; DML (INSERT, UPDATE, DELETE) changes rows. Turn business rules
-- into constraints, check the WHERE before every change, and use transactions. In MySQL, structure
-- changes can't be rolled back, so back up first. - Readable SQL is correct SQL more often. Always
-- hand-check one result. - MySQL runs the same SQL with a few different spellings, and four
-- behaviours that change results without an error: date subtraction (use DATEDIFF), || (use
-- CONCAT), case-insensitive comparison, and NULLs sorting first. - Install from official sources,
-- and check each tool before moving on: SELECT COUNT(*) FROM order_items; returning 19 proves the
-- database, the client, and the data all work.

-- ---

-- =============================================================================================
-- Key terms
-- =============================================================================================

-- attribute/column · row/record · table · relational database · DBMS · PostgreSQL · DBeaver ·
-- installer · localhost · port · driver · statement · clause · expression · function · argument ·
-- schema · data type · NUMERIC vs floating point · entity-relationship (ER) diagram · primary key
-- · composite key · foreign key · referential integrity · one-to-many · many-to-many · bridge
-- table · normalization · grain · SQL dialect · alias · DISTINCT · three-valued logic · NULL ·
-- COALESCE · CASE · cast · date literal · banker's rounding · aggregate function · GROUP BY ·
-- HAVING · inner join · left join · right join · full outer join · cross join · self-join · anti-
-- join · fan-out · reconciliation · logical execution order · subquery · correlated subquery ·
-- derived table · gross margin · ageing report · UNION / UNION ALL · INTERSECT / EXCEPT · DDL ·
-- DML · TCL · DCL · CREATE DATABASE · CREATE TABLE · constraint · NOT NULL · UNIQUE · CHECK ·
-- DEFAULT · identity column / AUTO_INCREMENT · INSERT · RETURNING / LAST_INSERT_ID() · UPDATE ·
-- DELETE · ON DELETE CASCADE · soft delete · upsert · ALTER TABLE · MODIFY COLUMN · schema
-- (PostgreSQL) · TRUNCATE · DROP · implicit commit · staging table · migration · transaction ·
-- COMMIT / ROLLBACK · auto-commit · MySQL · LTS release · collation · DATEDIFF ·
-- ONLY_FULL_GROUP_BY

-- (All terms are defined in the Glossary, Appendix A.)

-- ---

-- =============================================================================================
-- Check yourself
-- =============================================================================================

-- Be strict with yourself as you check each box:

-- - [ ] PostgreSQL (and, if I chose it, MySQL) and DBeaver are installed, and SELECT COUNT(*) FROM
-- order_items; returns 19 in the Riverstone database.

-- - [ ] I can explain what a table, row, column, primary key, and foreign key are, using an
-- example from my own work. - [ ] I can look at a schema and state the grain of each table. - [ ]
-- I can write SELECT, WHERE, ORDER BY, GROUP BY, and HAVING queries without looking up the syntax.
-- - [ ] I bracket every mix of AND and OR without thinking about it. - [ ] Before filtering a
-- column, I automatically ask whether it can be NULL. - [ ] I choose between INNER and LEFT JOIN
-- based on the business question, and I can write an anti-join. - [ ] When a join is involved, I
-- check whether counts or sums have fanned out. - [ ] I can explain why WHERE can't use an
-- aggregate or a SELECT alias. - [ ] I can create a table with keys and constraints, fill it,
-- correct it, change its structure with ALTER TABLE, and remove it, in PostgreSQL and in MySQL. -
-- [ ] Before any UPDATE, DELETE, ALTER, or DROP, I preview, back up, or use a transaction without
-- being reminded. - [ ] I have rebuilt one real report in SQL and reconciled it to the trusted
-- numbers. - [ ] (If you use MySQL.) I can move a query between PostgreSQL and MySQL and name the
-- four differences that change results without an error.

-- When a new business question arrives and your thinking is about the business, not about the
-- syntax, SQL has become a tool in your hands.

-- ---

-- =============================================================================================
-- Exercises
-- =============================================================================================

-- All exercises use the Riverstone database from section 12.2. Try each one before looking at the
-- answers. For every query, predict the number of rows first, then run it.

-- =============================================================================================
-- Warm-up
-- =============================================================================================

-- 1. List all products in the Kitchen category, cheapest first. 2. How many customers are in each
-- segment? Show the largest segment first. 3. List the orders placed in March 2026, using a half-
-- open date range. 4. Find customers whose name contains "Foods" or "Mart".

-- =============================================================================================
-- Core
-- =============================================================================================

-- 5. Show total units sold for every product, including products never sold (show 0), ignoring
-- cancelled orders. Most units first. 6. Show net revenue (non-cancelled orders) by sales rep
-- name. Orders with no rep should appear as "Unassigned". 7. Find customers who have placed at
-- least one order but have never had an order Delivered. 8. What is the average net order value
-- across non-cancelled orders? 9. Show the number of payments and total amount received by payment
-- method, largest amount first. 10. List the invoices that haven't received any payment at all,
-- with their amount and due date, earliest due date first.

-- =============================================================================================
-- Stretch
-- =============================================================================================

-- 11. For each customer who has ordered, show their first order date, most recent order date, and
-- the number of days between them, ignoring cancelled orders. Largest gap first. 12. Show net
-- revenue by product category and each category's percentage of total net revenue (non-cancelled
-- orders), to one decimal place. 13. Which customers' total net revenue is above the average
-- customer's total net revenue? 14. For every invoice with money still owed, show the invoice
-- amount, the number of payments, the amount paid, and the balance. Largest balance first. 15.
-- Operations wants to chase stuck orders as of 31 March 2026: orders Pending for more than 7 days,
-- or Shipped for more than 14 days (and not yet Delivered). Show the order, date, status, and days
-- open, oldest first.

-- =============================================================================================
-- Think about it (no SQL needed)
-- =============================================================================================

-- 16. A colleague's report says Riverstone had "19 orders" in Q1 2026. Where might that number
-- have come from, and what's the right figure? 17. The business wants to know revenue by city.
-- Sunrise Caterers has no city. Should the report drop it, show it as "Unknown", or something
-- else? Who should decide? 18. Explain to a non-technical manager, in three sentences, why the
-- sales report must not overwrite old prices when the price list changes. 19. In exercise 14 you
-- can safely join invoices to payments and show i.amount next to SUM(p.amount), but in section
-- 12.10 the same join made SUM(i.amount) wrong. What's the difference? Use invoice 9005 in your
-- explanation.

-- =============================================================================================
-- MySQL track (optional, section 12.16)
-- =============================================================================================

-- 20. Rewrite exercise 15 (stuck orders) so it runs in MySQL and gives the same result. 21. In
-- MySQL, show each employee as a single text column in the form Neha Kulkarni (Sales Executive),
-- next to their manager's name (or (none)). 22. A colleague moves a MySQL report to PostgreSQL. It
-- used WHERE segment = 'retail' and DATE '2026-03-31' - signup_date AS days_as_customer. What
-- happens to each line in PostgreSQL, and which result would have been wrong in MySQL all along?

-- =============================================================================================
-- Build and change (section 12.13)
-- =============================================================================================

-- Use the riverstone_lab database. If you've already dropped it, create it again first. Write each
-- answer for PostgreSQL, then change what's needed for MySQL.

-- 23. Create a warehouses table with: an automatic ID; a required, unique name; a required city of
-- up to 50 characters; a required capacity in units that must be above zero, enforced by a CHECK
-- constraint named chk_capacity; and an optional opening date. 24. Add three warehouses in one
-- statement: Bhiwandi Main in Bhiwandi (12,000 units, opened 1 April 2021), Chakan in Pune (8,000
-- units, opened 15 July 2023), and Sriperumbudur in Chennai (6,000 units, opening date not yet
-- known). Then list the table. 25. The Chennai warehouse has been extended by 25%, and Chakan has
-- been renamed Chakan Plant 2. Make both changes, checking which rows each change will touch
-- before you run it. 26. Change the table's structure: add an optional manager_email column,
-- rename capacity_units to capacity_boxes, and allow city names of up to 80 characters while
-- keeping the city required. 27. Riverstone closes the Chennai warehouse. Remove its row and list
-- what's left. Then remove the table completely. 28. A table called daily_stock_import is emptied
-- and reloaded with fresh data every morning. Compare DELETE FROM daily_stock_import;, TRUNCATE
-- TABLE daily_stock_import;, and DROP TABLE daily_stock_import; for this job. Which would you use,
-- and what's the one situation in MySQL where your choice behaves differently from PostgreSQL? 29.
-- At 6 p.m. on a Friday, a manager asks you to change every 'Open' status to 'Pending' in the live
-- purchase_orders table "quickly, before the weekend". List the steps you'd take, in order.

-- =============================================================================================
-- Back to earlier chapters
-- =============================================================================================

-- 30. (PostgreSQL, then MySQL; needs the one-year database from section 12.3.) Chapter 7, section
-- 7.6, asked for every customer with no non-cancelled order in the 60 days up to 31 December 2025,
-- including customers who have never ordered. On riverstone_2025, write the query, starting from
-- Question 1 in section 12.15. Predict first: Chapter 7 found 5 customers, with Tasty Tiffins at
-- 66 days. Then write the MySQL version (section 12.16). 31. Using the rounding Watch out in
-- section 12.8, predict each result, then run it to check: (a) PostgreSQL SELECT ROUND(4.5); (b)
-- PostgreSQL SELECT ROUND(4.5::double precision); (c) MySQL SELECT ROUND(45E-1); Explain each. 32.
-- (Needs the one-year database.) Chapter 11, section 11.5, built its first pivot table on the 2025
-- sales: segment in Rows, the quarters in Columns, net revenue in Values, and status in Filters
-- with Cancelled cleared. On riverstone_2025, write the same table in SQL, one row per segment and
-- one column per quarter plus a total. Check your numbers against Figure 11.3. 33. Write a short,
-- specific request to your IT team asking permission to install PostgreSQL and DBeaver on a work
-- laptop for learning. Say what each tool is for, what data you will and won't connect to, and ask
-- them one question.

-- ---

-- =============================================================================================
-- Answers
-- =============================================================================================

-- (Every query below was run against the Riverstone database, and the outputs are real.)

-- 1.

SELECT product_name, unit_price
FROM products
WHERE category = 'Kitchen'
ORDER BY unit_price ASC;

/* The chapter shows:
       product_name    | unit_price
   --------------------+------------
    Water Bottle 1L    |     120.00
    Food Container Set |     650.00
   (2 rows)
*/


-- 2.

SELECT segment, COUNT(*) AS num_customers
FROM customers
GROUP BY segment
ORDER BY num_customers DESC, segment;

/* The chapter shows:
      segment   | num_customers
   -------------+---------------
    Hospitality |             3
    Retail      |             3
    Wholesale   |             2
   (3 rows)
*/


-- The tie between Hospitality and Retail is broken alphabetically by the second sort column.
-- Without it, their order isn't guaranteed.

-- 3.

SELECT order_id, customer_id, order_date
FROM orders
WHERE order_date >= '2026-03-01'
  AND order_date <  '2026-04-01'
ORDER BY order_date;

/* The chapter shows:
    order_id | customer_id | order_date
   ----------+-------------+------------
        5010 |           3 | 2026-03-03
        5011 |           1 | 2026-03-10
        5012 |           5 | 2026-03-15
   (3 rows)
*/


-- 4.

SELECT customer_name
FROM customers
WHERE customer_name LIKE '%Foods%'
   OR customer_name LIKE '%Mart%';

/* The chapter shows:
    customer_name
   ---------------
    Coastal Foods
    Metro Mart
   (2 rows)
*/


-- 5. Aggregate the sales first, then left-join to the full product list, so the filter on order
-- status can't remove unsold products:

SELECT p.product_name,
       COALESCE(s.units_sold, 0) AS units_sold
FROM products AS p
LEFT JOIN (
    SELECT oi.product_id, SUM(oi.quantity) AS units_sold
    FROM order_items AS oi
    JOIN orders AS o ON oi.order_id = o.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY oi.product_id
) AS s ON p.product_id = s.product_id
ORDER BY units_sold DESC, p.product_name;

/* The chapter shows:
       product_name    | units_sold
   --------------------+------------
    Water Bottle 1L    |        230
    Industrial Crate   |        125
    Food Container Set |         85
    Storage Box 10L    |         85
    Storage Box 25L    |         60
    Garden Chair       |          0
   (6 rows)
*/


-- Common wrong answer: joining products → order_items → orders with left joins and then writing
-- WHERE o.status <> 'Cancelled'. That WHERE removes the Garden Chair, because its status is NULL.
-- It's the "left join became an inner join" trap again.

-- 6.

SELECT COALESCE(e.employee_name, 'Unassigned') AS sales_rep,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
LEFT JOIN employees AS e ON o.sales_rep_id = e.employee_id
WHERE o.status <> 'Cancelled'
GROUP BY COALESCE(e.employee_name, 'Unassigned')
ORDER BY net_revenue DESC;

/* The chapter shows:
      sales_rep   | net_revenue
   ---------------+-------------
    Rahul Mehta   |      146745
    Farah Khan    |       96660
    Neha Kulkarni |       57200
    Unassigned    |       23325
   (4 rows)
*/


-- The join to employees must be a left join. An inner join would drop order 5008 and its ₹23,325.

-- 7.

SELECT c.customer_name
FROM customers AS c
WHERE EXISTS (SELECT 1 FROM orders AS o
              WHERE o.customer_id = c.customer_id)
  AND NOT EXISTS (SELECT 1 FROM orders AS o
                  WHERE o.customer_id = c.customer_id
                    AND o.status = 'Delivered');

/* The chapter shows:
        customer_name
   ------------------------
    Northgate Distributors
   (1 row)
*/


-- Blue Bay Cafe is correctly excluded: it has never ordered at all.

-- 8.

SELECT ROUND(AVG(order_revenue), 2) AS avg_order_value
FROM (
    SELECT o.order_id,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS order_revenue
    FROM orders AS o
    JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY o.order_id
) AS per_order;

/* The chapter shows:
    avg_order_value
   -----------------
           29448.18
   (1 row)
*/


-- Check: total non-cancelled revenue is ₹3,23,930 across 11 orders; 3,23,930 ÷ 11 = 29,448.18. ✓

-- 9.

SELECT method, COUNT(*) AS payments, SUM(amount) AS amount_received
FROM payments
GROUP BY method
ORDER BY amount_received DESC;

/* The chapter shows:
       method     | payments | amount_received
   ---------------+----------+-----------------
    Bank transfer |        5 |       137960.00
    UPI           |        4 |        44740.00
    Cheque        |        1 |        14550.00
   (3 rows)
*/


-- The three amounts add up to ₹1,97,250, the total of the payments table. ✓

-- 10. An anti-join from invoices to payments:

SELECT i.invoice_id, i.amount, i.due_date
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id
WHERE p.payment_id IS NULL
ORDER BY i.due_date;

/* The chapter shows:
    invoice_id |  amount  |  due_date
   ------------+----------+------------
          9007 | 23325.00 | 2026-03-22
          9010 | 11700.00 | 2026-04-10
   (2 rows)
*/


-- Invoice 9007 is already overdue; 9010 isn't due until April.

-- 11.

SELECT c.customer_name,
       MIN(o.order_date)                     AS first_order,
       MAX(o.order_date)                     AS latest_order,
       MAX(o.order_date) - MIN(o.order_date) AS days_between
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.status <> 'Cancelled'
GROUP BY c.customer_name
ORDER BY days_between DESC, c.customer_name;

/* The chapter shows:
        customer_name      | first_order | latest_order | days_between
   ------------------------+-------------+--------------+--------------
    Sharma Hardware        | 2026-01-05  | 2026-03-10   |           64
    Metro Mart             | 2026-02-06  | 2026-03-15   |           37
    Coastal Foods          | 2026-01-09  | 2026-02-11   |           33
    Green Leaf Hotels      | 2026-03-03  | 2026-03-03   |            0
    Northgate Distributors | 2026-02-25  | 2026-02-25   |            0
    Patel Kitchenware      | 2026-01-14  | 2026-01-14   |            0
    Sunrise Caterers       | 2026-02-19  | 2026-02-19   |            0
   (7 rows)
*/


-- WHERE o.status <> 'Cancelled' drops Green Leaf Hotels' cancelled January order, so its first and
-- latest valid orders are the same day, 3 March. Grouping by name works here because names are
-- unique in this data. In real data, group by c.customer_id, c.customer_name so two customers with
-- the same name aren't merged.

-- 12.

SELECT p.category,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue,
       ROUND(100.0 * SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100))
             / (SELECT SUM(oi2.quantity * oi2.unit_price * (1 - oi2.discount_pct / 100))
                FROM order_items AS oi2
                JOIN orders AS o2 ON oi2.order_id = o2.order_id
                WHERE o2.status <> 'Cancelled'), 1) AS pct_of_total
FROM order_items AS oi
JOIN orders   AS o ON oi.order_id   = o.order_id
JOIN products AS p ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY net_revenue DESC;

/* The chapter shows:
     category  | net_revenue | pct_of_total
   ------------+-------------+--------------
    Industrial |      161385 |         49.8
    Storage    |       81810 |         25.3
    Kitchen    |       80735 |         24.9
   (3 rows)
*/


-- Notice the 100.0, which avoids integer division. The scalar subquery repeats the cancelled-order
-- filter; if it didn't, the percentages would be calculated against a different total and wouldn't
-- add up to 100. In Chapter 13, a window function does this far more neatly: SUM(...) OVER ().

-- 13.

SELECT customer_name, ROUND(customer_revenue, 0) AS customer_revenue
FROM (
    SELECT c.customer_name,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS customer_revenue
    FROM customers AS c
    JOIN orders      AS o  ON c.customer_id = o.customer_id
    JOIN order_items AS oi ON o.order_id    = oi.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY c.customer_name
) AS t
WHERE customer_revenue > (
    SELECT AVG(customer_revenue)
    FROM (
        SELECT o.customer_id,
               SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS customer_revenue
        FROM orders AS o
        JOIN order_items AS oi ON o.order_id = oi.order_id
        WHERE o.status <> 'Cancelled'
        GROUP BY o.customer_id
    ) AS x
)
ORDER BY customer_revenue DESC;

/* The chapter shows:
        customer_name      | customer_revenue
   ------------------------+------------------
    Coastal Foods          |           105885
    Northgate Distributors |            76560
   (2 rows)
*/


-- The average customer total is ₹46,276. Notice how much the logic repeats itself. That repetition
-- is exactly the problem CTEs solve in Chapter 13, where this becomes a short, readable query.

-- 14.

SELECT i.invoice_id,
       i.amount,
       COUNT(p.payment_id)                   AS num_payments,
       COALESCE(SUM(p.amount), 0)            AS amount_paid,
       i.amount - COALESCE(SUM(p.amount), 0) AS balance
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id
GROUP BY i.invoice_id, i.amount
HAVING i.amount - COALESCE(SUM(p.amount), 0) > 0
ORDER BY balance DESC;

/* The chapter shows:
    invoice_id |  amount  | num_payments | amount_paid | balance
   ------------+----------+--------------+-------------+----------
          9008 | 76560.00 |            1 |    30000.00 | 46560.00
          9007 | 23325.00 |            0 |           0 | 23325.00
          9006 | 32625.00 |            1 |    20000.00 | 12625.00
          9010 | 11700.00 |            0 |           0 | 11700.00
          9003 | 16250.00 |            1 |    10000.00 |  6250.00
   (5 rows)
*/


-- COUNT(p.payment_id) counts only real payments, so unpaid invoices show 0; COUNT(*) would wrongly
-- show 1 for them, because the left join still produces one row. The balances add up to ₹1,00,460.
-- ✓

-- 15.

SELECT order_id,
       order_date,
       status,
       DATE '2026-03-31' - order_date AS days_open
FROM orders
WHERE (status = 'Pending' AND DATE '2026-03-31' - order_date > 7)
   OR (status = 'Shipped' AND DATE '2026-03-31' - order_date > 14)
ORDER BY days_open DESC;

/* The chapter shows:
    order_id | order_date | status  | days_open
   ----------+------------+---------+-----------
        5009 | 2026-02-25 | Shipped |        34
        5011 | 2026-03-10 | Shipped |        21
        5012 | 2026-03-15 | Pending |        16
   (3 rows)
*/


-- The parentheses matter: each status has its own day limit (section 12.6). Order 5009 has been
-- "Shipped" for 34 days, which almost certainly means someone forgot to mark it Delivered, or it's
-- lost. Either way, somebody should find out today.

-- 16. 19 is the number of rows in order_items, i.e. order lines, probably from counting rows after
-- a join or from the wrong table. Riverstone had 12 orders in Q1 2026 (11 if the cancelled order
-- is excluded; which one to report is a business rule to agree on). It's the fan-out trap in the
-- wild.

-- 17. Dropping Sunrise Caterers would understate total revenue by ₹23,325, so total revenue by
-- city wouldn't match total revenue overall. Showing "Unknown" keeps the totals reconciled and
-- makes the data-quality gap visible. The business decides how to present it, but the analyst's
-- job is to flag it, and ideally to get the missing city fixed at the source.

-- 18. A sample answer: "Each sale records the price the customer actually paid on that day. If we
-- used today's price list to calculate old sales, every price change would rewrite our history,
-- and last quarter's revenue would keep changing. So we store the price at the moment of sale, and
-- the price list only affects new orders."

-- 19. In exercise 14, the query groups by invoice and uses i.amount only as a grouping column:
-- it's never summed, so repeating it on two rows does no harm. In section 12.10, the query summed
-- i.amount across the joined rows. Invoice 9005 (₹14,640) was paid in two instalments, so the join
-- produced two rows for it, and SUM(i.amount) counted ₹29,280. Repeated rows are only a problem
-- when you add up a column from the table that got repeated.

-- 20. (MySQL.) Replace each date subtraction with DATEDIFF, later date first:

SELECT order_id,
       order_date,
       status,
       DATEDIFF(DATE '2026-03-31', order_date) AS days_open
FROM orders
WHERE (status = 'Pending' AND DATEDIFF(DATE '2026-03-31', order_date) > 7)
   OR (status = 'Shipped' AND DATEDIFF(DATE '2026-03-31', order_date) > 14)
ORDER BY days_open DESC;

/* The chapter shows:
   +----------+------------+---------+-----------+
   | order_id | order_date | status  | days_open |
   +----------+------------+---------+-----------+
   |     5009 | 2026-02-25 | Shipped |        34 |
   |     5011 | 2026-03-10 | Shipped |        21 |
   |     5012 | 2026-03-15 | Pending |        16 |
   +----------+------------+---------+-----------+
*/


-- The same three orders as the PostgreSQL answer. If you had left DATE '2026-03-31' - order_date
-- in place, MySQL would have compared numbers like 20260331 - 20260315 = 16 for order 5012
-- (correct only by luck, because both dates are in the same month) and 20260331 - 20260225 = 106
-- for order 5009, instead of 34.

-- 21. (MySQL.) CONCAT joins any number of pieces; || would return 0:

SELECT CONCAT(e.employee_name, ' (', e.job_title, ')') AS employee,
       COALESCE(m.employee_name, '(none)')             AS reports_to
FROM employees AS e
LEFT JOIN employees AS m ON e.manager_id = m.employee_id
ORDER BY e.employee_id;

/* The chapter shows:
   +---------------------------------+--------------+
   | employee                        | reports_to   |
   +---------------------------------+--------------+
   | Anita Rao (Sales Head)          | (none)       |
   | Vikram Singh (Sales Manager)    | Anita Rao    |
   | Neha Kulkarni (Sales Executive) | Vikram Singh |
   | Rahul Mehta (Sales Executive)   | Vikram Singh |
   | Farah Khan (Sales Executive)    | Anita Rao    |
   +---------------------------------+--------------+
*/


-- This exact query also runs in PostgreSQL. One detail: in MySQL, CONCAT returns NULL if any piece
-- is NULL, so an employee with no job title would show a blank. CONCAT_WS(' ', …) or COALESCE on
-- each piece avoids that.

-- 22. WHERE segment = 'retail' found the three Retail customers in MySQL, because MySQL's default
-- collation ignores case, but returns zero rows in PostgreSQL, silently. Fix it with 'Retail' or
-- LOWER(segment) = 'retail'. The date line behaves the other way: PostgreSQL gives the correct
-- number of days, while MySQL was producing meaningless numbers (it subtracted dates as if they
-- were numbers like 20260331). So the report's "days as customer" figures were wrong all along in
-- MySQL, and nobody noticed because no error appeared. Moving between databases is a good moment
-- to reconcile every number against a trusted total.

-- 23. PostgreSQL:

CREATE TABLE warehouses (
    warehouse_id    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    warehouse_name  VARCHAR(100) NOT NULL UNIQUE,
    city            VARCHAR(50)  NOT NULL,
    capacity_units  INTEGER      NOT NULL CONSTRAINT chk_capacity CHECK (capacity_units > 0),
    opened_on       DATE
);


-- CONSTRAINT chk_capacity gives the rule the name the exercise asked for. Without it, PostgreSQL
-- would call it warehouses_capacity_units_check and MySQL warehouses_chk_1. opened_on has no NOT
-- NULL, so it's optional.

-- 24. The same in both:

INSERT INTO warehouses (warehouse_name, city, capacity_units, opened_on)
VALUES ('Bhiwandi Main', 'Bhiwandi', 12000, '2021-04-01'),
       ('Chakan',        'Pune',      8000, '2023-07-15'),
       ('Sriperumbudur', 'Chennai',   6000, NULL);


SELECT * FROM warehouses ORDER BY warehouse_id;

/* The chapter shows:
    warehouse_id | warehouse_name |   city   | capacity_units | opened_on
   --------------+----------------+----------+----------------+------------
               1 | Bhiwandi Main  | Bhiwandi |          12000 | 2021-04-01
               2 | Chakan         | Pune     |           8000 | 2023-07-15
               3 | Sriperumbudur  | Chennai  |           6000 |
   (3 rows)
*/


-- 25. Preview first, then update with the same WHERE. The same in both:

SELECT warehouse_id, warehouse_name, capacity_units
FROM warehouses
WHERE city = 'Chennai';

/* The chapter shows:
    warehouse_id | warehouse_name | capacity_units
   --------------+----------------+----------------
               3 | Sriperumbudur  |           6000
   (1 row)
*/


UPDATE warehouses
SET capacity_units = capacity_units * 1.25
WHERE city = 'Chennai';

UPDATE warehouses
SET warehouse_name = 'Chakan Plant 2'
WHERE warehouse_name = 'Chakan';


SELECT * FROM warehouses ORDER BY warehouse_id;

/* The chapter shows:
    warehouse_id | warehouse_name |   city   | capacity_units | opened_on
   --------------+----------------+----------+----------------+------------
               1 | Bhiwandi Main  | Bhiwandi |          12000 | 2021-04-01
               2 | Chakan Plant 2 | Pune     |           8000 | 2023-07-15
               3 | Sriperumbudur  | Chennai  |           7500 |
   (3 rows)
*/


-- 6,000 × 1.25 = 7,500. ✓ Filtering on city = 'Chennai' is fine here because there's one Chennai
-- warehouse; on a real table, WHERE warehouse_id = 3 is safer, because a key can only ever match
-- one row.

-- 26. PostgreSQL:

ALTER TABLE warehouses ADD COLUMN manager_email VARCHAR(100);
ALTER TABLE warehouses RENAME COLUMN capacity_units TO capacity_boxes;
ALTER TABLE warehouses ALTER COLUMN city TYPE VARCHAR(80);


-- Had you written MODIFY COLUMN city VARCHAR(80) without NOT NULL, the Null column would show YES:
-- the trap from section 12.13.

-- 27. The same in both:

DELETE FROM warehouses
WHERE warehouse_id = 3;

SELECT warehouse_id, warehouse_name, capacity_boxes
FROM warehouses
ORDER BY warehouse_id;

/* The chapter shows:
    warehouse_id | warehouse_name | capacity_boxes
   --------------+----------------+----------------
               1 | Bhiwandi Main  |          12000
               2 | Chakan Plant 2 |           8000
   (2 rows)
*/


DROP TABLE warehouses;


-- No other table points to warehouses with a foreign key, so the drop succeeds straight away. When
-- you've finished with the lab, remove it with DROP DATABASE riverstone_lab; (in PostgreSQL,
-- connected to a different database).

-- 28. DELETE FROM daily_stock_import; removes every row one at a time: correct, but slow on a big
-- table. DROP TABLE removes the table itself, so the morning load would first have to recreate it,
-- with every column and constraint, and anything that depends on it would break in between.
-- TRUNCATE TABLE is the right tool: it empties the table almost instantly and keeps the structure
-- ready for the new load. The MySQL difference: TRUNCATE commits immediately there, so if the
-- morning job wraps "empty, then reload" in a transaction and the reload fails, MySQL can't roll
-- back to yesterday's data, while PostgreSQL can. In MySQL, a job that must never leave the table
-- empty loads into a second table first and swaps the names with RENAME TABLE once the load has
-- succeeded.

-- 29. A sound order of steps:

-- 1. Clarify the request. Every open order, or only some? Does anything read the status column
-- (the ordering app, reports, the CHECK constraint that allows only four values)? Does "Pending"
-- mean the same thing to everyone? 2. Check the rules. If a CHECK constraint lists the allowed
-- statuses, it has to change first, or every update will fail. 3. Preview: SELECT COUNT(*) FROM
-- purchase_orders WHERE status = 'Open'; and note the number. 4. Back up the affected rows: CREATE
-- TABLE po_status_backup_YYYY_MM_DD AS SELECT po_id, status FROM purchase_orders WHERE status =
-- 'Open';. 5. Run the change inside a transaction, check that the reported row count matches the
-- preview, and only then COMMIT. 6. Verify afterwards: no rows left with 'Open', and the reports
-- still work. 7. Tell people what changed, and keep the script.

-- And the most important step: if steps 1 and 2 can't be settled with the people who own the app
-- and the reports before they leave, don't do it on a Friday evening. A change nobody is around to
-- check or fix over the weekend is a risk, not a favor. Saying "I'll have it ready first thing
-- Monday, tested" is the professional answer.

-- 30. Change two dates in Question 1's query, 31 March 2026 to 31 December 2025, and 1 March 2026
-- to 1 November 2025 (60 days before 31 December is 1 November), and run it on riverstone_2025.
-- PostgreSQL:

-- <!-- db: riverstone_2025 -->

SELECT c.customer_name,
       c.segment,
       MAX(o.order_date)                     AS last_order_date,
       DATE '2025-12-31' - MAX(o.order_date) AS days_since_last_order
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name, c.segment
HAVING MAX(o.order_date) < DATE '2025-11-01'
    OR MAX(o.order_date) IS NULL
ORDER BY last_order_date NULLS FIRST;

/* The chapter shows:
      customer_name   |   segment   | last_order_date | days_since_last_order
   -------------------+-------------+-----------------+-----------------------
    Home Plus         | Retail      |                 |
    City Needs Store  | Retail      | 2025-03-22      |                   284
    Sunrise Caterers  | Hospitality | 2025-06-10      |                   204
    Om Sai Provisions | Retail      | 2025-07-22      |                   162
    Tasty Tiffins     | Hospitality | 2025-10-26      |                    66
   (5 rows)
*/


-- The same five customers as Chapter 7, with Tasty Tiffins at 66 days. ✓ In plain words: the query
-- starts from every customer and looks up each one's orders, ignoring cancelled ones; for each
-- customer it finds the latest order date and counts the days from that date to 31 December 2025;
-- and it keeps only customers whose latest order was before 1 November, plus customers with no
-- orders at all. The blank dates are Home Plus: it signed up on 18 June 2025 and has never
-- ordered, so there's no date to show.

-- MySQL needs the two changes from section 12.16, DATEDIFF instead of subtracting dates and a
-- hand-made sort to put the blank dates first:

SELECT c.customer_name,
       c.segment,
       MAX(o.order_date)                              AS last_order_date,
       DATEDIFF(DATE '2025-12-31', MAX(o.order_date)) AS days_since_last_order
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name, c.segment
HAVING MAX(o.order_date) < DATE '2025-11-01'
    OR MAX(o.order_date) IS NULL
ORDER BY last_order_date IS NULL DESC, last_order_date;

/* The chapter shows:
   +-------------------+-------------+-----------------+-----------------------+
   | customer_name     | segment     | last_order_date | days_since_last_order |
   +-------------------+-------------+-----------------+-----------------------+
   | Home Plus         | Retail      | NULL            |                  NULL |
   | City Needs Store  | Retail      | 2025-03-22      |                   284 |
   | Sunrise Caterers  | Hospitality | 2025-06-10      |                   204 |
   | Om Sai Provisions | Retail      | 2025-07-22      |                   162 |
   | Tasty Tiffins     | Hospitality | 2025-10-26      |                    66 |
   +-------------------+-------------+-----------------+-----------------------+
*/


-- The same five rows. Both versions are in the companion files ch12_queries_postgresql.sql and
-- ch12_queries_mysql.sql.

-- 31. (a) and (b), in PostgreSQL:

SELECT ROUND(4.5)                   AS exact_numeric,
       ROUND(4.5::double precision) AS floating;

/* The chapter shows:
    exact_numeric | floating
   ---------------+----------
                5 |        4
   (1 row)
*/


-- (c), in MySQL:

SELECT ROUND(45E-1) AS approximate;

/* The chapter shows:
   +-------------+
   | approximate |
   +-------------+
   |           4 |
   +-------------+
*/


-- (a) 5: 4.5 is numeric, and PostgreSQL breaks ties away from zero. (b) 4: as double precision,
-- the usual rule is round half to even, and 4 is even. (c) 4: 45E-1 (45 × 10⁻¹, which is 4.5) is
-- written in scientific notation, which makes it an approximate value, so on most systems MySQL
-- rounds it to the nearest even number. A spreadsheet's =ROUND(4.5,0) would give 5, like (a).

-- 32. A derived table first works out each line's quarter and revenue (the pivot's source rows,
-- with the Filters condition as WHERE); the outer query groups by segment (Rows) and spreads the
-- quarters into columns with conditional aggregation (Columns and Values):

-- <!-- db: riverstone_2025 -->

SELECT segment,
       ROUND(SUM(CASE WHEN qtr = 1 THEN line_revenue ELSE 0 END), 2) AS q1,
       ROUND(SUM(CASE WHEN qtr = 2 THEN line_revenue ELSE 0 END), 2) AS q2,
       ROUND(SUM(CASE WHEN qtr = 3 THEN line_revenue ELSE 0 END), 2) AS q3,
       ROUND(SUM(CASE WHEN qtr = 4 THEN line_revenue ELSE 0 END), 2) AS q4,
       ROUND(SUM(line_revenue), 2)                                  AS grand_total
FROM (
    SELECT c.segment,
           EXTRACT(QUARTER FROM o.order_date)                  AS qtr,
           oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100) AS line_revenue
    FROM order_items AS oi
    JOIN orders    AS o ON oi.order_id   = o.order_id
    JOIN customers AS c ON o.customer_id = c.customer_id
    WHERE o.status <> 'Cancelled'
) AS sales_lines
GROUP BY segment
ORDER BY segment;

/* The chapter shows:
      segment   |    q1     |    q2     |    q3     |    q4     | grand_total
   -------------+-----------+-----------+-----------+-----------+-------------
    Hospitality | 149040.00 | 252170.00 | 307277.50 | 435551.25 |  1144038.75
    Retail      | 394327.50 | 198473.75 | 333972.50 | 562000.00 |  1488773.75
    Wholesale   | 190944.00 | 275924.50 | 479039.00 | 756751.00 |  1702658.50
   (3 rows)
*/

