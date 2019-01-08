"""
This override exists so that we can control what happens when the server is
started. I couldn't find any other satisfactory method for doing this aside
from implementing a main function and only starting the server that way.
This seemed more correct.
"""
import click
from flask import Flask
from flask.cli import FlaskGroup
from news_service import NewsService
from database import init_db


def create_app():
    """
    We override the default app creation logic so that we can start the
    news_service when the server is created.
    """
    app = Flask('government_up_yet')
    init_db()
    news_service = NewsService()
    news_service.startup(app)
    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass
