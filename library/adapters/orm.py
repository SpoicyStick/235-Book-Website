from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from library.domain import model

metadata = MetaData()


users_table = Table(

)

books_table = Table(

)

reviews_table = Table(

)

authors_table = Table(

)

authorship_table = Table(

)

publishers_table = Table(

)

similar_books_table = Table(

)

def map_model_to_tables():
    pass