#!/bin/bash

if [ ! $(podman image exists ubuntu-protobuf-generator-cpp:20.04) ] ; then
    podman build . -f Dockerfile.generator -t ubuntu-protobuf-generator-cpp:20.04
fi

podman run -v $PWD:/src:z ubuntu-protobuf-generator-cpp:20.04 protoc -I . --grpc_out . --cpp_out=. --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` intent.proto
