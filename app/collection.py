from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired

#from .models.auth import Auth
from .models.collections import Collections
#from .models.paper import Paper
from flask import Blueprint

bp = Blueprint('collection', __name__)

class CollectionNameForm(FlaskForm):
    collection_name = StringField('Collection Name', validators=[DataRequired()])
    submit = SubmitField('Create')
    def validate_collection_name(self, collection_name):
        if Collections.check_same_collection_name(collection_name.data):
            raise ValidationError('This collection already exists')

class RenameCollectionForm(FlaskForm):
    collection_name = StringField('Collection Name', validators=[DataRequired()])
    submit = SubmitField('Rename')


@bp.route('/collections', methods=['GET', 'POST'])
def collections():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    # the function returns a list of tuples
    # (collection_name, numbers of papers)
    collection_list=Collections.get_each_collection(current_user.uid)
    print("collection_list:",collection_list)
    return render_template('collections.html', title='Collections', collection_list=collection_list)

@bp.route('/add_collection', methods=['GET', 'POST'])
def add_collection():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = CollectionNameForm()
    if form.validate_on_submit():
        if Collections.add_new_collection(current_user.uid,form.collection_name.data):
            flash('Congratulations, you created a new collection!')
            return redirect(url_for('collection.collections'))
    return render_template('addcollection.html', title='addCollections', form=form)

@bp.route('/rename_collection/<old_name>', methods=['GET', 'POST'])
def rename_collection(old_name):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = RenameCollectionForm()
    if form.validate_on_submit():
        if Collections.rename_collection(current_user.uid,old_name,form.collection_name.data):
            print(form.collection_name.data)
            return redirect(url_for('collection.get_collection_papers',collection_name=form.collection_name.data))
    return render_template('renamecollection.html', title='renameCollections', form=form,old_name=old_name)

@bp.route('/get_collection_papers/<collection_name>', methods=['GET', 'POST'])
def get_collection_papers(collection_name):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    # the function returns a list of tuples
    # (collection_name, numbers of papers)
    paper_list=Collections.get_papers(current_user.uid,collection_name)
    print("paper_list:",paper_list)
    return render_template('collectedpaper.html', title='Collectedpaper', paper_list=paper_list,collection_name=collection_name)

@bp.route('/delete_collection/<collection_name>', methods=['GET', 'POST'])
def delete_collection(collection_name):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    if Collections.delete_collection(current_user.uid,collection_name):
        flash("You deleted a collection!")
    return redirect(url_for('collection.collections'))
    
    