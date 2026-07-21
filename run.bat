@echo off
cd /d %~dp0

python_embed\python.exe -m chainlit run main.py

pause