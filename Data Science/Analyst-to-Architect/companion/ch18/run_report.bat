@echo off
REM Analyst to Architect - Chapter 18, section 18.18
REM The one line Windows Task Scheduler runs. Nothing clever on purpose: a scheduled job runs
REM with no console, no current directory you can rely on, and nobody watching it.

REM 1. Work in the script's own folder, whatever folder the scheduler started us in.
REM    %~dp0 is the drive and path of this .bat file, with a trailing backslash.
cd /d "%~dp0"

REM 2. Use the project's own Python by full path. Do NOT rely on PATH: a scheduled task runs
REM    with a minimal environment and will usually find a different Python, or none.
REM    Change this line to your own virtual environment.
set PYTHON=%~dp0..\..\.venv\Scripts\python.exe
if not exist "%PYTHON%" set PYTHON=python

REM 3. Run it. Arguments pass straight through, so the same .bat serves the scheduler and you.
"%PYTHON%" run_report.py %*

REM 4. Hand the exit code back to the scheduler, so a failure shows as a failure in its history
REM    rather than as a success that wrote nothing.
exit /b %ERRORLEVEL%
