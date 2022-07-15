from django.conf import settings
from django.contrib.auth.backends import RemoteUserBackend
from ldap3 import ALL, Connection, Server


class LdapAuthenticationBackend(RemoteUserBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            ldap_server = Server(
                settings.LDAP_HOST, port=settings.LDAP_PORT, use_ssl=False, get_info=ALL
            )
            ldap_connection = Connection(
                ldap_server,
                settings.LDAP_APPUSER,
                password=settings.LDAP_APPUSER_PASSWORD,
                auto_bind=True,
            )
            # 1. connection with service account to find the user uid
            uid = useruid(s, login)

            if uid:
                # 2. Try to bind the user to the LDAP
                c = Connection(s, user=uid, password=password, auto_bind=True)
                c.open()
                c.bind()
                result = c.result["description"] == "success"  # "success" if bind is ok
                c.unbind()
        except Exception as e:
            print(f"Error: {str(e)}")
        return result
