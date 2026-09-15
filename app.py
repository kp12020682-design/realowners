from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key-12345")

# ---------- LOGIN CREDENTIALS ----------
USERNAME = os.environ.get("DASH_USER", "Keerth")
PASSWORD = os.environ.get("DASH_PASS", "kkkkk")

# ---------- IN-MEMORY MESSAGE STORE ----------
messages = []   # each: {"id": int, "text": str, "time": str}
counter = {"id": 0}


# ---------- ROUTES ----------
@app.route("/", methods=["GET"])
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username", "").strip()
        p = request.form.get("password", "").strip()
        if u == USERNAME and p == PASSWORD:
            session["user"] = u
            return redirect(url_for("dashboard"))
        flash("❌ Galat username ya password!", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("✅ Logout ho gaya", "success")
    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        text = request.form.get("message", "").strip()
        if text:
            counter["id"] += 1
            messages.append({
                "id": counter["id"],
                "text": text,
                "time": datetime.now().strftime("%d %b %Y, %I:%M %p")
            })
            flash("✅ Message add ho gaya!", "success")
        else:
            flash("⚠️ Khali message nahi bhej sakte", "error")
        return redirect(url_for("dashboard"))

    return render_template(
        "dashboard.html",
        user=session["user"],
        messages=list(reversed(messages))  # newest first
    )


@app.route("/delete/<int:msg_id>", methods=["POST"])
def delete_message(msg_id):
    if "user" not in session:
        return redirect(url_for("login"))
    global messages
    messages = [m for m in messages if m["id"] != msg_id]
    flash("🗑️ Message delete ho gaya", "success")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
