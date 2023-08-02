from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)

orderItemQuantities = {
    'EL0001': 0,
    'EL0002': 0,
    'EL0003': 0,
    'EL0004': 0,
    'EL0005': 0,
    'EL0006': 0,
    'EL0007': 0,
    'EL0008': 0,
    'EL0009': 0,
    'EL0010': 0,
    'EL0011': 0,
    'EL0012': 0,
    'EL0013': 0,
    'EL0014': 0,
    'EL0015': 0,
    'EL0016': 0,
    'EL0017': 0,
    'EL0018': 0,
    'EL0019': 0,
    'EL0020': 0
}

fName = ""
lName = ""
address = ""
cartTotal = 0
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    global cartTotal
    rounded_total = round(cartTotal, 2)
    return render_template('checkout.html', cartTotal=rounded_total)
    
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    item = data.get('item')
    quantity = data.get('quantity')
    orderItemQuantities[item] += int(quantity)
    return "Cart updated", 200

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    item = data.get('item')
    quantity = data.get('quantity')
    orderItemQuantities[item] = max(orderItemQuantities[item] - int(quantity), 0)
    return "Cart updated", 200

@app.route('/process_order', methods=['POST'])
def process_cart():
    flow_url = "https://prod-33.westus.logic.azure.com:443/workflows/0ade75fc9afa4a60886ae76f69f1c5d4/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=IoWUjcMxm5sTGbINhBid9zhgco_RLHPZ8sm8d0JhA68"
    data = request.get_json()
    global fName, lName, address, cartTotal
    fName = data.get('fname')
    lName = data.get('lname')
    address = data.get('addr')
    state = data.get('state')
    order_data = {
        "First Name": fName, 
        "Last Name": lName, 
        "Address": address, 
        "State": state,
        "Price": cartTotal
    }
    order_data.update(orderItemQuantities)
    count_non_zero_values = sum(value != 0 for value in orderItemQuantities.values())
    diffProducts = {'diffProducts': count_non_zero_values}
    order_data.update(diffProducts)
    response = requests.post(flow_url, json=order_data)
    return 'Order Placed'
    
@app.route('/updateTotal', methods=['POST'])
def updateTotal():
    global cartTotal
    data = request.get_json()
    cartTotal = data.get('total')
    return "Total updated successfully"

if __name__ == "__main__":
	app.run()
