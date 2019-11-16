from rest_framework.exceptions import APIException

class IntegrityException(APIException):
    status_code = 400
    default_detail = 'Data integrity violation'
    default_code = 'integrity_exception'

class InternalServerException(APIException):
    status_code = 500
    default_detail = 'Hmm...we do not support that yet'
    default_code = 'internal_exception'