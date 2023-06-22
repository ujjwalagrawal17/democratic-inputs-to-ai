from django.db import models

import keys
from account.models import User
from utils.models import CreationModificationBase

from typing import Dict, Tuple
import time
import random


# Create your models here.
class Question(CreationModificationBase):
    question_text = models.TextField()
    description = models.TextField()
    seed_statements = models.JSONField()

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


class Statement:
    """Statement model"""
    def __init__(self, statement: str):
        self.statement = statement
        self.engagement: int = 0
        self.init_boost: int = 10  # 10 boost for new statement
        self.base_score: int = 25  # 25 base score for any statement
        self.agreements: int = 0
        self.disagreements: int = 0

    @property
    def score(self):
        """Use exponential decay with engagement to calculate boost"""
        boost = self.init_boost * (0.75 ** self.engagement)
        return self.base_score + boost
    
    def engage(self, choice: UserInput.UserInputChoices):
        """Engage with statement"""
        self.engagement += 1
        if choice == UserInput.UserInputChoices.AGREE:
            self.agreements += 1
        elif choice == UserInput.UserInputChoices.DISAGREE:
            self.disagreements += 1
   
    def get_json(self):
        return {
            "statement": self.statement,
            "engagement": self.engagement,
            "agreements": self.agreements,
            "disagreements": self.disagreements,
            "score": self.score
        }
    
    def __str__(self):
        return self.statement


class StatementRouter:
    """Statement router"""
    def __init__(self, score_refresh_time: int = 10):
        self.statements: Dict[str, Statement] = dict()
        # dictionary to store all statements
        self.scores = list()
        # list to store scores of all statements
        self.score_refresh_rate = score_refresh_time
        # refresh score every 10 minutes
        self.last_refresh_time = time.time()

    def add_statement(self, statement: str):
        """Add statement to router"""
        statement_cls = Statement(statement)
        self.statements[statement] = statement_cls
        self.scores.append(statement_cls.score)

    def get_statement(self, statement: str):
        """Get statement from router"""
        return self.statements[statement]
    
    def get_next_statement(self):
        """Get next statement from router by probabilistically sampling using the scores"""
        return random.choices(self.statements.values(), weights=self.scores)[0]

    def refresh_scores(self):
        """Refresh scores of all statements"""
        self.scores = list()
        for statement in self.statements.values():
            self.scores.append(statement.score)
        self.last_refresh_time = time.time()

    def get_all_statements(self):
        """Get all statements from router"""
        return self.statements.values()
    
    def delete_statement(self, statement: str):
        """Delete statement from router"""
        del self.statements[statement]
