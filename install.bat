@echo off
echo BEGINNING INSTALLATION...
call python -m venv venv
call .\venv\Scripts\activate
call pip install -r requirements.txt
echo INSTALLATION COMPLETE!
pause