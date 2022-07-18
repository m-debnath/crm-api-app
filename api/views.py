from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.logging.utils import log_performance_to_kafka


@api_view(["GET"])
@log_performance_to_kafka
def getRoutes(request):
    routes = [
        "/api/token",
        "/api/token/refresh",
        "/api/admin/users",
        "/api/users",
    ]
    return Response(routes)
