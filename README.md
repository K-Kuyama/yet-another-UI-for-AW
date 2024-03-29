# yet-another-UI-for-AW
UI-client for ActivityWatch. Include a category editor and a viewer for multiple categorizations. 


## About
This is an experimental user interface client for ActivityWatch by using Jupyter notebook.
It provides a new features different from the original one.
It runs separately from the original GUI. So, it provides a new features without any change to your Activity Watch running on your computer.

<img src="docs/DefEditor_small.png" height="300">

<img src="docs/DashBoard_small.png" height="300">

## Features

### Multi categorization :
- Can be categorized from the different viewpoints.For example, 
	- from the "work" viewpoint : "Documentation","Programing","Meeting",etc.	
	- from the "project" viewpoint : "Project A", "Project B", etc.

### Easy configuration :
- Key-word base categorization
- Exact match for the window title 

### Internationalization and some Japanese localization :
- Added a feature to extract words from Japanese text.

### Unicode Normalization :
- Normalize keywords, by "NFC" and "NFD" to match both of “combined character sequence” and “precomposed character”  of unicode strings. 

## Installation

*You need Python environment and poetry for prerequisites.*  
*If you are Windows(64bit) user and not familiar with Python, try ["All-in-one package"](#all-in-one-package-for-windows-64bit).*

Prerequisites :  ActivityWatch server and watcher running and poetry need to be installed.

1. Download the latest release [here](https://github.com/K-Kuyama/yet-another-UI-for-AW/releases).
2. Unzip as `yet-another-UI-for-AW` folder.
3. Go to `yet-another-UI-for-AW` folder
4. Run `poetry install`


## Start program

### Start from shell script

1. Go to `yet-another-UI-for-AW` folder
2. Run `poetry run ./start_ui.sh` for Mac, `poetry run ./start_ui.bat` for Windows.

`start_ui.sh` calls [voila](https://github.com/voila-dashboards/voila) that turns Jupyter notebooks into standalone web applications.

### Start from Jupyter notebook
If you are familior with Jupyter notebook, you can call the program from Jupyter notebook. Start Jupyter notebook from `yet-another-UI-for-AW` folder, then select/run `DefEditorApp.ipynb` and `QtDashBoardApp.ipynb`.


##All-in-one package for Windows-64bit

Prerequisites :  ActivityWatch server and watcher running

The follosing instructions for installation.

1. Go to [the latest release page](https://github.com/K-Kuyama/yet-another-UI-for-AW/releases).
2. Download All-in-one module `yet-another-UI-for-AW-x.x.x-forWin64.zip` 
3. Unzip the zip file at any folder you like.

To start program, just click `aw_ya.bat` icon From Exploler 


## Usage
[Please refer from here](docs/USAGE.md)


