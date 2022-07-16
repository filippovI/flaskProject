from flask import Flask, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

from utils.config import DEBUG

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analytics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    offer_id = db.Column(db.Integer)
    name = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100))
    state_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Items %r>' % self.id


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    admin = db.Column(db.String(5), nullable=False, default="False")

    def __repr__(self):
        return '<Users %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ozon_stat')
def ozon():
    items = Items.query.all()
    return render_template('ozon_stat.html', title='Статистика Ozon', items=items)


@app.route('/kazan_stat')
def kazan():
    return render_template('kazan_stat.html', title='Статистика Kazan')


if __name__ == '__main__':
    app.run(debug=DEBUG)
