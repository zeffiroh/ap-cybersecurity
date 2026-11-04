@echo off
setlocal
set "GITBASH=%ProgramFiles%\Git\bin\bash.exe"
if not exist "%GITBASH%" set "GITBASH=%LocalAppData%\Programs\Git\bin\bash.exe"
if not exist "%GITBASH%" (
  echo Git Bash was not found. Install Git for Windows from https://git-scm.com/download/win
  exit /b 1
)
"%GITBASH%" "%~dp0teach" %*
exit /b %ERRORLEVEL%
