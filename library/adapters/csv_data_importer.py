import csv
from pathlib import Path
from werkzeug.security import generate_password_hash
from library.adapters.repository import AbstractRepository
from library.domain.model import Book, User, make_review
from library.adapters.jsondatareader import BooksJSONReader
from datetime import date, datetime


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


def load_users(data_path: Path, repo: AbstractRepository):
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


def load_books(data_path: Path, repo: AbstractRepository):
    books_filename = str(data_path / "comic_books_excerpt.json")
    author_filename = str(data_path / "book_authors_excerpt.json")

    data = BooksJSONReader(books_filename, author_filename)
    data.read_json_files()

    for book in data.dataset_of_books:
        repo.add_book(book)


def load_reviews(data_path: Path, repo: AbstractRepository, users):
    comments_filename = str(Path(data_path)/"reviews.csv")
    for data_row in read_csv_file(comments_filename):
        review = make_review(
            review_text=data_row[3],
            user=users[data_row[1]],
            book= repo.get_book(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4])
        )
        repo.add_review(review)