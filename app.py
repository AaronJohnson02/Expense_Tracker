from flask import Flask, request, render_template
import matplotlib.pyplot as plt
import cv2
import os

plt.switch_backend('Agg')

app = Flask(__name__)
expenses_list = []
total_expenses = 0
expense_limit = 0
percentage = 0.0

img_path = "static/display.jpeg"

if os.path.exists(img_path):
    os.remove(img_path)
@app.route('/', methods=['GET', 'POST'])
def index():
    global expense_limit, total_expenses, expenses_list, percentage
    error_message = ""

    if request.method == 'POST':
        amount = request.form.get('amount')
        if amount and amount.replace('.', '', 1).isdigit() and float(amount) >= 0:
            expenses_list.append(round(float(amount),2))
            total_expenses = sum(expenses_list)
            if expense_limit != 0:
                percentage = round((total_expenses / expense_limit) * 100 , 2)
                plt.clf()
                if total_expenses > expense_limit:
                    plt.pie([expense_limit, 0], labels=["Total Expenses", "Limit"], autopct='%1.1f%%')
                else:
                    plt.pie([total_expenses, expense_limit], labels=["Total Expenses", "Limit"], autopct='%1.1f%%')
                plt.savefig(img_path)
                plt.close()  
        else:
            error_message = "Please enter a valid non-negative number for the expense."
    
    return render_template('index.html', expenses=expenses_list, limit=expense_limit, error=error_message, limit_per = percentage, tex=total_expenses)

@app.route('/limiter', methods=['POST'])
def limit():
    global expense_limit
    error_message = ""

    limit_value = request.form.get('elimit')
    if limit_value and limit_value.replace('.', '', 1).isdigit() and float(limit_value) >= 0:
        expense_limit = float(limit_value)
    else:
        error_message = "Please enter a valid non-negative number for the limit."

    return render_template('index.html', expenses=expenses_list, limit=expense_limit, error=error_message, limit_per = percentage, tex=total_expenses)

if __name__ == '__main__':
    app.run(debug=True)
