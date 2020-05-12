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
    --rm \
    --tty \
    --user $USER \
    --env USER=${user} \
    --name ${containername} \
    --workdir=${workdir} \
    --volume $(realpath ../):${workdir}/ \
    --publish=${targetport}:8888 \
    ${imagename}

    #--user $(id -u $user):$(id -g $user) \
