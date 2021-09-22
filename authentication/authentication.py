from flask import Blueprint, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from functools import wraps
import authentication.services as services
import library.adapters.repository as repo
"""import covid.utilities.utilities as utilities"""


# Configure Blueprint.
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    formAuthentication = RegistrationForm()
    form = BookSearch()
    user_name_not_unique = None
    if (session.get('logged_in') == True):
        user_name = (session.get('user_name'))
    else:
        user_name = None
    if formAuthentication.validate_on_submit():
        # Successful POST, i.e. the user name and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        try:
            services.add_user(formAuthentication.user_name.data, formAuthentication.password.data, repo.repo_instance)

            # All is well, redirect the user to the login page.
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            user_name_not_unique = 'Your user name is already taken - please supply another'

    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'authentication/credentials.html',
        title='Register',
        formAuthentication=formAuthentication,
        form = form,
        user_name=user_name,
        user_name_error_message=user_name_not_unique,
        handler_url=url_for('authentication_bp.register')
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    formAuthentication = LoginForm()
    form = BookSearch()
    if (session.get('logged_in') == True):
        user_name = (session.get('user_name'))
    else:
        user_name = None
    user_name_not_recognised = None
    password_does_not_match_user_name = None

    if formAuthentication.validate_on_submit():
        # Successful POST, i.e. the user name and password have passed validation checking.
        # Use the service layer to lookup the user.
        try:
            user = services.get_user(formAuthentication.user_name.data, repo.repo_instance)

            # Authenticate user.
            services.authenticate_user(user['user_name'], formAuthentication.password.data, repo.repo_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['user_name'] = user['user_name']
            session['logged_in'] = True
            return redirect(url_for('home_bp.home'))

        except services.UnknownUserException:
            # User name not known to the system, set a suitable error message.
            user_name_not_recognised = 'User name not recognised - please supply another'

        except services.AuthenticationException:
            # Authentication failed, set a suitable error message.
            password_does_not_match_user_name = 'Password does not match supplied user name - please check and try again'

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'authentication/credentials.html',
        title='Login',
        form = form,
        user_name=user_name,
        user_name_error_message=user_name_not_recognised,
        password_error_message=password_does_not_match_user_name,
        formAuthentication=formAuthentication
    )


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    session['logged_in']=False
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)

class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Your user name is required'),
        Length(min=3, message='Your user name is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Login')

class BookSearch(FlaskForm):
    search_by = SelectField('Search by', choices=[("TITLE", "Title"), ("ISBN", "ISBN"), ("AUTHOR", "Author"),
                                                  ("RELEASE", "Release year"), ("PUBLISHER", "Publisher")],
                            default=("TITLE", "Title"))
    search_value = StringField('Search value', [DataRequired()],
                               render_kw={"placeholder": "\U0001F50E\uFE0E" + "Search.."})
    submit = SubmitField('Find')
