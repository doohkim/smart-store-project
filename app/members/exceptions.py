from rest_framework import status
from rest_framework.exceptions import APIException


class PasswordNotMatchingException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'password1과 password2과 다릅니다.'
    default_code = 'PasswordNotMatching'