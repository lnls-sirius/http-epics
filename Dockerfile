# Author: Cláudio Ferreira Carneiro
# LNLS - Brazilian Synchrotron Light Source Laboratory

FROM  python:3.8.0-slim-buster
LABEL maintainer="Claudio Carneiro <claudio.carneiro@lnls.br>"

ENV DEBIAN_FRONTEND noninteractive
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
        vim libpcre3-dev wget git libreadline-gplv2-dev tzdata && rm -rf /var/lib/apt/lists/* && \
        dpkg-reconfigure --frontend noninteractive tzdata

# IOC operation variables
ENV EPICS_VERSION R3.15.6
ENV ARCH linux-x86_64
ENV EPICS_HOST_ARCH linux-x86_64
ENV EPICS_BASE /opt/epics-${EPICS_VERSION}/base
ENV EPICS_MODULES /opt/epics-${EPICS_VERSION}/modules
ENV PATH ${EPICS_BASE}/bin/${ARCH}:${PATH}
ENV EPICS_CA_AUTO_ADDR_LIST YES
ENV CONS_IP 10.0.38.42
ENV CONS_REPO http://${CONS_IP}:20081/download

# Pyepics libca location
ENV PYEPICS_LIBCA ${EPICS_BASE}/lib/${ARCH}/libca.so

RUN mkdir -p /opt/epics-${EPICS_VERSION}

WORKDIR /opt/epics-${EPICS_VERSION}
# Epics Base
RUN wget -O /opt/epics-R3.15.6/base-3.15.6.tar.gz ${CONS_REPO}/EPICS/base-3.15.6.tar.gz &&\
        cd /opt/epics-R3.15.6 && tar -xvzf base-3.15.6.tar.gz && rm base-3.15.6.tar.gz &&\
        mv base-3.15.6 base && cd base && make -j 32

# Python3
RUN pip3 install pyepics requests

WORKDIR /opt

COPY interface.py interface.py
COPY PV.txt PV.txt

CMD python /opt/interface.py --host ${SRV_HOST:-10.128.255.5} --port ${SRV_PORT:-7379}
