from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, ForeignKey
import sys
sys.path.append('../')

from src.db_config import Base

class Article(Base):
    __tablename__ = 'articles'
    article_id = Column(String, primary_key=True)
    source_name = Column(String)
    published_at = Column(TIMESTAMP)
    title = Column(Text)
    full_content = Column(Text)

class Topic(Base):
    __tablename__ = 'topics'
    topic_id = Column(Integer, primary_key=True, autoincrement=True)
    topic_keywords = Column(Text)
    article_id = Column(String, ForeignKey('articles.article_id'))

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_description = Column(Text)
    article_id = Column(String, ForeignKey('articles.article_id'))

class Feature(Base):
    __tablename__ = 'features'
    feature_id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(String, ForeignKey('articles.article_id'))
    tfidf_vector = Column(Text)
    topic = Column(Integer)
    event_cluster = Column(Integer)
