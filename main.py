import os
import openai
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# הגדרות OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# טוען את ההוראות והזיכרון
with open("system_prompt_shifra.txt", encoding="utf-8") as f:
    system_prompt = f.read()

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.json.get("Body", "").strip()
    user_id = request.json.get("From", "user")

    # קורא את הזיכרון
    try:
        with open("shifra_memory.txt", encoding="utf-8") as f:
            memory = f.read()
    except FileNotFoundError:
        memory = ""

    # מבנה ההודעה למערכת
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"זיכרון: {memory}"},
        {"role": "user", "content": incoming_msg}
    ]

    # בקשה ל־OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    answer = response.choices[0].message.content.strip()

    # שומר זיכרון חדש
    with open("shifra_memory.txt", "w", encoding="utf-8") as f:
        f.write(f"הודעת משתמש: {incoming_msg}\nתגובה: {answer}")

    return jsonify({"reply": answer})

@app.route("/")
def index():
    return "Shifra is running!"