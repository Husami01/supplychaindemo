from flask import Flask, render_template, request, session
import json
import requests

app = Flask(__name__)
app.secret_key = 'some-secret-key' # Replace with a strong secret key

@app.route("/")
def index():
    session['orderItemQuantities'] = {f'EL{i:04d}': 0 for i in range(1, 21)}
    session['cartTotal'] = 0
    return render_template("index.html")

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    rounded_total = round(session['cartTotal'], 2)
    return render_template('checkout.html', cartTotal=rounded_total)
    
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    item = data.get('item')
    quantity = data.get('quantity')
    if 'orderItemQuantities' not in session:
        session['orderItemQuantities'] = {f'EL{i:04d}': 0 for i in range(1, 21)}
    session['orderItemQuantities'][item] += int(quantity)
    session.modified = True  # Ensure that the session is marked as modified
    return "Cart updated", 200

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    item = data.get('item')
    quantity = data.get('quantity')
    # Check if the item exists in the session and the quantity is greater than 0
    if 'orderItemQuantities' in session and item in session['orderItemQuantities']:
        session['orderItemQuantities'][item] = max(session['orderItemQuantities'][item] - int(quantity), 0)
        session.modified = True  # Ensure that the session is marked as modified
        return "Cart updated", 200
    else:
        return "Item not found in cart", 400


@app.route('/process_order', methods=['POST'])
def process_cart():
    flow_url = "https://prod-33.westus.logic.azure.com:443/workflows/0ade75fc9afa4a60886ae76f69f1c5d4/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=IoWUjcMxm5sTGbINhBid9zhgco_RLHPZ8sm8d0JhA68"
    data = request.get_json()
    fName = data.get('fname')
    lName = data.get('lname')
    address = data.get('addr')
    state = data.get('state')
    cartTotal = session['cartTotal']
    order_data = {
        "First Name": fName,
        "Last Name": lName,
        "Address": address,
        "State": state,
        "Price": cartTotal
    }
    order_data.update(session['orderItemQuantities'])
    count_non_zero_values = sum(value != 0 for value in session['orderItemQuantities'].values())
    diffProducts = {'diffProducts': count_non_zero_values}
    order_data.update(diffProducts)
    #response = requests.post(flow_url, json=order_data)
    print(order_data)
    # Optionally, you could reset the cart after processing the order:
    session.clear()
    return 'Order Placed'


@app.route('/updateTotal', methods=['POST'])
def updateTotal():
    data = request.get_json()
    session['cartTotal'] = data.get('total')
    return "Total updated successfully"

if __name__ == "__main__":
    app.run()
