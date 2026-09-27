# Pre-publication refresh list

Facts in approved chapters that go out of date. Before publication (and before any new edition), re-check each against its source, update the chapter, rerun its check script, and rebuild the PDF. Part chats: add new items through your status report; the coordinator keeps this file.

| Chapter | Section | What to refresh | Source | Retrieved | Check script |
|---|---|---|---|---|---|
| 6 | 6.2, 6.3 | Tool versions and install methods: PostgreSQL 18, MySQL 9.7 LTS, DBeaver 26.2, Python 3.13/3.14 (3.15 due 1 Oct 2026), Git 2.55, Power BI Desktop (Store, Windows only), Excel for the web free tier, end of free desktop preview | official sites (listed in `planning/parts/part-0-status.md`) | 17 Sep 2026 | `companion/ch06/check_setup.py` |
| 6 | 6.6 | Rounding behavior quotes (PostgreSQL, MySQL, Python docs) | official docs | 17 Sep 2026 | verify_sql / verify_python |
| 4 | Spreadsheet links | `RRI` availability in Excel and Google Sheets | Microsoft Support, Google Docs Editors Help | 16 Sep 2026 | `companion/ch04/make_ch04_workbook.py` |
| 3 | 3.3 | Example product names for ERP, CRM, HRMS, e-commerce, support desks | vendor sites | 16 Sep 2026 | — |
| 7 | 7.7 | Stack Overflow Developer Survey AI figures (2025: 84% use or plan to use; 46% distrust vs 33% trust). **Update when 2026 results are published.** | survey.stackoverflow.co | 16 Sep 2026 | `checks/ch07_check.py` |
| 7 | 7.7 | World Economic Forum Future of Jobs Report 2025 (fastest-growing and declining roles) | weforum.org | 16 Sep 2026 | — |
| 8 | 8.6, exercises 6–7 | PayScale India (Data Analyst, Data Scientist, Data Engineer) and Indeed India (Data Analyst) salary figures | payscale.com, in.indeed.com | 16 Sep 2026 | `checks/ch08_check.py` |
| 12 | 12.3, 12.16 | MySQL LTS version and install steps (9.7 LTS; 8.0 end of life); spot-check companion files on MySQL 9.7 (tested on 8.0.46) | dev.mysql.com | 16 Sep 2026 | `tools/verify_sql.py` |
| 28 | 28.4–28.9 | PostgreSQL 18 and MySQL 9.7 LTS behavior for `MERGE`, `CYCLE`, partial and covering indexes, and the shape of query plans | official docs | 18 Sep 2026 | `tools/verify_sql.py`, `checks/ch28_check.py` |
| 28 | 28.12 | Flyway edition and command names (`info`, `validate`, `repair`); Liquibase and Alembic descriptions | Redgate docs | 18 Sep 2026 | — |
| 29 | Tools | uv 0.12.15, pandas 3.0.5, pytest 9.1.1, mypy 2.3.1, requests 2.34.2; Python 3.13/3.14 behavior | PyPI, official docs | 18 Sep 2026 | `checks/ch29_check.py` |
| 32 | Tools, 32.3 | dbt Core version, dbt Cloud pricing, SQLFluff rules | getdbt.com, sqlfluff docs | 18 Sep 2026 | `checks/ch32_check.py` |
| 34 | 34.2, 34.9 | WSL install command, macOS GNU-tool differences, `ss` vs `netstat` availability | Microsoft Learn, man pages | 18 Sep 2026 | `tools/verify_shell.py` |
| 30 | 30.11 | Experiment platform names and feature claims | vendor sites | 18 Sep 2026 | — |
| 31 | 31.9 | Causal inference package names and versions (DoWhy, EconML, CausalPy) | PyPI | 18 Sep 2026 | `checks/ch31_check.py` |
| 35–44 | Tools | Library versions: NumPy 2.4.4, pandas 3.0.2, scikit-learn 1.8.0 (current release 1.9.1 at the time of writing), SciPy 1.17.1; PyTorch for Chapter 43 | PyPI, scikit-learn docs | 18 Sep 2026 | `checks/ch3*_check.py`, `checks/ch4*_check.py` |
| 35 | 35.7 | Google Sheets statistical function names (`BINOM.DIST`, `NORM.DIST`, `POISSON.DIST`, `COVARIANCE.S`) | support.google.com/docs | 17 Sep 2026 | — |
| 36 | 36.5 | scikit-learn `TargetEncoder` behavior (cross-fitting in `fit_transform`) | scikit-learn docs | 17 Sep 2026 | `checks/ch36_check.py` |
| 52 | all | **Run the chapter's Dockerfile, Kubernetes manifest, Terraform configuration and GitHub Actions workflow on a real cloud account**, or state in the chapter that they are parser-validated and unexecuted. The only unverified chapter in the book | - | 19 Sep 2026 | `checks/ch52_check.py` |
| 52 | 52.7 | Cloud pricing for the compute and storage estimate | provider pricing pages | 19 Sep 2026 | `checks/ch52_check.py` |
| 45-52 | Tools | DuckDB 1.5.5, psycopg2 2.9.13, requests 2.33.1, Dagster and Airflow versions, Spark, Kafka, Terraform and Docker versions | official docs | 19 Sep 2026 | `checks/ch4*_check.py`, `checks/ch5*_check.py` |
| 45 | 45.11 | DPDP Act 2023 and GDPR wording on web data, and the "not legal advice" framing | official sources | 16 Sep 2026 | - |
| 45 | 45.6 | PostgreSQL logical decoding setup steps by OS (tested on Ubuntu 24.04 only) | PostgreSQL docs | 16 Sep 2026 | - |

