from pathlib import Path
from datetime import datetime
from typing import List
import csv

from werkzeug.security import generate_password_hash
from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import Book, BooksInventory, User, Review
from library.adapters.jsondatareader import BooksJSONReader

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__books = list()
        self.__users = list()
        self.__pages = dict()
        self.__reviews = list()

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self) -> Book:
        if self._current >= len(self.__books):
            raise StopIteration
        else:
            self._current += 1
            return self.__books[self._current - 1]

    def get_page(self):
        key = 0
        for num in self.__books:
            if self.__books.index(num) % 10 == 0:
                key += 1
                self.__pages[str(key)] = []
                self.__pages[str(key)].append(num)
            else:
                self.__pages[str(key)].append(num)
        return(self.__pages)

    def add_book(self, book: Book):
        self.__books.append(book)

    def get_book(self, id: int):
        return next((book for book in self.__books if book.book_id == id), None)

    def search_by_title(self, title: str):
        matching =[]
        if isinstance(title, str):
            for book in sorted(self.__books, key=lambda x: x.title.lower()):
                if book.title.lower() == title.lower():
                    matching.append(book)
        return matching

    def search_by_isbn(self, isbn: int):
        matching = []
        if isinstance(isbn, int):
            for book in sorted(self.__books, key=lambda x: -1 if x.isbn is None else x.isbn):
                if book.isbn == isbn:
                    matching.append(book)
        else:
            return None
        return matching

    def search_by_author(self, author_name: str):
        matching=[]
        if isinstance(author_name, str):
            for book in self.__books:
                for author in sorted(book.authors, key=lambda x: x.full_name.lower()):
                    if author.full_name.lower() == author_name.lower():
                        matching.append(book)
        return matching

    def search_by_release_year(self, release_year):
        matching=[]
        if isinstance(release_year, int):
            for book in sorted(self.__books, key=lambda x: -1 if x.release_year is None else x.release_year):
                if book.release_year == release_year:
                    matching.append(book)
        return matching

    def search_by_publisher(self, publisher_name):
        matching=[]
        if isinstance(publisher_name, str):
            for book in sorted(self.__books, key=lambda x: x.publisher.name.lower()):
                if book.publisher.name.lower() == publisher_name.lower():
                    matching.append(book)
        return matching

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_review(self):
        return self.__reviews

    def add_review(self, review: Review):
        super().add_review(review)
        self.__reviews.append(review)

    def get_similar_books(self, book: Book):
        matching = []
        for book_id in book.similar_book:
            book= self.get_book(book_id)
            if book!=None:
                matching.append(book)
        return matching

def load_books(data_path: Path, repo: MemoryRepository):
    books_filename = str(data_path / "comic_books_excerpt.json")
    author_filename = str(data_path / "book_authors_excerpt.json")

    data = BooksJSONReader(books_filename, author_filename)
    data.read_json_files()

    for book in data.dataset_of_books:
        repo.add_book(book)


def load_users(data_path: Path, repo: MemoryRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users

def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row

def populate(data_path: Path, repo: MemoryRepository):
    load_books(data_path, repo)
    users = load_users(data_path, repo)