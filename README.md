## Health & Fitness Tracker (Flask + HTML/CSS)

This is a simple **health & fitness tracker** web app built with **Python (Flask)** and a modern HTML/CSS frontend.

Features:
- **User auth**: Register, login, logout (in‑memory, for demo).
- **Dashboard**: Summary of latest BMI, profile, and goals.
- **BMI calculator**: Enter weight & height, get BMI value and category.
- **Profile**: Save age, gender, height, weight, activity level.
- **Goals**: Add health/fitness goals and mark them as completed.

### 1. Install dependencies

Open a terminal in the project folder (`health fitness tracker`) and run:

```bash
pip install -r requirements.txt
```

If you have multiple Python versions installed, use `python -m pip` or `py -m pip` on Windows:

```bash
py -m pip install -r requirements.txt
```

### 2. Run the app

In the same folder:

```bash
py app.py
```

or

```bash
python app.py
```

You should see Flask start on something like `http://127.0.0.1:5000/`.

Open that URL in your browser.

### 3. Using the app

- Go to **Register** to create a new account.
- After logging in you can:
  - Use the **BMI** page to calculate and store BMI records.
  - Update your **Profile** metrics.
  - Add and complete **Goals**.

> Note: Data is stored only in memory (Python dictionary) and will reset when you restart the server. For a real project, you’d connect a database (e.g. SQLite, PostgreSQL).


