import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .exceptions import InternalServerException


logger = logging.getLogger(__name__)

class CustomUserAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        token = request.query_params.get('token')
        if not token:
            raise AuthenticationFailed('Token request parameter is required')

        User = get_user_model()
        user = None
        try:
            user = User.objects.get(uuid=token)
        except User.DoesNotExist:
            raise AuthenticationFailed('No such user')
        except ValidationError as ex:
            message = '; '.join(ex.messages)
            raise AuthenticationFailed(message)
        except Exception as ex:
            logger.exception(ex, exc_info=True, stack_info=True)
            raise InternalServerException()

        return (user, None)