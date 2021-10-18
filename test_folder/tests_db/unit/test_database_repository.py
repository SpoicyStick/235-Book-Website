import pytest

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository

from library.domain.model import User, Book, Author, Review, make_review
from library.adapters.repository import RepositoryException

def test_database_repository_can_get_users(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Stephen', '123456789')
    repo.add_user(user)

    repo.add_user(User('Grace', '123456789'))

    user2 = repo.get_user('Stephen')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('StphenGrace')
    assert user is None

def test_repository_can_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book= Book(
        1234, "book_title"
    )
    book.image="https://images.gr-assets.com/books/1503109082m/3995495.jpg"
    repo.add_book(book)

    assert repo.get_book(1234) == book


def test_repository_can_retrieve_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book(25742454)

    assert book.title == "The Switchblade Mamma"
    assert book.reviews[0].review_text == "Pretty average book"

    assert book.authors==[Author(8551671, "author")]
    assert book in book.authors[0].authorship


def test_repository_cant_retrieve_non_existent_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book(1)
    assert book == None


def test_repository_cant_retrieve_book_with_no_matching_info(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.search_by_isbn(1)
    assert books == []

    books = repo.search_by_title("non existent title")
    assert books == []

    books = repo.search_by_author("non existent author")
    assert books == []

    books = repo.search_by_publisher("Non existent author")
    assert books == []

    books = repo.search_by_release_year(2020)
    assert books == []

def test_repository_can_retrieve_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    authors = repo.get_authors()
    assert len(authors) == 55

def test_repository_can_sort(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert  (repo.sort_books_by_isbn())[0].book_id == 13571772
    assert (repo.sort_books_by_publisher())[0].publisher.name == "Avatar Press"
    assert (repo.sort_books_by_release_year()[0]).release_year == None
    assert  (repo.sort_books_by_title())[0].title == '20th Century Boys, Libro 15: ¡Viva la Expo! (20th Century Boys, #15)'


def test_repository_can_get_similar_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_book(13571772)
    assert len(book.similar_book) == 8


def test_repository_can_get_all_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_all_books()
    assert len(books)==30

def test_repository_can_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book(13571772)
    book.add_review(Review(book, "test", 5))
    assert len(book.reviews)==2

def test_repository_can_get_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_book(25742454)
    review = book.reviews[0]
    assert review.review_text == "Pretty average book"

def test_repository_can_get_page(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_page()

    assert len(books)==4
    assert len(books['1'])==8