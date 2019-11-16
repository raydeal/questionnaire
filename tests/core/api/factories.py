import factory
from faker import Faker

from django.contrib.auth import get_user_model

from core.models import Question, Answer


# ---------------- FACTORIES ----------------------------

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()


class QuestionFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('text', max_nb_chars=100)
    ordinal_number = factory.Faker('random_int', min=1)
    class Meta:
        model = Question
        

class AnswerFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    question = factory.SubFactory(QuestionFactory)
    answer = factory.Faker('text', max_nb_chars=50)
    
    class Meta:
        model = Answer
        