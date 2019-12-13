FROM lnlscon/epics-r3.15.6:v1.2
RUN mkdir -p /opt/conv-ioc
WORKDIR /opt/conv-ioc
COPY Makefile Makefile
COPY ConvApp ConvApp
COPY iocBoot iocBoot
COPY configure configure
RUN make -j 16
CMD /usr/local/bin/procServ -L - -f --chdir /opt/conv-ioc/iocBoot/iocConv ${PORT} ./st.cmd
