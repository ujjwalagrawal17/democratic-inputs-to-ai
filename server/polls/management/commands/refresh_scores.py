import json

from django.core.management import BaseCommand

from polls.models import Question, UserInput, Statement


class Command(BaseCommand):
    help = 'Command to store/update scores of statements in the DB. this command will run in CRON every 30 minutes.'

    def handle(self, *args, **options):

        statements = Statement.objects.all()
