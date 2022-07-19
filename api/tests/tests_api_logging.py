from datetime import datetime
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class APILoggingTestCase(APITestCase):
    def setUp(self):
        # Inputs
        username = settings.TEST_USER
        password = settings.TEST_USER_PASSWORD
        self.user = User.objects.create_user(username=username, password=password)
        self.token = AccessToken.for_user(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    def test_logging_example_get_ok(self):
        # Inputs
        endpoint = "/api/logging/"

        # Expected outputs
        expected_response_status = status.HTTP_200_OK
        expected_output = {
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
        }

        # Execute
        response = self.client.get(endpoint)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
        self.assertEquals(response.data, expected_output)

    def test_logging_example_get_unauthorized(self):
        # Inputs
        endpoint = "/api/logging/"

        # Expected outputs
        expected_response_status = status.HTTP_401_UNAUTHORIZED

        # Execute
        self.client.force_authenticate(user=None)
        response = self.client.get(endpoint)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)

    def test_logging_create_post_ok(self):
        # Inputs
        endpoint = "/api/logging/"
        data = {
            "host": "user-agent",
            "host_ip": "user-ip",
            "id": uuid4().hex,
            "event_type": "api",
            "@timestamp": datetime.utcnow().isoformat(),
            "env_code": "development",
            "func_name": "testing.logging.create",
            "username": "mukudebn",
        }

        # Expected outputs
        expected_response_status = status.HTTP_201_CREATED

        # Execute
        response = self.client.post(endpoint, data=data)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)

    def test_logging_create_post_unauthorized(self):
        # Inputs
        endpoint = "/api/logging/"
        data = {
            "host": "user-agent",
            "host_ip": "user-ip",
            "id": uuid4().hex,
            "event_type": "api",
            "@timestamp": datetime.utcnow().isoformat(),
            "env_code": "development",
            "func_name": "testing.logging.create",
            "username": "mukudebn",
        }

        # Expected outputs
        expected_response_status = status.HTTP_401_UNAUTHORIZED

        # Execute
        self.client.force_authenticate(user=None)
        response = self.client.post(endpoint, data=data)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
