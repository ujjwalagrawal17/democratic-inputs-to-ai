from django.shortcuts import render
from requests import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

import keys
from account.permissions import IsKycAuthenticated
from polls.models import Question
from polls.serializers import UserInputSerializer, QuestionSerializer


# Create your views here.
class PollViewSet(viewsets.GenericViewSet):
    # permission_classes = [IsKycAuthenticated]
    permission_classes = [IsKycAuthenticated]

    @action(
        detail=False,
        methods=["get"],
        url_path="get-question-list", url_name="get-question-list",
    )
    def get_question(self, request, version):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Show all unanswered questions to the user for now.
        answered_questions = UserInput.obquestion

        question = Question.objects.exclude(input=keys.SKIP_THIS_QUESTION)


        data = QuestionSerializer(question).data
        return Response(data, status=status.HTTP_200_OK)





    def suggest(self, request, version):
        return Response(InvoiceSuggestionSerializer(self.company, context=self.serializer_context).data)
