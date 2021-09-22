import flask
from flask import Blueprint, render_template, url_for, session

from books.books import BookSearch


home_blueprint = Blueprint(
    'home_bp', __name__
)


@home_blueprint.route('/', methods=['GET'])
def home():
    if (session.get('logged_in')==True):
        user_name = (session.get('user_name'))
    else:
        user_name = None
    form = BookSearch()
    return render_template(
        'home.html',
        form= form,
        user_name=user_name,
        home_url = url_for('home_bp.home'),
        list_url = url_for('books_bp.list_book'),
        book_url = url_for('books_bp.book_info'),

    )

