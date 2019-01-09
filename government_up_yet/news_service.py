"""
Defines a NewsService class. When startup is called on a NewsService, a
BackgroundScheduler will be created that calls out to NewsAPI every five minutes
and populates the database with what it gathers.
"""
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from database import db_session
from datetime import date, timedelta, datetime
from dateutil import parser
import json
from collections import namedtuple
import models

# I arbritrarily decided upon which sources to use here. Sorry vice :(
# Tried to be politically balanced about it...
SOURCES = [
    'abc-news', 'bbc-news', 'bloomberg', 'breitbart-news', 'cbs-news', 'cnbc',
    'cnn', 'fox-news', 'google-news', 'msnbc', 'nbc-news', 'politico',
    'reuters', 'the-economist', 'the-guardian-uk', 'the-huffington-post',
    'the-new-york-times', 'the-wall-street-journal', 'the-washington-post',
    'usa-today'
]


def request_all_articles(params, headers):
    """
    Requests articles from news api, handles pagination if needed.
    Assumes that params is a dict containining a pageSize key
    Returns a list of all articles from all pages
    """
    all_articles = []
    response = requests.get(
        'https://newsapi.org/v2/everything', params=params, headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        # TODO: Add logging
        pass

    response = response.json()

    all_articles += response['articles']

    total_results = int(response['totalResults'])
    page_size = int(params['pageSize'])
    num_pages = 1 + int(total_results / page_size)

    if num_pages == 1:
        return all_articles

    for page in range(2, num_pages):
        params['page'] = page
        response = requests.get(
            'https://newsapi.org/v2/everything',
            params=params,
            headers=headers).json()

        # page depth allowed for free tier news api is strange. just stop when we stop getting articles
        if 'articles' not in response.keys():
            break

        all_articles += response['articles']

    return all_articles


def request_news(api_key):
    """
    Makes an http request to the news api
    Parses the resulting data into a list of Articles and returns it
    """
    yesterdays_date = date.today() - timedelta(1)
    yesterdays_date = yesterdays_date.strftime('%y-%m-%d')

    req_params = {
        'q': ['government shutdown', 'shutdown'],
        'sortBy': 'popularity',
        'from': yesterdays_date,
        'pageSize': 100,  # max page size to minimize number of requests
        # news api requires this to be a comma-separated list
        'sources': ','.join(SOURCES)
    }

    req_headers = {'Authorization': api_key}

    return request_all_articles(req_params, req_headers)


def article_exists(article):
    """
    Queries the db to check if an article with the same url already exists.
    """
    articles = db_session().query(
        models.Article).filter(models.Article.url == article['url']).all()
    if articles:
        return True
    return False


def source_exists(source):
    """
    Queries the db to check if a source with the same name already exists.
    """
    sources = db_session().query(
        models.Source).filter(models.Source.name == source['name']).all()
    if sources:
        return True
    return False


def add_sources(articles):
    """
    Adds sources to the database if they do not exist yet.
    """
    for article in articles:
        if not source_exists(article['source']):
            source = models.Source(name=article['source']['name'])
            db_session().add(source)
            db_session().commit()


def get_all_sources():
    """
    Fetches all of the sources from the database.
    Returns a dict of {source_name: source_id}
    """
    sources = db_session().query(models.Source)
    output_ids = {}
    for source in sources:
        output_ids[source.name] = source.source_id

    return output_ids


def persist_articles(articles, source_ids):
    """
    Adds this article as a record to the article table using db_session.
    We assume that the source exists in source_ids.
    """
    for article in articles:
        if article_exists(article):
            continue

        formatted_time = parser.parse(article['publishedAt'])
        looked_up_id = source_ids[article['source']['name']]

        db_article = models.Article(
            headline=article['title'],
            url=article['url'],
            image_url=article['urlToImage'],
            publish_time=formatted_time,
            source_id=looked_up_id)

        db_session().add(db_article)
    db_session().commit()


def fetch_news():
    """
    Requests news matching keywords from NewsAPI.
    Uses api key from environment variable.
    Stores results in database.
    """
    news_api_key = os.environ['NEWS_API_KEY']
    recent_articles = request_news(news_api_key)

    add_sources(recent_articles)

    source_ids = get_all_sources()

    persist_articles(recent_articles, source_ids)


class NewsService:
    """
    Simply responsible for starting up the BackgroundScheduler that starts
    fetching data from News API every five minutes.
    """
    TEN_MINUTES_SECS = 600

    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def startup(self, app):
        """
        Adds the news service to the BackgroundScheduler and starts it.
        """
        self.scheduler.add_job(
            fetch_news,
            'interval',
            seconds=self.TEN_MINUTES_SECS,
            misfire_grace_time=10,
            next_run_time=datetime.now())
        app.logger.info('Starting news service...')
        self.scheduler.start()
