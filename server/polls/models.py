from django.db import models

import keys
from account.models import User
from utils.models import CreationModificationBase


# Create your models here.
class Question(CreationModificationBase):
    question_text = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.question_text


class UserInput(CreationModificationBase):
    class UserInputChoices(models.Choices):
        SKIP_THIS_QUESTION = keys.SKIP_THIS_QUESTION
        AGREE = keys.AGREE
        DISAGREE = keys.DISAGREE

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    statement_shown_to_user = models.TextField()
    input = models.CharField(max_length=40, choices=UserInputChoices.choices)
    answer = models.TextField(blank=True)

    def __str__(self):
        return self.answer
