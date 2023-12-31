#!/bin/bash

CONTAINER_NAME=localhost:5001/admission-control
VERSION=0.0.2

(docker build -t ${CONTAINER_NAME}:latest .
docker tag ${CONTAINER_NAME}:latest ${CONTAINER_NAME}:${VERSION}
docker push ${CONTAINER_NAME}:latest
docker push ${CONTAINER_NAME}:${VERSION}) >&2

echo ${VERSION}
