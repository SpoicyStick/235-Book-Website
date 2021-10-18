
from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import Book, BooksInventory, User, Review, Author

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__books = list()
        self.__users = list()
        self.__pages = dict()
        self.__reviews = list()
        self.__authors = list()

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
            if self.__books.index(num) % 8 == 0:
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

    def add_author(self, author: Author):
        self.__authors.append(author)

    def get_authors(self):
        return self.__authors

    def get_number_of_books(self):
        return len(self.__books)

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
        for book in book.similar_book:
            matching.append(book)
        return matching

    def sort_books_by_title(self):
        self.__books= sorted(self.__books, key=lambda x: x.title.lower())
        return self.__books

    def sort_books_by_isbn(self):
        self.__books=  sorted(self.__books, key=lambda x: -1 if x.isbn is None else x.isbn, reverse = True)
        return self.__books


    def sort_books_by_release_year(self):
        self.__books=  sorted(self.__books, key=lambda x: -1 if x.release_year is None else x.release_year, reverse = True)
        return self.__books

    def sort_books_by_publisher(self):
        self.__books = sorted(self.__books, key=lambda x: x.publisher.name.lower(), reverse = True)
        return self.__books

    def get_all_books(self):
        return self.__books






