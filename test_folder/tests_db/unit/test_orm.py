import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from library.domain.model import User, Book, Review, Publisher, Author, make_author_association, make_review

def insert_user(empty_session, values=None):
    name = "GraceKim"
    password = "Yumi1123"

    if values is not None:
        name = values[0]
        password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': name, 'password': password})

    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_book(empty_session):
    empty_session.execute(
        'INSERT INTO books (id, isbn, title, description, release_year, ebook, num_pages, image, rating) VALUES '
        '(1234, 12345, "book title", "book_description", 2020, 1, 123, "https://images.gr-assets.com/books/1503109082m/3995495.jpg", 5)'
    )
    row = empty_session.execute('SELECT id from books').fetchone()
    return row[0]

def insert_authors(empty_session):
    empty_session.execute(
        'INSERT INTO authors (id, name) VALUES (1234, "author name")'
    )
    rows = list(empty_session.execute('SELECT id FROM authors'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_book_author_associations(empty_session, book_key, author_keys):
    stmt = 'INSERT INTO authorships (book_id, author_id) VALUES (:book_id, :author_id)'
    for author_key in author_keys:
        empty_session.execute(stmt, {'book_id': book_key, 'author_id': author_key})

def insert_reviewed_book(empty_session):
    book_key = insert_book(empty_session)
    user_key = insert_user(empty_session)

    empty_session.execute(
        'INSERT INTO reviews (user_id, book_id, description, rating) VALUES '
        '(:user_id, :book_id, "Comment 1", 5),'
        '(:user_id, :book_id, "Comment 2", 4)',
        {'user_id': user_key, 'book_id': book_key}
    )
    row = empty_session.execute('SELECT id FROM books').fetchone()
    return row[0]

def make_book():
    book= Book(
        1234, "book_title"
    )
    book.image="https://images.gr-assets.com/books/1503109082m/3995495.jpg"
    return book

def make_user():
    user= User("swon778", "password1")
    return user

def make_author():
    author = Author(4312, "Author1")
    return author

def test_loading_users(empty_session):
    users= list()
    users.append(("User1111", "awd12345"))
    users.append(("User1112", "5432asd"))
    insert_users(empty_session, users)

    expected = [
        User("User1111", "awd12345"),
        User("User1112", "5432asd")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_users(empty_session):
    user=make_user()
    empty_session.add(user)
    empty_session.commit()
    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("swon778", "password1")]

def test_saving_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("GraceKim", "Yumi1123"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("GraceKim", "Yumi1123")
        empty_session.add(user)
        empty_session.commit()

def test_loading_book(empty_session):
    book_key = insert_book(empty_session)
    expected_book = make_book()
    fetched_book = empty_session.query(Book).one()
    assert expected_book == fetched_book
    assert book_key == fetched_book.book_id

def test_loading_authorship(empty_session):
    book_key = insert_book(empty_session)
    author_keys = insert_authors(empty_session)
    insert_book_author_associations(empty_session, book_key, author_keys)

    book = empty_session.query(Book).get(book_key)
    authors = [empty_session.query(Author).get(key) for key in author_keys]

    for author in authors:
        assert author in book.authors
        assert book in author.authorship

def test_loading_reviewed_book(empty_session):
    insert_reviewed_book(empty_session)
    rows = empty_session.query(Book).all()
    book = rows[0]

    for review in book.reviews:
        assert review.book is book

def test_saving_comment(empty_session):
    book_key = insert_book(empty_session)
    user_key = insert_user(empty_session, ("GraceKim", "Yumi1123"))

    rows = empty_session.query(Book).all()
    book = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "GraceKim").one()

    review_text = "Review text"
    review = make_review(review_text, user, book, 5)

    empty_session.add(review)
    empty_session.commit

    rows = list(empty_session.execute('SELECT user_id, book_id, description FROM reviews'))
    assert rows == [(user_key, book_key, review_text)]

def test_saving_book(empty_session):
    book =make_book()
    empty_session.add(book)
    empty_session.commit()
    rows = list(empty_session.execute('SELECT title FROM books'))
    assert rows == [('book_title',)]


def test_saving_authorship(empty_session):
    book = make_book()
    author = make_author()

    make_author_association(book, author)

    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id FROM books'))
    book_key = rows[0][0]

    rows = list(empty_session.execute('SELECT id, name FROM authors'))
    author_key = rows[0][0]
    assert  rows[0][1] == "Author1"

    rows = list(empty_session.execute('SELECT book_id, author_id FROM authorships'))

    book_fk = rows[0][0]
    author_fk = rows[0][1]

    assert book_key == book_fk
    assert author_key == author_fk

def test_save_reviewed_book(empty_session):
    book = make_book()
    user = make_user()

    review_text = "review texts"
    review = make_review(review_text, user, book, 5)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id FROM books'))
    book_key = rows[0][0]

    rows = list(empty_session.execute('SELECT id FROM users'))
    user_key = rows[0][0]

    rows = list(empty_session.execute('SELECT user_id, book_id, description, rating FROM reviews'))
    assert  rows == [(user_key, book_key, review_text, 5)]

