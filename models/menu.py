# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################


response.title = request.application.replace('_',' ').title()
response.subtitle = T('')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Srikant Patnaik <srikant@fossee.in>'
response.meta.description = 'a remote debugger'
response.meta.keywords = 'aakash, support, debug'
response.meta.generator = ''

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T(''), False, URL('default', 'index'), [])
]
