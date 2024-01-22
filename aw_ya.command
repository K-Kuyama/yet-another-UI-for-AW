#!/bin/zsh
trap killall SIGINT

killall(){
  echo 'good bye'
  kill 0
}

SHELL_DIR=$(cd $(dirname $0) && pwd)

$SHELL_DIR/.venv/bin/voila $SHELL_DIR/DefEditorApp.ipynb &
sleep 5
$SHELL_DIR/.venv/bin/voila $SHELL_DIR/QtDashBoardApp.ipynb &

wait
