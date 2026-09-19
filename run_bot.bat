@echo off
REM Run the sentiment bot. Double-click-safe: always cds to this folder first.
setlocal
cd /d %~dp0
if "%1"=="dashboard" (
  shift
  streamlit run sentiment_bot\dashboard.py %*
) else if "%1"=="scheduler" (
  shift
  python -m sentiment_bot.scheduler %*
) else if "%1"=="cli" (
  shift
  python -m sentiment_bot.cli %*
) else (
  python -m sentiment_bot.cli %*
)
