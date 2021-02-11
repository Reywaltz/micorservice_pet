from dataclasses import dataclass

import requests
from flask import Flask, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from producer import publish

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://main:local_password@db:5432/local_db"
CORS(app)

db = SQLAlchemy(app)

@dataclass
class Product(db.Model):
    
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')

@app.route('/api/products')
def index():
    print(Product.query.all())
    return jsonify(Product.query.all())

@app.route('/api/product/<int:id>/like', methods=["POST"])
def like(id):
    req = requests.get("http://172.26.0.1:8000/api/user")
    result = req.json()

    try:
        productUser = ProductUser(user_id=result['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id)
    except:
        abort(400, 'You already liked this product')

    return jsonify({
        'message': 'success'
    })

if __name__== '__main__':
    app.run(debug=True,
            host='0.0.0.0')
