import json
from typing import List

from library.domain.model import Publisher, Author, Book


class BooksJSONReader:

    def __init__(self, books_file_name: str, authors_file_name: str):
        self.__books_file_name = books_file_name
        self.__authors_file_name = authors_file_name
        self.__dataset_of_books = []
        self.__dataset_of_authors = {}
        self.__dataset_of_publishers = {}
        self.__dataset_of_similar_books = {}

    @property
    def dataset_of_books(self) -> List[Book]:
        return self.__dataset_of_books

    @property
    def dataset_of_authors(self) -> dict[Author]:
        return self.__dataset_of_authors

    @property
    def dataset_of_similar_books(self) -> dict[Author]:
        return self.__dataset_of_similar_books

    @property
    def dataset_of_publishers(self) -> dict[Publisher]:
        return self.__dataset_of_publishers

    def read_books_file(self) -> list:
        books_json = []
        with open(self.__books_file_name, encoding='UTF-8') as books_jsonfile:
            for line in books_jsonfile:
                book_entry = json.loads(line)
                books_json.append(book_entry)
        return books_json

    def read_authors_file(self) -> list:
        authors_json = []
        with open(self.__authors_file_name, encoding='UTF-8') as authors_jsonfile:
            for line in authors_jsonfile:
                author_entry = json.loads(line)
                authors_json.append(author_entry)
        return authors_json


    def read_json_files(self):
        authors_json = self.read_authors_file()
        books_json = self.read_books_file()

        for book_json in books_json:
            book_instance = Book(int(book_json['book_id']), book_json['title'])
            publisher = Publisher(book_json['publisher'])
            if publisher not in self.__dataset_of_publishers.keys():
                self.__dataset_of_publishers[publisher] = []
            self.__dataset_of_publishers[publisher].append(book_instance)

            book_instance.image = book_json['image_url']

            try:
                if book_json['isbn'] != "":
                    book_instance.isbn = int(float(book_json['isbn']))
            except:
                pass

            if book_json['publication_year'] != "":
                book_instance.release_year = int(book_json['publication_year'])

            if book_json['average_rating'] != "":
                book_instance.average_rating = float(book_json['average_rating'])

            if book_json['is_ebook'].lower() == 'false':
                book_instance.ebook = False
            else:
                if book_json['is_ebook'].lower() == 'true':
                    book_instance.ebook = True
            book_instance.description = book_json['description']
            if book_json['num_pages'] != "":
                book_instance.num_pages = int(book_json['num_pages'])
            for book_id in (book_json['similar_books']):
                if int(book_id) not in self.__dataset_of_similar_books.keys():
                    self.__dataset_of_similar_books[int(book_id)] = []
                self.__dataset_of_similar_books[int(book_id)].append(book_instance)

            # extract the author ids:
            list_of_authors_ids = book_json['authors']
            for author_id in list_of_authors_ids:

                numerical_id = int(author_id['author_id'])
                # We assume book authors are available in the authors file,
                # otherwise more complex handling is required.
                author_name = None
                for author_json in authors_json:
                    if int(author_json['author_id']) == numerical_id:
                        author_name = author_json['name']
                author = Author(numerical_id, author_name)
                if author not in self.__dataset_of_authors.keys():
                    self.__dataset_of_authors[author] = []
                self.__dataset_of_authors[author].append(book_instance)

            self.__dataset_of_books.append(book_instance)