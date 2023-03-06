from flask import Flask, jsonify, request,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
from flask import LoginManager
from flask import login_required


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def _repr_(self):
        return'< Name % r>' % self.id
    
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html') 

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/books', methods=['POST'])
def create_book():
    title = request.json['title']
    author = request.json['author']
    book = Book(title=title, author=author)
    db.session.add(book)
    db.session.commit()
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author})


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    result = []
    for book in books:
        result.append({'id': book.id, 'title': book.title, 'author': book.author})
    return jsonify({'books': result})


@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({'error': 'Book not found'})
    title = request.json.get('title')
    author = request.json.get('author')
    if title is not None:
        book.title = title
    if author is not None:
        book.author = author
    db.session.commit()
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author})


@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({'error': 'Book not found'})
    db.session.delete(book)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/books/<string:title>', methods=['GET'])
def get_book_by_title(title):
    book = Book.query.filter_by(title=title).first()
    if book is None:
        return jsonify({'error': 'Book not found'})
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data and store it in database
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Add code to store the user information in your database using SQLAlchemy

        # Redirect user to sign in page
        return redirect(url_for('signin'))
    else:
        # Display sign up form
        return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Retrieve login credentials and check against stored user information
        email = request.form['email']
        password = request.form['password']
        # Add code to check if the login credentials are valid

        if login_successful:
            # Redirect user to private page or display success message
            return redirect(url_for('private'))
        else:
            # Display error message
            return render_template('signin.html', error='Invalid login credentials')
    else:
        # Display sign in form
        return render_template('signin.html')


if __name__ == '__main__':
    app.run(debug=True)
