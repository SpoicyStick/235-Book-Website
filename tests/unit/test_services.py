from datetime import date, datetime
from typing import List

import pytest

from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory, make_review
from authentication import services as auth_services
from books.services import NonExistentBookException
from books import services as books_services
from authentication.services import AuthenticationException

def test_can_add_user(in_memory_repo):
    new_user_name = 'jz'
    new_password = 'abcd1A23'
    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False

def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd123'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)



def test_can_add_review(in_memory_repo):
    review_text = 'The loonies are stripping the supermarkets bare!'
    user_name = 'fmercury'

    books_services.add_review(30128855, review_text, user_name, 5, in_memory_repo)
    assert len(in_memory_repo.get_book(30128855).reviews)==1

def test_cannot_add_review_for_non_existent_book(in_memory_repo):
    review_text = 'The loonies are stripping the supermarkets bare!'
    user_name = 'fmercury'

    with pytest.raises(books_services.NonExistentBookException):
        books_services.add_review(1, review_text, user_name, 5, in_memory_repo)

def test_cannot_add_review_by_unknown_user(in_memory_repo):
    review_text = 'The loonies are stripping the supermarkets bare!'
    user_name = 'grace'
    with pytest.raises(books_services.UnknownUserException):
        books_services.add_review(30128855, review_text, user_name, 5, in_memory_repo)

def test_can_get_book(in_memory_repo):
    book = books_services.get_book(25742454, in_memory_repo)
    assert book == Book(25742454, "Title")

def test_return_none_for_book_with_non_existent_id(in_memory_repo):
    book = books_services.get_book(1, in_memory_repo)
    assert book == None