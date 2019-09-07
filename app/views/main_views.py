import datetime

from flask import Blueprint, redirect, render_template, flash, jsonify
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db, tasks
from app.models.feedeater_models import Feed
from app.models.user_models import UserProfileForm

main_blueprint = Blueprint('main', __name__, template_folder='templates')


# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    return render_template('main/home_page.html')


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('main/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('main/admin_page.html')


@main_blueprint.route('/main/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html',
                           form=form)


@main_blueprint.route('/task')
def task():
    feeds = Feed.query.filter_by(status=1)

    for feed in feeds:
        tasks.fetch_articles.delay(feed.id)

    flash('Fetch articles task kicked off')
    return render_template('main/home_page.html')


@main_blueprint.route('/new-task', methods=['GET', 'POST'])
def new_task():
    title = request.args.get('title')
    url = request.args.get('url')

    feed = Feed(
        title=title, status=1, url=url, type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed)

    db.session.commit()

    tasks.fetch_articles.delay(feed.id)

    return jsonify({'message': 'Feed created.', 'feed_id': feed.id})
