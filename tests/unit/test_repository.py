from datetime import date, datetime
from typing import List

import pytest

from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory, make_review
from library.adapters.repository import RepositoryException
from books.services import UnknownUserException

def test_repository_can_add_a_user(in_memory_repo):
    user = User('Grace', '123456789')
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user('Grace') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', 'mvNNbc1eLA$i')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_books_by_book_id(in_memory_repo):
    book = in_memory_repo.get_book(25742454)
    assert book == Book(25742454, "Title")


def test_repository_can_retrieve_books_by_isbn(in_memory_repo):
    book1 = in_memory_repo.search_by_isbn(2205073346)
    book2 = Book(30128855, "Cruelle")
    assert book1 == [book2]


def test_repository_can_retrieve_books_by_title(in_memory_repo):
    book1 = in_memory_repo.search_by_title("Cruelle")
    book2 = Book(30128855, "Cruelle")
    assert book1 == [book2]


def test_repository_can_retrieve_books_by_author(in_memory_repo):
    book1 = in_memory_repo.search_by_author("Florence Dupre la Tour")
    book2 = Book(30128855, "Cruelle")
    book2.authors.append(Author(37450, "Authorname"))
    assert book1 == [book2]


def test_repository_can_retrieve_books_by_publisher(in_memory_repo):
    book1 = in_memory_repo.search_by_publisher("Dargaud")
    book2 = Book(30128855, "Cruelle")
    book2.publisher = "Dargaud"
    assert book1 == [book2]


def test_repository_can_retrieve_books_by_release_year(in_memory_repo):
    book1 = in_memory_repo.search_by_release_year(2013)
    book2 = Book(17405342, "Title")
    book2.publisher = 2013
    assert book1 == [book2]


def test_repository_returns_an_empty_list_for_non_existent_search_results(in_memory_repo):
    book1 = in_memory_repo.search_by_title("Non-Existent")
    assert book1 == []
    book2 = in_memory_repo.search_by_publisher("Non-Existent")
    assert book2 == []
    book3 = in_memory_repo.search_by_isbn(1000)
    assert book3 == []
    book4 = in_memory_repo.search_by_author("Non-Existent")
    assert book4 == []
    book5 = in_memory_repo.search_by_release_year(2020)
    assert book5 == []


def test_repository_can_add_a_review(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    book = in_memory_repo.get_book(30128855)
    review = make_review("Very good book!", user, book, 5)

    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_review()


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    book = in_memory_repo.get_book(30128855)
    review = make_review("Very good book!", None, book, 5)

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_review(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    book = in_memory_repo.get_book(30128855)
    review = make_review("Very good book!", user, book, 5)
    in_memory_repo.add_review(review)

    user = in_memory_repo.get_user('thorke')
    book = in_memory_repo.get_book(30128855)
    review = make_review("Very bad book!", user, book, 1)
    in_memory_repo.add_review(review)
    assert len(in_memory_repo.get_review()) == 2
