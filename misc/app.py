# from game_state import create_game, get_secret, end_game
# from engine import *
# app = Flask(__name__)
#
#
# @app.route("/start", methods=["POST"])
# def start():
#     session_id = request.json.get("session_id")
#     create_game(session_id)
#
#     return jsonify({"message": "Game started"})
#
#
#
# @app.route("/ask", methods=["POST"])
# def ask():
#     data = request.json
#     session_id = data.get("session_id")
#     question = data.get("question")
#     secret = get_secret(session_id)
#
#     if not secret:
#         return jsonify({"error": "Game not found"}), 404
#
#     if secret.lower() in question.lower():
#         end_game(session_id)
#         return jsonify({
#             "answer": "🎉 ТОЧНО!",
#             "game_over": True
#         })
#     answer = get_yes_no_answer(secret, question)
#     return jsonify({
#         "answer": answer,
#         "game_over": False
#     })
#
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)