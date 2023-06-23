import json

from django.core.management import BaseCommand

import keys
from account.models import User
from polls.models import Question, UserInput, Statement


class Command(BaseCommand):
    help = 'Command to populate initial data in the DB'

    def handle(self, *args, **options):
        f = open("account/fixtures/questions_and_statements.json", "r")
        question_json_array = json.loads(f.read())
        user = User.objects.all()[0]
        for question in question_json_array:
            print("question", question)
            print("question-statements", question["statements"])
            question_instance = Question.objects.create(question_text=question["question"])
            seed_statements = question["statements"]
            # print(type(seed_statements))
            for seed_statement in seed_statements:
                Statement.objects.create(question=question_instance, statement=seed_statement, flag_seed_statement=True, score=0)
