import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_fanstatic',
    'js.d3_cloud',
    'js.bootstrap',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='mist',
      version='0.0',
      description='mist',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='mist',
      install_requires=requires,
      extras_require={
          'dev': ['ipdb', 'pyramid_debugtoolbar'],
      },
      entry_points="""\
      [paste.app_factory]
      main = mist:main
      [console_scripts]
      initialize_mist_db = mist.scripts.initializedb:main
      """,
      )
