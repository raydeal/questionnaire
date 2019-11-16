from django.db.utils import IntegrityError

from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from .serializers import QuestionSerializer, AnswerSerializer, UserSerializer, QuestionUserSerializer
from .authentication import CustomUserAuthentication
from .exceptions import IntegrityException

from ..models import Question, Answer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class QuestionListView(ListAPIView):
    queryset = Question.objects.ordinal_ordered()
    serializer_class = QuestionSerializer
    

class AnswerViewSet(ModelViewSet):
    serializer_class = AnswerSerializer
    authentication_classes = [CustomUserAuthentication]

    def get_queryset(self):
        return self.request.user.answer_set

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError as ex:
            raise IntegrityException(detail='An answer to the question already exists')


class UserViewSet(ModelViewSet):
    queryset = UserSerializer.Meta.model.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class QuestionUserListView(ListAPIView):
    """View which allows an Administrator to retrieve a
        list of email addresses of users whose answer for a given question matches a given
        'search term'"""
    queryset = QuestionUserSerializer.Meta.model.objects.all()
    serializer_class = QuestionUserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = LargeResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['answer__answer']

    def get_queryset(self):
        """
        Optionally restricts the users that answered to the question,
        by filtering against a 'question' parameter in the URL.
        """
        qs = self.queryset
        question_id = self.request.query_params.get('question')
        if question_id is not None:
            qs = qs.filter(answer__question_id=question_id)
        return qs