from datetime import datetime
import logging
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


__all__ = ['DBSession', 'Base', 'Keyword', 'Source', 'Message', 'handle_message']
logger = logging.getLogger(__name__)


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


from nltk import clean_html
from mist.config import WORD_TOKENIZER, STOP_WORDS, PROFANITY

def process_text(text):
    """ Process incoming text into individual tokens.
    """
    lowercase = text.lower()
    clean_text = clean_html(lowercase)
    tokens = WORD_TOKENIZER.tokenize(clean_text)
    clean_tokens = [t for t in tokens if t not in PROFANITY]

    if len(tokens) != len(clean_tokens):
        raise ValueError('Profanity detected in incoming message.')

    return [t for t in tokens if t not in STOP_WORDS]


def handle_message(text, source_id, source_type):
    """ Handle any sort of incoming message.

    :param text: The message text
    :param source_id: The unique identifier of the source
       such as phone number or Twitter user ID.
    :param source_type: Type of source this message comes from
       - such as 'sms' or 'twitter'
    """

    #Create or obtain the source for the message
    source = DBSession.query(Source).filter(Source.id == source_id).first()
    if not source:
        source = Source(source_id, source_type, ignored=False)
        DBSession.add(source)

    if source.ignored:
        logging.info('Ignored new message from %s containing: %r' % (source_id,
                                                                     text))
        return

    #Process the text and clean into tokens
    try:
        keywords = process_text(text)
    except ValueError:
        #Abort processing if any poor form happens
        source.ignored = True
        logging.info('Profanity detected from %s: %r' % (source_id,
                                                         text))
        return

    #Add message to the database
    message = Message(text, source)
    DBSession.add(message)

    #Add keywords to the database
    for keyword_text in keywords:
        keyword = DBSession.query(Keyword).filter(Keyword.keyword == keyword_text).first()
        if not keyword:
            keyword = Keyword(keyword_text)
            DBSession.add(keyword)
        keyword.count += 1

    logging.info('Received new message from %s containing: %r' % (source_id,
                                                                  text))
