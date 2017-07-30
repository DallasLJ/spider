#!/usr/bin/python3

class Error(Exception):
    pass

class DomainUrlError(Error):

    def __init__(self, message):
        self.message = message

class SpiderError(Error):

    def __init__(self, message):
        self.message = message
