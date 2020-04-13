#!/bin/bash

#adjust to your needs
targetport="8888"
containername="covid19_eda"
#------------------------------------
imagename="ai2ys/jupyterlab:covid19eda"
workdir="/workspace"


var="$1"
if [ ! -n "$var" ]
then
	user=$USER
else
	user=$var
fi
cd `dirname $0`

docker run \
    --user $(id -u $user):$(id -g $user) \
    --env USER=${user} \
    --name ${containername} \
    --workdir=${workdir} \
    --volume $(realpath ../):${workdir}/ \
    --publish=8888:${targetport} \
    ${imagename}
