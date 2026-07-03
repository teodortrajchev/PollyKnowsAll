import os
import uuid

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import random
import google.genai as genai
from dotenv import load_dotenv

from .models import Word

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
        word = word_obj.word

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    session_id = str(uuid.uuid4())
    games[session_id] = {
        "word": word,
        "num_questions": 0,
        "category": word_obj.category,
    }

    return JsonResponse({
        "message": "Game started",
        "session_id": session_id,
        "category": word_obj.category,
    })





@csrf_exempt
def ask(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    session_id = data.get('session_id')
    question = data.get('question', '').strip()
    if not session_id or not question:
        return JsonResponse({'error': 'Missing session_id or question'}, status=400)
    if session_id not in games:
        return JsonResponse({'error': 'Game not found, start a new game'}, status=404)
    game = games[session_id]
    secret = game["word"]
    game["num_questions"] += 1

    if secret.lower() in question.lower():
        del games[session_id]
        return JsonResponse({
            'answer': '🎉 ТОЧНО! Победивте!',
            'game_over': True,
            'num_questions': game["num_questions"]
        })
    answer = ask_gemini(secret, question)
    return JsonResponse({
        'answer': answer,
        'game_over': False,
        'num_questions': game["num_questions"]
    })
def index(request):
    return render(request, '../frontend/index.html')