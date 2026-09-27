# Chapter 16 — page review checklist

Before publishing any Power BI page:

**Numbers**
- [ ] Every card matches a SQL query you ran (`ch16_checks_postgresql.sql`).
- [ ] The parts add to the whole: region bars + "Region missing" = the card total.
- [ ] Orders use `DISTINCTCOUNT` on the order key, not the row count.
- [ ] Cancelled orders are excluded once, in one documented place.
- [ ] Ratios use `DIVIDE`, and totals of ratios are recomputed, not summed.

**Model**
- [ ] Star schema; keys hidden; fields renamed to business language; formats set.
- [ ] Date table marked, whole years, month sorted by month number, Auto date/time off.
- [ ] Relationships one-way from dimensions to facts unless a pattern needs otherwise.

**Design (Chapter 15)**
- [ ] The page answers one question; the headline is visible in ten seconds.
- [ ] Bars sorted and starting at zero; direct labels instead of legends.
- [ ] One highlight color; theme applied; palette checked for color vision deficiency.
- [ ] Titles state findings; units and exclusions stated in subtitles.
- [ ] Alt text on every visual; tab order set; mobile layout built.

**Delivery**
- [ ] Published to a shared workspace, not "My workspace".
- [ ] Credentials use a service account; refresh scheduled after the source load; failure alerts to a team address.
- [ ] Roles tested with View as and Test as role against a known total.
- [ ] Last-refresh timestamp on the page; an "About this report" page with sources, exclusions, and definitions.
- [ ] Licences confirmed for every reader.
