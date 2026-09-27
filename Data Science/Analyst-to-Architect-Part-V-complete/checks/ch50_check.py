# Analyst to Architect - Chapter 50 checks. Run from the book root:
#   PYTHONPATH=companion/ch50 python3 checks/ch50_check.py      (needs the Chapter 48 sensor data)
# Riverstone Supplies is fictional; every name and number is invented.
import os, sys
os.chdir('companion/ch50'); sys.path.insert(0, '.')
import sensor_events as se
from mini_log import MessageLog
ok=True
def check(label,got,exp):
    global ok; good=(got==exp); ok&=good
    print(('OK  ' if good else 'FAIL'),label,got,'' if good else f'(expected {exp})')
first = se.batch(600, minute_from=0, minute_to=1)
check('first batch events', len(first), 300)
check('25 machines x 6 readings x 2 minutes', 25*6*2, 300)
log = MessageLog("check_log", partitions=2, reset=True)
for e in first: log.produce(e["machine_id"], e)
check('partition sizes', log.end_offsets(), {0: 144, 1: 156})
check('M-07 partition', log.partition_for("M-07"), 1)
msgs, offs = log.consume("g")
check('messages read', len(msgs), 300)
check('above 205 C', sum(1 for m in msgs if m["value"]["temperature_c"] > 205.0), 82)
log.commit("g", offs)
check('no re-read after commit', len(log.consume("g")[0]), 0)
late = se.batch(50, minute_from=2, minute_to=2, machine="M-07")
check('late events for M-07 in minute 2', len(late), 6)
check('window 00:00-00:05 Bhiwandi on time', 15*6*5, 450)
check('window with late events', 450+6, 456)
# watermark arithmetic from 50.5 and exercise 7
import datetime as dt
wm = lambda newest: (dt.datetime.fromisoformat(newest) - dt.timedelta(minutes=10)).strftime("%H:%M:%S")
check('watermark after batch 2', wm("2025-12-01 00:19:50"), "00:09:50")
check('watermark after batch 3', wm("2025-12-01 00:29:50"), "00:19:50")
check('Ex9 files per day at 30s', 2*60*24, 2880)
import shutil; shutil.rmtree("check_log", ignore_errors=True)
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
