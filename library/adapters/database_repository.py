from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from library.domain.model import User, Book, Review, Author, Publisher
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

    def add_author(self, author: Author):
        with self._session_cm as scm:
            scm.session.add(author)
            scm.commit()

    def get_authors(self) -> Author:
        authors = self._session_cm.session.query(Author).all()
        return authors

    def add_book(self, book: Book):
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()

    def get_book(self, target_book_id) -> Book:
        if target_book_id is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            books = self._session_cm.session.query(Book).filter(Book.book_id==target_book_id).all()
            return books

    def get_user(self, user_name) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_publisher(self, publisher_name) -> Publisher:
        publisher = None
        try:
            publisher = self._session_cm.session.query(User).filter(Publisher._Publisher__name == publisher_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return publisher

    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.add(publisher)
            scm.commit()


    def search_by_title(self, title: str):
        if title is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return articles matching target_date; return an empty list if there are no matches.
            articles = self._session_cm.session.query(Article).filter(Article._Article__date == target_date).all()
            return articles

    def search_by_isbn(self, isbn: int):
        if isbn is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return articles matching target_date; return an empty list if there are no matches.
            articles = self._session_cm.session.query(Article).filter(Article._Article__date == target_date).all()
            return articles

    def search_by_author(self, author_name: str):
        if author_name is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return articles matching target_date; return an empty list if there are no matches.
            articles = self._session_cm.session.query(Article).filter(Article._Article__date == target_date).all()
            return articles

    def search_by_release_year(self, release_year: int):
        if release_year is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return articles matching target_date; return an empty list if there are no matches.
            articles = self._session_cm.session.query(Article).filter(Article._Article__date == target_date).all()
            return articles

    def search_by_publisher(self, publisher: int):
        if publisher is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return articles matching target_date; return an empty list if there are no matches.
            articles = self._session_cm.session.query(Article).filter(Article._Article__date == target_date).all()
            return articles

    def get_page(self):
        return

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_review(self):
        reviews = self._session_cm.session.query(Review).all()
        return reviews

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
        books = self._session_cm.session.query(Book).all()
        return books
