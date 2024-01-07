 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    isbn = db.Column(db.String(13), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        description = request.form['description']

        book = Book(title=title, author=author, isbn=isbn, description=description)
        db.session.add(book)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_book.html')

@app.route('/book_detail/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()
    return render_template('book_detail.html', book=book, reviews=reviews)

@app.route('/add_review/<int:book_id>', methods=['GET', 'POST'])
def add_review(book_id):
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        rating = request.form['rating']

        review = Review(title=title, body=body, rating=rating, book_id=book_id)
        db.session.add(review)
        db.session.commit()

        return redirect(url_for('book_detail', book_id=book_id))

    return render_template('add_review.html')

if __name__ == '__main__':
    app.run()
