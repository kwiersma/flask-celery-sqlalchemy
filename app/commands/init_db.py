# This file defines command line commands for manage.py

import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.feedeater_models import Feed
from app.models.user_models import User, Role


class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()
        print('Database has been initialized.')


def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()
    create_feeds()


def create_feeds():
    feed = Feed(
        title='Real Python', status=1, url='https://realpython.com/atom.xml', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed)
    feed2 = Feed(
        title='Planet Python', status=1, url='http://planetpython.org/rss20.xml', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed2)
    feed3 = Feed(
        title="Simon Willison's Weblog", url='https://simonwillison.net/atom/everything/', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow()
    )
    db.session.add(feed3)
    feed4 = Feed(
        title="Django community", url='https://www.djangoproject.com/rss/community/blogs/', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed4)
    feed5 = Feed(
        title="PyCharm Blog", url='http://feeds.feedburner.com/Pycharm', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed5)
    feed6 = Feed(
        title="The Django weblog",	url='https://www.djangoproject.com/rss/weblog/', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed6)
    feed7 = Feed(
        title="SQLAlchemy", url='https://www.sqlalchemy.org/blog/feed/atom/index.xml', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed7)
    feed8 = Feed(
        title="Blog — Pallets Project", url='http://www.palletsprojects.com/blog/feed.xml', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed8)

    db.session.commit()


def create_users():
    """ Create users """

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')

    # Add users
    user = find_or_create_user(u'Admin', u'Example', u'admin@example.com', 'Password1', admin_role)
    user = find_or_create_user(u'Member', u'Example', u'member@example.com', 'Password1')

    # Save to DB
    db.session.commit()


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(first_name, last_name, email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=current_app.user_manager.password_manager.hash_password(password),
                    active=True,
                    email_confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user



