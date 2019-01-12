from datetime import datetime
from time import mktime
from typing import List

import feedparser
from attr import attrib, attrs

from app import db
from app.models import feedeater_models as models


@attrs
class Article:
    id: str = attrib(default=None)
    title: str = attrib(default=None)
    published: str = attrib(default=None)
    summary: str = attrib(default=None)
    link: str = attrib(default=None)


@attrs
class FeedResult:
    title: str = attrib(default=None)
    etag: str = attrib(default=None)
    updated: str = attrib(default=None)
    articles: List[Article] = attrib(default=None)
    status: str = attrib(default=None)
    exception: str = attrib(default=None)

    def __attrs_post_init__(self):
        self.articles = []


@attrs
class Log:
    articles: int = attrib(default=0)
    new_articles: int = attrib(default=0)
    exception: str = attrib(default=None)

    def to_dict(self):
        return self.__dict__


class FeedEater:

    def fetch(self, feed_id: int) -> models.Feed:
        db_sess = db.session
        feed = models.Feed.query.get(feed_id)
        feed_url = feed.url

        print(f'Fetching feed: {feed_url}')
        result = self._process(feed_url, feed.etag)
        # print('====================== Results ======================')
        # print(result)

        feed_result = models.FeedResult()
        feed_result.feed = feed
        feed_result.status_code = result.status
        feed_result.completed_date = datetime.utcnow()
        db_sess.add(feed_result)

        if result.status == "302":
            # Feed has not changed (via etag value)
            db_sess.commit()
            return feed

        feed.etag = result.etag
        if result.updated:
            feed.updated = datetime.fromtimestamp(mktime(result.updated))
        feed.fetched = datetime.utcnow()

        created_count = 0
        for article in result.articles:
            newarticle, created = self._get_or_create(
                db_sess,
                models.Article,
                article_id=article.id,
                feed_id=feed.id)
            if not newarticle.published:
                newarticle.published = datetime.utcnow()
            if not newarticle.fetched:
                newarticle.fetched = datetime.utcnow()
            newarticle.title = article.title
            newarticle.article_id = article.id
            newarticle.summary = article.summary
            newarticle.link = article.link
            newarticle.fetched = datetime.utcnow()
            if article.published:
                newarticle.published = datetime.fromtimestamp(mktime(article.published))
            if created:
                created_count += 1
                newarticle.feed = feed
            db_sess.add(newarticle)

        log = Log(articles=len(result.articles), new_articles=created_count)
        if result.exception:
            feed_result.had_exception = True
            log.exception = str(result.exception)
            feed.status = models.Feed.INACTIVE  # Inactive
        feed_result.log = log.to_dict()

        db_sess.commit()

        return feed

    def _get_or_create(self, session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            instance = model(**kwargs)
            session.add(instance)
            return instance, True

    def _process(self, feedUrl: str, etag: str) -> FeedResult:
        feed = feedparser.parse(feedUrl, etag=etag)
        print('Feed fetched, parsing now...')

        result = FeedResult()
        if feed.get('status'):
            result.status = feed.status
        if feed.get('bozo') and feed.get('bozo') == 1 and not feed.get('entries'):
            result.exception = feed.get('bozo_exception')
            print(f"Feed {feedUrl} returned an exception {feed.get('bozo_exception')}")
            return result
        if (feed.status and feed.status == 302) and feed.get('etag'):
            # print(feed)
            print('** Feed has not changed and returned 302.')
            result.status = "302"
            return result

        result.title = feed['feed'].get('title')
        result.etag = feed.get('etag')
        result.updated = feed.get('updated_parsed')

        articles = []
        for item in feed['entries']:
            if item.get('id'):
                article = Article()
                article.id = item.get('id')
                article.title = item.get('title')
                article.published = item.get('published_parsed')
                article.summary = item.get('summary')
                article.link = item.get('link')
                articles.append(article)

        result.articles = articles

        return result
