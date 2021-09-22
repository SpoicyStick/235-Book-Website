"""Initialize Flask app."""
import library.adapters.repository as repo
from library.adapters.memory_repository import MemoryRepository, populate
from pathlib import Path
from flask import Flask, render_template
from authentication.authentication import logout





def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object('config.Config')


    data_path = Path('library') / 'adapters' / 'data'
    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
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
