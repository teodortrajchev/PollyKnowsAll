from google import genai
import random

client = genai.Client(api_key="AIzaSyDorCKlU071UCkecZg7uy66kK9k2pVrbJk")
# models = client.models.list()
#
# for m in models:
#     print(m.name)
# topics = [
#     "Тигар",
#     "Слон",
#     "Ајкула",
#     "Орел",
#     "Париз",
#     "Илон Маск"
# ]
#
# secret = random.choice(topics)


def get_yes_no_answer(secret, question):
    prompt = f"""
Ти си игра за погодување.

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

    answer = response.text.strip().upper()

    if answer.startswith("ДА"):
        return "ДА"
    elif answer.startswith("НЕ"):
        return "НЕ"
    else:
        return "НЕ"


# while True:
#     q = input("Прашање: ")
#
#     if q.lower() == "крај":
#         print("🏁 Играта заврши. Зборот беше:", secret)
#         break
#     if secret.lower() in q.lower():
#         print("🎉 Точно! Го погоди зборот!")
#         break
#
#     print("Одговор:", ask(q))


