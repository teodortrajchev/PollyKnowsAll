from django.contrib.auth.models import User
from django.db import models

# Create your models here.
categories = [("Animals", "Animals"), ("People", "People"), ("Countries", "Countries"), ("Abstract", "Abstract")]


class Word(models.Model):
    word = models.CharField(max_length=255, unique=True)
    difficulty = models.IntegerField(default=1)
    category = models.CharField(choices=categories, max_length=255, default="People")

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    num_questions = models.IntegerField(default=0)

    def increment_num_questions(self):
        self.num_questions += 1
        self.save()

    def __str__(self):
        return f"Game Session for User {self.user} with word '{self.word_id.word}' "

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    question_text = models.TextField()
    answer = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return f"{self.question_text} (Word: {self.word_id})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, default='mk')
    created_at = models.DateTimeField(auto_now_add=True)
    num_games = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)

    def winner(self):
        self.wins += 1
        self.save()
    def add_coins(self, amount):
        self.coins += amount
        self.save()
    def increment_num_games(self):
        self.num_games += 1
        self.save()
