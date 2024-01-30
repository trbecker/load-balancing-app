#!/bin/bash

podman stop xapp 
podman stop gnb1 
podman stop gnb2 
podman stop gnb3 
podman stop gnb4 
podman stop gnb5
podman stop gnb6

sleep 5

mkdir -p results/$1

podman run -d --rm --name xapp --hostname xapp -v $PWD/results/$1:/data:z \
    --network podman docker.io/trbecker/admission-control-xapp:latest

sleep 1

for gnb in gnb1 gnb2 gnb3 gnb4 gnb5 gnb6 ; do
    podman run -d --rm --name $gnb --hostname $gnb --network podman \
        docker.io/trbecker/e2node:latest -i $gnb -s \
        $(podman inspect xapp -f '{{.NetworkSettings.IPAddress}}'):50101
done

sleep 1

for gnb in gnb1 gnb2 gnb3 gnb4 gnb5 gnb6 ; do
    echo "        'http://$(podman inspect $gnb -f '{{.NetworkSettings.IPAddress}}'):8081/v1',"
done
