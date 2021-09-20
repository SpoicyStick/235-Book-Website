import flask
from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired

import library.adapters.repository as repo


home_blueprint = Blueprint(
    'home_bp', __name__
)


@home_blueprint.route('/', methods=['GET'])
def home():
    form = BookSearch()
    return render_template(
        'home.html',
        form= form,
        home_url = url_for('home_bp.home'),
        list_url = url_for('books_bp.list_book'),
        book_url = url_for('books_bp.book_info'),

    )


class BookSearch(FlaskForm):
    search_by = SelectField('Search by', choices=[("TITLE", "Title"), ("ISBN", "ISBN"), ("AUTHOR", "Author"), ("RELEASE", "Release year"), ("PUBLISHER", "Publisher")], default= ("TITLE", "Title"))
    search_value= StringField('Search value', [DataRequired()],  render_kw={"placeholder": "\U0001F50E\uFE0E" + "Search.."})
    submit = SubmitField('Find')