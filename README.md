# yet-another-UI-for-AW
UI for ActivityWatch. Include category editor and viewer for multiple categorizations. 

## About
This is an experimental user interface for ActivityWatch by using Jupyter notebook.
It provides a new web GUI different from the original, but ActivityWatch's server and watcher can still be used as they are.
Of course, you can also use the original GUI of ActivityWatch as it is.

## Feature

### Multi categorization :
- Can be categorized from the different viewpoints.For example, 
	- from the "work" viewpoint : "Documentation","Programing","Meeting",etc.	
	- from the "project" viewpoint : "Project A", "Project B", etc.

### Easy configuration :
- Key-word base categorization
- Exact match for the window title 

### Internationaraization and some Japanese localozation :
- Added a feature to extract words from Japanese text.

### Unicode Normalization :
- Neormalize keywords, by "NFC" and "NFD" unicode normailzation

## Installation
Prerequisites :  ActivityWatch server and watcher running and poetry need to be installed.

1. Download the latest release [here](https://github.com/K-Kuyama/yet-another-UI-for-AW/releases).
2. Unzip as `yet-another-UI-for-AW` folder.
3. Go to `yet-another-UI-for-AW` folder
4. Run `poetry install`


## Start program

1. Go to `yet-another-UI-for-AW` folder
2. Run `poetry run ./start_ui.sh`

`start_ui.sh` calls [voila](https://github.com/voila-dashboards/voila) that turns Jupyter notebooks into standalone web applications.
If you want to call the program from Jupyter notebook, just select/run 'DefEditorApp.ipynb' and 'QtDashBoardApp.ipynb'.

## Usage
[Please refer from here](docs/USAGE.md)

