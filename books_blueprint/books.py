from flask import Blueprint, render_template, url_for, request
import library.adapters.repository as repo
from library.domain.model import Book
books_blueprint = Blueprint(
    'books_bp', __name__
)


@books_blueprint.route('/')
def home():
    return render_template(
        'home.html',
        home_url = url_for('books_bp.home'),
        list_url = url_for('books_bp.list_book'),
        book_url = url_for('books_bp.simple_book')
    )

@books_blueprint.route('/book')
def list_book():
    return render_template(
        'list_of_book.html',
        books = repo.repo_instance,
        home_url = url_for('books_bp.home'),
        list_url = url_for('books_bp.list_book'),
        book_url=url_for('books_bp.simple_book')
    )
@books_blueprint.route('/single_book', methods=['GET', 'POST'])
def simple_book():
    book_id = int(request.form['book_id'])
    a_book = Book(book_id, "Harry Potter and the Chamber of Secrets")
    a_book.description = "Ever since Harry Potter had come home for the summer, the Dursleys had been so mean \
                         and hideous that all Harry wanted was to get back to the Hogwarts School for \
                         Witchcraft and Wizardry. But just as he’s packing his bags, Harry receives a \
                         warning from a strange impish creature who says that if Harry returns to Hogwarts, \
                         disaster will strike."
    a_book.release_year = 1999
    a_book.ebook = False
    a_book.image = "https://d1w7fb2mkkr3kw.cloudfront.net/assets/images/book/lrg/9781/4088/9781408855669.jpg"
    return render_template(
        'simple_book.html',
        book = a_book,
        home_url = url_for('books_bp.home'),
        list_url = url_for('books_bp.list_book'),
        book_url=url_for('books_bp.simple_book')
    )