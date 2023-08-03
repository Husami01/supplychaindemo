from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    return render_template("checkout.html")

@app.route('/process_order', methods=['POST'])
def process_order():
    flow_url = "https://prod-33.westus.logic.azure.com:443/workflows/0ade75fc9afa4a60886ae76f69f1c5d4/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=IoWUjcMxm5sTGbINhBid9zhgco_RLHPZ8sm8d0JhA68"
    data = request.get_json()
    global fName, lName, address, cartTotal
    fName = data.get('fname')
    lName = data.get('lname')
    address = data.get('addr')
    state = data.get('state')
    cartTotal = data.get('price')
    products = data.get('prods')

    order_data = {
        "First Name": fName,
        "Last Name": lName,
        "Address": address,
        "State": state,
        "Price": float(cartTotal)
    }
    order_data.update(products)
    count_non_zero_values = sum(value != 0 for value in products.values())
    diffProducts = {'diffProducts': count_non_zero_values}
    order_data.update(diffProducts)
    print(order_data)

    response = requests.post(flow_url, json=order_data)
    return 'Order Placed'

if __name__ == "__main__":
    app.run()
