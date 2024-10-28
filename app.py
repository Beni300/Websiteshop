from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import json  # For serializing the cart items to store in the database

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

def get_db_connection():
    conn = sqlite3.connect('ecommerce.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page with product listing
@app.route('/')
def home():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('home.html', products=products)

# Product detail page
@app.route('/product/<int:product_id>')
def product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    return render_template('product.html', product=product)

# Cart page
@app.route('/cart')
def cart():
    return render_template('cart.html', cart=session.get('cart', {}))

# Add to cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()

    if product is None:
        return "Product not found", 404

    # Initialize the cart in the session if it doesn’t exist
    if 'cart' not in session:
        session['cart'] = {}

    # Convert product ID to string for consistency in session storage
    product_id_str = str(product_id)
    cart = session['cart']

    # If the product is already in the cart, increase the quantity
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        # Otherwise, add the product to the cart with initial quantity
        cart[product_id_str] = {
            'name': product['name'],
            'image': product['image'],
            'price': product['price'],
            'quantity': 1
        }

    session['cart'] = cart
    return redirect(url_for('cart'))

# Checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        postal_code = request.form['postal_code']
        country = request.form['country']
        
        # Get cart data from the session
        cart = session.get('cart', {})
        
        # Calculate total price
        total_price = 0
        for item in cart.values():
            total_price += item['price'] * item['quantity']

        # Serialize cart items to JSON format to store in the database
        cart_json = json.dumps(cart)

        # Save the order to the database
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO orders (name, address, city, postal_code, country, items, total_price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, address, city, postal_code, country, cart_json, total_price))
        conn.commit()
        conn.close()

        # Clear the cart after successful checkout
        session.pop('cart', None)
        flash("Thank you for your purchase, {}! Your order has been placed.".format(name))

        return redirect(url_for('home'))

    # If GET request, display the checkout form
    return render_template('checkout.html')

# Admin page to view all orders
@app.route('/admin/orders')
def view_orders():
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)
@app.route('/admin/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()
    flash("Order #{} has been successfully deleted.".format(order_id))
    return redirect(url_for('view_orders'))

if __name__ == '__main__':
    app.run(debug=True)
