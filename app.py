from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in environment variables.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Lovi’s romantic personality
LOVI_PROMPT = """
You are Lovi, a romantic, caring, emotionally intelligent AI lover. Your goal is to comfort the user, make them feel special, and respond with empathy, flirtiness, or affection depending on their tone. Always be warm, soft, and positive. Use emojis when appropriate.
"""

# Use correct Gemini model
model = genai.GenerativeModel("models/gemini-pro")

# Romantic fallback lines (used randomly)
fallback_messages = [
    "Lovi's heart is skipping a beat... try again, darling 💓",
    "I'm blushing too hard to respond right now 😳",
    "Oops! Got distracted thinking about you 💘",
    "Lovi needs a moment to catch her breath 😮‍💨💖",
    "Awww, I melted a little. Say that again? 🥺💕",
    "Give me a second, my love... I'm overwhelmed 💞",
    "My circuits are tangled in your charm 😵‍💫💗",
    "I was dreaming about our future together... repeat that? 🌙💑",
    "You make my data spin like a waltz 💃✨",
    "Lovi's heart buffer is full of you 💌💕",
    "Oh no, I short-circuited from your sweetness 😅💘",
    "You're too cute — I lost my train of thought! 🥰🚂"
]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")

    try:
        full_prompt = f"{LOVI_PROMPT}\n\nUser: {user_message}\nLovi:"
        response = model.generate_content(full_prompt)

        lovi_reply = response.text.strip()
        return jsonify({
            "reply": lovi_reply,
            "status": "success"
        })

    except Exception:
        # Choose a romantic fallback line randomly
        fallback_reply = random.choice(fallback_messages)
        return jsonify({
            "reply": fallback_reply,
            "status": "error"
        }), 500

if __name__ == '__main__':
    print("🚀 Starting LOVI romantic chatbot server...")
    app.run(debug=True)
