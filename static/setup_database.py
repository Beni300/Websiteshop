import sqlite3

# Connect to the database (will create the database if it doesn't exist)
connection = sqlite3.connect("ecommerce.db")
cursor = connection.cursor()

# Drop the existing tables if they exist (optional, for a fresh setup)
cursor.execute("DROP TABLE IF EXISTS products")
cursor.execute("DROP TABLE IF EXISTS orders")

# Create products table
cursor.execute('''
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        image TEXT NOT NULL
    )
''')

# Insert sample data into products table
products = [
    ("Blau Jacke", "Blue jacket description", 60, "blau_jacke.png"),
    ("Dunkelblau Jacke", "Dark blue jacket description", 65, "dunkelblau_jacke.png"),
    ("Rot Jacke", "Red jacket description", 60, "rot_jacke.png"),
    ("Schwarz Hoodie", "Black hoodie description", 45, "schwarz_hoodie.png"),
    ("Tiger Sweatshirt", "Tiger sweatshirt description", 20, "tiger_sweatshirt_black.png"),
    ("Mechanical Keyboard L700", "Mechanical keyboard description", 40, "mechanical_keyboard_L700.png"),
]

cursor.executemany("INSERT INTO products (name, description, price, image) VALUES (?, ?, ?, ?)", products)

# Create orders table
cursor.execute('''
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        city TEXT NOT NULL,
        postal_code TEXT NOT NULL,
        country TEXT NOT NULL,
        items TEXT NOT NULL,  -- This will store the cart items as a JSON string
        total_price REAL NOT NULL
    )
''')

# Commit the transaction and close the connection
connection.commit()
connection.close()

print("Database setup completed.")
