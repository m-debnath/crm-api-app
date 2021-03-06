from core.logging.utils import log_performance_to_kafka
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
@log_performance_to_kafka
def getRoutes(request):
    routes = [
        "/api/token",
        "/api/token/refresh",
        "/api/admin/users",
        "/api/logging",
        "/api/users",
    ]
    return Response(routes)
