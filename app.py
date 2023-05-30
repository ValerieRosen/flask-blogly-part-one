"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

#Homepage redirect to users
@app.route('/')
def root():
    """Shows list of users"""
    return redirect("/users")

#User routes
@app.route('/users')
def users_index():
    """Shows page with info on all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

#Create new user form
@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Show form to create new user"""
    return render_template('users/new.html')

#Submitting new user
@app.route('/users/new', methods=["POST"])
def users_new():
    """Submitting form to create new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')
    
#Individual user page
@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show individual user page"""
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

#Edit user info
@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show form to edit user info"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

#Submitting form to update user info
@app.route('/users/<int:user_id>/edit', methods=['POST'])
def users_update(user_id):
    """Submitting form to update user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

#Deleting a user
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Form deleting a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')





