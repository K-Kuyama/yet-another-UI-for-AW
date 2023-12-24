#!/bin/zsh
trap killall SIGINT

killall(){
  echo 'good bye'
  kill 0
}

voila DefEditorApp.ipynb &
sleep 5
voila QtDashBoardApp.ipynb &

wait
