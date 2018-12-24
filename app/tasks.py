from app import celeryapp
from app.services import FeedEater

celery = celeryapp.celery


@celery.task()
def fetch_articles(feed_id: int):
    feedeater = FeedEater()
    feedeater.fetch(feed_id)
