import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session




def test_login_required_to_comment(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the comment page.
    response = client.get('/review?book_id=25742454&submit_param=submit_value&book_id=25742454')

    response = client.post(
        '/review',
        data={'review': 'Who needs quarantine?', 'book_id': 25742454, 'rating': 5}
    )
    assert response.headers['Location'] == 'http://localhost/list_book'


@pytest.mark.parametrize(('review', 'messages'), (
        ('Hey', (b'Your comment is too short')),
))
def test_comment_with_invalid_input(client, auth, review, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an article.
    response = client.post(
        '/review',
        data={'review': review, 'book_id': 25742454}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_search_title(client, auth):
    # Login a user.
    auth.login()
    response = client.get('/search_book?search_by=TITLE&search_value=Cruelle&submit=Find&clicked_page_number=1')
    assert b'Cruelle' in response.data

def test_search_isbn(client, auth):
    # Login a user.
    auth.login()

    response = client.get('/search_book?search_by=ISBN&search_value=2205073346+&submit=Find&clicked_page_number=1')

    assert b'Cruelle' in response.data

def test_search_author(client, auth):
    # Login a user.
    auth.login()

    response = client.get('/search_book?search_by=AUTHOR&search_value=Florence Dupre la Tour&submit=Find&clicked_page_number=1')

    assert b'Cruelle' in response.data

def test_search_release_year(client, auth):
    # Login a user.
    auth.login()

    response = client.get('/search_book?search_by=RELEASE&search_value=2016&=Find&clicked_page_number=1')

    assert b'Cruelle' in response.data
    assert b'War Stories, Volume 3' in response.data
    assert b'Crossed, Volume 15' in response.data
    assert b'Crossed + One Hundred, Volume 2 (Crossed +100 #2)' in response.data

def test_search_release_publisher(client, auth):
    # Login a user.
    auth.login()

    response = client.get('/search_book?search_by=PUBLISHER&search_value=Dargaud&=Find&clicked_page_number=1')
    assert b'Cruelle' in response.data

def test_pagnavigation_takes_user_to_correct_page(client, auth):
    response =client.get('/list_book?clicked_page_number=3')
    assert b'She Wolf #1' in response.data
    response =client.get('/list_book?clicked_page_number=4')
    assert b'Doctor Strange: The Oath' in response.data

def test_sort_by_title(client):
    resource = client.get('/list_book_by_title')
    assert b'Cruelle' in resource.data

def test_sort_by_isbn(client):
    resource = client.get('/list_book_by_isbn')
    assert b'Sherlock Holmes: Year One' in resource.data

def test_sort_by_release_year(client):
    resource = client.get('/list_book_by_release_year')
    assert b'Crossed, Volume 15' in resource.data

def test_sort_by_publisher(client):
    resource = client.get('/list_book_by_publisher')
    assert b'Twin Spica, Volume: 03' in resource.data