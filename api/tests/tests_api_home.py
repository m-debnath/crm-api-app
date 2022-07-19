from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase


class APIHomePageTestCase(APITestCase):
    def test_api_home_get_ok(self):
        # Inputs
        endpoint = "/api/"

        # Expected outputs
        expected_response_status = status.HTTP_200_OK
        expected_output = [
            "/api/token",
            "/api/token/refresh",
            "/api/admin/users",
            "/api/logging",
            "/api/users",
        ]
        expected_output = sorted(expected_output)

        # Execute
        response = self.client.get(endpoint)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
        self.assertEquals(sorted(response.data), expected_output)

    def test_api_home_html_get_ok(self):
        # Inputs
        endpoint = "/api/"
        custom_accept_header_name = "HTTP_ACCEPT"
        custom_accept_header_value = "text/html"

        # Expected outputs
        expected_response_status = status.HTTP_200_OK
        expected_text_in_response_html = settings.APP_NAME

        # Execute
        response = self.client.get(
            endpoint, None, **{custom_accept_header_name: custom_accept_header_value}
        )

        # Verify
        text_found = expected_text_in_response_html in response.content.decode("utf-8")
        self.assertEquals(response.status_code, expected_response_status)
        self.assertEquals(text_found, True)

    def test_api_home_post_not_allowed(self):
        # Inputs
        endpoint = "/api/"
        data = {}

        # Expected Outputs
        expected_response_status = status.HTTP_405_METHOD_NOT_ALLOWED

        # Execute
        response = self.client.post(endpoint, data=data)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
