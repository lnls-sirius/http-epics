#!/usr/bin/env python3
import time
import argparse
import logging
import urllib.parse
import requests
import json
import threading

from datetime import datetime
from requests.exceptions import HTTPError
from epics import PV

def format_severity(severity):
    if severity== 0:
        return 'OK'
    elif severity== 1:
        return 'MINOR'
    elif severity== 2:
        return 'MAJOR'
    elif severity== 3:
        return 'INVALID'

def format_ts(ts):
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def http_pub_val(pvname, payload):
    p2 = urllib.parse.quote('{}/{}'.format(pvname, payload))
    return requests.get(url='{}/{}'.format(PUB, p2))

def http_set_val(pvname, payload):
    p2 = urllib.parse.quote('{}/{}'.format(pvname, payload))
    return requests.get(url='{}/{}'.format(SET, p2))

def post_cb(**kwargs):
    try:
        pvname = kwargs['pvname']
        payload = json.dumps({
            'value':kwargs['value'],
            'units':kwargs['units'],
            'severity':format_severity(kwargs['severity']),
            'timestamp':format_ts(kwargs['timestamp']),
            'host':kwargs['host'],
            'status':kwargs['status'],
        })
        response = http_pub_val(pvname, payload)
        response.raise_for_status()

        response = http_set_val(pvname, payload)
        response.raise_for_status()
    except HTTPError as http_err:
        logger.exception('HTTP error occurred: {}'.format(http_err))  # Python 3.6
    except Exception as err:
        logger.exception('Other error occurred: {}'.format(err))  # Python 3.6
    else:
        pass

def load_pvs():
    pvs = []
    with open('PV.txt', 'r') as f_:
        for pv in f_.readlines():
            pvs.append(pv)
    return set(pvs)

class Manager():
    def __init__(self, pvs_list=[], **kwargs):
        self.pvs = {}
        for pv in pvs_list:
            self.pvs[pv] = PV(pv, callback=post_cb)
        
        self.info_worker = threading.Thread(
            target=self.update_info, daemon=True)
        self.info_worker.start()
        logger.info('Managing {} '.format(self.pvs.imtems
        ))


    def update_info(self):
        logger.info('PV info thread start')
        while True:
            for pvname ,pv in self.pvs.items():
                print(pvname, pv.get_ctrlvars())
            time.sleep(10)
        logger.info('PV info thread finish')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EPICS interface')
    parser.add_argument('--host', required=True, help='Server ip')
    parser.add_argument('--port', required=True, help='Server port', type=int)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format='[%(levelname)s] %(asctime)-15s %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')
    logger = logging.getLogger()

    URL = 'http://{}:{}'.format(args.host, args.port)
    SET = URL + '/SET'
    POST = URL + '/POST'
    PUB = URL + '/PUBLISH'

    manager = Manager(pvs_list=load_pvs())

    while True:
        time.sleep(1)
