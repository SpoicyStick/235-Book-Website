from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from library.domain.model import User, Book, Review
from library.adapters.repository import AbstractRepository

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_book(self, book: Book):
        return

    def get_book(self, book) -> Book:
        return

    def get_user(self, user_name) -> User:
        return

    def add_user(self, user: User):
        return

    def search_by_title(self, title: str):
        return

    def search_by_isbn(self, isbn: int):
        return

    def search_by_author(self, author_name: str):
        return

    def search_by_release_year(self, release_year: int):
        return

    def search_by_publisher(self, publisher: int):
        return

    def get_page(self):
        return

    def add_review(self, review: Review):
        return

    def get_review(self):
        return

    def sort_books_by_title(self):
        return

    def sort_books_by_isbn(self):
        return

    def sort_books_by_release_year(self):
        return

    def sort_books_by_publisher(self):
        return

    def get_similar_books(self):
        return

    def get_all_books(self):
        return