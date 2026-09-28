# Chapter 15 companion files

For readers:

- `ch15_chart_data.xlsx`: one sheet for every chart in Chapter 15 (the sheet names are listed in the
  chapter's project, "Tools you'll need").
- `chart_data/*.csv`: the same tables as CSV files.
- `ch15_queries_mysql.sql`: the chapter's SQL in its MySQL 8.0 form (section 15.15).

For instructors and maintainers (not reader files; Chapter 15 comes before Python in the reading order):

- `build_ch15_data.py` rebuilds `ch15_chart_data.xlsx` and `chart_data/` from `../full/*.parquet`
  (Python 3.10+, pandas, pyarrow, openpyxl): `python3 build_ch15_data.py`. The output is deterministic.
- The chapter's figures are drawn by `figures/make_figs15.py` and `figures/make_figs15_diagrams.py` from
  `chart_data/`. The Python moved out of the chapter is parked for Chapter 18 in
  `manuscript/_parked/ch15-moved-out.md`.
