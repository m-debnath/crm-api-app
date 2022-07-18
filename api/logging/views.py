import json
import logging
import threading

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.logging.utils import log_performance_to_kafka

logger = logging.getLogger("requestlogs")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@log_performance_to_kafka
def log_to_kafka(request):
    kafka_entry = threading.local()
    kafka_entry.val = request.data
    t = threading.Thread(target=logger.info, args=(json.dumps(kafka_entry.val),))
    t.start()
    return Response(status=status.HTTP_200_OK)
