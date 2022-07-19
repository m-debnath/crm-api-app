from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class APIAdminTestCase(APITestCase):
    def setUp(self):
        # Inputs
        self.user = User.objects.create_superuser(
            username="apiadmintest", password="password", email="username@password.com"
        )
        self.token = AccessToken.for_user(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    def test_user_list_ok(self):
        # Inputs
        endpoint = "/api/admin/users/"

        # Expected outputs
        expected_response_status = status.HTTP_200_OK

        # Execute
        response = self.client.get(endpoint)
        # print(response.data)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
