from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed
from django.views.generic.simple import direct_to_template
from views import *
from feeds import GroupFeed

feeds = {
    'collection': GroupFeed,
}

urlpatterns = patterns('',
    url(r'^collections/$', collections, name='data-collections'),
    url(r'^collection/(?P<id>\d+)/(?P<name>[-\w]+)/$', collection_raw, name='data-collection'),
    url(r'^record/(?P<id>\d+)/(?P<name>[-\w]+)/$', record, name='data-record'),
    url(r'^record/(?P<id>\d+)/(?P<name>[-\w]+)/edit/$', record, kwargs={'edit': True}, name='data-record-edit'),
    url(r'^record/(?P<id>\d+)/(?P<name>[-\w]+)/edit/(?P<contexttype>\w+)/(?P<contextid>\d+)/(?P<contextname>[-\w]+)/$', record, kwargs={'edit': True}, name='data-record-edit-context'),
    url(r'^record/(?P<id>\d+)/(?P<name>[-\w]+)/edit/personal/$', record, kwargs={'edit': True, 'personal': True}, name='data-record-edit-personal'),
    url(r'^record/new/$', record, kwargs={'id': None, 'name': None, 'edit': True}, name='data-record-new'),
    url(r'^selected/$', selected_records, name='data-selected'),
    (r'^feeds/(?P<url>.*)/$', feed, {'feed_dict': feeds}),
)
