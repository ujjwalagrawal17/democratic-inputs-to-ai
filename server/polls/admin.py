from django.contrib import admin

from polls.models import UserInput, Question


# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', 'question_text', 'created')


class UserInputAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', 'question', 'user', 'statement_shown_to_user', 'input', 'answer')


admin.site.register(Question, QuestionAdmin)
admin.site.register(UserInput, UserInputAdmin)
