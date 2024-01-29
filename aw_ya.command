#!/bin/zsh
trap killall SIGINT

killall(){
  echo 'good bye'
  kill 0
}

SHELL_DIR=$(cd $(dirname $0) && pwd)

$SHELL_DIR/.venv/bin/python $SHELL_DIR/aw_ya_launcher.py $SHELL_DIR/DefEditorApp.ipynb &
$SHELL_DIR/.venv/bin/python $SHELL_DIR/aw_ya_launcher.py $SHELL_DIR/QtDashBoardApp.ipynb &

wait
