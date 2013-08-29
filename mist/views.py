import json
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy import func
from sqlalchemy.sql.expression import desc
from sqlalchemy.exc import DBAPIError
from fanstatic import Resource, Library
from js.jquery import jquery
from js.d3_cloud import d3_cloud
from js.bootstrap import bootstrap

from zombie_translator import to_zombish

from .models import (
    DBSession,
    Keyword,
    Source,
    Message,
    )

library = Library('mist', 'static')
word_cloud_js = Resource(library, 'keyword_cloud.js', bottom=True,
                         depends=(jquery, d3_cloud))

@view_config(route_name='home', renderer='templates/home.pt')
class HomeView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.dbsession = DBSession

    def __call__(self):
        bootstrap.need()
        word_cloud_js.need()
        return {}

    def keywords(self, maximum=200):
        keywords = self.dbsession.query(Keyword)[:maximum]
        for keyword in keywords:
            yield {'text': keyword.keyword,
                   'color': 1,
                   'size': float(keyword.count)}

    def keywords_json(self):
        return json.dumps(list(self.keywords()))

    def top_people(self, type):
        return self.dbsession.query(Source, func.count(Message.id).label('count')) \
                .join(Message) \
                .group_by(Source) \
                .filter(Source.type == type) \
                .order_by(desc('count'))[:5]

    def latest_messages(self):
        return self.dbsession.query(Message).order_by(Message.entry_datetime.desc())[:5]


@view_config(route_name='zombie', renderer='templates/home.pt')
class ZombieHomeView(HomeView):

    def keywords(self, maximum=200):
        keywords = super(ZombieHomeView, self).keywords(maximum)
        #convert keywords to zombie
        zombie_keywords = []
        for keyword in keywords:
            keyword['text'] = to_zombish(keyword['text'])
            zombie_keywords.append(keyword)
        return zombie_keywords
