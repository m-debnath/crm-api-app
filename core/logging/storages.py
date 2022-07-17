import logging
import json
import datetime
import socket

from django.conf import settings
from requestlogs.storages import LoggingStorage

logger = logging.getLogger("requestlogs")


class KafkaStorage(LoggingStorage):
    def store(self, entry):
        kafka_entry = {}

        kafka_entry["host"] = socket.gethostname()
        kafka_entry["host_ip"] = socket.gethostbyname(socket.gethostname())

        kafka_entry["id"] = entry.request.request_id
        kafka_entry["event_type"] = "api_log"
        kafka_entry["request_path"] = entry.request.full_path
        kafka_entry["@timestamp"] = datetime.datetime.utcnow().isoformat()
        kafka_entry["msecs"] = round(entry.execution_time.total_seconds() * 1000)
        try:
            kafka_entry["username"] = entry.user["username"]
        except AttributeError:
            kafka_entry["username"] = "None"

        kafka_entry["http_method"] = entry.request.method
        kafka_entry["request_headers"] = json.dumps(entry.request.request_headers)

        bp_header_name = settings.BUSINESS_PROCESS_HEADER
        kafka_entry["bp_id"] = entry.response.response.headers.get(bp_header_name)

        kafka_entry["request_query_params"] = json.dumps(entry.request.query_params)
        kafka_entry["request_data"] = json.dumps(entry.request.data)
        kafka_entry["response_code"] = entry.response.status_code
        kafka_entry["response_data"] = json.dumps(entry.response.data)
        kafka_entry["env_code"] = settings.DJANGO_ENV

        logger.info(json.dumps(kafka_entry))
