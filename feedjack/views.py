# -*- coding: utf-8 -*-

"""
feedjack
Gustavo Picón
views.py
"""


from django.utils import feedgenerator
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils.cache import patch_vary_headers
from django.template import RequestContext, loader

from feedjack import models
from feedjack import fjlib
from feedjack import fjcache

import feedparser
import json

def initview(request):
    """ Retrieves the basic data needed by all feeds (host, feeds, etc)

    Returns a tuple of:
    1. A valid cached response or None
    2. The current site object
    3. The cache key
    4. The subscribers for the site (objects)
    5. The feeds for the site (ids)
    """

    site_id, cachekey = fjlib.getcurrentsite(request.META['HTTP_HOST'], \
      request.META.get('REQUEST_URI', request.META.get('PATH_INFO', '/')), \
      request.META['QUERY_STRING'])
    response = fjcache.cache_get(site_id, cachekey)
    if response:
        return response, None, cachekey, [], []

    site = models.Site.objects.get(pk=site_id)
    sfeeds_obj = fjlib.sitefeeds(site)
    sfeeds_ids = [subscriber.feed.id for subscriber in sfeeds_obj]

    return None, site, cachekey, sfeeds_obj, sfeeds_ids

def blogroll(request, btype):
    """ View that handles the generation of blogrolls.
    """

    response, site, cachekey, sfeeds_obj, sfeeds_ids = initview(request)
    if response:
        return response

    # for some reason this isn't working:
    #
    #response = render_to_response('feedjack/%s.xml' % btype, \
    #  fjlib.get_extra_content(site, sfeeds_ids))
    #response.mimetype = 'text/xml; charset=utf-8'
    #
    # so we must use this:

    template = loader.get_template('feedjack/%s.xml' % btype)
    ctx = {}
    fjlib.get_extra_content(site, sfeeds_ids, ctx)
    ctx = RequestContext(request, ctx)
    response = HttpResponse(template.render(ctx) , \
      mimetype='text/xml; charset=utf-8')


    patch_vary_headers(response, ['Host'])
    fjcache.cache_set(site, cachekey, response)
    return response

def foaf(request):
    """ View that handles the generation of the FOAF blogroll.
    """

    return blogroll(request, 'foaf')

def opml(request):
    """ View that handles the generation of the OPML blogroll.
    """

    return blogroll(request, 'opml')


def buildfeed(request, feedclass, tag=None, subscription=None):
    """ View that handles the feeds.
    """

    response, site, cachekey, sfeeds_obj, sfeeds_ids = initview(request)
    if response:
        return response

    object_list = fjlib.get_paginator(site, sfeeds_ids, page=0, tag=tag, \
      subscription=subscription)[1]

    feed = feedclass(\
        title=site.title,
        link=site.url,
        description=site.description,
        feed_url='%s/%s' % (site.url, '/feed/rss/'))
    for post in object_list:
        feed.add_item( \
          title = '%s: %s' % (post.feed.name, post.title), \
          link = post.link, \
          description = post.content, \
          author_email = post.author_email, \
          author_name = post.author, \
          pubdate = post.date_modified, \
          unique_id = post.link, \
          categories = [tag.name for tag in post.tags.all()])
    response = HttpResponse(mimetype=feed.mime_type)

    # per host caching
    patch_vary_headers(response, ['Host'])

    feed.write(response, 'utf-8')
    if site.use_internal_cache:
        fjcache.cache_set(site, cachekey, response)
    return response

def rssfeed(request, tag=None, subscription=None):
    """ Generates the RSS2 feed.
    """
    return buildfeed(request, feedgenerator.Rss201rev2Feed, tag, subscription)

def atomfeed(request, tag=None, subscription=None):
    """ Generates the Atom 1.0 feed. 
    """
    return buildfeed(request, feedgenerator.Atom1Feed, tag, subscription)

def mainview(request, tag=None, subscription=None, group=None, newer=None, asc=None):
    """ View that handles all page requests.
    """

    response, site, cachekey, sfeeds_obj, sfeeds_ids = initview(request)
    if response:
        return response

    ctx = RequestContext(request, fjlib.page_context(request, site, tag, subscription, group, newer, asc, (sfeeds_obj, \
      sfeeds_ids)))

    response = render_to_response('feedjack/post_list.html', ctx)
    
    # per host caching, in case the cache middleware is enabled
    patch_vary_headers(response, ['Host'])

    if site.use_internal_cache:
        fjcache.cache_set(site, cachekey, response)
    return response

def feedtitle(request):
    if not "url" in request.GET:
        return HttpResponse('""')
    else:
        try:
            #FIXME: do not make http-calls in frontend
            return HttpResponse(json.write(feedparser.parse(request.GET['url']).feed.title), mimetype="text/plain")
        except Exception, e: #404, not a feed, etc.
            return HttpResponse(repr(e))

#~

