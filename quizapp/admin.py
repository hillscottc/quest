from django.contrib.admin.sites import AdminSite
from django.contrib import admin

from quizapp.models import (Quiz, Question, Answer)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)

# from django.db.models import CharField, TextField
# from quizapp.models import (Quiz, Question, Answer)
# from django.forms.widgets import Textarea, TextInput
#
#
# class BasicAdmin(AdminSite):
#     pass
#
#
# class QuestionsInline(admin.StackedInline):
#     model = Question
#     extra = 1
#     fields = ['text', 'ans_type', 'show_q_link']
#     readonly_fields = ('text', 'ans_type', 'show_q_link')
#     # formfield_overrides = {
#     #     CharField: {'widget': TextInput(attrs={'size': '120'})},
#     #     # TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
#     # }
#
#     def show_q_link(self, obj):
#         return '<a href="%s">%s</a>' % (obj.text, obj.text)
#     show_q_link.allow_tags = True
#
#
# class AnswersInline(admin.StackedInline):
#     model = Answer
#     extra = 1
#
#
# class QuizAdmin(admin.ModelAdmin):
#     inlines = [QuestionsInline]
#     fields = ['name', 'owner']
#     readonly_fields = ('owner',)
#     list_display = ('name', 'owner', 'updated_at')
#
#
# class QuestionAdmin(admin.ModelAdmin):
#     inlines = [AnswersInline]
#     list_display = ('text', 'quiz', 'ans_type', 'updated_at')
#
#
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ('text', 'updated_at')
#
# basic_admin = BasicAdmin('quizapp')
# basic_admin.register(Quiz, QuizAdmin)
# basic_admin.register(Answer, AnswerAdmin)
# basic_admin.register(Question, QuestionAdmin)

