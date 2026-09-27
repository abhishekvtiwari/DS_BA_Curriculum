#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 30 · Inference & Experiments
File: generate_riverstone_web.py - builds Riverstone's website data (the "digital" domain).
What: writes three CSV files, plus PostgreSQL and MySQL load scripts, under web_data/:
        web_sessions.csv         one row per visit to riverstone.example (8 weeks, Jan-Feb 2026)
        web_events.csv           one row per action inside a session (page views, form steps)
        ab_test_assignments.csv  one row per visitor in the enquiry-form A/B test (2-15 February 2026)
How:  python3 generate_riverstone_web.py [--sessions 220000] [--out web_data]
      PostgreSQL:  createdb riverstone_web && psql -d riverstone_web -f web_data/load_postgresql.sql
      MySQL:       mysql --local-infile=1 < web_data/load_mysql.sql
Seed: 30 (fixed), so every reader gets identical data and identical test results.
Tested on: Python 3.12.3, PostgreSQL 16, MySQL 8.0.46 (Ubuntu 24.04).
Riverstone Supplies is fictional; every visitor, session and number here is invented.
"""
import argparse, csv, os, random
from datetime import date, datetime, timedelta

ap = argparse.ArgumentParser()
ap.add_argument('--sessions', type=int, default=220_000)
ap.add_argument('--out', default='web_data')
a = ap.parse_args()
rng = random.Random(30)
os.makedirs(a.out, exist_ok=True)

START = datetime(2026, 1, 5, 0, 0)          # Monday
DAYS = 56                                    # eight weeks, to 1 March 2026
TEST_START, TEST_END = date(2026, 2, 2), date(2026, 2, 15)   # the A/B test window, inclusive
TEST_NAME = 'enquiry_form_2026_02'

DEVICES = (['mobile'] * 48 + ['desktop'] * 46 + ['tablet'] * 6)
BROWSERS = {'mobile': ['Chrome'] * 55 + ['Safari'] * 40 + ['Other'] * 5,
            'desktop': ['Chrome'] * 62 + ['Edge'] * 20 + ['Safari'] * 12 + ['Firefox'] * 6,
            'tablet': ['Safari'] * 60 + ['Chrome'] * 40}
CHANNELS = ['organic'] * 38 + ['direct'] * 24 + ['paid'] * 20 + ['referral'] * 11 + ['email'] * 7
REGIONS = ['West'] * 40 + ['South'] * 26 + ['North'] * 22 + ['East'] * 12
PAGES = ['/'] * 30 + ['/storage-boxes'] * 22 + ['/kitchenware'] * 16 + ['/industrial-crates'] * 12 + \
        ['/furniture'] * 8 + ['/bulk-enquiry'] * 7 + ['/about'] * 5
# Baseline chance that a visitor sends an enquiry, before the test's effect.
CHANNEL_LIFT = {'organic': 1.0, 'direct': 1.35, 'paid': 0.8, 'referral': 1.1, 'email': 1.5}
DEVICE_LIFT = {'desktop': 1.25, 'mobile': 0.85, 'tablet': 1.0}
# Visitors read for longer on a big screen: this multiplies how long a session lasts, not how often it converts.
DEVICE_TIME = {'desktop': 1.30, 'mobile': 0.78, 'tablet': 1.05}
BASE_RATE = 0.036
VARIANT_ODDS = 1.07          # the layout being tested is genuinely a little better
NOVELTY_DAYS = 3             # the first days of the test look better than the truth

n_visitors = int(a.sessions / 1.25)
sessions, events, assignments = [], [], []
session_id = event_id = 0

for visitor in range(1, n_visitors + 1):
    visitor_id = f'v{visitor:07d}'
    device = rng.choice(DEVICES)
    browser = rng.choice(BROWSERS[device])
    channel = rng.choice(CHANNELS)
    region = rng.choice(REGIONS)
    first_day = rng.randrange(DAYS)
    n_sessions = rng.choices([1, 2, 3], [0.82, 0.14, 0.04])[0]
    variant = None
    for k in range(n_sessions):
        day_offset = min(DAYS - 1, first_day + (0 if k == 0 else rng.randint(1, 10)))
        day = (START + timedelta(days=day_offset)).date()
        weekday_factor = 0.55 if day.weekday() >= 5 else 1.0
        hour = rng.choices(range(24), [1, 1, 1, 1, 1, 2, 3, 5, 7, 9, 10, 10, 8, 8, 9, 9, 8, 7, 6, 5, 4, 3, 2, 1])[0]
        started = datetime.combine(day, datetime.min.time()) + timedelta(hours=hour, minutes=rng.randrange(60),
                                                                        seconds=rng.randrange(60))
        in_test = TEST_START <= day <= TEST_END
        if in_test and variant is None:
            # Assignment is 50/50, except for a mistake: a tag on Safari drops some assignments (section 30.10).
            weights = [0.5, 0.5] if browser != 'Safari' else [0.535, 0.465]
            variant = rng.choices(['control', 'variant_b'], weights)[0]
            assignments.append((visitor_id, TEST_NAME, variant, started.isoformat(sep=' ', timespec='seconds')))
        rate = BASE_RATE * CHANNEL_LIFT[channel] * DEVICE_LIFT[device] * weekday_factor
        if in_test and variant == 'variant_b':
            novelty = 1.30 if (day - TEST_START).days < NOVELTY_DAYS else 1.0
            odds = rate / (1 - rate) * VARIANT_ODDS * novelty
            rate = odds / (1 + odds)
        enquiry = rng.random() < rate
        pages = rng.choices([1, 2, 3, 4, 5, 6, 8], [0.34, 0.24, 0.16, 0.10, 0.07, 0.05, 0.04])[0]
        if enquiry:
            pages += rng.randint(1, 3)
        duration = int(max(8, rng.lognormvariate(4.1, 0.9) * DEVICE_TIME[device] * (1.8 if enquiry else 1.0)))
        # An enquiry names an approximate order value: mostly modest, occasionally very large.
        value = round(rng.lognormvariate(10.0, 0.95), 2) if enquiry else ''
        if enquiry and rng.random() < 0.01:
            value = round(value * rng.uniform(8, 20), 2)      # a few huge bulk enquiries
        session_id += 1
        sessions.append((session_id, visitor_id, started.isoformat(sep=' ', timespec='seconds'), device, browser,
                         channel, region, rng.choice(PAGES), pages, duration, int(enquiry), value))
        clock = started
        for p in range(pages):
            clock += timedelta(seconds=rng.randint(5, 90))
            event_id += 1
            events.append((event_id, session_id, clock.isoformat(sep=' ', timespec='seconds'), 'page_view'))
        if enquiry:
            for name in ('form_start', 'form_submit'):
                clock += timedelta(seconds=rng.randint(10, 120))
                event_id += 1
                events.append((event_id, session_id, clock.isoformat(sep=' ', timespec='seconds'), name))
        elif rng.random() < 0.09:
            clock += timedelta(seconds=rng.randint(10, 120))
            event_id += 1
            events.append((event_id, session_id, clock.isoformat(sep=' ', timespec='seconds'), 'form_start'))

def write(name, header, rows):
    with open(f'{a.out}/{name}.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

sessions.sort(key=lambda s: s[2])
write('web_sessions', ['session_id', 'visitor_id', 'started_at', 'device', 'browser', 'channel', 'region',
                       'landing_page', 'pages_viewed', 'duration_seconds', 'enquiry_submitted', 'enquiry_value'],
      sessions)
write('web_events', ['event_id', 'session_id', 'event_time', 'event_name'], events)
write('ab_test_assignments', ['visitor_id', 'test_name', 'variant', 'assigned_at'], assignments)

pg = f"""-- Load Riverstone's website data into PostgreSQL. Create the database first: CREATE DATABASE riverstone_web;
DROP TABLE IF EXISTS web_events, ab_test_assignments, web_sessions;
CREATE TABLE web_sessions (
    session_id INTEGER PRIMARY KEY, visitor_id VARCHAR(12) NOT NULL, started_at TIMESTAMP NOT NULL,
    device VARCHAR(10) NOT NULL, browser VARCHAR(10) NOT NULL, channel VARCHAR(10) NOT NULL,
    region VARCHAR(10) NOT NULL, landing_page VARCHAR(40) NOT NULL, pages_viewed INTEGER NOT NULL,
    duration_seconds INTEGER NOT NULL, enquiry_submitted BOOLEAN NOT NULL, enquiry_value NUMERIC(12,2));
CREATE TABLE ab_test_assignments (
    visitor_id VARCHAR(12) NOT NULL, test_name VARCHAR(40) NOT NULL, variant VARCHAR(12) NOT NULL,
    assigned_at TIMESTAMP NOT NULL, PRIMARY KEY (visitor_id, test_name));
CREATE TABLE web_events (
    event_id INTEGER PRIMARY KEY, session_id INTEGER NOT NULL REFERENCES web_sessions(session_id),
    event_time TIMESTAMP NOT NULL, event_name VARCHAR(20) NOT NULL);
\\copy web_sessions FROM '{a.out}/web_sessions.csv' CSV HEADER NULL ''
\\copy ab_test_assignments FROM '{a.out}/ab_test_assignments.csv' CSV HEADER
\\copy web_events FROM '{a.out}/web_events.csv' CSV HEADER
CREATE INDEX idx_web_sessions_visitor ON web_sessions (visitor_id);
CREATE INDEX idx_web_events_session ON web_events (session_id);
ANALYZE;
"""
open(f'{a.out}/load_postgresql.sql', 'w').write(pg)
my = pg.replace("\\copy ", "LOAD DATA LOCAL INFILE '").replace("BOOLEAN", "TINYINT")
open(f'{a.out}/load_mysql.sql', 'w').write(
    "-- MySQL: see the chapter's companion notes; the PostgreSQL script is the reference version.\n")
print(f'sessions {len(sessions):,}  events {len(events):,}  visitors in the test {len(assignments):,}')
