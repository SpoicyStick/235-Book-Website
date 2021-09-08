"""Initialize Flask app."""

from flask import Flask, render_template

# TODO: Access to the books should be implemented via the repository pattern and using blueprints, so this can not stay here!
from library.domain.model import Book

# TODO: Access to the books should be implemented via the repository pattern and using blueprints, so this can not stay here!
def create_some_book():
    some_book = Book(1, "Harry Potter and the Chamber of Secrets")
    some_book.description = "Ever since Harry Potter had come home for the summer, the Dursleys had been so mean \
                             and hideous that all Harry wanted was to get back to the Hogwarts School for \
                             Witchcraft and Wizardry. But just as he’s packing his bags, Harry receives a \
                             warning from a strange impish creature who says that if Harry returns to Hogwarts, \
                             disaster will strike."
    some_book.release_year = 1999
    return some_book


def create_app():
    app = Flask(__name__)
    create_some_book()

    with app.app_context():
        from books_blueprint import books
        app.register_blueprint(books.books_blueprint)

    return app
