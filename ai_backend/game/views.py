import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
import google.genai as genai


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
    if request.method == "POST":
        body = json.loads(request.body)
        session_id = body.get("session_id")

        games[session_id] = random.choice(topics)

        return JsonResponse({"message": "Game started"})

    return JsonResponse({"error": "Only POST allowed"}, status=405)


@csrf_exempt
def ask(request):
    if request.method == "POST":
        body = json.loads(request.body)

        session_id = body.get("session_id")
        question = body.get("question")

        secret = games.get(session_id)

        if not secret:
            return JsonResponse({"error": "Game not found"}, status=404)

        if secret.lower() in question.lower():
            del games[session_id]
            return JsonResponse({
                "answer": "🎉 ТОЧНО!",
                "game_over": True
            })

        answer = ask_gemini(secret, question)
        return JsonResponse({
            "answer": answer,
            "game_over": False
        })

    return JsonResponse({"error": "Only POST allowed"}, status=405)