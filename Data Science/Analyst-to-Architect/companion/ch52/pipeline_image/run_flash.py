"""Chapter 52 companion: run the Daily Sales Flash once, for one day, then exit.
With no --day it builds yesterday (India time), the day Chapter 46's 6:30 schedule builds.
The container's scheduler (section 52.8) starts it each morning; its exit code says whether it worked.
Riverstone Supplies is fictional; every name and number is invented."""
import argparse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from riverstone_pipeline import defs

parser = argparse.ArgumentParser(description="Run the Daily Sales Flash for one day.")
parser.add_argument("--day", help="the day to build, as YYYY-MM-DD (default: yesterday, India time)")
args = parser.parse_args()
yesterday = datetime.now(ZoneInfo("Asia/Kolkata")) - timedelta(days=1)
day = args.day or yesterday.strftime("%Y-%m-%d")

job = defs.resolve_job_def("daily_flash_job")
result = job.execute_in_process(partition_key=day, raise_on_error=False)
print(f"Flash for {day}:", "succeeded" if result.success else "FAILED")
raise SystemExit(0 if result.success else 1)
