from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "change-this-secret-key"  # For demo only – replace in production


# In-memory "database" for demo purposes
users = {}


def calculate_bmi(weight_kg: float, height_cm: float):
    if height_cm <= 0:
        return None, None
    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return round(bmi, 2), category


def login_required(view_func):
    from functools import wraps

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped_view


@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = users.get(email)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password", "error")
            return render_template("login.html")

        session["user"] = {
            "email": email,
            "name": user["name"],
        }
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not name or not email or not password:
            flash("All fields are required", "error")
            return render_template("register.html")

        if password != confirm:
            flash("Passwords do not match", "error")
            return render_template("register.html")

        if email in users:
            flash("Email already registered. Please log in.", "error")
            return redirect(url_for("login"))

        users[email] = {
            "name": name,
            "password_hash": generate_password_hash(password),
            "profile": {
                "age": None,
                "gender": None,
                "height_cm": None,
                "weight_kg": None,
                "activity_level": None,
            },
            "bmi_history": [],
            "goals": [],
        }

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    user_email = session["user"]["email"]
    user = users.get(user_email)
    bmi_latest = user["bmi_history"][-1] if user["bmi_history"] else None
    return render_template("dashboard.html", user=user, bmi_latest=bmi_latest)


@app.route("/bmi", methods=["GET", "POST"])
@login_required
def bmi():
    user_email = session["user"]["email"]
    user = users.get(user_email)

    result = None
    if request.method == "POST":
        try:
            weight = float(request.form.get("weight", "0"))
            height = float(request.form.get("height", "0"))
        except ValueError:
            flash("Please enter valid numbers for weight and height.", "error")
            return render_template("bmi.html", result=None)

        bmi_value, category = calculate_bmi(weight, height)
        if bmi_value is None:
            flash("Height must be greater than 0.", "error")
            return render_template("bmi.html", result=None)

        result = {
            "weight": weight,
            "height": height,
            "bmi": bmi_value,
            "category": category,
        }

        user["profile"]["weight_kg"] = weight
        user["profile"]["height_cm"] = height
        user["bmi_history"].append(result)

    return render_template("bmi.html", result=result)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_email = session["user"]["email"]
    user = users.get(user_email)

    if request.method == "POST":
        age = request.form.get("age") or None
        gender = request.form.get("gender") or None
        height = request.form.get("height") or None
        weight = request.form.get("weight") or None
        activity = request.form.get("activity_level") or None

        try:
            height_val = float(height) if height else None
            weight_val = float(weight) if weight else None
            age_val = int(age) if age else None
        except ValueError:
            flash("Please enter valid numbers for age, height and weight.", "error")
            return render_template("profile.html", user=user)

        user["profile"].update(
            {
                "age": age_val,
                "gender": gender,
                "height_cm": height_val,
                "weight_kg": weight_val,
                "activity_level": activity,
            }
        )
        flash("Profile updated.", "success")

    return render_template("profile.html", user=user)


@app.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    user_email = session["user"]["email"]
    user = users.get(user_email)

    if request.method == "POST":
        goal_text = request.form.get("goal", "").strip()
        if goal_text:
            user["goals"].append({"text": goal_text, "completed": False})
            flash("Goal added!", "success")
    return render_template("goals.html", user=user)


@app.route("/goals/complete/<int:goal_index>", methods=["POST"])
@login_required
def complete_goal(goal_index):
    user_email = session["user"]["email"]
    user = users.get(user_email)
    if 0 <= goal_index < len(user["goals"]):
        user["goals"][goal_index]["completed"] = True
        flash("Goal marked as completed.", "success")
    return redirect(url_for("goals"))


if __name__ == "__main__":
    app.run(debug=True)


