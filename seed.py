from models import User, db, Post, Tag, PostTag
from app import app

db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

ross = User(
    first_name="Ross",
    last_name="Cummings",
    image_url="https://people.com/thmb/QYvd4bDjMXZbm6XacFf73RxEW4E=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():focal(729x88:731x90):format(webp)/10-Year-Old-Boy-Starts-Petition-to-Change-Nerd-Glasses-Emoji-112923-bec304032f7a45e2aa4957e003755126.jpg",
)

john = User(
    first_name="Michael",
    last_name="Jordan",
    image_url="https://cdn.nba.com/headshots/nba/latest/1040x760/893.png",
)
jeannine = User(first_name="Jeannine", last_name="Vestuto")

db.session.add(ross)
db.session.add(john)
db.session.add(jeannine)
db.session.commit()

post1 = Post(
    title="flask is fantastic",
    content="flask is my favorite thing to learn",
    user_id=1,
)

post2 = Post(
    title="I love basketball",
    content="I am one of the greatest to play",
    user_id=2,
)

post3 = Post(
    title="I hate flask",
    content="Writing flask code is horrible, I miss Javascript",
    user_id=3,
)


db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.commit()

tag1 = Tag(name="Funny")
tag2 = Tag(name="Great")
tag3 = Tag(name="True")
tag4 = Tag(name="Amazing")

db.session.add_all([tag1, tag2, tag3, tag4])
db.session.commit()


p1t2 = PostTag(
    post_id=1,
    tag_id=2,
)

p2t3 = PostTag(
    post_id=2,
    tag_id=3,
)

p2t4 = PostTag(
    post_id=2,
    tag_id=4,
)

p3t1 = PostTag(
    post_id=3,
    tag_id=1,
)

db.session.add(p1t2)
db.session.add(p2t3)
db.session.add(p2t4)
db.session.add(p3t1)
db.session.commit()
