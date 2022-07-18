from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.utils import timezone
from ldap3 import ALL, ALL_ATTRIBUTES, Connection, Server
from ldap3.core.exceptions import LDAPException

from core.logging.utils import log_memory_usage


class LdapAuthenticationBackend(BaseBackend):
    @log_memory_usage
    def authenticate(self, request, username=None, password=None):
        try:
            ldap_server = Server(
                settings.LDAP_HOST,
                port=int(settings.LDAP_PORT),
                use_ssl=False,
                get_info=ALL,
            )
            ldap_connection = Connection(
                ldap_server,
                settings.LDAP_APPUSER,
                password=settings.LDAP_APPUSER_PASSWORD,
                auto_bind=True,
            )
            if ldap_connection.result["description"] != "success":
                ldap_connection.unbind()
                print(
                    f"Unable to connect to LDAP server {settings.LDAP_HOST} using {settings.LDAP_APPUSER}"
                )
                return None
        except LDAPException:
            print(f"Unable to connect to LDAP server {settings.LDAP_HOST}")
            return None
        if not ldap_connection.search(
            settings.LDAP_USER_BASEDN,
            "(" + settings.LDAP_USERNAME_FIELD + "=" + username + ")",
            attributes=ALL_ATTRIBUTES,
        ):
            ldap_connection.unbind()
            print(f"User {username} not found on LDAP dn {settings.LDAP_USER_BASEDN}")
            return None
        else:
            if len(ldap_connection.entries) > 0:
                uid = ldap_connection.entries[0].entry_dn
                first_name = ldap_connection.entries[0].cn
                last_name = ldap_connection.entries[0].sn
                email_addr = ldap_connection.entries[0].mail
            ldap_connection.unbind()
            if uid:
                try:
                    ldap_connection = Connection(
                        ldap_server, user=uid, password=password, auto_bind=True
                    )
                    ldap_connection.open()
                    ldap_connection.bind()
                    if ldap_connection.result["description"] != "success":
                        ldap_connection.unbind()
                        print("Invalid username / password")
                        return None
                    else:
                        try:
                            user = User.objects.get(username=username)
                            if not user.is_active:
                                print("User inactive or deleted")
                                return None
                        except User.DoesNotExist:
                            user = User(username=username)
                        user.first_name = first_name
                        user.last_name = last_name
                        user.email = email_addr
                        user.last_login = timezone.now()
                        user.save()
                        ldap_connection.unbind()
                        return user
                except LDAPException:
                    print("Invalid username / password")
                    return None
        return None
