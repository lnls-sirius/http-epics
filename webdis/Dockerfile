FROM centos:7 AS stage
MAINTAINER Claudio Ferreira Carneiro <claudiofcarneiro@hotmail.com>

RUN yum update -y && yum install -y epel-release && yum update
RUN yum install -y add wget make gcc libevent-devel msgpack-devel musl-devel
RUN wget https://github.com/nicolasff/webdis/archive/0.1.10.tar.gz -O webdis-0.1.10.tar.gz
RUN tar -xvzf webdis-0.1.10.tar.gz
RUN cd webdis-0.1.10 && make && make install && cd ..
RUN sed -i -e 's/"daemonize":.*true,/"daemonize": false,/g' /etc/webdis.prod.json

# main image
FROM centos:7
RUN yum update -y && yum install -y epel-release && yum update
RUN yum install -y libevent msgpack redis
COPY --from=stage /usr/local/bin/webdis /usr/local/bin/
COPY --from=stage /etc/webdis.prod.json /etc/webdis.prod.json
RUN echo "daemonize yes" >> /etc/redis.conf
RUN sed -i -e 's/^bind .*/bind 0.0.0.0/g' /etc/redis.conf
CMD /usr/bin/redis-server /etc/redis.conf && /usr/local/bin/webdis /etc/webdis.prod.json

EXPOSE 7379
