# Chapter 83, The Long Game (Closing): summary

**Rows:** 17 (6 content, 11 visual). Fixed and checked in the rebuilt PDF: 83.1, 83.2, 83.3, 83.6, V83.1, V83.2, V83.4, V83.7, V83.11. Checked, nothing to change here: 83.5 (Ch 67 already fixed). Already done by the style pass and rechecked: V83.3, V83.5, V83.6, V83.8, V83.9, V83.10. Left Open: 83.4 (no Glossary file exists yet).

**What changed**
- **The hours (T12).** §83.1's table is now exactly what `tools/hours_table.py` prints: **957–1193 hours** for Chapters 1 to 67, **394–488** to job-ready (15 to 19 months at 6 h/week), 3.1 to 3.8 years for the whole book. Parts 2–7 grew a lot in this build, so the chapter's argument was re-counted with code (`checks/ch83_numbers.py`): job-ready is now **two fifths** of the book (41%), not a quarter; the sprinter's 300 hours fall **94 to 188 hours short**, about the last seven to nine chapters of Part 2 (was "one to five chapters"); the steady reader reaches job-ready in weeks 66–81 and finishes in weeks 160–199. The crossover stays at week 50.
- **Figures.** Both redrawn at ≥ 7.19 pt from the same script. Figure 83.1 no longer repeats the table: it shows the book end to end with the job-ready mark and the years. Figure 83.2 uses dashed/solid lines and a hatched, labelled band, so it reads in greyscale; x-axis in years (0–208 weeks); side panel removed (it copied the table above it).
- **Meera's story** now matches Chapter 1 (joined as a sales coordinator; about a year, not five). No dates added.
- **D8.** The closing sections carry the standard names and stage order (Common mistakes · In the real world · Project with Tools you'll need · Recap · Key terms · Check yourself · Exercises · Where this leads). The closing lines sit under "### The map and the territory" inside Where this leads.
- **Cross-references** checked against the current files: Ch 7 (the posting), Ch 8, Ch 9 §9.1/9.3/9.6/9.7, Ch 11 (Power Query pack), Ch 16, Ch 20, Ch 25, Ch 26 §26.7/26.9/26.11, Ch 27 §27.1, Ch 28, Ch 32, Ch 49, Ch 64 §64.4, Ch 67, Ch 68, Part 8 (68–82).

**Skipped, and why**
- 83.4 (glossary): there is no Appendix A in the manuscript. Terms and draft definitions are in the questions file.
- The chapter number (83) and "Part 8, Chapters 68 to 82" stay until the D2 renumbering.

**Option picks:** 83.6 "change the pointer" (Ch 64 already has the content); V83.4 "own heading, kept with Where this leads"; V83.11 "ticks at years"; V83.7 "keep one", adapted: the table stays because of T12 and the figure was redrawn to show something else.

**Time needed:** was "about an hour to read"; now "about an hour to read, and 4–5 hours for the project, spread over one week" (the Monday-to-Sunday tasks: two hours on Saturday, the rest short). Ch 83 is not counted in the book's hours table.

**Verification:** no code blocks (verify_sql, verify_python, verify_shell: 0 run, 0 mismatches; check_code_teaching: 0 findings). fig_check: 0 figures under 7 pt. Build: 16 pages; layout_check clean (map 15/15, no stranded headings or lead-ins, no sparse pages, tofu 0; "coordinator" is "sales coordinator"); prescan clean.
