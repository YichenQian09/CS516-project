from webbrowser import get
from flask import  Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.auth import Auth
from .models.users import Users
from .models.comment import Comment
from .models.paper import Paper, Abstract
from .models.browses import Browses
from .models.citationcart import CitationCart
from .models.collections import Collections
from .models.citations import Citations

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
import json 

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
    nickname = StringField('Nickname', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if Auth.email_exists(email.data):
            raise ValidationError('Already a user with this email.')
    def validate_nickname(self, nickname):
        if Users.nickname_exists(nickname.data):
            raise ValidationError('Already a user with this nickname.')

class UpdateForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    #oldemail = StringField('OldEmail', validators=[DataRequired(), Email()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    oldpassword = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if Auth.email_exists(email.data,current_user.uid):
            raise ValidationError('Already a user with this email.')
    def validate_nickname(self, nickname):
        if Users.nickname_exists(nickname.data,current_user.uid):
            raise ValidationError('Already a user with this nickname.')

class UpdateNicknameForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired()])
    submit = SubmitField('Update')

    # def validate_email(self, email):
    #     if Auth.email_exists(email.data):
    #         raise ValidationError('Already a user with this email.')


def get_word_by_freq(uid):
    collected =Collections.get_collected_by_uid(uid)
    citationCart = CitationCart.get_all_citations_of_a_citation_cart(uid)
    citationHistory = Citations.get_citations(uid)
    browsed = Browses.get_papers(uid,"all")

    words =""
    for paper in collected:
        t = paper.title
        a = Abstract.get_by_pid(paper.pid)
        words = words +" "+t
        words = words +" "+t
        if a is not None:
            words = words +" "+a.abstract
            words = words +" "+a.abstract
    for paper in citationCart:
        t = paper.title
        a = Abstract.get_by_pid(paper.pid)
        words = words +" "+t
        words = words +" "+t
        if a is not None:
            words = words +" "+a.abstract
            words = words +" "+a.abstract

    for paper in citationHistory:
        t = paper.title
        a = Abstract.get_by_pid(paper.pid)
        words = words +" "+t
        words = words +" "+t
        if a is not None:
            words = words +" "+a.abstract
            words = words +" "+a.abstract

    for paper in browsed:
        t = paper.title
        a = Abstract.get_by_pid(paper.pid)
        words = words +" "+t
        if a is not None:
            words = words +" "+a.abstract
    words = [words]
    new_stop_words = ["using", "used", "use", "iii", "given", "requires",
                "require", "required"]

    stop_words = text.ENGLISH_STOP_WORDS.union(new_stop_words)

    # Instantiate a count vectorizer
    vectorizer = CountVectorizer(stop_words=stop_words)
    X = vectorizer.fit_transform(words)
    term = vectorizer.get_feature_names()
    freq = (X.toarray()[0]).tolist()
    sorted_term = [x for _,x in sorted(zip(freq,term),reverse=True)]
    sorted_freq = [y for y,_ in sorted(zip(freq,term),reverse=True)]

    first_term = sorted_term[0:20]
    first_freq = sorted_freq[0:20]
    return first_term, first_freq

@bp.route('/word_cloud', methods=['GET'])
def word_cloud():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    try:
        first_term, first_freq = get_word_by_freq(current_user.uid)
        # modifed based on https://github.com/prateekkrjain/newsapi_word_cloud/blob/master/news_word_cloud.py
        words_json = [{'text': word, 'weight': count} for word, count in zip(first_term,first_freq)]

        return json.dumps(words_json)
    except Exception as e:
        return '[]'

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    interests=['Artificial Intelligence (AI)'
                    ,'Computer Architecture & Engineering (ARC)'
                    ,'Biosystems & Computational Biology (BIO)'
                    ,'Cyber-Physical Systems and Design Automation (CPSDA)'
                    ,'Database Management Systems (DBMS)'
                    ,'Education (EDUC)'
                    ,'Graphics (GR)'
                    ,'Human-Computer Interaction (HCI)'
                    ,'Operating Systems & Networking (OSNT)'
                    ,'Programming Systems (PS)'
                    ,'Scientific Computing (SCI)'
                    ,'Security (SEC)'
                    ,'Theory (THY)']
    form = RegistrationForm()
    if form.validate_on_submit():
        newUser=Auth.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.school.data)
        
        chosenInterests=request.form.getlist("reInterest")                       
        if newUser:
            flash('Congratulations, you are now a registered user!')
            #set basic information for new user
            Users.set_basic_info(newUser.get_id(),form.nickname.data,chosenInterests)  
            # create a default collection 'Liked' for new user
            Collections.create_default_collection(newUser.get_id())
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form, interests=interests)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@bp.route('/update', methods=['GET', 'POST'])
def update():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    user_info=Users.get_info(current_user.uid)
    interests=['Artificial Intelligence (AI)'
                    ,'Computer Architecture & Engineering (ARC)'
                    ,'Biosystems & Computational Biology (BIO)'
                    ,'Cyber-Physical Systems and Design Automation (CPSDA)'
                    ,'Database Management Systems (DBMS)'
                    ,'Education (EDUC)'
                    ,'Graphics (GR)'
                    ,'Human-Computer Interaction (HCI)'
                    ,'Operating Systems & Networking (OSNT)'
                    ,'Programming Systems (PS)'
                    ,'Scientific Computing (SCI)'
                    ,'Security (SEC)'
                    ,'Theory (THY)']
    form = UpdateForm()
    if form.validate_on_submit():
        #if old password is not right, the user cannot change information
        user = Auth.get_by_auth(current_user.get_email(), form.oldpassword.data)
        if user is None:
            flash('Invalid password')
            return redirect(url_for('users.update'))
        chosenInterests=request.form.getlist("reInterest")
        authUpdate=Auth.update(user,form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.school.data)
        userUpdate=Users.update_info(current_user.uid,form.nickname.data,chosenInterests)
        if authUpdate and userUpdate:
            flash('Congratulations, you updated your information!')
            return redirect(url_for('users.profile'))
    return render_template('update.html', title='update', form=form, user=current_user,user_info=user_info,interests=interests)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    user_profile=Users.get_profile(current_user.uid)
    email=current_user.email
    if user_profile is None:
        flash('Something wrong with your account, please login again!')
        return redirect(url_for('users.login'))
    first_term, first_freq = get_word_by_freq(current_user.uid)
    k1 = first_term[0]
    k2 = first_term[1]
    k3 = first_term[2]
    recommended_pid = Comment.recommend_by_keyword(k1,k2,k3)
    recommended_paper = []
    for pid in recommended_pid:
        recommended_paper.append(Paper.get_by_pid(pid)[0])
    return render_template('profile.html', title='profile',profile=user_profile, email=email,recommended_paper=recommended_paper)

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

@bp.route('/view_comment/<int:pagenum>',methods=('GET','POST'))
def view_comment(pagenum):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    if request.method == 'POST':
        pagenum = int(request.form['pagenum'])
        if not pagenum:
            pagenum = 0

    comments, total_num = Comment.fetch_comment_by_uid(current_user.uid,pagenum)
    if ((total_num/10)-int(total_num/10))<0.0000001:
        total_page= int(total_num/10)-1
    else: total_page = int(total_num/10)
    return render_template('view_comment.html',comments = comments,pagenum=pagenum, total_num = total_page)

@bp.route('/edit_comment/<pid>',methods=('GET','POST'))
def edit_comment(pid):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    comment = Comment.fetch_comment_by_pid_uid(current_user.uid,pid)
    return render_template('edit_comment.html',comment = comment)

@bp.route('/update_comment/<pid>',methods=('GET','POST'))
def update_comment(pid):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    comment_sum = request.form.get("comment_summary")
    comment = request.form.get("comment")
    star = int(request.form.get("star"))
    Comment.edit_comment_by_pid_uid(pid,current_user.uid,star,comment_sum,comment)
    return redirect(url_for('users.view_comment',pagenum=0))


@bp.route('/delete_comment/<pid>',methods=('GET','POST'))
def delete_comment(pid):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    Comment.delete_comment_by_pid_uid(pid,current_user.uid)
    return redirect(url_for('users.view_comment', pagenum= 0))






    