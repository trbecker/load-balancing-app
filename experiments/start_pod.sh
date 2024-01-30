#!/bin/bash -x

DOCKERFILE=$1; shift
NAME=$1 ; shift

CONTAINER=docker.io/trbecker/${DOCKERFILE##*.}:latest

podman stop $NAME &
STOP_PID=$!
podman build . -t $CONTAINER -f $DOCKERFILE
wait ${STOP_PID}
podman run --rm -d --name $NAME --network podman --hostname $NAME $@ $CONTAINER
podman inspect $NAME -f '{{.NetworkSettings.IPAddress}}'
