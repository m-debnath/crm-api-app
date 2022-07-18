import datetime
import functools
import json
import logging
import socket
import threading
import uuid
from time import monotonic_ns
from resource import getrusage, RUSAGE_SELF

from django.conf import settings
from django.http import HttpRequest
from rest_framework.request import Request

logger = logging.getLogger("requestlogs")


def log_performance_to_kafka(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            mem_before = getrusage(RUSAGE_SELF).ru_maxrss
        except OSError:
            mem_before = -1
            pass

        start_timer = monotonic_ns()
        return_value = func(*args, **kwargs)
        stop_timer = monotonic_ns()

        try:
            mem_after = getrusage(RUSAGE_SELF).ru_maxrss
        except OSError:
            mem_after = -1
            pass

        if mem_before != -1 and mem_after != -1:
            username = ""
            for arg in args:
                if isinstance(arg, Request) or isinstance(arg, HttpRequest):
                    username = getattr(arg.user, "username", "")
                    break
            mem_usage = mem_after - mem_before
            duration = round((stop_timer - start_timer) / 1_000_000)
            kafka_entry = threading.local()
            kafka_entry.val = {
                "host": socket.gethostname(),
                "host_ip": socket.gethostbyname(socket.gethostname()),
                "id": uuid.uuid4().hex,
                "event_type": "perf",
                "@timestamp": datetime.datetime.utcnow().isoformat(),
                "env_code": settings.DJANGO_ENV,
                "func_name": f"{func.__module__}.{func.__qualname__}",
                "mem_before_kb": mem_before,
                "mem_after_kb": mem_after,
                "mem_usage_kb": mem_usage,
                "msecs": duration,
                "username": username,
            }
            t = threading.Thread(
                target=logger.info, args=(json.dumps(kafka_entry.val),)
            )
            t.start()
        return return_value

    return wrapper


def log_error_to_kafka(*args, **kwargs):
    kafka_entry = threading.local()
    kafka_entry.val = {
        "host": socket.gethostname(),
        "host_ip": socket.gethostbyname(socket.gethostname()),
        "id": uuid.uuid4().hex,
        "event_type": "error",
        "@timestamp": datetime.datetime.utcnow().isoformat(),
        "env_code": settings.DJANGO_ENV,
        "func_name": kwargs.get("func_name"),
        "error_message": kwargs.get("error_message"),
        "username": kwargs.get("username"),
    }
    t = threading.Thread(target=logger.info, args=(json.dumps(kafka_entry.val),))
    t.start()
