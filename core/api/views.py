from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from .serializers import QuestionSerializer, AnswerSerializer
from ..models import Question, Answer

class QuestionListView(ListAPIView):
    queryset = Question.objects.ordinal_ordered()
    serializer_class = QuestionSerializer
    

class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

