from django.contrib import admin

from .models import *
# Register your models here.


class WordAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'num_games', 'wins',"coins", 'language']

class GameAdmin(admin.ModelAdmin):
    list_display = ['user', 'word', 'num_questions', 'start_time']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'answer', 'game', 'user']



admin.site.register(Question, QuestionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GameSession, GameAdmin)
admin.site.register(Word, WordAdmin)