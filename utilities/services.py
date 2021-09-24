from flask import Blueprint, request, render_template, redirect, url_for, session

import library.adapters.repository as repo
import utilities.services as services

from library.adapters.repository import AbstractRepository
from random import randrange


def get_random_book(repo: AbstractRepository):
    books = repo.get_all_books()
    book_count = len(books)
    random_ids = (randrange(book_count))

    book = books[random_ids]

    return book