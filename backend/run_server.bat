@echo off
cd /d "%~dp0"
echo Starting Django server...
venv\Scripts\python.exe manage.py runserver
