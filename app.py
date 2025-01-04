from flask import Flask, request, jsonify
import json

app = Flask(__name__)

PRODUCTS_FILE = 'products.json'

def load_products():
    try:
        with open(PRODUCTS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_products(products):
    with open(PRODUCTS_FILE, 'w') as file:
        json.dump(products, file, indent=4)

@app.route('/api/products', methods=['GET'])
def get_products():
    products = load_products()
    return jsonify(products), 200

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product_by_id(id):
    products = load_products()
    product = next((p for p in products if p['id'] == id), None)
    if product:
        return jsonify(product), 200
    return jsonify({'message': 'Product not found'}), 404

@app.route('/api/products', methods=['POST'])
def add_product():
    products = load_products()
    new_product = request.get_json()
    new_product['id'] = max([p['id'] for p in products], default=0) + 1
    products.append(new_product)
    save_products(products)
    return jsonify(new_product), 201

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    products = load_products()
    updated_data = request.get_json()
    for product in products:
        if product['id'] == id:
            product.update(updated_data)
            save_products(products)
            return jsonify(product), 200
    return jsonify({'message': 'Product not found'}), 404

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    products = load_products()
    product = next((p for p in products if p['id'] == id), None)
    if product:
        products.remove(product)
        save_products(products)
        return jsonify({'message': 'Product deleted successfully'}), 200
    return jsonify({'message': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
