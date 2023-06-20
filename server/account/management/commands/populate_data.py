import json

from django.core.management import BaseCommand

from polls.models import Question


class Command(BaseCommand):
    help = 'Command to populate initial data in the DB'

    def handle(self, *args, **options):
        f = open("account/fixtures/questions_and_statements.json", "r")
        question_json_array = json.loads(f.read())
        for question in question_json_array:
            Question.objects.create(question_text=question["question"], seed_statements=question["statements"])
