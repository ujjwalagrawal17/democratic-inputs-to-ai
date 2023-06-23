from django.contrib import admin

from polls.models import UserInput, Question, Statement


# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', 'question_text', 'created')


class StatementAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', 'question', 'statement', 'score', 'flag_seed_statement')
    list_filter = ['flag_seed_statement']


class UserInputAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', 'question', 'user', 'statement', 'input')


admin.site.register(Question, QuestionAdmin)
admin.site.register(UserInput, UserInputAdmin)
admin.site.register(Statement, StatementAdmin)
