"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag

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
    tags = Tag.query.all()
    return render_template("addPost.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Handle submission of new post"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user=user, tags=tags)
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
    tags = Tag.query.all()
    return render_template("editPost.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """handle edit post submission"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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


@app.route("/tags")
def list_tags():
    """show list of tags"""
    tags = Tag.query.all()
    return render_template("listTags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """show detail about a tag"""
    tag = Tag.query.get_or_404(tag_id)

    return render_template("tagDetails.html", tag=tag)


@app.route("/tags/new")
def new_tag_form():
    """shows form to add new tag"""

    posts = Post.query.all()
    return render_template("newTag.html", posts=posts)


@app.route("/tags/new", methods=["POST"])
def add_tag():
    """handle new tag form"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form["name"], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def show_tag_edit_form(tag_id):
    """show tag edit form"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template("editTag.html", tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """handle tag edit form"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """delete a tag"""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
