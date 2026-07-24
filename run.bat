@echo off
cd /d %~dp0

embed\python_embed\python.exe -m chainlit run main.py

pause