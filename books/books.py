import flask
from flask import Blueprint, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, IntegerField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
# from better_profanity import profanity
from authentication.authentication import login_required

import books.services as services
import library.adapters.repository as repo

books_blueprint = Blueprint(
    'books_bp', __name__)


@books_blueprint.route('/list_book')
def list_book():
    if (session.get('logged_in')==True):
        user_name = (session.get('user_name'))
    else:
        user_name = None
    form = BookSearch()
    clicked_page_number = '1'
    try:
        if request.args.get('clicked_page_number') != None:
            clicked_page_number = str(request.args.get('clicked_page_number'))
    except:
        pass
    return render_template(
        'list_of_book.html',
        page_number=len(services.get_page(repo.repo_instance)) + 1,
        form=form,
        user_name = user_name,
        books=(services.get_page(repo.repo_instance))[str(clicked_page_number)],
        home_url=url_for('home_bp.home'),
        list_url=url_for('books_bp.list_book'),
        book_url=url_for('books_bp.book_info')
    )

@books_blueprint.route('/list_book_by_title')
def list_book_by_title():

    if (session.get('logged_in')==True):
        user_name = (session.get('user_name'))
    else:
        user_name = None
    form = BookSearch()
    clicked_page_number = '1'
    try:
        if request.args.get('clicked_page_number') != None:
            clicked_page_number = str(request.args.get('clicked_page_number'))
    except:
        pass
    return render_template(
        'list_of_book.html',
        page_number=len(services.get_page(repo.repo_instance)) + 1,
        form=form,
        user_name = user_name,
        books = services.sort_books_by_title(repo.repo_instance),
        home_url=url_for('home_bp.home'),
        list_url=url_for('books_bp.list_book'),
        book_url=url_for('books_bp.book_info')
    )

@books_blueprint.route('/list_book_by_isbn')
def list_book_by_isbn():

    if (session.get('logged_in')==True):
        user_name = (session.get('user_name'))
    else:
        user_name = None
    form = BookSearch()
    clicked_page_number = '1'
    try:
        if request.args.get('clicked_page_number') != None:
            clicked_page_number = str(request.args.get('clicked_page_number'))
    except:
        pass
    return render_template(
        'list_of_book.html',
        page_number=len(services.get_page(repo.repo_instance)) + 1,
        form=form,
        user_name = user_name,
        books = services.sort_books_by_isbn(repo.repo_instance),
        home_url=url_for('home_bp.home'),
        list_url=url_for('books_bp.list_book'),
        book_url=url_for('books_bp.book_info')
    )

@books_blueprint.route('/list_book_by_release_year')
def list_book_by_release_year():

    if (session.get('logged_in')==True):
        user_name = (session.get('user_name'))
    else:
        user_name = None
    form = BookSearch()
    clicked_page_number = '1'
    try:
        if request.args.get('clicked_page_number') != None:
            clicked_page_number = str(request.args.get('clicked_page_number'))
    except:
        pass
    return render_template(
        'list_of_book.html',
        page_number=len(services.get_page(repo.repo_instance)) + 1,
        form=form,
        user_name = user_name,
        books = services.sort_books_by_release_year(repo.repo_instance),
        home_url=url_for('home_bp.home'),
        list_url=url_for('books_bp.list_book'),
        book_url=url_for('books_bp.book_info')
    )

@books_blueprint.route('/list_book_by_publisher')
def list_book_by_publisher():

    if (session.get('logged_in')==True):
        user_name = (session.get('user_name'))
    else:
        user_name = None
    form = BookSearch()
    clicked_page_number = '1'
    try:
        if request.args.get('clicked_page_number') != None:
            clicked_page_number = str(request.args.get('clicked_page_number'))
    except:
        pass
    return render_template(
        'list_of_book.html',
        page_number=len(services.get_page(repo.repo_instance)) + 1,
        form=form,
        user_name = user_name,
        books = services.sort_books_by_publisher(repo.repo_instance),
        home_url=url_for('home_bp.home'),
        list_url=url_for('books_bp.list_book'),
        book_url=url_for('books_bp.book_info')
    )

@books_blueprint.route('/book_info', methods=['GET'])
def book_info():
    if (session.get('logged_in')==True):
        user_name = (session.get('user_name'))
    else:
        user_name = None
    form = BookSearch()
    book_id = int(request.args.get('book_id'))

    return render_template(
        'book_info.html',
        form=form,
        user_name=user_name,
        book=services.get_book(book_id, repo.repo_instance),
        similar_books= services.get_similar_books(services.get_book(book_id, repo.repo_instance), repo.repo_instance),
        home_url=url_for('home_bp.home'),
        list_url=url_for('books_bp.list_book'),
        numbers = {"numbers": range(5)}
    )


@books_blueprint.route('/search_book', methods=['GET', 'POST'])
def search_book():
    if (session.get('logged_in') == True):
        user_name = (session.get('user_name'))
    else:
        user_name = None
    form = BookSearch()
    search_by = (request.args.get('search_by'))
    search_value = (request.args.get('search_value'))
    if search_by == "TITLE":
        book_title = str(search_value)
        return render_template(
            'list_of_book.html',
            form=form,
            user_name = user_name,
            page_number=1,
            books=services.search_by_title(book_title, repo.repo_instance),
            home_url=url_for('home_bp.home'),
            list_url=url_for('books_bp.list_book'),

        )
    elif search_by == "AUTHOR":
        book_author = str(search_value)
        return render_template(
            'list_of_book.html',
            form=form,
            user_name=user_name,
            page_number=1,
            books=services.search_by_author(book_author, repo.repo_instance),
            home_url=url_for('home_bp.home'),
            list_url=url_for('books_bp.list_book'),
        )
    elif search_by == "PUBLISHER":
        try:
            book_publisher = int(search_value)
        except:
            return render_template(
                'list_of_book.html',
                form=form,
                user_name=user_name,
                page_number=1,
                books=services.search_by_publisher(str(search_value), repo.repo_instance),
                home_url=url_for('home_bp.home'),
                list_url=url_for('books_bp.list_book'),
            )
        return render_template(
            'list_of_book.html',
            form=form,
            user_name=user_name,
            books=None,
            page_number=1,
            home_url=url_for('home_bp.home'),
            list_url=url_for('books_bp.list_book'),
        )
    elif search_by == "ISBN":
        try:
            book_isbn = int(search_value)
        except:
            book_isbn = None;
        return render_template(
            'list_of_book.html',
            form=form,
            user_name=user_name,
            page_number=1,
            books=services.search_by_isbn(book_isbn, repo.repo_instance),
            home_url=url_for('home_bp.home'),
            list_url=url_for('books_bp.list_book'),

        )
    else:
        try:
            book_release_year = int(search_value)
        except:
            book_release_year = None;
        if isinstance(book_release_year, int) and book_release_year >= 0:
            return render_template(
                'list_of_book.html',
                form=form,
                user_name=user_name,
                page_number=1,
                books=services.search_by_release_year(book_release_year, repo.repo_instance),
                home_url=url_for('home_bp.home'),
                list_url=url_for('books_bp.list_book'),
            )
        else:
            return render_template(
                'list_of_book.html',
                form=form,
                user_name=user_name,
                page_number=1,
                books=None,
                home_url=url_for('home_bp.home'),
                list_url=url_for('books_bp.list_book'),
            )


@books_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_a_book():
    user_name = session['user_name']
    reviewForm = ReviewForm()
    form = BookSearch()
    if reviewForm.validate_on_submit():
        book_id = int(float(reviewForm.book_id.data))
        rating = int(reviewForm.rating.data)
        services.add_review(book_id, reviewForm.review.data, user_name, rating, repo.repo_instance)

        return redirect(url_for('books_bp.list_book'))

    if request.method == 'GET':
        book_id = int(request.args.get('book_id'))
        reviewForm.book_id.data = book_id
    else:
        book_id = int(reviewForm.book_id.data)
    book = services.get_book(book_id, repo.repo_instance)
    return render_template(
        'review.html',
        book=book,
        user = user_name,
        reviewForm=reviewForm,
        form=form,
        handler_url=url_for('books_bp.review_a_book')
    )


class ReviewForm(FlaskForm):
    review = TextAreaField('Write a review for', [DataRequired(), Length(min=4, message='Your comment is too short')])  # , ProfanityFree(message='Your comment must not contain profanity')
    book_id = HiddenField("Book id")
    rating = SelectField("Rating", choices=[("5", "⭐⭐⭐⭐⭐"), ("4", "⭐⭐⭐⭐"), ("3", "⭐⭐⭐"), ("2", "⭐⭐"), ("1", "⭐")])
    submit = SubmitField('Submit')



class BookSearch(FlaskForm):
    search_by = SelectField('Search by', choices=[("TITLE", "Title"), ("ISBN", "ISBN"), ("AUTHOR", "Author"),
                                                  ("RELEASE", "Release year"), ("PUBLISHER", "Publisher")],
                            default=("TITLE", "Title"))
    search_value = StringField('Search value', [DataRequired()],
                               render_kw={"placeholder": "\U0001F50E\uFE0E" + "Search.."})
    submit = SubmitField('Find')
