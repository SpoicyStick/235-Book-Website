from library.domain.model import Book
from library.adapters.repository import AbstractRepository
from library.domain.model import make_review

class NonExistentBookException(Exception):
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


def search_by_release_year(release_year: int, repo: AbstractRepository):
    books = repo.search_by_release_year(release_year)
    return books


def search_by_publisher(publisher_name, repo: AbstractRepository):
    books = repo.search_by_publisher(publisher_name)
    return books

def search_by_author(author_name, repo: AbstractRepository):
    books = repo.search_by_author(author_name)
    return books

def add_review(book_id: int, review_text: str, user_name: str, rating: int, repo: AbstractRepository):
    # Check that the article exists.
    book = repo.get_book(book_id)

    if book is None:
        raise NonExistentBookException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    review = make_review(review_text, user, book, rating)

    repo.add_review(review)


def get_similar_books(book: Book, repo: AbstractRepository):
    similar_books = repo.get_similar_books(book)
    return similar_books


def sort_books_by_title(repo: AbstractRepository):
    return repo.sort_books_by_title()


def sort_books_by_isbn(repo: AbstractRepository):
    return repo.sort_books_by_isbn()


def sort_books_by_author(repo: AbstractRepository):
    return repo.sort_books_by_author()


def sort_books_by_release_year(repo: AbstractRepository):
    return repo.sort_books_by_release_year()


def sort_books_by_publisher(repo: AbstractRepository):
    return repo.sort_books_by_publisher()


def get_all_books(repo: AbstractRepository):
    return repo.get_all_books()
