from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework import status


class AdminHomeTestCase(TestCase):
    def setUp(self):
        # Inputs
        super_user_name = settings.TEST_ADMIN_USER
        super_user_password = "AdminPassword"

        self.user = User.objects.create_superuser(
            username=super_user_name, password=super_user_password, email="admin@example.com"
        )

        self.client = Client()
        self.client.login(username=super_user_name, password=super_user_password)

    def test_admin_user_loads_normal(self):
        # Inputs
        endpoint = "/admin/auth/user/"

        # Expected outputs
        expected_response_status = status.HTTP_200_OK

        # Execute
        response = self.client.get(endpoint)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)

    def test_admin_group_loads_normal(self):
        # Inputs
        endpoint = "/admin/auth/group/"

        # Expected outputs
        expected_response_status = status.HTTP_200_OK

        # Execute
        response = self.client.get(endpoint)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)

    def test_admin_blacklisted_token_loads_normal(self):
        # Inputs
        endpoint = "/admin/token_blacklist/blacklistedtoken/"

        # Expected outputs
        expected_response_status = status.HTTP_200_OK

        # Execute
        response = self.client.get(endpoint)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)

    def test_admin_outstanding_token_loads_normal(self):
        # Inputs
        endpoint = "/admin/token_blacklist/outstandingtoken/"
        # Expected outputs
        expected_response_status = status.HTTP_200_OK

        # Execute
        response = self.client.get(endpoint)

        # Verify
        self.assertEquals(response.status_code, expected_response_status)
