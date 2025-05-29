# הקובץ המעודכן מוכן, הנה ההתחלה
import os
import openai
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("system_prompt_shifra.txt", encoding="utf-8") as f:
    system_prompt = f.read()

@app.route("/")
def home():
    return "Shifra is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message received"}), 400

    prompt = f"{system_prompt}\n\nמשתמש: {user_message}\nשיפרה:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": user_message}]
    )

    reply = response['choices'][0]['message']['content'].strip()
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()
