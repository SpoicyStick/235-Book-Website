import flask
from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired

import library.adapters.repository as repo
from library.domain.model import Book
books_blueprint = Blueprint(
    'books_bp', __name__
)


@books_blueprint.route('/')
def home():
    form = BookSearch()
    return render_template(
        'home.html',
        form= form,
        home_url = url_for('books_bp.home'),
        list_url = url_for('books_bp.list_book'),
        book_url = url_for('books_bp.book_info'),

    )

@books_blueprint.route('/book')
def list_book():
    form = BookSearch()
    return render_template(
        'list_of_book.html',
        form = form,
        books = repo.repo_instance,
        home_url = url_for('books_bp.home'),
        list_url = url_for('books_bp.list_book'),
        book_url=url_for('books_bp.book_info'),

    )
@books_blueprint.route('/book_info', methods=['GET'])
def book_info():
    form = BookSearch()
    book_id = int(request.args.get('book_id'))
    return render_template(
        'book_info.html',
        form = form,
        book = repo.repo_instance.get_book(book_id),
        home_url = url_for('books_bp.home'),
        list_url = url_for('books_bp.list_book'),

    )

@books_blueprint.route('/search_book', methods=['GET', 'POST'])
def search_book():
    form = BookSearch()
    search_by= (request.args.get('search_by'))
    search_value= (request.args.get('search_value'))
    if search_by == "TITLE":
        book_title = str(search_value)
        return render_template(
            'list_of_book.html',
            form = form,
            books= repo.repo_instance.search_by_title(book_title),
            home_url=url_for('books_bp.home'),
            list_url=url_for('books_bp.list_book'),

        )
    elif search_by == "ISBN":
        book_isbn = int(search_value)
        return render_template(
            'list_of_book.html',
            form= form,
            books= repo.repo_instance.search_by_isbn(book_isbn),
            home_url=url_for('books_bp.home'),
            list_url=url_for('books_bp.list_book'),

        )
    return "asd"


class TitleSearchForm(FlaskForm):
    book_title = StringField('Book Title', [DataRequired()])
    submit = SubmitField('Find')

class ISBNSearchForm(FlaskForm):
    book_isbn = IntegerField('Book ISBN number', [DataRequired()])
    submit = SubmitField('Find')


class BookSearch(FlaskForm):
    search_by = SelectField('Search by', choices=[("TITLE", "Title"), ("ISBN", "ISBN")], default= ("TITLE", "Title"))
    search_value= StringField('Search value', [DataRequired()],  render_kw={"placeholder": "\U0001F50E\uFE0E" + "Search.."})
    submit = SubmitField('Find')