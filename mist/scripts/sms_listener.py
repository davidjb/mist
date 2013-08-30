import argparse
import time

import transaction
from pyramid.paster import bootstrap
from telstra.mobile import autodetect_modem

from mist.models import handle_message


def handleSms(sms):
    """ Convert SMS into our database.
    """
    handle_message(sms.text, sms.number.replace('+61', '0'), 'sms')
    transaction.commit()


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
    configuration = parser.parse_args()
    env = bootstrap(configuration.file)

    modem = autodetect_modem(
        modem_options={'baudrate': 9600,
                       'smsReceivedCallbackFunc': handleSms})

    while True:
        time.sleep(60)




