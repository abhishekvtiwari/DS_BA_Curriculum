# Data spec: Riverstone machine sensor readings (`riverstone-sensors`)

**Built by:** Part IV (first used in Chapter 40). **Planned reuse:** Ch 48 (big data; `--full`), Ch 50 (streaming).
**Generator:** `companion/generate_riverstone_sensors.py` · **Seed:** 20241 + machine number · **Output:** default `companion/sensors/machine_readings_week.csv` (10,080 rows, one machine, one week); `--full` writes `machine_readings_full.parquet` (12 machines × 40 weeks = 4,838,400 rows, ~5M as the blueprint asks). The one-week file is exactly machine M01's first week of the full run.
**Tested:** Python 3.12.3, NumPy 2.4.4, pandas 3.0.2 (18 Sep 2026). The full run takes a few minutes and needs pyarrow.

## Columns
timestamp (one-minute) · machine_id (M01–M12) · temperature_c · pressure_bar · cycle_seconds · status (running / stopped)

## Planted structure
Barrel temperature around 215 °C (+2 °C per machine number step), a ±1.5% day-shift warm-up cycle, a slow drift of +0.02 °C per day, and AR(1) noise (coefficient 0.8, sd 0.6). Pressure ≈ 118 bar + 0.15 × temperature deviation + noise 1.5; cycle time ≈ 18.5 s + 0.03 × temperature deviation + noise 0.25.
**Every week, every machine:** one heater fault (temperature ramps +12 °C over 50 minutes, then decays over 40), one pressure spike (3 readings, +25–40 bar), one stoppage (20–60 minutes; status stopped, pressure 0, cycle NaN). Sensor glitches: 0.2% of temperature readings missing.

## Week-one facts used in Chapter 40 (M01)
Stoppage Wed 22:02–22:33 (32 min) · heater fault peaks Wed 22:53 at 225.2 °C; z-score there only +2.8 (rolling 2-hour z-score misses it); slow-baseline rule (24-hour median, > 6 °C for 10 minutes) fires Wed 22:51 · pressure spikes Tue 12:00–12:02 · 18 missing temperature readings.

## Consistency
Machine IDs M01–M12 are new (the teaching databases don't model machines). New Riverstone fact for the coordinator: 12 injection-moulding machines logging one-minute sensor data from March 2025.
