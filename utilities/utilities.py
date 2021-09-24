from flask import Blueprint, request, render_template, redirect, url_for, session

import library.adapters.repository as repo
import utilities.services as services

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)

