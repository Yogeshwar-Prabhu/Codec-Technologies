from flask import Flask, render_template, request, redirect, url_for
import json
import datetime

app = Flask(__name__)

# Load FAQ data
with open("data/faq.json", "r") as f:
    faq_data = json.load(f)

# Store chat logs in memory
chat_logs = []

def get_response(user_input):
    user_input = user_input.lower()
    for item in faq_data:
        if item["question"].lower() in user_input:
            return item["answer"]
    return "Sorry, I don't understand that. Can you rephrase?"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_message = request.form["message"]
        bot_response = get_response(user_message)

        log_entry = {
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_message,
            "bot": bot_response
        }
        chat_logs.append(log_entry)

        return render_template("index.html", logs=chat_logs)
    return render_template("index.html", logs=chat_logs)

@app.route("/logs")
def logs():
    return render_template("logs.html", logs=chat_logs)

if __name__ == "__main__":
    app.run(debug=True)
