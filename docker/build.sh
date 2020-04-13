#!/bin/bash

tag="ai2ys/jupyterlab:covid19eda"

var="$1"
if [ ! -n "$var" ]
then
	user=$USER
else
	user=$var
fi

cd `dirname $0`
echo $PWD
docker build \
    --build-arg USER_NAME=$user \
    --build-arg USER_UID=$(id -u $user) \
    --build-arg USER_GID=$(id -g $user) \
    --file ./dockerfile --tag $tag .
