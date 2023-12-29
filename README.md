# yet-another-UI-for-AW
UI-client for ActivityWatch. Include a category editor and a viewer for multiple categorizations. 

## About
This is an experimental user interface client for ActivityWatch by using Jupyter notebook.
It provides a new features different from the original one.
It runs separately from the original GUI. So, it provides a new features without any change to your Activity Watch running on your computer.

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
Prerequisites :  ActivityWatch server and watcher running and poetry need to be installed.

1. Download the latest release [here](https://github.com/K-Kuyama/yet-another-UI-for-AW/releases).
2. Unzip as `yet-another-UI-for-AW` folder.
3. Go to `yet-another-UI-for-AW` folder
4. Run `poetry install`


## Start program

### Start from shell script

1. Go to `yet-another-UI-for-AW` folder
2. Run `poetry run ./start_ui.sh`

`start_ui.sh` calls [voila](https://github.com/voila-dashboards/voila) that turns Jupyter notebooks into standalone web applications.

### Start from Jupyter notebook
If you are familior with Jupyter notebook, you can call the program from Jupyter notebook. Start Jupyter notebook from `yet-another-UI-for-AW` folder, then select/run `DefEditorApp.ipynb` and `QtDashBoardApp.ipynb`.

## Usage
[Please refer from here](docs/USAGE.md)


