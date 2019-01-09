from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import DateTime


class Article(Base):
    """
    Table to store articles gathered from News API
    """
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    headline = Column(String(256))
    url = Column(String(256), unique=True)
    image_url = Column(String(256), unique=True)
    publish_time = Column(DateTime())
    source_id = Column(Integer, ForeignKey("source.source_id"))


class Source(Base):
    """
    Table to store sources that articles reference
    """
    __tablename__ = 'source'
    source_id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True)
