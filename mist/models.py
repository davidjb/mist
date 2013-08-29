from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    UnicodeText,
    Unicode,
    String,
    Boolean,
    ForeignKey,
    DateTime
    )
from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension


__all__ = ['DBSession', 'Base', 'Keyword', 'Source', 'Message']


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Keyword(Base):
    __tablename__ = 'keywords'

    keyword = Column(Unicode, primary_key=True)
    count = Column(Integer, nullable=False)

    def __init__(self, keyword, count=0):
        self.keyword = keyword
        self.count = count


class Source(Base):
    __tablename__ = 'sources'

    #: Either the phone number or Twitter user ID
    id = Column(String, primary_key=True)

    #: Describe the type of the source - Twitter, SMS, etc
    type = Column(String)

    #: Whether to ignore this source or not
    ignored = Column(Boolean)

    def __init__(self, id, type, ignored=False):
        self.id = id
        self.type = type
        self.ignored = ignored


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    text = Column(UnicodeText, nullable=False)
    entry_datetime = Column(DateTime, default=datetime.now, nullable=False)
    source_id = Column(String, ForeignKey(Source.id))
    source = relationship(Source,
                          backref=backref('messages', order_by=id))

    def __init__(self, text, source):
        """@todo: Docstring for __init__
        """
        self.text = text
        self.source = source


def handle_message(text, source_id, source_type):

    #Create or obtain the source for the message
    source = DBSession.query(Source).filter(Source.id == source_id).first()
    if not source:
        source = Source(source_id, source_type, ignored=False)
        DBSession.add(source)

    #Add message to the database
    message = Message(text, source)
    DBSession.add(message)

    #Add keywords to the database
    #XXX Filter here
    keywords = text.split()
    #if profanity_detected(text):
    #source.ignored = True
    #pass

    for keyword_text in keywords:
        keyword = DBSession.query(Keyword).filter(Keyword.keyword == keyword_text).first()
        if not keyword:
            keyword = Keyword(keyword_text)
            DBSession.add(keyword)
        keyword.count += 1
