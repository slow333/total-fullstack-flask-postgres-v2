from flask import Blueprint, request, jsonify
from ...models import Book
from ...extensions import db

bp = Blueprint('rest_api_book_bp', __name__, url_prefix='/apps/books')

@bp.route('/', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify(books)

@bp.route('/', methods=['POST'])
def create_book():
    data = request.get_json()

    new_book =db.session.add(Book(title=data.get("title"), 
                        author=data.get("author"), 
                        language=data.get("language"), 
                        published_date=data.get("published_date")))
    db.session.commit()

    return jsonify(new_book), 201

@bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = db.session.get(Book, book_id)

    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)

@bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = db.session.get(Book, book_id)
    book.title = data.get("title")
    book.author = data.get("author")
    book.language = data.get("language")
    book.published_date = data.get("published_date")
    db.session.commit()

    return jsonify({"message": "Book updated successfully"})

@bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    db.session.delete(Book, book_id)
    db.session.commit()

    return jsonify({"message": "Book deleted successfully"})