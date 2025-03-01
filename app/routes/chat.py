from flask import render_template, redirect, url_for, request, session
from flask_login import current_user, login_required

from app import app
from connection import get_db_connection
from .answer import answers


@app.get("/")
def get_start():
    if current_user.is_authenticated:
        return redirect(url_for("chat"))
    return redirect(url_for("get_login"))

@app.get("/about/")
def get_about():
    return render_template("about.html")

@app.route("/chat/", methods=["GET", "POST"])
@login_required
def chat():
    if request.method == "POST":
        if "clear" in request.form:
            session["chat_cleared"] = True
            return redirect(url_for("chat"))
        user_message = request.form["user_input"]
        response = get_bot_response(user_message)
        save_chat_history(current_user.user_id, user_message, response)
        session["chat_cleared"] = False
        return redirect(url_for("chat"))

    chat_history = get_chat_history(current_user.user_id)
    cleared = session.get("chat_cleared", False)
    if cleared:
        chat_history = []
    return render_template("chat.html", chat_history=chat_history, cleared=cleared)

def get_bot_response(user_message):
    for question_answer_pair in answers["questions"]:
        if question_answer_pair["question"].lower() in user_message.lower():
            return question_answer_pair["answer"]
    return "I'm sorry, I don't understand the question."

def save_chat_history(user_id, user_message, bot_response):
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute("INSERT INTO history (user_id, name, answer) VALUES (?, ?, ?)", 
                 (user_id, user_message, bot_response))
    conn.commit()
    conn.close()

def get_chat_history(user_id):
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute("SELECT name, answer FROM history WHERE user_id = ?", (user_id,))
    chat_history = curs.fetchall()
    conn.close()
    return chat_history