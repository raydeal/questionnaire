import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


logger = logging.getLogger(__name__)

class CustomUserAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        user_uuid = request.query_params.get('user_uuid')
        if not user_uuid:
            raise AuthenticationFailed('User UUID request parameter is required')

        User = get_user_model()
        try:
            user = User.objects.get(uuid=user_uuid)
        except User.DoesNotExist:
            raise AuthenticationFailed('No such user')
        except ValidationError as ex:
            message = '; '.join(ex.messages)
            raise AuthenticationFailed(message)
        except Exception as ex:
            logger.exception(ex, exc_info=True, stack_info=True)
            raise AuthenticationFailed('Something went wrong')

        return (user, None)