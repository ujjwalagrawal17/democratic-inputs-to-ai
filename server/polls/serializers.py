from rest_framework import serializers

from polls.models import Question, UserInput


class QuestionSerializer(serializers.Serializer):
    statement_to_display = serializers.SerializerMethodField()

    def get_statement_to_display(self, instance):
        request = self.context.get('request')
        # If user has not interacted with the question yet:
        if UserInput.objects.filter(question=instance).exists():
            # Returns a random statement to the user.
            return UserInput.objects.filter(question=instance).exclude(user=request.user).order_by('?').first()
        # else:
        #     # Returns a random seed statement
        #     return instance.seed_statements[0]
        return ""

    class Meta:
        model = Question
        fields = '__all__'


class UserInputSerializer(serializers.Serializer):

    class Meta:
        model = UserInput
        # fields = '__all__'
        fields = ['id', 'answer_text', 'votes']
