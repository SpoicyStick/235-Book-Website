from pathlib import Path
from datetime import datetime
from typing import List

from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import Book, BooksInventory
from library.adapters.jsondatareader import BooksJSONReader

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__books = list()

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self) -> Book:
        if self._current >= len(self.__books):
            raise StopIteration
        else:
            self._current += 1
            return self.__books[self._current - 1]

    def add_book(self, book: Book):
        self.__books.append(book)

    def get_book(self, id: int):
        return next((book for book in self.__books if book.book_id == id), None)

    def search_by_title(self, title: str):
        matching =[]
        if isinstance(title, str):
            for book in self.__books:
                if book.title.lower() == title.lower():
                    matching.append(book)
        return matching

    def search_by_isbn(self, isbn: int):
        matching = []
        if isinstance(isbn, int):
            for book in self.__books:
                if book.isbn == isbn:
                    matching.append(book)
        else:
            return None;
        return matching

    def search_by_author(self, author_name: str):
        matching=[]
        if isinstance(author_name, str):
            for book in self.__books:
                for author in book.authors:
                    if author.full_name.lower() == author_name.lower():
                        matching.append(book)
        return matching

    def search_by_release_year(self, release_year):
        matching=[]
        if isinstance(release_year, int):
            for book in self.__books:
                if book.release_year == release_year:
                    matching.append(book)
        return matching

    def search_by_publisher(self, publisher_name):
        matching=[]
        if isinstance(publisher_name, str):
            for book in self.__books:
                if book.publisher.name.lower() == publisher_name.lower():
                    matching.append(book)
        return matching


def load_books(data_path: Path, repo: MemoryRepository):
    books_filename = str(data_path / "comic_books_excerpt.json")
    author_filename = str(data_path / "book_authors_excerpt.json")

    data = BooksJSONReader(books_filename, author_filename)
    data.read_json_files()

    for book in data.dataset_of_books:
        repo.add_book(book)

def populate(data_path: Path, repo: MemoryRepository):
    load_books(data_path, repo)