#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def bakeries():
    bakeries = Bakery.query.all()
    bakery_list = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakery_list), 200

@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)
    return jsonify(bakery.to_dict()), 200

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_list = [bg.to_dict() for bg in baked]
    return jsonify(baked_list), 200

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_baked_good = expensive.to_dict()
    return jsonify(most_expensive_baked_good), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
