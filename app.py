from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    category = db.Column(db.String(100))
    imgUrl = db.Column(db.Text)
    stock = db.Column(db.Integer)
    brand = db.Column(db.String(100))

# Initialize the database and create the table
with app.app_context():
    db.create_all()

# HTML template for the UI
UI_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Products API UI</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .form-group { margin-bottom: 10px; }
        input, textarea { width: 100%; padding: 5px; }
        button { padding: 10px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        .product-list { margin-top: 20px; }
        .product-item { border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; }
    </style>
    <script>
        async function addProduct() {
            const formData = {
                name: document.getElementById('name').value,
                description: document.getElementById('description').value,
                price: parseFloat(document.getElementById('price').value),
                category: document.getElementById('category').value,
                imgUrl: document.getElementById('imgUrl').value,
                stock: parseInt(document.getElementById('stock').value),
                brand: document.getElementById('brand').value
            };

            const response = await fetch('/api/products', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(formData)
            });
            location.reload();
        }

        async function updateProduct(id) {
            const formData = {
                name: document.getElementById(`name_${id}`).value,
                description: document.getElementById(`description_${id}`).value,
                price: parseFloat(document.getElementById(`price_${id}`).value),
                category: document.getElementById(`category_${id}`).value,
                imgUrl: document.getElementById(`imgUrl_${id}`).value,
                stock: parseInt(document.getElementById(`stock_${id}`).value),
                brand: document.getElementById(`brand_${id}`).value
            };

            const response = await fetch(`/api/products/${id}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(formData)
            });
            location.reload();
        }

        async function deleteProduct(id) {
            if (confirm('Are you sure you want to delete this product?')) {
                const response = await fetch(`/api/products/${id}`, {
                    method: 'DELETE'
                });
                location.reload();
            }
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>Products API UI</h1>
        
        <h2>Add New Product</h2>
        <div class="form-group">
            <input type="text" id="name" placeholder="Name" required>
        </div>
        <div class="form-group">
            <textarea id="description" placeholder="Description"></textarea>
        </div>
        <div class="form-group">
            <input type="number" id="price" placeholder="Price" step="0.01" required>
        </div>
        <div class="form-group">
            <input type="text" id="category" placeholder="Category">
        </div>
        <div class="form-group">
            <input type="text" id="imgUrl" placeholder="Image URL">
        </div>
        <div class="form-group">
            <input type="number" id="stock" placeholder="Stock" required>
        </div>
        <div class="form-group">
            <input type="text" id="brand" placeholder="Brand">
        </div>
        <button onclick="addProduct()">Add Product</button>

        <h2>Existing Products</h2>
        <div class="product-list">
            {% for product in products %}
            <div class="product-item">
                <h3>Product ID: {{ product.id }}</h3>
                <div class="form-group">
                    <input type="text" id="name_{{ product.id }}" value="{{ product.name }}" placeholder="Name">
                </div>
                <div class="form-group">
                    <textarea id="description_{{ product.id }}" placeholder="Description">{{ product.description }}</textarea>
                </div>
                <div class="form-group">
                    <input type="number" id="price_{{ product.id }}" value="{{ product.price }}" step="0.01" placeholder="Price">
                </div>
                <div class="form-group">
                    <input type="text" id="category_{{ product.id }}" value="{{ product.category }}" placeholder="Category">
                </div>
                <div class="form-group">
                    <input type="text" id="imgUrl_{{ product.id }}" value="{{ product.imgUrl }}" placeholder="Image URL">
                </div>
                <div class="form-group">
                    <input type="number" id="stock_{{ product.id }}" value="{{ product.stock }}" placeholder="Stock">
                </div>
                <div class="form-group">
                    <input type="text" id="brand_{{ product.id }}" value="{{ product.brand }}" placeholder="Brand">
                </div>
                <button onclick="updateProduct({{ product.id }})">Update</button>
                <button onclick="deleteProduct({{ product.id }})" style="background-color: #f44336;">Delete</button>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
'''

# Home route
@app.route('/')
def index():
    products = Product.query.all()
    return render_template_string(UI_TEMPLATE, products=products)

# GET - Retrieve all products
@app.route('/api/products', methods=["GET"])
def get_products():
    products = Product.query.all()
    product_list = [{
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "imgUrl": product.imgUrl,
        "stock": product.stock,
        "brand": product.brand
    } for product in products]
    return jsonify({'res': product_list})

# POST - Add a new product
@app.route('/api/products', methods=["POST"])
def add_product():
    data = request.json
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        category=data['category'],
        imgUrl=data['imgUrl'],
        stock=data['stock'],
        brand=data['brand']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'res': f'Product {new_product.name} added successfully'}), 201

# PUT - Update an existing product
@app.route('/api/products/<int:product_id>', methods=["PUT"])
def update_product(product_id):
    data = request.json
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    product.name = data['name']
    product.description = data['description']
    product.price = data['price']
    product.category = data['category']
    product.imgUrl = data['imgUrl']
    product.stock = data['stock']
    product.brand = data['brand']

    db.session.commit()
    return jsonify({'res': f'Product {product_id} updated successfully'})

# DELETE - Delete a product
@app.route('/api/products/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'res': f'Product {product_id} deleted successfully'})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)