Mist
====

In Norse mythology, `Mist` is a valkyrie, and the name is believed to stem
from `mistr`, meaning `cloud, mist`. Little information is known about
this valkyrie, much like this project.  Much like a valkyrie, this project 
may ensure your survival if your requirements match what it does.

This is a Pyramid-based project that creates live tag clouds using the
`d3-cloud <https://github.com/jasondavies/d3-cloud>`_ library from various
data sources.

Technologies used
-----------------



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
