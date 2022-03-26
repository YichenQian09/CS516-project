from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.auth import Auth
from .models.users import Users


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Auth.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    school = StringField('School', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if Auth.email_exists(email.data):
            raise ValidationError('Already a user with this email.')

class UpdateForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    #oldemail = StringField('OldEmail', validators=[DataRequired(), Email()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    oldpassword = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    submit = SubmitField('Update')

class UpdateNicknameForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired()])
    submit = SubmitField('Update')

    # def validate_email(self, email):
    #     if Auth.email_exists(email.data):
    #         raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if Auth.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.school.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@bp.route('/update', methods=['GET', 'POST'])
def update():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = UpdateForm()
    if form.validate_on_submit():
        #if old email or old password is not right, the user cannot change information
        user = Auth.get_by_auth(current_user.get_email(), form.oldpassword.data)
        if user is None:
            flash('Invalid password')
            return redirect(url_for('users.update'))
        if (Auth.update(user,form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.school.data)):
            flash('Congratulations, you updated your information!')
            return redirect(url_for('users.update'))
    return render_template('update.html', title='update', form=form, user=current_user)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    user_profile=Users.get_profile(current_user.uid)
    if user_profile is None:
        flash('Something wrong with your account, please login again!')
        return redirect(url_for('users.login'))
    return render_template('profile.html', title='profile',profile=user_profile)

@bp.route('/update_nickname/<old_name>', methods=['GET', 'POST'])
def update_nickname(old_name):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = UpdateNicknameForm()
    if form.validate_on_submit():
        if Users.update_nickname(current_user.uid,form.nickname.data):
            flash('You updated your nickname!')
            return redirect(url_for('users.profile'))
    return render_template('updatenickname.html', title='updateNickname',form=form, old_name=old_name)
