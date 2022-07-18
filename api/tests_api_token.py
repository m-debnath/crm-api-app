from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase


class APITokenTestCase(APITestCase):
    def test_token_obtain_pair_ok(self):
        # Inputs
        endpoint = "/api/token/"
        username = settings.TEST_USER
        password = settings.TEST_USER_PASSWORD
        data = {"username": username, "password": password}

        # Expected outputs
        expected_response_status = status.HTTP_200_OK
        expected_response_keys = ["access", "refresh"]
        expected_response_keys = sorted(expected_response_keys)

        # Execute
        response = self.client.post(endpoint, data=data)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
        self.assertEquals(sorted(list(response.data.keys())), expected_response_keys)

    def test_token_obtain_pair_unauthorized(self):
        # Inputs
        endpoint = "/api/token/"
        username = "no_match"
        password = "n0_Ma8ch"
        data = {"username": username, "password": password}

        # Expected outputs
        expected_response_status = status.HTTP_401_UNAUTHORIZED

        # Execute
        response = self.client.post(endpoint, data=data)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)

    def test_token_refresh_ok(self):
        # Inputs
        endpoint_1 = "/api/token/"
        endpoint_2 = "/api/token/refresh/"
        username = settings.TEST_USER
        password = settings.TEST_USER_PASSWORD
        data = {"username": username, "password": password}

        # Expected Outputs
        expected_response_status = status.HTTP_200_OK
        expected_response_keys = ["access", "refresh"]
        expected_response_keys = sorted(expected_response_keys)

        # Execute
        response = self.client.post(endpoint_1, data=data)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
        self.assertEquals(sorted(list(response.data.keys())), expected_response_keys)

        # Execute
        refresh_token = response.data["refresh"]
        data = {"refresh": refresh_token}
        response = self.client.post(endpoint_2, data=data)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
        self.assertEquals(sorted(list(response.data.keys())), expected_response_keys)

    def test_token_refresh_invalid(self):
        # Inputs
        endpoint = "/api/token/refresh/"
        refresh_token = "invalid_refresh_token"
        data = {"refresh": refresh_token}

        # Expected Outputs
        expected_response_status = status.HTTP_401_UNAUTHORIZED

        # Execute
        response = self.client.post(endpoint, data=data)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)

    def test_token_refresh_rotate(self):
        # Inputs
        endpoint_1 = "/api/token/"
        endpoint_2 = "/api/token/refresh/"
        username = settings.TEST_USER
        password = settings.TEST_USER_PASSWORD
        data = {"username": username, "password": password}

        # Expected Outputs
        expected_response_status = status.HTTP_200_OK
        expected_response_keys = ["access", "refresh"]
        expected_response_keys = sorted(expected_response_keys)

        # Execute
        response = self.client.post(endpoint_1, data=data)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
        self.assertEquals(sorted(list(response.data.keys())), expected_response_keys)

        # Execute
        refresh_token = response.data["refresh"]
        data = {"refresh": refresh_token}
        response = self.client.post(endpoint_2, data=data)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
        self.assertEquals(sorted(list(response.data.keys())), expected_response_keys)

        # Execute
        refresh_token = response.data["refresh"]
        data = {"refresh": refresh_token}
        response = self.client.post(endpoint_2, data=data)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
        self.assertEquals(sorted(list(response.data.keys())), expected_response_keys)

    def test_token_refresh_blacklist(self):
        # Inputs
        endpoint_1 = "/api/token/"
        endpoint_2 = "/api/token/refresh/"
        username = settings.TEST_USER
        password = settings.TEST_USER_PASSWORD
        data = {"username": username, "password": password}

        # Expected Outputs
        expected_token_success_status = status.HTTP_200_OK
        expected_token_failure_status = status.HTTP_401_UNAUTHORIZED
        expected_response_keys = ["access", "refresh"]
        expected_response_keys = sorted(expected_response_keys)

        # Execute
        response = self.client.post(endpoint_1, data=data)

        # Verify
        self.assertEquals(response.status_code, expected_token_success_status)
        self.assertEquals(sorted(list(response.data.keys())), expected_response_keys)

        # Execute
        refresh_token = response.data["refresh"]
        data = {"refresh": refresh_token}
        response = self.client.post(endpoint_2, data=data)

        # Verify
        self.assertEquals(response.status_code, expected_token_success_status)
        self.assertEquals(sorted(list(response.data.keys())), expected_response_keys)

        # Execute
        data = {"refresh": refresh_token}
        response = self.client.post(endpoint_2, data=data)

        # Verify
        self.assertEquals(response.status_code, expected_token_failure_status)
