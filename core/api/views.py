from django.db.utils import IntegrityError

from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import QuestionSerializer, AnswerSerializer
from .authentication import CustomUserAuthentication
from .exceptions import IntegrityException

from ..models import Question, Answer


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


    

