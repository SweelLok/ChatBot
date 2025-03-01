from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, logout_user
import sqlite3

from app import app
from connection import get_db_connection


@app.get("/profile/")
@login_required
def get_profile_page():
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute("SELECT * FROM users WHERE user_id = ?", (current_user.user_id,))
    user = curs.fetchone()
    curs.execute("SELECT * FROM profile WHERE user_id = ?", (current_user.user_id,))
    profile = curs.fetchone()
    curs.execute("SELECT * FROM history WHERE user_id = ?", (current_user.user_id,))
    history = curs.fetchall()
    conn.close()

    return render_template("profile.html", user=user, profile=profile, history=history)

@app.get("/edit_profile/")
@login_required
def get_edit_profile_page():
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute("SELECT * FROM users WHERE user_id = ?", (current_user.user_id,))
    user = curs.fetchone()
    conn.close()

    return render_template("edit_profile.html", user=user)

@app.post("/edit_profile/")
@login_required
def post_edit_profile():
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    photo = request.form["photo"]
    description = request.form["description"].strip()
    if not username or not password:
        flash("Please fill out all the fields.", "error")
        return redirect(url_for("get_edit_profile_page"))
    
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute("UPDATE users SET username = ?, password = ? WHERE user_id = ?", 
                 (username, password, current_user.user_id))
    curs.execute("UPDATE profile SET description = ?, photo = ? WHERE user_id = ?", 
                 (description, photo, current_user.user_id))
    conn.commit()
    conn.close()

    return redirect(url_for("get_profile_page"))

@app.post("/delete_profile/")
@login_required
def post_delete_profile():
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute("DELETE FROM users WHERE user_id = ?", (current_user.user_id,))
    conn.commit()
    conn.close()
    logout_user()
    flash("Your account has been deleted.", "success")

    return redirect(url_for("get_login"))