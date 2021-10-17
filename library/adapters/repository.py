import abc
from datetime import datetime
from typing import List

from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory

repo_instance = None

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):
    #@abc.abstractmethod
    #def __iter__(self):
        #raise NotImplementedError

   #@abc.abstractmethod
    #def __next__(self) -> Book:
        #raise NotImplementedError

    @abc.abstractmethod
    def add_author(self, author: Author):
        raise NotImplementedError

    @abc.abstractmethod
    def get_authors(self) -> Author:
        raise NotImplementedError

    @abc.abstractmethod
    def add_book(self, book: Book):
        raise NotImplementedError

    @abc.abstractmethod
    def get_book(self, book) -> Book:
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_title(self, title: str):
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_isbn(self, isbn: int):
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_author(self, author_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_release_year(self, release_year: int):
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_publisher(self, publisher: int):
        raise NotImplementedError


    @abc.abstractmethod
    def get_page(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Comment not correctly attached to a User')
        if review.book is None or review not in review.book.reviews:
            raise RepositoryException('Comment not correctly attached to an Article')

    @abc.abstractmethod
    def get_review(self):
        raise NotImplementedError

    @abc.abstractmethod
    def sort_books_by_title(self):
        raise NotImplementedError

    @abc.abstractmethod
    def sort_books_by_isbn(self):
        raise NotImplementedError


    @abc.abstractmethod
    def sort_books_by_release_year(self):
        raise NotImplementedError

    @abc.abstractmethod
    def sort_books_by_publisher(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_similar_books(self):
      raise NotImplementedErr
      
    @abc.abstractmethod
    def get_all_books(self):
        raise NotImplementedError
