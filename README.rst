Mist
====

In Norse mythology, `Mist` is a valkyrie, and the name is believed to stem
from `mistr`, meaning `cloud, mist`. Little information is known about
this valkyrie, much like this project.  Much like a valkyrie, this project 
may ensure your survival if your requirements match what it does.

This is a Pyramid-based project that creates live tag clouds using the
`d3-cloud <https://github.com/jasondavies/d3-cloud>`_ library from various
data sources.

Getting Started
---------------

This project installs using `Buildout <http://buildout.org>`_. Tested
with Python 2.7.3 for now. Python 3 is supported by some dependencies
but isn't likely to work with all of them at the time of writing.

.. code:: bash

    git clone https://github.com/davidjb/mist.git
    cd mist
    python2.7 bootstrap.py
    ./bin/buildout
    ./bin/initialize_mist_db development.ini
    ./bin/pserve development.ini
    
Twitter integration
~~~~~~~~~~~~~~~~~~~
    
For integration with Twitter, you require API keys for OAuth 1. See 
https://twython.readthedocs.org/en/latest/usage/starting_out.html#oauth1
for information.

.. code:: bash

    ./bin/run_twitter_listener --help
    
Cellular (SMS) integration
~~~~~~~~~~~~~~~~~~~~~~~~~~
    
For integration with SMSes, you need to have a Cellular modem (USB or serial
will work), and something that is supported by ``python-gsmmodem``. Plug
this into your computer, ensure that you can connect to it and communicate
in some fashion (``screen``, ``cu``, etc).  Then, run the listener:

.. code:: bash

    ./bin/run_sms_listener --help

Technologies used
-----------------

waitress
    For basic web serving
    
pyramid
    The Python web framework. Not built by aliens.
    
SQLAlchemy
    Used for Object Relational Mapping (ORM) with database storage.
    
transaction
    Transactional support for the application.
    
pyramid_tm
    Transactions for web requests in Pyramid.
    
    
Fanstatic
    Easy static resource serving for Python web frameworks. Easily
    depend on JavaScript and CSS libraries from your Python egg, and include
    them on any given page using ``my_library.need()``.
pyramid_fanstatic
    Integration of Fanstatic with Pyramid. Allows ini-based
    configuration for Fanstatic options.
js.jquery
    jQuery for Fanstatic.
js.d3_cloud
    D3-based word cloud library for Fanstatic. Works like http://wordle.net. 
js.bootstrap
    Twitter bootrap resources for Fanstatic.

natural
    Human Data display of dates (eg ``1 hour ago``)
nltk
    Language tokenisation and filtering
twython
    Twitter streaming of data via its API
python-gsmmodem
    Library for managing cellular modems. Allows SMS callbacks in Python!
telstra.mobile
    Auto-detection of modem for ``python-gsmmodem``. May be integrate

zombie-translator
    For fun. Translates all words in word-cloud into zombie speak.
