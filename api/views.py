from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "/api/users",
        "/api/token",
        "/api/token/refresh",
        "/api/token/verify/",
        "/api/token/blacklist/",
    ]

    return Response(routes)
