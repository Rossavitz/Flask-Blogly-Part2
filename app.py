"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.app_context().push()

connect_db(app)


@app.route("/")
def home_page():
    return redirect("/users")


@app.route("/users")
def list_users():
    """shows users page"""
    users = User.query.all()
    return render_template("list.html", users=users)


@app.route("/users/new", methods=["GET"])
def show_form():
    """shows add user form"""

    return render_template("addUser.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    first_name = request.form["first"]
    last_name = request.form["last"]
    image_url = request.form["image"]

    new_user = User(
        first_name=first_name, last_name=last_name, image_url=image_url or None
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect("/")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["GET"])
def show_edit_form(user_id):
    """shows edit user form"""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first"]
    user.last_name = request.form["last"]
    user.image_url = request.form["image"]

    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")


@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def show_post_form(user_id):
    """Show post form"""
    user = User.query.get_or_404(user_id)
    return render_template("addPost.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Handle submission of new post"""
    user = User.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user=user)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """show a single post"""
    post = Post.query.get_or_404(post_id)
    return render_template("postDetails.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """show edit post form"""
    post = Post.query.get_or_404(post_id)
    return render_template("editPost.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """handle edit post submission"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """handle delete of post"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")
