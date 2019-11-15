from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import QuestionSerializer, AnswerSerializer
from .authentication import CustomUserAuthentication

from ..models import Question, Answer


class QuestionListView(ListAPIView):
    queryset = Question.objects.ordinal_ordered()
    serializer_class = QuestionSerializer
    

class AnswerViewSet(ModelViewSet):
    serializer_class = AnswerSerializer
    authentication_classes = [CustomUserAuthentication]

    def get_queryset(self):
        return self.request.user.answer_set

    

