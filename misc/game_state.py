import random

topics = ["Дота 2","Тигар", "Слон", "Ајкула", "Орел", "Париз", "Илон Маск"]

games = {}


def create_game(session_id):
    games[session_id] = random.choice(topics)


def get_secret(session_id):
    return games.get(session_id)


def end_game(session_id):
    if session_id in games:
        del games[session_id]