"""Initialize Flask app."""
import library.adapters.repository as repo
from library.adapters.memory_repository import MemoryRepository, populate
from pathlib import Path
from flask import Flask, render_template
# TODO: Access to the books should be implemented via the repository pattern and using blueprints, so this can not stay here!
from library.domain.model import Book


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    data_path = Path('library') / 'adapters' / 'data'
    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    with app.app_context():

        from books_blueprint import books
        app.register_blueprint(books.books_blueprint)

        from authentication_blueprint import authentication
        app.register_blueprint(authentication.authentication_blueprint)

    return app
