from django.contrib.auth import get_user_model

from rest_framework import serializers

from ..models import Question, Answer, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'uuid', 'username', 'email',
                'password', 'is_active', 'is_staff']
        
    def create(self, validate_data):
        user = self.Meta.model.objects.create_user(
            validate_data['username'], validate_data['email'], validate_data['password'],
            is_active=validate_data['is_active'], is_staff=validate_data['is_staff'])
        return user


class QuestionUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ['email']


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'title', 'ordinal_number']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer', 'language']