# -*- coding: utf-8 -*-

"""
feedjack
Gustavo Picón
admin.py
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _ 
from feedjack import models


class LinkAdmin(admin.ModelAdmin):
    pass
class GroupAdmin(admin.ModelAdmin):
    pass



class SiteAdmin(admin.ModelAdmin):
    list_display = ('url', 'name')
    filter_vertical = ('links',)



class FeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'feed_url', 'title', 'last_modified', \
      'is_active')
    fieldsets = (
      (None,
        {'fields':('feed_url', 'name', 'is_active')}),
      (_('Fields updated automatically by Feedjack'),
        {'classes':('collapse',),
         'fields':('title', 'tagline', 'link', 'etag', 'last_modified',
                   'last_checked'),
        })
    )
    search_fields = ('feed_url', 'name', 'title')
    list_filter=('last_modified',)
    date_hierarchy = 'last_modified'
    class Media:
        js = ('feedjack/load_feed_name.js',)



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'author', 'date_modified')
    search_fields = ['link', 'title']
    date_hierarchy = 'date_modified'
    filter_vertical = ('tags',)



class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'feed')
    list_filter = ('site',)
    search_fields=('name',)


admin.site.register(models.Link, LinkAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.Site, SiteAdmin)
admin.site.register(models.Feed, FeedAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Subscriber, SubscriberAdmin)

#~
