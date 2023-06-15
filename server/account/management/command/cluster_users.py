from django.core.management import BaseCommand

from account.models import User
from polls.models import UserInput


class Command(BaseCommand):
    help = 'Command to cluster users based on their opinions'

    def handle(self, *args, **options):
        user_inputs = UserInput.objects.all()
        user_input_json = [
            {
                "question": 1,
                "user": 1,
                "statement_shown_to_user": "some statement shown to the user",
                "input": "agree",
                "answer": "users answer that he described in detail",
            },
            {
                "question": 1,
                "user": 2,
                "statement_shown_to_user": "some statement shown to the user",
                "input": "agree",
                "answer": "users answer that he described in detail",
            },
            {
                "question": 1,
                "user": 3,
                "statement_shown_to_user": "some statement shown to the user",
                "input": "agree",
                "answer": "users answer that he described in detail",
            },
            {
                "question": 2,
                "user": 1,
                "statement_shown_to_user": "some statement shown to the user",
                "input": "agree",
                "answer": "users answer that he described in detail",
            },
            {
                "question": 2,
                "user": 2,
                "statement_shown_to_user": "some statement shown to the user",
                "input": "agree",
                "answer": "users answer that he described in detail",
            },
            {
                "question": 2,
                "user": 3,
                "statement_shown_to_user": "some statement shown to the user",
                "input": "agree",
                "answer": "users answer that he described in detail",
            },
        ]


        output_user_list = [
            {
                "user": 1,
                "cluster": 1
            },
            {
                "user": 2,
                "cluster": 2
            },
        ]


