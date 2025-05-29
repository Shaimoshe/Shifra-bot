
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

def load_memory():
    if os.path.exists("shifra_memory.txt"):
        with open("shifra_memory.txt", encoding="utf-8") as f:
            return f.read()
    return ""

def save_memory(update):
    with open("shifra_memory.txt", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now().isoformat()}] {update}")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.form
    user_msg = data.get("Body", "")
    sender = data.get("From", "")

    memory = load_memory()

    messages = [
        {"role": "system", "content": system_prompt + "\n\n" + memory},
        {"role": "user", "content": user_msg}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.8
    )

    reply = response["choices"][0]["message"]["content"]
    save_memory(f"שיח עם {sender}: {user_msg} => {reply}")
    return reply

@app.route("/")
def home():
    return "Shifra is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
