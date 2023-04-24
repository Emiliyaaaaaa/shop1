import pytest
import flask_sqlalchemy
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)


@pytest.fixture()
def app_context():
    with app.app_context():
        yield


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.LargeBinary, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title


# @app.route('/buy/<int:id>')
# def item_buy(id):
#    item= Item.query.get(id)
#     api = Api(merchant_id=1396424,
#               secret_key='test')
#     checkout = Checkout(api=api)
#    data = {
#       "currency": "RUB",
#         "amount": str(item.price) + "00"
#     }
#     url = checkout.url(data).get('checkout_url')
#     return redirect(url)


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():  # put application's code here
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        photo = request.form['photo']
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        item = Item(photo=photo, title=title, description=description, price=price)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except SystemExit:
            return "Получилась ошибка"
    else:
        return render_template('create.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,host='localhost', port=5000)
