import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class QuestionManager(models.Manager):

    def ordinal_ordered(self):
        return self.get_queryset().order_by('ordinal_number')


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    # 2-letter country name abbreviations
    country = models.CharField(max_length=2, default='UK')

    objects = UserManager()
    
    class Meta:
        db_table = 'auth_user'
        
    def __str__(self):
        return '{} [{}]'.format(self.username, self.email)

    
class Question(models.Model):
    title = models.CharField(max_length=250, unique=True)
    user = models.ManyToManyField(User, through='Answer')
    ordinal_number = models.PositiveSmallIntegerField(null=True, blank=True)

    objects = QuestionManager()
    
    def __str__(self):
        return self.title[:50]

    
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    answer = models.TextField()
    language = models.CharField(max_length=5, default='en-gb')

    class Meta:
        unique_together = [['user', 'question']]
        
    def __str__(self):
        return '[{}-{}] {}'.format(self.user.uuid, self.question.id, self.answer)