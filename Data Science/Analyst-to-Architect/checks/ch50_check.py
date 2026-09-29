# Analyst to Architect - Chapter 50 checks. Run from the book root (needs the Chapter 48 sensor data):
#   python3 checks/ch50_check.py
# Recomputes the chapter's numbers independently of the printed outputs.
# Riverstone Supplies is fictional; every name and number is invented.
import os, sys, shutil, datetime as dt
os.chdir('companion/ch50'); sys.path.insert(0, '.')
import sensor_events as se
from mini_log import MessageLog
ok = True
def check(label, got, exp):
    global ok; good = (got == exp); ok &= good
    print(('OK  ' if good else 'FAIL'), label, got, '' if good else f'(expected {exp})')

first = se.readings(0, 2)
check('first two minutes: events', len(first), 300)
check('25 machines x 6 readings x 2 minutes', 25 * 6 * 2, 300)
check('first event time', first[0]['event_time'], '2025-12-01 00:00:00')
check('last event time', first[-1]['event_time'], '2025-12-01 00:01:50')
log = MessageLog("check_log", partitions=2, reset=True)
for e in first: log.produce(e["machine_id"], e)
check('partition sizes', log.end_offsets(), {0: 144, 1: 156})
parts = [log.partition_for(f"M-{i:02d}") for i in range(1, 26)]
check('machines per partition (answer 4)', (parts.count(0), parts.count(1)), (12, 13))
check('12 x 12 and 13 x 12', (12 * 12, 13 * 12), (144, 156))
check('M-07 partition', log.partition_for("M-07"), 1)
check('figure 50.1: M-04, M-08 in 0; M-07, M-21 in 1',
      [log.partition_for(m) for m in ("M-04", "M-08", "M-07", "M-21")], [0, 0, 1, 1])
msgs, offs = log.consume("g")
check('messages read', len(msgs), 300)
check('above 205 C', sum(1 for m in msgs if m["value"]["temperature_c"] > 205.0), 82)
check('hot readings have unique machine + event time',
      len({m["key"] + m["value"]["event_time"] for m in msgs if m["value"]["temperature_c"] > 205.0}), 82)
log.commit("g", offs)
check('committed offsets are whole numbers', log.committed("g"), {0: 144, 1: 156})
check('no re-read after commit', len(log.consume("g")[0]), 0)
shutil.rmtree("check_log", ignore_errors=True)

check('late M-07 readings in minute 2', len(se.readings(2, 3, machine="M-07")), 6)
check('late M-09 readings in minute 2', len(se.readings(2, 3, machine="M-09")), 6)
check('ten minutes of readings', len(se.readings(0, 10)), 1500)
plants = {e["machine_id"]: e["plant"] for e in first}
check('M-07 and M-09 are at Bhiwandi Main', (plants["M-07"], plants["M-09"]), ("Bhiwandi Main", "Bhiwandi Main"))
check('Bhiwandi machines', sum(1 for p in plants.values() if p == "Bhiwandi Main"), 15)
check('window 00:00-00:05 Bhiwandi on time', 15 * 6 * 5, 450)
check('window with late events', 450 + 6, 456)
check('Chakan window', 10 * 6 * 5, 300)

# watermark arithmetic (hand table, figure 50.2, answers 6 and 7)
wm = lambda newest: (dt.datetime.fromisoformat(newest) - dt.timedelta(minutes=10)).strftime("%H:%M:%S")
check('watermark after run 1', wm("2025-12-01 00:09:50"), "23:59:50")
check('watermark after run 2', wm("2025-12-01 00:19:50"), "00:09:50")
check('watermark after run 3', wm("2025-12-01 00:29:50"), "00:19:50")
check('run 3 input rows', 1500 + 6, 1506)
check('state after batch 4: 5 open windows x 2 plants', 5 * 2, 10)
check('state after batch 5: 3 open windows x 2 plants', 3 * 2, 6)

# the three kinds of window, by hand (section 50.5)
t = [1, 3, 4, 7, 13, 14, 21, 22]
tumbling = {s: sum(1 for x in t if s <= x < s + 5) for s in range(0, 25, 5)}
check('tumbling counts', {k: v for k, v in tumbling.items() if v}, {0: 3, 5: 1, 10: 2, 20: 2})
sliding = {s: sum(1 for x in t if s <= x < s + 10) for s in range(-5, 25, 5)}
check('sliding counts', sliding, {-5: 3, 0: 4, 5: 3, 10: 2, 15: 2, 20: 2})
check('sliding counts each reading twice', sum(sliding.values()), 16)
sessions, cur = [], [t[0]]
for x in t[1:]:
    if x - cur[-1] < 5: cur.append(x)
    else: sessions.append(cur); cur = [x]
sessions.append(cur)
check('sessions (start, end, count)', [(s[0], s[-1] + 5, len(s)) for s in sessions], [(1, 12, 4), (13, 19, 2), (21, 27, 2)])

check('Ex 9 files per day at 30 s', 2 * 60 * 24, 2880)
check('readings per machine per day', 86400 // 10, 8640)
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
