import datetime
import json
import logging
import socket

from django.conf import settings
from requestlogs.storages import LoggingStorage

logger = logging.getLogger("requestlogs")


class KafkaStorage(LoggingStorage):
    def store(self, entry):
        kafka_entry = {}

        response_code = entry.response.status_code
        response_data = json.dumps(entry.response.data)
        print(response_data)

        # Skip logging in certain conditions
        if (
            response_code == 401
            and "AccessToken" in response_data
            and "token_not_valid" in response_data
        ) or (
            response_code == 405
            and "GET" in response_data
            and "not allowed" in response_data
        ):
            return None

        print(response_code)
        print("AccessToken" in response_data)
        print("token_not_valid" in response_data)

        kafka_entry["host"] = socket.gethostname()
        kafka_entry["host_ip"] = socket.gethostbyname(socket.gethostname())

        kafka_entry["id"] = entry.request.request_id
        kafka_entry["request_path"] = entry.request.full_path

        if kafka_entry["request_path"].startswith("/api"):
            kafka_entry["event_type"] = "api"
        else:
            kafka_entry["event_type"] = "admin_site"
        kafka_entry["@timestamp"] = datetime.datetime.utcnow().isoformat()
        kafka_entry["msecs"] = round(entry.execution_time.total_seconds() * 1000)
        try:
            kafka_entry["username"] = entry.user["username"]
        except AttributeError:
            kafka_entry["username"] = "None"

        kafka_entry["http_method"] = entry.request.method

        bp_header_name = settings.BUSINESS_PROCESS_HEADER
        kafka_entry["bp_id"] = entry.response.response.headers.get(bp_header_name)

        kafka_entry["request_headers"] = json.dumps(entry.request.request_headers)
        kafka_entry["request_query_params"] = json.dumps(entry.request.query_params)
        kafka_entry["request_data"] = json.dumps(entry.request.data)

        kafka_entry["response_code"] = response_code
        kafka_entry["response_headers"] = str(entry.response.response.headers)
        kafka_entry["response_data"] = response_data

        kafka_entry["env_code"] = settings.DJANGO_ENV

        logger.info(json.dumps(kafka_entry))
