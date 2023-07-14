from flask import Flask, render_template, request
import json

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

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
	return render_template("checkout.html")

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    item = data.get('item')
    quantity = data.get('quantity')
    if item in orderItemQuantities:
        orderItemQuantities[item] += int(quantity)
    else:
        return "Invalid item", 400

    return "Cart updated", 200

@app.route('/process_cart', methods=['POST'])
def process_cart():
    # cart_data = request.form.get('cartData')
    # Process the cart data as needed
    # cart_items = json.loads(cart_data)
    # for item in cart_items:
    #     name = item['name']
    #     quantity = item['quantity']
    #     total = item['total']
    #     print(name, quantity, total)
    #for x in orderItemQuantities:
    #    print(orderItemQuantities[x])
    return 'Cart data received'
    
if __name__ == "__main__":
	app.run()
