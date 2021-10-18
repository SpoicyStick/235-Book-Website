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
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id==target_book_id).one()
        except:
            pass
        return book

    def get_user(self, user_name) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
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
            pass
        return publisher

    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.add(publisher)
            scm.commit()


    def search_by_title(self, title: str):
        books=[]
        if title is None:
            return books
        else:
            books = self._session_cm.session.query(Book).filter(Book._Book__title == title).all()
            return books

    def search_by_isbn(self, isbn: int):
        books=[]
        if isbn is None:
            return books
        else:
            books = self._session_cm.session.query(Book).filter(Book._Book__isbn == isbn).all()
            return books

    def search_by_author(self, author_name: str):
        books=[]
        if author_name is None:
            return books
        else:
            try:
                author = self._session_cm.session.query(Author).filter(Author._Author__full_name == author_name).one()
                author = author.unique_id
                authorship = self._session_cm.session.execute('SELECT book_id FROM authorships WHERE author_id = :author', {'author': author}).fetchall()
                for book_id in authorship:
                    book =self.get_book(book_id[0])
                    if book != None:
                        books.append(book)
            except:
                pass
            return books

    def search_by_release_year(self, release_year: int):
        books=[]
        if release_year is None:
            return books
        else:
            books = self._session_cm.session.query(Book).filter(Book._Book__release_year == release_year).all()
            return books

    def search_by_publisher(self, publisher_name: str):
        books=[]
        if publisher_name is None:
            return books
        else:
            books = self._session_cm.session.query(Book).filter(Book.publisher_name == publisher_name).all()
            return books

    def get_page(self):
        key = 0
        pages = {}

        books = self._session_cm.session.query(Book).all()
        for num in books:
            if books.index(num) % 8 == 0:
                key += 1
                pages[str(key)] = []
                pages[str(key)].append(num)
            else:
                pages[str(key)].append(num)
        return pages

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_review(self):
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def sort_books_by_title(self):
        books = self._session_cm.session.query(Book).order_by(Book._Book__title).all()
        return books

    def sort_books_by_isbn(self):
        books = self._session_cm.session.query(Book).order_by(Book._Book__isbn).all()
        return books

    def sort_books_by_release_year(self):
        books = self._session_cm.session.query(Book).order_by(Book._Book__release_year).all()
        return books

    def sort_books_by_publisher(self):
        books = (self._session_cm.session.query(Book).order_by(Book.publisher_name).all())
        return books

    def get_similar_books(self, book: Book):
        sim_books = []
        for sim_book in book.similar_book:
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id == sim_book.book_id).one()
            if book!=None:
                sim_books.append(book)

        return sim_books

    def get_all_books(self):
        books = self._session_cm.session.query(Book).all()
        return books
