#!/bin/bash
groupID="$(id -g)"
userID="$(id -u)"
tag="ai2ys/jupyterlab:covid19eda"

cd `dirname $0`
echo $PWD
docker build \
    --build-arg USERNAME=$USER \
    --build-arg USER_UID=$userID \
    --build-arg USER_GID=$groupID \
    --file ./dockerfile --tag $tag .
