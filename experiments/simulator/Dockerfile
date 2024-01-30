FROM docker.io/trbecker/envman-standalone:0.0.4

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    cmake build-essential autoconf libtool pkg-config git \
    libgrpc++-dev libprotobuf-dev protobuf-c-compiler \
    protobuf-compiler && apt-get clean

RUN rm -fr /playpen && mkdir /playpen
WORKDIR /playpen

RUN git clone --depth 1 https://github.com/trbecker/admission-control-grpc.git /acgrpc \
    && mkdir -p /acgrpc/client/build && cd /acgrpc/client/build && cmake .. && make && make install \
    && cd && rm -fr /acgrpc

COPY simulator.cpp CMakeLists.txt /playpen/
RUN mkdir /playpen/build && cd /playpen/build && cmake .. && make && make install

ENTRYPOINT [ "/usr/local/bin/simulator" ]