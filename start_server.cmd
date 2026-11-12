@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start_server.ps1" %*
exit /b %errorlevel%
