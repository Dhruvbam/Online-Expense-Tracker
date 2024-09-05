from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

recorded_purchases = []


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    name = request.form.get('name')
    month = request.form.get('month')
    return render_template('reports.html', name=name, month=month)
  return render_template('index.html')


@app.route('/record', methods=['GET', 'POST'])
def record():
  if request.method == 'POST':
    # Handle form submission
    item = request.form.get('item')
    price = request.form.get('price')
    if item and price:
      # Create a dictionary for the purchase
      purchase = {'item': item, 'price': float(price)}
      # Append the purchase to recorded_purchases list
      recorded_purchases.append(purchase)
      return "Purchase recorded successfully!"
    else:
      return "Error: Missing item or price in form data."
  else:
    # Render the record page
    return render_template('record.html')


@app.route('/reports')
def reports():
  # Retrieve user's name and selected month from the query parameters
  name = request.args.get('name')
  month = request.args.get('month')
  # Calculate total price and format the report
  total_price = sum(purchase['price'] for purchase in recorded_purchases)
  report_data = {
      'recorded_purchases': recorded_purchases,
      'total_price': total_price,
      'name': name,
      'month': month
  }
  return render_template('reports.html', report_data=report_data)


@app.route('/viewreports')
def view_reports():
  # Return recorded purchases data in JSON format
  return jsonify(recorded_purchases)


if __name__ == '__main__':
  app.run(debug=True)
