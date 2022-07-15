import base64
import binascii

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ldap3 import ALL, Connection, Server, ALL_ATTRIBUTES
from ldap3.core.exceptions import LDAPException
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication,
    TokenAuthentication,
    get_authorization_header,
)


class ApiTokenAuthentication(TokenAuthentication):
    def __init__(self) -> None:
        self.keyword = "Bearer"
        super().__init__()


class LdapAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b"basic":
            return None

        if len(auth) == 1:
            msg = _("Invalid basic header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _(
                "Invalid basic header. Credentials string should not contain spaces."
            )
            raise exceptions.AuthenticationFailed(msg)

        try:
            try:
                auth_decoded = base64.b64decode(auth[1]).decode("utf-8")
            except UnicodeDecodeError:
                auth_decoded = base64.b64decode(auth[1]).decode("latin-1")
            auth_parts = auth_decoded.partition(":")
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = _("Invalid basic header. Credentials not correctly base64 encoded.")
            raise exceptions.AuthenticationFailed(msg)

        userid, password = auth_parts[0], auth_parts[2]
        return self.authenticate_credentials(userid, password, request)

    def authenticate_credentials(self, userid, password, request=None):
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
                raise exceptions.AuthenticationFailed(
                    _("Unable to connect to LDAP server using specified LDAP_APPUSER.")
                )
        except LDAPException:
            raise exceptions.AuthenticationFailed(
                _("Unable to connect to LDAP server.")
            )
        if not ldap_connection.search(
            settings.LDAP_USER_BASEDN,
            "(" + settings.LDAP_USERNAME_FIELD + "=" + userid + ")",
            attributes=ALL_ATTRIBUTES,
        ):
            ldap_connection.unbind()
            raise exceptions.AuthenticationFailed(_("User not found on LDAP server."))
        else:
            if len(ldap_connection.entries) > 0:
                uid = ldap_connection.entries[0].entry_dn
                print("User ----------")
                print(type(ldap_connection.entries[0]))
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
                        raise exceptions.AuthenticationFailed(
                            _("Invalid username/password.")
                        )
                    else:
                        try:
                            user = User.objects.get(username=userid)
                            if not user.is_active:
                                raise exceptions.AuthenticationFailed(
                                    _("User inactive or deleted.")
                                )
                        except User.DoesNotExist:
                            user = User(username=userid)
                        user.first_name = first_name
                        user.last_name = last_name
                        user.email = email_addr
                        user.last_login = timezone.now()
                        user.save()
                        ldap_connection.unbind()
                except LDAPException:
                    raise exceptions.AuthenticationFailed(
                        _("Invalid username/password.")
                    )
        return (user, None)
