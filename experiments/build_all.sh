#!/bin/bash

for df in Dockerfile.* ; do
	echo "building $df"
	podman build . -t docker.io/trbecker/${df##*.}:latest -f ${df} $@ > /dev/null
done
