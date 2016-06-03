#!/bin/bash

#Shell script for controlling the daemon

if [ $1 == "start" ]; then
	echo 'starting...'
	nohup python -u ./server/server.py > ./server/server.log &
elif [ $1 == "stop" ]; then
	echo 'stopping...'
	killall 'python'
else
	echo 'nothing specified...'
fi


