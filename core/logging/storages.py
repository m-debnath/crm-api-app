import datetime
import json
import logging
import socket

from django.conf import settings
from requestlogs.storages import LoggingStorage

logger = logging.getLogger("requestlogs")


class MyKafkaStorage(LoggingStorage):
    def store(self, entry):
        request_path = entry.request.full_path
        response_code = entry.response.status_code
        response_data = json.dumps(entry.response.data)

        # Skip logging in certain conditions
        if (
            (
                response_code == 401
                and "AccessToken" in response_data
                and "token_not_valid" in response_data
            )
            or (
                response_code == 405
                and "GET" in response_data
                and "not allowed" in response_data
            )
            or (response_code == 200 and "/api/token/refresh/" in request_path)
        ):
            return None

        host = socket.gethostname()
        host_ip = socket.gethostbyname(socket.gethostname())

        _id = entry.request.request_id

        if request_path.startswith("/api"):
            event_type = "api"
        else:
            event_type = "admin"

        msecs = round(entry.execution_time.total_seconds() * 1000)

        username = ""
        try:
            username = (
                entry.user["username"] if entry.user["username"] is not None else ""
            )
        except AttributeError:
            pass

        http_method = entry.request.method

        bp_header_name = settings.BUSINESS_PROCESS_HEADER
        bp_id = entry.response.response.headers.get(bp_header_name)

        request_headers = json.dumps(entry.request.request_headers)
        request_query_params = json.dumps(entry.request.query_params)
        request_data = json.dumps(entry.request.data)
        response_headers = str(entry.response.response.headers)

        kafka_entry = {
            "host": host,
            "host_ip": host_ip,
            "id": _id,
            "request_path": request_path,
            "event_type": event_type,
            "@timestamp": datetime.datetime.utcnow().isoformat(),
            "msecs": msecs,
            "username": username,
            "http_method": http_method,
            "bp_id": bp_id,
            "request_headers": request_headers,
            "request_query_params": request_query_params,
            "request_data": request_data,
            "response_code": response_code,
            "response_headers": response_headers,
            "response_data": response_data,
            "env_code": settings.DJANGO_ENV,
        }

        logger.info(json.dumps(kafka_entry))
