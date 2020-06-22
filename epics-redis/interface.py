#!/usr/bin/env python3
import time
import argparse
import logging
import urllib.parse
import requests
import json
import threading
import redis

from datetime import datetime
from requests.exceptions import HTTPError
from epics import PV


def format_severity(severity):
    if severity == 0:
        return "OK"
    elif severity == 1:
        return "MINOR"
    elif severity == 2:
        return "MAJOR"
    elif severity == 3:
        return "INVALID"


def format_ts(ts):
    #return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def load_pvs():
    pvs = []
    with open("PV.txt", "r") as f_:
        for pv in f_.readlines():
            pvs.append(pv.replace("\n", ""))
    return set(pvs)


class RedisManager:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        # @todo: Consider using a blocking connection pool
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
        logger.info("RedisManager: Connected at {}:{} db {}".format(host, port, db))

    def getPoolConn(self) -> redis.Redis:
        return redis.Redis(connection_pool=self.pool)

    def pub_val(self, pvname: str, payload: str):
        self.getPoolConn().publish(pvname.encode("utf-8"), payload.encode("utf-8"))

    def set_val(self, pvname: str, payload: str):
        self.getPoolConn().set(pvname.encode("utf-8"), payload.encode("utf-8"))


class Manager:
    def __init__(self, redis_manager, pvs_list=[], **kwargs):
        self.pvs = {}
        self.redis_manager = redis_manager
        for pv in pvs_list:
            try:
                self.pvs[pv] = PV(pv, callback=self.post_cb)
                logger.info('Manager: Connected to PV "{}"'.format(pv))
            except:
                logger.exception('Manager: Unable to create PV "{}"'.format(pv))

        self.info_worker = threading.Thread(target=self.update_info, daemon=True)
        self.info_worker.start()

    def update_info(self):
        logger.info("Manager: PV info thread start.")
        while True:
            for pvname, pv in self.pvs.items():
                pv.get_ctrlvars()
            time.sleep(10)
        logger.info("Manager: PV info thread finish")

    def post_cb(self, **kwargs):
        pvname = kwargs["pvname"]
        try:
            payload = json.dumps(
                {
                    "value": kwargs["value"],
                    "units": kwargs["units"],
                    "severity": format_severity(kwargs["severity"]),
                    "timestamp": format_ts(kwargs["timestamp"]),
                    "host": kwargs["host"],
                    "status": kwargs["status"],
                    "precision": kwargs["precision"],
                }
            )
            self.redis_manager.pub_val(pvname, payload)
            self.redis_manager.set_val(pvname, payload)
        except Exception as err:
            logger.exception(
                "Manager Post Callback: Failed to handle callback of {}: {}".format(
                    pvname, err
                )
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EPICS interface")
    parser.add_argument("--host", required=True, help="Redis host")
    parser.add_argument("--port", help="Redis port", type=int, default=6379)
    parser.add_argument("--db", help="Redis db", type=int, default=0)
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)-15s %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )
    logger = logging.getLogger()

    redis_manager = RedisManager(args.host, args.port, args.db)
    manager = Manager(redis_manager=redis_manager, pvs_list=load_pvs())

    while True:
        time.sleep(1)
