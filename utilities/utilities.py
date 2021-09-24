from flask import Blueprint, request, render_template, redirect, url_for, session

import library.adapters.repository as repo
import utilities.services as services

from library.adapters.repository import AbstractRepository
from random import randrange



# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_selected_book():
    book = services.get_random_book(repo.repo_instance)
    return book
