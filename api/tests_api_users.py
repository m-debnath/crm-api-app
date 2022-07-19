from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class APIUsersTestCase(APITestCase):
    def setUp(self):
        # Inputs
        username = settings.TEST_USER
        password = settings.TEST_USER_PASSWORD
        self.user = User.objects.create_user(username=username, password=password)
        self.query_user = User.objects.create_user(username="query_user", password="password")
        self.token = AccessToken.for_user(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    def test_users_self_get_ok(self):
        # Inputs
        endpoint = f"/api/users/{self.user.id}/"

        # Expected outputs
        expected_response_status = status.HTTP_200_OK
        expected_user_name = self.user.username

        # Execute
        response = self.client.get(endpoint)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
        self.assertEquals(response.data["username"], expected_user_name)

    def test_users_not_self_get_forbidden(self):
        # Inputs
        endpoint = f"/api/users/{self.query_user.id}/"

        # Expected outputs
        expected_response_status = status.HTTP_403_FORBIDDEN

        # Execute
        response = self.client.get(endpoint)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)

    def test_users_get_unauthorized(self):
        # Inputs
        endpoint_1 = f"/api/users/{self.user.id}/"
        endpoint_2 = "/api/users/"

        # Expected outputs
        expected_response_status = status.HTTP_401_UNAUTHORIZED

        # Execute
        self.client.force_authenticate(user=None)
        response = self.client.get(endpoint_1)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)

        # Execute
        self.client.force_authenticate(user=None)
        response = self.client.get(endpoint_2)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)

    def test_users_post_not_allowed(self):
        # Inputs
        endpoint = "/api/users/"

        # Expected outputs
        expected_response_status = status.HTTP_405_METHOD_NOT_ALLOWED

        # Execute
        response = self.client.post(endpoint)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
