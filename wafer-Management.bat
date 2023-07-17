@echo off

pwd
start cmd /k python app.py
timeout /t 5
start chrome http://localhost:3000

exit