
import asyncio
import socket
import getpass
import logging
import time
import datetime
from functools import wraps
from typing import Callable

from influxdb_access import InfluxDB_Access

log = logging.getLogger(__name__)


def instrument(tool_name: str):

    host = socket.gethostname()
    user = getpass.getuser()

    def decorate(fn: Callable):

        if asyncio.iscoroutinefunction(fn):

            @wraps(fn)
            async def aw(*args, **kwargs):

                data_ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                t0 = time.perf_counter()

                try:
                    return await fn(*args, **kwargs)
                finally:

                    dur_ms = (time.perf_counter() - t0) * 1000.0

                    data_dict = {
                        "measurement": "mcp_tool",
                        "tags": {
                            "hostname": host,
                            "username": user,
                            "tool": tool_name
                        },
                        "fields": {
                            "duration_ms": dur_ms
                        },
                        "time": data_ts
                    }

                    status, output = InfluxDB_Access.write_points(data_dict)
                    if not status:
                        log.error("write_points failed: %s", output)

            return aw

        else:

            @wraps(fn)
            def sw(*args, **kwargs):

                data_ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                t0 = time.perf_counter()

                try:
                    return fn(*args, **kwargs)
                finally:

                    dur_ms = (time.perf_counter() - t0) * 1000.0

                    data_dict = {
                        "measurement": "mcp_tool",
                        "tags": {
                            "hostname": host,
                            "username": user,
                            "tool": tool_name
                        },
                        "fields": {
                            "duration_ms": dur_ms
                        },
                        "time": data_ts
                    }

                    status, output = InfluxDB_Access.write_points(data_dict)
                    if not status:
                        log.error("write_points failed: %s", output)

            return sw

    return decorate
