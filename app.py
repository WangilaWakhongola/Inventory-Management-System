"""
Inventory Management System
A Flask-based application for managing inventory with SQLite database
"""

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, template_folder='.')

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'inventory.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, nullable=False)
    reorder_level = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'quantity': self.quantity,
            'price': self.price,
            'reorder_level': self.reorder_level,
            'total_value': self.quantity * self.price,
            'status': 'Low Stock' if self.quantity <= self.reorder_level else 'In Stock',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Routes

@app.route('/')
def index():
    """Display dashboard with inventory overview"""
    products = db.session.execute(db.select(Product)).scalars().all()
    total_products = len(products)
    total_value = sum(p.quantity * p.price for p in products)
    low_stock = sum(1 for p in products if p.quantity <= p.reorder_level)
    
    return render_template('index.html', 
                         products=products,
                         total_products=total_products,
                         total_value=total_value,
                         low_stock=low_stock)

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products (API endpoint)"""
    products = db.session.execute(db.select(Product)).scalars().all()
    return jsonify([p.to_dict() for p in products])

@app.route('/api/products', methods=['POST'])
def create_product():
    """Create a new product"""
    try:
        data = request.get_json() or request.form
        
        product = Product(
            name=data.get('name'),
            description=data.get('description'),
            category=data.get('category'),
            quantity=int(data.get('quantity', 0)),
            price=float(data.get('price')),
            reorder_level=int(data.get('reorder_level', 10))
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({'message': 'Product created successfully', 'product': product.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    """Get a specific product"""
    product = db.get_or_404(Product, id)
    return jsonify(product.to_dict())

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    """Update a product"""
    try:
        product = db.get_or_404(Product, id)
        data = request.get_json() or request.form
        
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.category = data.get('category', product.category)
        product.quantity = int(data.get('quantity', product.quantity))
        product.price = float(data.get('price', product.price))
        product.reorder_level = int(data.get('reorder_level', product.reorder_level))
        
        db.session.commit()
        
        return jsonify({'message': 'Product updated successfully', 'product': product.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    """Delete a product"""
    try:
        product = db.get_or_404(Product, id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/products/search', methods=['GET'])
def search_products():
    """Search products by name or category"""
    query = request.args.get('q', '').lower()
    category = request.args.get('category', '').lower()
    
    products = db.session.execute(db.select(Product)).scalars().all()
    
    if query:
        products = [p for p in products if query in p.name.lower() or query in p.description.lower()]
    
    if category:
        products = [p for p in products if p.category.lower() == category]
    
    return jsonify([p.to_dict() for p in products])

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get inventory statistics"""
    products = db.session.execute(db.select(Product)).scalars().all()
    
    stats = {
        'total_products': len(products),
        'total_value': sum(p.quantity * p.price for p in products),
        'low_stock_count': sum(1 for p in products if p.quantity <= p.reorder_level),
        'categories': list(set(p.category for p in products))
    }
    
    return jsonify(stats)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)