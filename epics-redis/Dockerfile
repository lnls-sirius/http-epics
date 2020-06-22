# Author: Cláudio Ferreira Carneiro
# LNLS - Brazilian Synchrotron Light Source Laboratory
FROM lnlscon/epics-r3.15.8:v1.0
LABEL maintainer="Claudio Carneiro <claudio.carneiro@lnls.br>"
ENV TZ America/Sao_Paulo
RUN date
# Python3
WORKDIR /opt

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY interface.py interface.py
COPY PV.txt PV.txt

CMD python /opt/interface.py --host ${SRV_HOST:-10.128.255.5} --port ${SRV_PORT:-7379} --db ${SRV_DB:-0}
