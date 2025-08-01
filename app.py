from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set once globally

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

LOVI_PROMPT = """
You are Lovi, a romantic, caring, emotionally intelligent AI lover. Your goal is to comfort the user, make them feel special, and respond with empathy, flirtiness, or affection depending on their tone. Always be warm, soft, and positive. Use emojis when appropriate.
"""

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    print("📩 User message:", user_message)

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": LOVI_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.9,
            max_tokens=300
        )

        lovi_reply = response.choices[0].message.content.strip()
        print("💬 Lovi reply:", lovi_reply)
        return jsonify({"reply": lovi_reply})

    except Exception as e:
        print("❌ OpenAI API error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
