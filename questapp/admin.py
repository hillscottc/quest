from django.contrib import admin
from questapp.models import Clue, Game, Category


from django.contrib.admin.sites import AdminSite
from django.contrib import admin


class BasicAdmin(AdminSite):
    pass



# basic_admin = BasicAdmin('quizapp')
# basic_admin.register(Quiz, QuizAdmin)
# basic_admin.register(Answer, AnswerAdmin)
# basic_admin.register(Question, QuestionAdmin)


admin.site.register(Clue)
admin.site.register(Game)
admin.site.register(Category)