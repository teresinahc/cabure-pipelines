#!/bin/bash

NETWORK=luigi
WORKDIR=/usr/src/app
ENVIRONMENT="PYTHONPATH=${WORKDIR}"
LOCAL_PATH=/root
VOLUME_LUIGICFG=$LOCAL_PATH/luigi.cfg:$WORKDIR/luigi.cfg
VOLUME_DATA=$LOCAL_PATH/cabure-data:$WORKDIR/data
IMAGE_NAME=teresinahackerclube/cabure-pipeline
TASK=DumpMonthSpendsTask
PARAMS="--validity `date +'%Y-%m'`"
COMMAND="luigi --module cabure $TASK $PARAMS"

COMPLETE_COMMAND="docker run --network $NETWORK --env $ENVIRONMENT -v $VOLUME_LUIGICFG -v $VOLUME_DATA $IMAGE_NAME $COMMAND"

echo "Running '${COMPLETE_COMMAND}'..."

$COMPLETE_COMMAND