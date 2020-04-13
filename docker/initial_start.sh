#!/bin/bash

#adjust to your needs
targetport="8888"
containername="covid19_eda"
#------------------------------------
imagename="ai2ys/jupyterlab:testeda"
workdir="/workspace"
username="$USER"
groupID="$(id -g)"
userID="$(id -u)"

cd `dirname $0`

docker run \
    --user $userID:$groupID \
    --env USER=${username} \
    --name ${containername} \
    --workdir=${workdir} \
    --volume $(realpath ../):${workdir}/ \
    --publish=8888:${targetport} \
    ${imagename}
