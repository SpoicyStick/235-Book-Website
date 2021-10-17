from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime, Boolean, Text, CheckConstraint,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from library.domain import model

metadata = MetaData()

books_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True),
    Column('isbn', Integer, unique=True),
    Column('title', Text),
    Column('description', Text),
    Column('release_year', Integer),
    Column('ebook', Boolean),
    Column('num_pages', Integer),
    Column('image', Text, nullable=False),
    Column('rating', Integer),
    Column('publisher_id', ForeignKey('publishers.id'))
)

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)


reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.id')),
    Column('description', Text, nullable=False),
    Column('rating', Integer, nullable=False)
)

authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Text, nullable=False)
)

authorships_table = Table(
    'authorships', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.id')),
    Column('author_id', ForeignKey('authors.id'))
)

publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Text,  nullable=False, unique=True)
)

similar_books_table = Table(
    'similar_books', metadata,
    Column('book_id', ForeignKey('books.id')),
    Column('similar_book_id', ForeignKey('books.id')),
)

def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(model.Review, backref='_Review__user')
    })

    mapper(model.Review, reviews_table, properties={
        '_Review__review_text': reviews_table.c.description,
        '_Review__rating': reviews_table.c.rating
    })

    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__name': publishers_table.c.name,
        '_Publisher__books_published': relationship(model.Book, backref='_Book__publisher')
    })

    mapper(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.id,
        '_Book__isbn': books_table.c.isbn,
        '_Book__title': books_table.c.title,
        '_Book__description': books_table.c.description,
        '_Book__release_year': books_table.c.release_year,
        '_Book__ebook': books_table.c.ebook,
        '_Book__num_pages': books_table.c.num_pages,
        '_Book__image': books_table.c.image,
        '_Book__average_rating': books_table.c.rating,
        '_Book__reviews': relationship(model.Review, backref='_Review__book'),
        '_Book__authors': relationship(model.Author, secondary=authorships_table, back_populates='_Author__authorship')
    })

    mapper(model.Author, authors_table, properties={
        '_Author__unique_id': authors_table.c.id,
        '_Author__full_name': authors_table.c.name,
        '_Author__authorship': relationship(model.Book, secondary=authorships_table, back_populates='_Book__authors')
    })