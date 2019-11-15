from rest_framework import serializers

from ..models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'title', 'ordinal_number']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields=['question', 'answer', 'language']