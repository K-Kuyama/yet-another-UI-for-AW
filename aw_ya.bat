@echo off
 
echo %~dp0

set fpath=%~dp0
set PATH=%fpath%.venv\Scripts;%PATH%
echo %PATH%


start python.exe %fapath%aw_ya_launcher.py %fapath%DefEditorApp.ipynb
start python.exe %fapath%aw_ya_launcher.py %fapath%QtDashBoardApp.ipynb
