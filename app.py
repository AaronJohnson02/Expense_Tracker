from flask import Flask, request, render_template
import matplotlib.pyplot as plt
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

def is_valid_number(value):
    """ Check if the input value is a valid non-negative number. """
    try:
        float_value = float(value)
        return float_value >= 0 
    except ValueError:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    global expense_limit, total_expenses, expenses_list, percentage
    error_message = ""

    if request.method == 'POST':
        amount = request.form.get('amount')
        if amount:
            if is_valid_number(amount):
                amount = round(float(amount), 2)
                expenses_list.append(amount)
                total_expenses = sum(expenses_list)
                print(f"LIMIT: {expense_limit} AND TOTAL: {total_expenses}")

                if expense_limit != 0:
                    percentage = round((total_expenses / expense_limit) * 100, 2)
                    plt.clf()
                    
                    remaining_limit = expense_limit - total_expenses
                    
                    if total_expenses > expense_limit:
                        plt.pie([expense_limit, 0], labels=["Total Expenses", "Limit"], autopct='%1.1f%%')
                    else:
                        plt.pie([total_expenses, remaining_limit], labels=["Total Expenses", "Remaining Limit"], autopct='%1.1f%%')

                    plt.savefig(img_path)
                    plt.close()
            else:
                error_message = "Invalid input for amount. Please enter a non-negative number."

    return render_template('index.html', expenses=expenses_list[::-1], limit=expense_limit, error=error_message, limit_per=percentage, tex=total_expenses)

@app.route('/limiter', methods=['POST'])
def limit():
    global expense_limit
    error_message = ""
    percentage = total_expenses = percentage = expense_limit = 0
    limit_value = request.form.get('elimit')
    if limit_value:
        if is_valid_number(limit_value):
            expense_limit = float(limit_value)

            total_expenses = sum(expenses_list)
            percentage = round((total_expenses / expense_limit) * 100, 2)
            print(f"LIMIT: {expense_limit} AND TOTAL: {total_expenses}")
            
            plt.clf()
            
            remaining_limit = expense_limit - total_expenses
            
            if total_expenses > expense_limit:
                plt.pie([expense_limit, 0], labels=["Total Expenses", "Limit"], autopct='%1.1f%%')
            else:
                plt.pie([total_expenses, remaining_limit], labels=["Total Expenses", "Remaining Limit"], autopct='%1.1f%%')
            
            plt.savefig(img_path)
            plt.close()
        else:
            error_message = "Please enter a valid non-negative number for the limit."

    return render_template('index.html', expenses=expenses_list[::-1], limit=expense_limit, error=error_message, limit_per=percentage, tex=total_expenses)

@app.route('/clear', methods=['POST'])
def clear():
    global expense_limit, expenses_list, percentage, total_expenses
    expenses_list.clear()  
    total_expenses = 0
    expense_limit = 0
    percentage = 0.0
    error_message = ""

    if os.path.exists(img_path):
        os.remove(img_path)

    return render_template('index.html', expenses=expenses_list, limit=expense_limit, error=error_message, limit_per=percentage, tex=total_expenses)

if __name__ == '__main__':
    app.run(debug=True)
