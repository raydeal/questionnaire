import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'auth_user'
        
    def __str__(self):
        return '{} [{}]'.format(self.username, self.email)

    
class Question(models.Model):
    title = models.CharField(max_length=250, unique=True)
    user = models.ManyToManyField(User, through='Answer')
    
    def __str__(self):
        return self.title[:10]

    
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    answer = models.TextField()

    class Meta:
        unique_together = [['user', 'question']]
        
    def __str__(self):
        return '[{}-{}] {}'.format(self.user.uuid, self.question.id, self.answer)