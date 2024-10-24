from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='public')

# Serve the index.html when accessing the root URL
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# Serve any other static files (e.g., images)
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('public', path)

# Endpoint to handle checkout and write order to order.txt
@app.route('/checkout', methods=['POST'])
def checkout():
    order_data = request.get_json()

    # Create or append the order to 'order.txt'
    order_details = f"Order Summary:\n"
    order_details += "-----------------------------\n"
    for item in order_data['cart']:
        order_details += f"Product: {item['name']}\n"
        order_details += f"Color: {item['color']}\n"
        order_details += f"Size: {item['size']}\n"
        order_details += f"Quantity: {item['quantity']}\n"
        order_details += f"Price: {item['price']} CHF\n"
        order_details += f"Total for this item: {item['total']} CHF\n\n"
    order_details += f"-----------------------------\n"
    order_details += f"Total Amount: {order_data['total']} CHF\n\n"

    with open("order.txt", "a") as f:
        f.write(order_details)

    return jsonify({"message": "Order placed successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
