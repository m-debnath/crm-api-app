from uuid import uuid4

from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase


class APIMiddlewareTestCase(APITestCase):
    def test_custom_header_in_response_ok(self):
        # Inputs
        endpoint = "/api/"
        custom_header_name = "HTTP_" + settings.BUSINESS_PROCESS_HEADER.upper().replace("-", "_")
        custom_header_value = uuid4().hex

        # Expected outputs
        expected_response_status = status.HTTP_200_OK

        # Execute
        response = self.client.get(endpoint, None, **{custom_header_name: custom_header_value})

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
        self.assertEquals(response.headers["X-Crm-Api-Bpid"], custom_header_value)
