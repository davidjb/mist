import unittest
import transaction

from pyramid import testing

from mist.models import *

class BaseTest(unittest.TestCase):
    def setUp(self):
        from sqlalchemy import create_engine
        from mist.models import Base

        self.config = testing.setUp()
        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()


class TestSmsReception(BaseTest):

    def test_sms_handler(self):
        from mist.scripts import sms_listener
        from gsmmodem import modem
        sms = modem.Sms('+61123456789', 'My other cat is a dog.')
        sms_listener.handleSms(sms)

        message = DBSession.query(Message).one()
        self.assertEqual(message.text, 'My other cat is a dog.')

        source = DBSession.query(Source).one()
        self.assertEqual(source.id, '0123456789')
        self.assertEqual(source.type, 'sms')

class TestTwitterReception(BaseTest):

    def test_twitter_handler(self):
        from mist.scripts import twitter_listener
        pass

class TestSources(BaseTest):

    def test_source(self):
        handle_message('Test', '@davidjb_', 'twitter')
        source = DBSession.query(Source).one()
        self.assertEqual(source.id, '@davidjb_')
        self.assertEqual(source.type, 'twitter')

    def test_ignored_source(self):
        handle_message('Test', '@davidjb_', 'twitter')
        source = DBSession.query(Source).one()
        source.ignored = True

        handle_message('This is a nasty message.', '@davidjb_', 'twitter')
        messages = DBSession.query(Message).all()
        self.assertEqual(len(messages), 1)

    def test_profanity(self):
        handle_message('This is a shit message.', '@davidjb_', 'twitter')
        messages = DBSession.query(Message).all()
        self.assertEqual(len(messages), 0)
        source = DBSession.query(Source).one()
        self.assertTrue(source.ignored)


