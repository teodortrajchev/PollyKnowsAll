from django.contrib import admin

from .models import *
# Register your models here.
#TODO Logika so inkrementiranje za prasanja,logika za profil i za igri


class WordAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

class GameAdmin(admin.ModelAdmin):
    pass
class QuestionAdmin(admin.ModelAdmin):
    pass
class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Question, QuestionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GameSession, GameAdmin)
admin.site.register(Word, WordAdmin)