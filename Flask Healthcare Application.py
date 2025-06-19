from flask import Flask, request, render_template_string
from datetime import datetime, timezone
import csv
import os
import traceback

app = Flask(__name__)

# Define the User class
class User:
    def __init__(self, age, gender, income, expenses, total_expenses):
        self.age = age
        self.gender = gender
        self.income = income
        self.expenses = expenses
        self.total_expenses = total_expenses
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_csv_row(self):
        return [
            self.timestamp,
            self.age,
            self.gender,
            self.income,
            self.expenses.get("utilities", 0),
            self.expenses.get("entertainment", 0),
            self.expenses.get("school_fees", 0),
            self.expenses.get("shopping", 0),
            self.expenses.get("healthcare", 0),
            self.total_expenses,
        ]

csv_file = os.path.join(os.path.dirname(__file__), "user_data.csv")
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "age", "gender", "income",
            "utilities", "entertainment", "school_fees", "shopping", "healthcare",
            "total_expenses"
        ])

@app.before_request
def log_everything():
    print(f"\n[REQUEST] {request.method} {request.path}")
    print("Headers:", dict(request.headers))
    print("Form Data:", request.form)

html_form = """
<!doctype html>
<html>
<head>
  <title>Income Survey</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; color: #222; }
    h2 { margin-bottom: 20px; }
    label { display: block; margin-top: 15px; font-weight: bold; }
    input[type=text], input[type=number], select {
      width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box;
    }
    fieldset { margin-top: 20px; padding: 10px; border: 1px solid #ccc; }
    legend { font-weight: bold; }
    .expense-item { margin-top: 10px; }
    .submit-btn { margin-top: 20px; padding: 10px 20px; }
    .hint { font-size: 0.9em; color: #666; }
  </style>
  <script>
    function toggleInput(checkbox, id) {
      const input = document.getElementById(id);
      input.style.display = checkbox.checked ? 'block' : 'none';
      if (!checkbox.checked) input.value = '';
    }
  </script>
</head>
<body>
  <h2>Income & Expense Survey</h2>
  <form method="POST">
    <label>Age:
      <input type="number" name="age" required min="0" placeholder="Enter your age">
      <div class="hint">Enter your age as a number (e.g., 30)</div>
    </label>

    <label>Gender:
      <select name="gender" required>
        <option value="" disabled selected>Select gender</option>
        <option value="female">Female</option>
        <option value="male">Male</option>
        <option value="non-binary">Non-binary</option>
        <option value="prefer_not_to_say">Prefer not to say</option>
      </select>
      <div class="hint">Please choose one option from the list</div>
    </label>

    <label>Total Income (Monthly in USD):
      <input type="number" name="income" required min="0" placeholder="e.g., 3000">
      <div class="hint">Enter your total monthly income in dollars (e.g., 3200)</div>
    </label>

    <fieldset>
      <legend>Expenses (check and enter amount for each)</legend>

      <div class="expense-item">
        <input type="checkbox" name="expenses_selected" value="utilities"
               onchange="toggleInput(this, 'utilities_amount')"> Utilities
        <input type="number" name="utilities_amount" id="utilities_amount"
               placeholder="Amount for Utilities" min="0" style="display:none;">
      </div>

      <div class="expense-item">
        <input type="checkbox" name="expenses_selected" value="entertainment"
               onchange="toggleInput(this, 'entertainment_amount')"> Entertainment
        <input type="number" name="entertainment_amount" id="entertainment_amount"
               placeholder="Amount for Entertainment" min="0" style="display:none;">
      </div>

      <div class="expense-item">
        <input type="checkbox" name="expenses_selected" value="school_fees"
               onchange="toggleInput(this, 'school_fees_amount')"> School Fees
        <input type="number" name="school_fees_amount" id="school_fees_amount"
               placeholder="Amount for School Fees" min="0" style="display:none;">
      </div>

      <div class="expense-item">
        <input type="checkbox" name="expenses_selected" value="shopping"
               onchange="toggleInput(this, 'shopping_amount')"> Shopping
        <input type="number" name="shopping_amount" id="shopping_amount"
               placeholder="Amount for Shopping" min="0" style="display:none;">
      </div>

      <div class="expense-item">
        <input type="checkbox" name="expenses_selected" value="healthcare"
               onchange="toggleInput(this, 'healthcare_amount')"> Healthcare
        <input type="number" name="healthcare_amount" id="healthcare_amount"
               placeholder="Amount for Healthcare" min="0" style="display:none;">
      </div>
    </fieldset>

    <button class="submit-btn" type="submit">Submit</button>
  </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        try:
            age_raw = request.form.get("age", "").strip()
            income_raw = request.form.get("income", "").strip()
            gender = request.form.get("gender", "").strip()

            if not age_raw or not income_raw or not gender:
                return "Missing required inputs", 400

            age = int(age_raw)
            income = float(income_raw)

            selected = request.form.getlist("expenses_selected")
            expenses = {}
            total_expenses = 0.0
            for category in ["utilities", "entertainment", "school_fees", "shopping", "healthcare"]:
                value = request.form.get(f"{category}_amount", "0").strip()
                try:
                    amount = float(value) if category in selected else 0.0
                except ValueError:
                    amount = 0.0
                expenses[category] = amount
                total_expenses += amount

            user = User(age, gender, income, expenses, total_expenses)

            with open(csv_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(user.to_csv_row())

            return f"<h3>Thank you! Your response has been recorded.</h3><a href='/'>Submit another response</a>"

        except Exception as e:
            print("[ERROR] Exception during form processing:", str(e))
            traceback.print_exc()
            return "Server error during form processing.", 500

    return render_template_string(html_form)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

