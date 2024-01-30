#!/bin/bash -x

function pod_ip() {
    return podman inspect $1 -f '{{.NetworkSettings.IPAddress}}'
}

rm -fr experiment.db
./start_pod.sh Dockerfile.admission-control-xapp xapp -v $PWD:/data:z 
podman stop gnb1
sleep 1
podman run -d --rm --name gnb1 --hostname gnb1 --network podman docker.io/trbecker/e2node -i gnb1 -s $(podman inspect xapp -f '{{.NetworkSettings.IPAddress}}'):50101
sleep 1
podman exec sbrc-24 /usr/bin/python3 e2sim_client/e2sim_client.py connect http://$(podman inspect gnb1 -f '{{.NetworkSettings.IPAddress}}'):8081/v1 72401100000000001
