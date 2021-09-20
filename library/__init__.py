"""Initialize Flask app."""
import library.adapters.repository as repo
from library.adapters.memory_repository import MemoryRepository, populate
from pathlib import Path
from flask import Flask, render_template



def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    data_path = Path('library') / 'adapters' / 'data'
    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    with app.app_context():

        from books import books
        app.register_blueprint(books.books_blueprint)

        from authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from home import home
        app.register_blueprint(home.home_blueprint)
    return app
