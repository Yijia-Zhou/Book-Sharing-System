# -*- coding: utf-8 -*-
from __future__ import print_function, with_statement

import os
import shelve
from contextlib import closing

import web

class bookBase:
    '''
    用于 init 的父类。
    '''
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

class listBook(bookBase):

    def GET(self):
        with closing(shelve.open('books.db', flag='c', writeback=True)) as booksDB:
            keys = [key for key in booksDB.keys()]
            keys.remove('counter')
            books = [booksDB[key] for key in keys]
        return self.render.listbook(books)

class shareBook(bookBase):

    def GET(self):
        return self.render.sharebook()

class receiveBook(bookBase):

    def POST(self):
        data = web.input()
        with closing(shelve.open('books.db', flag='c', writeback=True)) as booksDB:
            key = str(booksDB['counter'] + 1)
            booksDB['counter'] += 1
            booksDB[key] = {
                'key': key,
                'title': data['title'],
                'command': data['command'],
                'owner': data['owner'],
                'taker': data['owner'],
                'tel': data['tel'],
                'taker_tel': data['tel'],
                'question': data['question'],
                'answer': data['answer'],
                'reqs': 0,
                'req_cases': {}
            }
        return self.render.receivebook()

class requestBook(bookBase):
    
    def POST(self):
        data = web.input()
        with closing(shelve.open('books.db', flag='c', writeback=True)) as booksDB:
              book = booksDB[str(data['key'])]
        return self.render.requestbook(book)


class receiveRequest(bookBase):

    def POST(self):
        data = web.input()
        key = str(data['key'])
        with closing(shelve.open('books.db', flag='c', writeback=True)) as booksDB:
            book = booksDB[key]
            book['reqs'] += 1
            book['req_cases'][str(book['reqs'])] = {
                'requester': data['requester'],
                'requester_tel': data['requester_tel'],
                'req_reason': data['req_reason']
            }
            booksDB[key] = book
        
        return self.render.reply_to_request()

class manageBook(bookBase):
    
    def GET(self):
        with closing(shelve.open('books.db', flag='c', writeback=True)) as booksDB:
            keys = [key for key in booksDB.keys()]
            keys.remove('counter')
            books = [booksDB[key] for key in keys]
        return self.render.managebook(books)

class checkPermission(bookBase):

    def POST(self):
        data = web.input()
        key = str(data['key'])
        with closing(shelve.open('books.db', flag='c', writeback=True)) as booksDB:
            book = booksDB[key]
        return self.render.checkpermission(book)

class listRequest(bookBase):

    def POST(self):
        data = web.input()
        key = str(data['key'])
        with closing(shelve.open('books.db', flag='c', writeback=True)) as booksDB:
            book = booksDB[key]
        
        if str(data['apply_answer']).strip() != str(book['answer']).strip():
            return 'Answer incorrect! Please press return and try again.'
        
        return self.render.listrequest(book)

class receiveChange(bookBase):

    def POST(self):
        data = web.input()
        key = str(data['key'])
        req_key = str(data['req_key'])
        with closing(shelve.open('books.db', flag='c', writeback=True)) as booksDB:
            book = booksDB[key]
            req = book['req_cases'][req_key]
            booksDB[key]['taker'] = req['requester']
            booksDB[key]['taker_tel'] = req['requester_tel']
            del booksDB[key]['req_cases'][req_key]
        return 'Complete!'
