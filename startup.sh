#!/bin/bash

NAME="app"
ROOTDIR=/home/pi/lawnwatcher
CODEDIR=/home/pi/lawnwatcher/rpi-irrigation-controller
NUM_WORKERS=4

echo "Starting $NAME"

cd $ROOTDIR

source bin/activate

cd $CODEDIR

gunicorn app:app -b 0.0.0.0:5000 \
  --name $NAME \
  --workers $NUM_WORKERS \
  --log-level="debug" \
  --timeout 60 \
  --access-logfile "/home/pi/debug.log" \
  --error-logfile "/home/pi/error.log" \
  --worker-class gevent
