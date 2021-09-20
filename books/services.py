from library.domain.model import Book, BooksInventory, User, Author, Publisher
from library.adapters.repository import AbstractRepository


def get_page(repo: AbstractRepository):
    books = repo.get_page()
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


