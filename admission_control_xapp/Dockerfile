FROM ubuntu:20.04

ARG RMR_VER=4.8.2

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
	python3 python3-pip build-essential cmake git \
	&& apt-get clean

RUN mkdir -p /playpen

RUN git clone "https://gerrit.o-ran-sc.org/r/ric-plt/lib/rmr" /playpen/rmr \
	&& cd /playpen/rmr \
	&& mkdir build \
	&& cd build \
	&& cmake .. \
	&& make \
	&& make install \
	&& cd /playpen \
	&& rm -fr /playpen/rmr \
	&& ldconfig

RUN pip install ricxappframe

COPY admission_control.py /playpen

RUN mkdir /etc/xapp

COPY init/routes.txt init/config-map.yaml init/config-file.json /etc/xapp/

ENV RMR_STG_SVC="9999" \
    RMR_SEED_RT="/etc/xapp/routes.txt" \
    CONFIG_MAP_NAME="/etc/xapp/config-map.yaml" \
    CONFIG_FILE="/etc/xapp/config-file.json" \
    SERVICE_RICXAPP_ADMISSION_CONTROL_XAPP_HTTP_PORT="8080" \
    SERVICE_RICXAPP_ADMISSION_CONTROL_XAPP_RMR_PORT="4560"
    

WORKDIR /playpen
CMD ["sleep", "1000000000"]
