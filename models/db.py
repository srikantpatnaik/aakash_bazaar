# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()
import os


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')


db.define_table('package',
                 Field('Package_name', 'string', requires=IS_NOT_EMPTY()),
                 Field('user_id', writable=False, readable=False, default=auth.user_id),
               )
 
db.define_table('developer',
                 Field('Name_of_the_apk', 'string', requires=IS_NOT_EMPTY()),
                 Field('Package_name', 'string', requires=IS_NOT_EMPTY()),
                 Field('Category', requires=IS_IN_SET(['Teaching', 'Game', 'Design', 'Development', 'Others'])),
                 Field('License', requires=IS_IN_SET(['GNU GPLv3', 'GNU GPLv2', 'BSD'])),
                 Field('Web_Site', 'string', requires=IS_NOT_EMPTY()),
                 Field('Source_Code', 'string', requires=IS_NOT_EMPTY()),
                 Field('Issue_Tracker', 'string', requires=IS_NOT_EMPTY()),
                 Field('Summary', 'text', requires=IS_NOT_EMPTY()),
                 Field('Description', 'text', requires=IS_NOT_EMPTY()),
                 Field('Changelog', 'text', requires=IS_NOT_EMPTY()),
                 Field('user_id', writable=False, readable=False, default=auth.user_id),
                )
