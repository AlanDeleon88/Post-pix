from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

follows = db.Table('follows',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id')),
    db.UniqueConstraint('follower_id', 'followed_id')
)

# if environment == "production":
#     follows.schema = SCHEMA

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    # if environment == "production":
    #     __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255),
    default='https://t3.ftcdn.net/jpg/00/64/67/52/240_F_64675209_7ve2XQANuzuHjMZXP3aIYIpsDKEbF5dD.jpg')
    #added first/lastname ----------------------------------------
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    posts = db.relationship('Post', back_populates='users', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='users', cascade='all, delete-orphan')

    # follows = db.relationship('User', secondary='follows', primaryjoin="follows.c.user_id==users.c.id",
    #                             secondaryjoin="follows.c.following_id==users.c.id", backref=db.backref('follows', lazy='dynamic'),
    #                             cascade='all, delete-orphan', single_parent=True)
    followers = db.relationship(
        'User', secondary=follows,
        primaryjoin=(follows.c.followed_id == id),
        secondaryjoin=(follows.c.follower_id == id),
        backref=db.backref('follows', lazy='dynamic'), lazy='dynamic')

    post_likes = db.relationship('PostLike', back_populates='users', cascade='all, delete-orphan')

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            #added firstname and lastname -------------------------
            'firstName': self.first_name,
            'lastName': self.last_name,
            'followers': [{'userId': follower.id, 'username': follower.username, 'profilePicture': follower.profile_picture} for follower in self.followers],
            'following': [{'userId': follower.id, 'username': follower.username, 'profilePicture': follower.profile_picture} for follower in self.follows],
            'likes' : [{'postId': like.post_id} for like in self.post_likes],
            'profilePicture': self.profile_picture,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }
    # def un_follow(self, id):
    #     for i in range(len(self.follows)):
    #         user = self.follows[i]
    #         if(user.id == id):
    #             return
