@echo off
 
echo %~dp0

set fpath=%~dp0
set PATH=%fpath%python-3.11.7-embed;%PATH%
echo %PATH%


start python.exe %fpath%aw_ya_launcher.py %fpath%DefEditorApp.ipynb
start python.exe %fpath%aw_ya_launcher.py %fpath%QtDashBoardApp.ipynb
