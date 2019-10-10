#!/usr/bin/env python3
import time
import logging
import urllib.parse
import requests
import json

from requests.exceptions import HTTPError
from epics import PV

pvs = ['MTEST:RAND']
URL = 'http://10.0.6.48:7379'
SET = URL + '/SET'
POST = URL + '/POST'
PUB = URL + '/PUBLISH'

logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] %(asctime)-15s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger()


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
            'severity':kwargs['severity'],
            'timestamp':kwargs['timestamp'],
            'host':kwargs['host'],
            'status':kwargs['status'],
        })
        response = http_pub_val(pvname, payload)
        response.raise_for_status()

        response = http_set_val(pvname, payload)
        response.raise_for_status()
    except HTTPError as http_err:
        logger.exception(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        logger.exception(f'Other error occurred: {err}')  # Python 3.6
    else:
        pass#logger.info('Success !{}'.format(payload))

if __name__ == '__main__':
    for pv in pvs:
        PV(pv, callback=post_cb)

    while True:
        time.sleep(1)
