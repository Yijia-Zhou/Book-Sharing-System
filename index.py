# coding: UTF-8
import sys
import os

import web

reload(sys)
sys.setdefaultencoding('utf8')

from book import listBook, shareBook, receiveBook, requestBook, receiveRequest, manageBook, checkPermission, listRequest, receiveChange

urls = (
    '/', 'listBook',
    '/listbook', 'listBook',
    '/sharebook', 'shareBook',
    '/receivebook', 'receiveBook',
    '/requestbook', 'requestBook',
    '/receiverequest', 'receiveRequest',
    '/managebook', 'manageBook',
    '/checkpermission', 'checkPermission',
    '/listrequest', 'listRequest',
    '/receivechange', 'receiveChange',
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)


class hello:
    def GET(self):
        return "Hello, world!"

application = web.application(urls, globals()).wsgifunc()
web.config.debug = True
