#!/bin/bash

for df in Dockerfile.* ; do
	echo "building $df"
	podman build . -t docker.io/trbecker/${df##*.}:0.0.1 -f ${df} $@ > /dev/null
done
