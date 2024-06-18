from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    isActive = db.Column(db.Boolean, default = True)

    def __repr__(self):
        return f'{self.title}'


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/support')
def support():
    return render_template('support.html')


@app.route('/create', methods = ['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        
        item = Item(title=title, price=price )
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(str(e))
            return 'There is an error'

    else:
        return render_template('create.html')
    
@app.route('/buy/<int:id>')
def buy(id):
    return f'Felecitations {id}'

if __name__ == '__main__':
    app.run(debug=True)