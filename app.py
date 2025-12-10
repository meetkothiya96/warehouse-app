import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///warehouse.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return f'<Location {self.name}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location', backref='products')

    def __repr__(self):
        return f'<Product {self.name}>'


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        location_name = request.form['location_name']
        new_loc = Location(name=location_name)

        try:
            db.session.add(new_loc)
            db.session.commit()
            return redirect('/')
        except:
            return "Error Adding Location.."

    else:
        locations = Location.query.all()
        return render_template('index.html', locations=locations)


@app.route('/add_product', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product_name'] 
        product_quantity = request.form['product_quantity']
        loc_id = request.form['location_id'] 

        new_product = Product(name=product_name, quantity=product_quantity, location_id=loc_id)

        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your product..'

    else:
        locations = Location.query.all()
        return render_template('add_product.html', locations=locations)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)

