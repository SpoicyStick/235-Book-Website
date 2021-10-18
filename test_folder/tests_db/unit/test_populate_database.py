from sqlalchemy import select, inspect

from library.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors',
                                           'authorships',
                                           'books',
                                           'publishers',
                                           'reviews',
                                           'similar_books',
                                           'users']

def test_database_populate_select_all_authors(database_engine):

    inspector = inspect(database_engine)
    name_of_author_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_author_table]])
        result = connection.execute(select_statement)

        all_author_names = []
        for row in result:
            all_author_names.append(row['name'])
        assert len(all_author_names)==55

def test_database_populate_select_all_users(database_engine):
    inspector = inspect(database_engine)
    name_of_user_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_user_table]])
        result = connection.execute(select_statement)

        all_user_names = []
        for row in result:
            all_user_names.append(row['user_name'])
        assert len(all_user_names)==3

def test_database_populate_select_all_reviews(database_engine):
    inspector = inspect(database_engine)
    name_of_review_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_review_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append(row['id'])
        assert len(all_reviews) == 1


def test_database_populate_select_all_authorships(database_engine):
    inspector = inspect(database_engine)
    authorship_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[authorship_table]])
        result = connection.execute(select_statement)

        all_authorship = []
        for row in result:
            all_authorship.append(row['id'])
        assert len(all_authorship) == 59

def test_database_populate_select_all_publishers(database_engine):
    inspector = inspect(database_engine)
    publisher_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[publisher_table]])
        result = connection.execute(select_statement)

        all_publishers = []
        for row in result:
            all_publishers.append(row['id'])
        assert len(all_publishers) == 16

def test_database_populate_select_all_books(database_engine):
    inspector = inspect(database_engine)
    books_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[books_table]])
        result = connection.execute(select_statement)

        all_books = []
        for row in result:
            all_books.append(row['id'])
        assert len(all_books) == 16

def test_database_populate_select_all_similar_books(database_engine):
    inspector = inspect(database_engine)
    similar_books_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[similar_books_table]])
        result = connection.execute(select_statement)

        all_similar_books = []
        for row in result:
            all_similar_books.append(row['book_id'])
        assert len(all_similar_books) == 24