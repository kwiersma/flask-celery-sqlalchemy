from app import db


class Feed(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)

    ACTIVE = 1
    INACTIVE = 2
    DELETED = 0
    STATUSES = (
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted'),
        (INACTIVE, 'Inactive (fetch failed)'),
    )

    status: int = db.Column(db.Integer, nullable=False, default='1', server_default='1')

    url: str = db.Column(db.String(200), nullable=False)
    title: str = db.Column(db.String(100), nullable=False)
    type: str = db.Column(db.String(10), nullable=False)
    htmlUrl: str = db.Column(db.String(200), nullable=True)

    etag: str = db.Column(db.String(200), nullable=True)
    updated: str = db.Column(db.DateTime(), nullable=True)

    created: str = db.Column(db.DateTime(), nullable=False)
    fetched: str = db.Column(db.DateTime(), nullable=True)

    # articles: List[Article] = attrib(default=None)

    # tags: List[str] = attrib(default=None)

    def __str__(self):
        return f'<Feed {self.id} - {self.title} ({self.status})>'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    article_id: str = db.Column(db.String(200), nullable=False)
    title: str = db.Column(db.String(500), nullable=True)
    published: str = db.Column(db.DateTime(), nullable=True)
    summary: str = db.Column(db.Text(), nullable=True)
    link: str = db.Column(db.String(300), nullable=True)
    fetched: str = db.Column(db.DateTime(), nullable=False)

    feed_id = db.Column(db.Integer(), db.ForeignKey('feed.id', ondelete='CASCADE'), nullable=False)
    feed = db.relationship('Feed', backref=db.backref('articles', lazy='dynamic'))


class FeedResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    status_code = db.Column(db.Integer, nullable=True)
    completed_date = db.Column(db.DateTime(), nullable=False)
    log = db.Column(db.JSON, nullable=True)
    had_exception = db.Column(db.Boolean, default=False, nullable=False)

    feed_id = db.Column(db.Integer(), db.ForeignKey('feed.id', ondelete='CASCADE'), nullable=False)
    feed = db.relationship('Feed', backref=db.backref('results', lazy='dynamic'))
