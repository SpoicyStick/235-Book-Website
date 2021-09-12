import flask
from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired

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
        book_url = url_for('books_bp.book_info'),
        search_book_title_url = url_for('books_bp.search_by_book_title'),
        search_book_isbn_url=url_for('books_bp.search_by_book_isbn')
    )

@books_blueprint.route('/book')
def list_book():
    return render_template(
        'list_of_book.html',
        books = repo.repo_instance,
        home_url = url_for('books_bp.home'),
        list_url = url_for('books_bp.list_book'),
        book_url=url_for('books_bp.book_info'),
        search_book_title_url = url_for('books_bp.search_by_book_title'),
        search_book_isbn_url=url_for('books_bp.search_by_book_isbn')
    )
@books_blueprint.route('/book_info', methods=['GET'])
def book_info():
    book_id = int(request.args.get('book_id'))
    return render_template(
        'book_info.html',
        book = repo.repo_instance.get_book(book_id),
        home_url = url_for('books_bp.home'),
        list_url = url_for('books_bp.list_book'),
        search_book_title_url=url_for('books_bp.search_by_book_title'),
        search_book_isbn_url=url_for('books_bp.search_by_book_isbn')
    )
@books_blueprint.route('/search_book_title', methods=['GET', 'POST'])
def search_by_book_title():
    form = TitleSearchForm()
    if form.validate_on_submit():
        book_title = str(form.book_title.data)

        return render_template(
            'list_of_book.html',
            books= repo.repo_instance.search_by_title(book_title),
            home_url=url_for('books_bp.home'),
            list_url=url_for('books_bp.list_book'),
            search_book_title_url=url_for('books_bp.search_by_book_title'),
            search_book_isbn_url=url_for('books_bp.search_by_book_isbn')
        )
    return render_template(
        'search_book_title.html',
        form = form,
        home_url=url_for('books_bp.home'),
        list_url=url_for('books_bp.list_book'),
        search_book_title_url=url_for('books_bp.search_by_book_title'),
        search_book_isbn_url=url_for('books_bp.search_by_book_isbn')
    )

@books_blueprint.route('/search_book_isbn', methods=['GET', 'POST'])
def search_by_book_isbn():
    form = ISBNSearchForm()
    if form.validate_on_submit():
        book_isbn = int(form.book_isbn.data)

        return render_template(
            'list_of_book.html',
            books= repo.repo_instance.search_by_isbn(book_isbn),
            home_url=url_for('books_bp.home'),
            list_url=url_for('books_bp.list_book'),
            search_book_title_url=url_for('books_bp.search_by_book_title'),
            search_book_isbn_url=url_for('books_bp.search_by_book_isbn')
        )
    return render_template(
        'search_book_isbn.html',
        form = form,
        home_url=url_for('books_bp.home'),
        list_url=url_for('books_bp.list_book'),
        search_book_title_url=url_for('books_bp.search_by_book_title'),
        search_book_isbn_url=url_for('books_bp.search_by_book_isbn')
    )


class TitleSearchForm(FlaskForm):
    book_title = StringField('Book Title', [DataRequired()])
    submit = SubmitField('Find')

class ISBNSearchForm(FlaskForm):
    book_isbn = IntegerField('Book ISBN number', [DataRequired()])
    submit = SubmitField('Find')