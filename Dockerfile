# Author: Cláudio Ferreira Carneiro
# LNLS - Brazilian Synchrotron Light Source Laboratory

FROM  ubuntu:18.04
LABEL maintainer="Claudio Carneiro <claudio.carneiro@lnls.br>"

RUN apt-get update &&\
    apt-get install -y --fix-missing\
        build-essential             \
        vim                         \
        libpcre3-dev                \
        wget                        \
        git                         \
        libreadline-gplv2-dev       

# IOC operation variables
ENV EPICS_VERSION R3.15.6
ENV ARCH linux-x86_64
ENV EPICS_HOST_ARCH linux-x86_64
ENV EPICS_BASE /opt/epics-${EPICS_VERSION}/base
ENV EPICS_MODULES /opt/epics-${EPICS_VERSION}/modules

ENV PATH ${EPICS_BASE}/bin/${ARCH}:/opt/procServ:${PATH}
ENV EPICS_CA_AUTO_ADDR_LIST YES


ENV CONS_IP 10.0.38.42
ENV CONS_REPO http://${CONS_IP}:20081/download

# set correct timezone
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Pyepics libca location
ENV PYEPICS_LIBCA ${EPICS_BASE}/lib/${ARCH}/libca.so

RUN mkdir -p /opt/epics-${EPICS_VERSION}

RUN wget -O /opt/epics-R3.15.6/base-3.15.6.tar.gz   \
    ${CONS_REPO}/EPICS/base-3.15.6.tar.gz

WORKDIR /opt/epics-${EPICS_VERSION}

# Epics Base
RUN cd /opt/epics-R3.15.6           &&\
    tar -xvzf base-3.15.6.tar.gz    &&\
    rm base-3.15.6.tar.gz           &&\
    mv base-3.15.6 base             &&\
    cd base                         &&\
    make -j 32

# Python3
RUN apt-get update  --fix-missing  &&\
    apt-get -y install swig        &&\
    apt-get -y install python3     &&\
    apt-get -y install python3-pip &&\
    pip3 install pyepics
