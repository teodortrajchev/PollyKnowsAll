import os
import uuid
from django.utils import timezone

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import random
import google.genai as genai
from dotenv import load_dotenv
from django.contrib.auth.models import User
from .models import Word, GameSession, Question, UserProfile
from .models import Word
from math import *
load_dotenv()


client = genai.Client(api_key=os.getenv("API_KEY"))

topics = ["Дота 2","Тигар", "Слон", "Ајкула", "Орел", "Париз", "Илон Маск"]
games = {}


def ask_gemini(secret, question):
    prompt = f"""
Ти мислиш на: {secret}

Правила:
- Одговарај САМО со "ДА" или "НЕ"
- НЕ објаснувај
- НЕ додавај текст
- Ако не си сигурен → кажи НЕ
- Ако не го разбираш прашањето → кажи НЕЈАСНО ПРАШАЊЕ
Прашање: {question}
Одговор:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip().upper()
    return "ДА" if text.startswith("ДА") else "НЕ"

@csrf_exempt
def start(request):
    category = request.GET.get('category', None)

    try:
        words = Word.objects.all()
        if category:
            words = words.filter(category=category)

        if not words.exists():
            return JsonResponse({'error': f'No words found for category: {category}'}, status=404)

        word_obj = random.choice(list(words))

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    session_id = str(uuid.uuid4())

    # For now use a default user until auth is set up
    user = User.objects.first()

    # Create GameSession in DB
    game_session = GameSession.objects.create(
        user=user,
        word=word_obj,
    )

    # Create or get UserProfile and increment num_games
    profile = get_or_create_profile(user)
    profile.increment_num_games()

    # Store in memory for fast access during game
    games[session_id] = {
        "word": word_obj.word,
        "word_obj": word_obj,
        "num_questions": 0,
        "category": word_obj.category,
        "game_session_id": game_session.id,
        "user": user,
    }

    return JsonResponse({
        "message": "Game started",
        "session_id": session_id,
        "category": word_obj.category,
        "coins": profile.coins,
    })

def get_proximity(secret, question):
    prompt = f"""You are a "hot or cold" judge for a word guessing game.
The secret word is: "{secret}"
The player asked: "{question}"

Rate how close this question is to guessing the secret word.
Reply with ONLY one of these words:
- BURNING (they basically said the answer)
- HOT (very close, related concept)
- WARM (somewhat related)
- COLD (not related at all)

Reply with ONE word only."""

    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]

    for model in models_to_try:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            text = response.text.strip().upper()
            if "BURNING" in text:
                return "BURNING"
            elif "HOT" in text:
                return "HOT"
            elif "WARM" in text:
                return "WARM"
            return "COLD"
        except Exception as e:
            print(f"Proximity model {model} failed: {e}")
            continue

    return "COLD"




@csrf_exempt
def ask(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    session_id = data.get('session_id')
    question_text = data.get('question', '').strip()

    if not session_id or not question_text:
        return JsonResponse({'error': 'Missing session_id or question'}, status=400)

    if session_id not in games:
        return JsonResponse({'error': 'Game not found, start a new game'}, status=404)

    try:
        game = games[session_id]
        secret = game["word"]
        user = game["user"]
        game["num_questions"] += 1

        # Get DB game session
        game_session = GameSession.objects.get(id=game["game_session_id"])
        game_session.increment_num_questions()

        # Check win condition
        if secret.lower() in question_text.lower():
            # Save winning question
            Question.objects.create(
                game=game_session,
                user=user,
                question_text=question_text,
                answer="ТОЧНО"
            )

            # Mark game session as won
            game_session.is_won = True
            game_session.end_time = timezone.now()
            game_session.save()
            game_session.refresh_from_db()
            profile = get_or_create_profile(user)
            profile.winner()
            coins_earned=5+ceil(10/game_session.num_questions)
            profile.add_coins(coins_earned)
            profile.refresh_from_db()

            del games[session_id]
            return JsonResponse({
                'answer': 'ТОЧНО! Победивте!',
                'game_over': True,
                'num_questions': game["num_questions"],
                'coins': profile.coins,
                'coins_earned': coins_earned,
                'proximity': None,
            })

        # Get Gemini answer
        answer = ask_gemini(secret, question_text)
        proximity = get_proximity(secret, question_text)

        # Save question to DB
        Question.objects.create(
            game=game_session,
            user=user,
            question_text=question_text,
            answer=answer
        )

        return JsonResponse({
            'answer': answer,
            'game_over': False,
            'num_questions': game["num_questions"],
            'proximity': proximity,
        })

    except Exception as e:
        print(f"Ask error: {e}")
        return JsonResponse({'error': str(e)}, status=500)
def get_or_create_profile(user):
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile


def index(request):
    return render(request, '../frontend/index.html')