from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import json
import os

app = Flask(__name__)


genai.configure(api_key="")
model = genai.GenerativeModel("models/gemini-2.0-flash-lite")

HISTORY_FILE = "chat_history.json"


if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        chat_history = json.load(f)
else:
    chat_history = []

def save_message(sender, message):
    chat_history.append({"sender": sender, "message": message})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html", history=chat_history)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    save_message("You", user_input)

    try:
        response = model.generate_content(user_input)
        reply = response.text
    except Exception as e:
        reply = f"Error: {e}"

    save_message("Gemini", reply)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
