import json
import logging
import threading

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.logging.utils import log_performance_to_kafka

logger = logging.getLogger("requestlogs")


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
@log_performance_to_kafka
def log_to_kafka(request):
    if request.method == "POST":
        kafka_entry = threading.local()
        kafka_entry.val = request.data
        t = threading.Thread(target=logger.info, args=(json.dumps(kafka_entry.val),))
        t.start()
        return Response(status=status.HTTP_201_CREATED)
    else:
        # Sample message for post
        return Response(
            {
                "host": "user-agent",
                "host_ip": "user-ip",
                "id": "fec724450e154cc88587cd55865ec667",
                "event_type": "ui|ui-error",
                "@timestamp": "2022-07-18T17:04:31.038Z",
                "env_code": "development",
                "func_name": "react.component.method.name",
                "request_path": "/your/app/name",
                "username": "username",
                "details": "this is a sample logging message for post request",
            },
            status=status.HTTP_200_OK,
        )
