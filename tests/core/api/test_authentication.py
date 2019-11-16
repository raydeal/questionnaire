from unittest import mock

from django.test import TestCase
from django.db import InternalError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

from core.api.authentication import CustomUserAuthentication
from core.api.exceptions import InternalServerException

from .factories import UserFactory


class CustomUserAuthenticationTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.req_factory = APIRequestFactory()
        cls.auth_obj = CustomUserAuthentication()
        cls.token = '92d43661bd7b44d188acd695b09fea5c'

    @classmethod
    def tearDownClass(cls):
        cls.req_factory = None
        cls.auth_obj = None
        cls.token = None
        
    def test_authentication_no_token(self):
        """tests when token request parameter is not given"""
        
        request = self.req_factory.get('/')  # , {'title': 'new idea'})
        # trick because of: AttributeError: 'WSGIRequest' object has no attribute 'query_params'
        request = APIView().initialize_request(request)
        with self.assertRaisesMessage(AuthenticationFailed, 'Token request parameter is required'):
            self.auth_obj.authenticate(request)
            
    def test_authentication_wrong_token(self):
        """tests token has incorrect format/value - ValidationError"""
        
        request = self.req_factory.get('/', {'token': 'dsf'})
        # trick because of: AttributeError: 'WSGIRequest' object has no attribute 'query_params'
        request = APIView().initialize_request(request)
        with self.assertRaisesMessage(AuthenticationFailed, "'dsf' is not a valid UUID"):
            self.auth_obj.authenticate(request)

    def test_authentication_no_user(self):
        """test when user containing token not egzists"""
        
        request = self.req_factory.get('/', {'token': self.token})
        # trick because of: AttributeError: 'WSGIRequest' object has no attribute 'query_params'
        request = APIView().initialize_request(request)
        with self.assertRaisesMessage(AuthenticationFailed, 'No such user'):
            self.auth_obj.authenticate(request)

    @mock.patch('core.api.authentication.get_user_model')
    @mock.patch('core.api.authentication.logger.exception')
    def test_authentication_server_exception(self, logger_mock, get_user_mock):
        """tests internal server exception"""

        get_user_mock.return_value.DoesNotExist = ObjectDoesNotExist
        get_user_mock.return_value.objects.get.side_effect = InternalError('internal server exception')
        request = self.req_factory.get('/', {'token': self.token})
        # trick because of: AttributeError: 'WSGIRequest' object has no attribute 'query_params'
        request = APIView().initialize_request(request)
        with self.assertRaisesMessage(InternalServerException, 'Hmm...we do not support that yet'):
            self.auth_obj.authenticate(request)
        get_user_mock.assert_called_once()
        logger_mock.assert_called_once()

    def test_authentication(self):
        """test case when everything is ok"""

        user = UserFactory(uuid=self.token)
        request = self.req_factory.get('/', {'token': self.token})
        # trick because of: AttributeError: 'WSGIRequest' object has no attribute 'query_params'
        request = APIView().initialize_request(request)
        result = self.auth_obj.authenticate(request)
        self.assertEqual(result, (user, None))