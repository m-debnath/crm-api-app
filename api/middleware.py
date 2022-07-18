import uuid

from django.conf import settings


class CustomHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        bp_header_name = settings.BUSINESS_PROCESS_HEADER
        request_meta_header = "HTTP_" + bp_header_name.upper().replace("-", "_")
        if request_meta_header in request.META.keys():
            response[bp_header_name] = request.META.get(request_meta_header)
        else:
            response[bp_header_name] = uuid.uuid4().hex
        return response
