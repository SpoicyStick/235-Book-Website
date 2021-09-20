from library.domain.model import Book, BooksInventory, User, Author, Publisher
from library.adapters.repository import AbstractRepository
from library.domain.model import make_review, Review

class NonExistentArticleException(Exception):
    pass


class UnknownUserException(Exception):
    pass

def get_page(repo: AbstractRepository):
    books = repo.get_page()
    return books

def get_book(book_id: int, repo: AbstractRepository):
    books = repo.get_book(book_id)
    return books


def search_by_title(title: str, repo: AbstractRepository):
    books = repo.search_by_title(title)
    return books


def search_by_isbn(isbn: int, repo: AbstractRepository):
    books = repo.search_by_isbn(isbn)
    return books


def search_by_author(author_name: str, repo: AbstractRepository):
    books = repo.search_by_author(author_name)
    return books


def search_by_release_year(release_year: int, repo: AbstractRepository):
    books = repo.search_by_release_year(release_year)
    return books


def search_by_publisher(publisher_name, repo: AbstractRepository):
    books = repo.search_by_publisher(publisher_name)
    return books

def add_review(book_id: int, review_text: str, user_name: str, rating: int, repo: AbstractRepository):
    # Check that the article exists.
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentArticleException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create comment.
    review = make_review(review_text, user, book, rating)

    # Update the repository.
    repo.add_review(review)

