import argparse
import time

import transaction
from pyramid.paster import bootstrap
from twython import TwythonStreamer

from mist.models import handle_message

class TweetStreamer(TwythonStreamer):
    """ Convert tweets into our database.
    """

    def on_success(self, data):
        if 'text' in data and 'user' in data:
            text = data['text']
            for ignore in self.ignore:
                text = text.replace(ignore, '')
            screen_name = data['user']['screen_name']
            handle_message(text, screen_name, 'twitter')
            transaction.commit()

    def on_error(self, status_code, data):
        print(status_code)
        print(data)
        #self.disconnect()


def main():
    """ Listen for SMS incoming on the first cellular modem connected.
    """
    parser = argparse.ArgumentParser(
        description=main.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file',
                        default='production.ini',
                        help="Path to ini configuration to load environment " \
                             "settings from.")
    parser.add_argument('-t', '--track',
                        default='#jcuopenday',
                        help="Search to track for tweets.")
    parser.add_argument('--app-key')
    parser.add_argument('--app-secret')
    parser.add_argument('--oauth-token')
    parser.add_argument('--oauth-token-secret')
    config = parser.parse_args()
    env = bootstrap(config.file)

    stream = TweetStreamer(config.app_key, config.app_secret, config.oauth_token, config.oauth_token_secret)
    stream.ignore = [config.track]
    stream.statuses.filter(track=config.track)

    while True:
        time.sleep(60)




