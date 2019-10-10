#!/usr/bin/env python3

from pcaspy import SimpleServer, Driver
import random

prefix = 'MTEST:'
pvdb = {
    'RAND' : {
        'prec' : 3,
        'scan' : 0.1,
        'egu':'rand'
    },
}

class myDriver(Driver):
    def __init__(self):
        super(myDriver, self).__init__()

    def read(self, reason):
        if reason == 'RAND':
            value = random.random()
        else:
            value = self.getParam(reason)
        return value

if __name__ == '__main__':
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()

    # process CA transactions
    while True:
        server.process(0.1)
