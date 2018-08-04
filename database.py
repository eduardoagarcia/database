#! /usr/bin/python

import os
import json
import pprint
import urllib
import urllib2
import random
import string
import re
import base64
import hashlib


# --------------------------------------------------------
# EXAMPLE USAGE:
# --------------------------------------------------------
#
# from modules.database import DB
# db = DB('main')
# results = db.table('users').select('*').where('age < 30').where('rank > 20').orWhere('nickname = "John"').orWhere('nickname != "Peter"').orderByAsc('created_by').orderByDesc('name').get()
# for result in results:
#   db.debug(result['name'])
#
# --------------------------------------------------------


# Create new Database Class
class DB:

    # Init
    def __init__(self, database):

        # Define mysql endpoint
        self.endpoint = ''

        # Grab the private key and public key from the json data
        self.private_key = ''
        self.public_key  = ''

        # Init query parts
        self.database     = database
        self._where       = []
        self._orWhere     = []
        self._table       = ''
        self._select      = ''
        self._orderByAsc  = ''
        self._orderByDesc = ''
        self._raw         = ''

        # Init results count
        self.results      = []
        self.recent       = False

    # Debug
    def debug(self, o):
        pprint.pprint(o)

    # Create a random string
    def randomString(self, size=6, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    # Encode Query String
    def encodeQueryString(self, query):

        # Build the query string structure
        query_string = self.database + '|' + query

        # First pass
        query_string = self.randomString( 3 ) + base64.b64encode( query_string ) + self.randomString( 8 )

        # Second pass
        query_string = self.randomString( 11 ) + base64.b64encode( query_string ) + self.randomString( 4 )

        # Third pass
        query_string = base64.b64encode( query_string )

        # return the query string
        return query_string

    # Execute a POST request
    def post(self, query_string):

        # Define parameters for request
        parameters = {}

        # URL Encode our parameters
        data = urllib.urlencode(parameters)

        # Execute the request
        request  = urllib2.Request(self.endpoint, data)
        response = urllib2.urlopen(request)

        # return the response (in JSON)
        return json.loads( response.read() )

    # Query
    def query(self, query):

        # Encode Query String
        query_string = self.encodeQueryString(query)

        # Execute the query with the encoded query_string
        results = self.post(query_string)

        # Assign results to self
        self.results = results

        # Recet recent results
        self.recent = False

        # Return the results
        return results

    # Assemble Query String
    def assembleQueryString(self):

        # Start building the query string
        query_string = 'SELECT ' + self._select + ' FROM ' + self._table + ' '

        # AND wheres
        if self._where:
            if 'WHERE' in query_string:
                query_string += ' AND '
            if not 'WHERE' in query_string:
                query_string += ' WHERE '
            query_string += ' AND '.join(self._where)

        # OR wheres
        if self._orWhere:
            if 'WHERE' in query_string:
                query_string += ' OR '
            if not 'WHERE' in query_string:
                query_string += ' WHERE '
            query_string += ' OR '.join(self._orWhere)

        # Order By ASC
        if self._orderByAsc:
            if 'ORDER BY' in query_string:
                query_string += ', '
            if not 'ORDER BY' in query_string:
                query_string += ' ORDER BY '
            query_string += self._orderByAsc + ' ASC '

        # Order By DESC
        if self._orderByDesc:
            if 'ORDER BY' in query_string:
                query_string += ', '
            if not 'ORDER BY' in query_string:
                query_string += ' ORDER BY '
            query_string += self._orderByDesc + ' DESC '

        # raw
        if self._raw:
            query_string = self._raw

        # clean query
        query_string = re.sub(' +', ' ', query_string)
        query_string = re.sub(' ,', ',', query_string)
        query_string = query_string.strip()

        # Return assembled query string
        return query_string

    # Table
    def table(self, table):
        self._table = table
        return self

    # Select
    def select(self, select):
        self._select = select
        return self

    # Where
    def where(self, where):
        self._where.append(where)
        return self

    # OR Where
    def orWhere(self, where):
        self._orWhere.append(where)
        return self

    # orderByAsc
    def orderByAsc(self, orderByAsc):
        self._orderByAsc = orderByAsc
        return self

    # orderByDesc
    def orderByDesc(self, orderByDesc):
        self._orderByDesc = orderByDesc
        return self

    # Execute a raw query
    def raw(self, query):
        self._raw = query
        return self

    # Work with the most recent result set
    def latestResults(self):
        self.recent = True
        return self

    # get
    def get(self):

        # Recent results?
        if not self.recent:

            # Assemble query string
            query_string = self.assembleQueryString()

            # Run the query
            self.query(query_string)

        # Return the results
        return self.results

    # execute (clone of get)
    def execute(self):

        # Recent results?
        if not self.recent:

            # Assemble query string
            query_string = self.assembleQueryString()

            # Run the query
            self.query(query_string)

        # Return the results
        return self.results

    # count
    def count(self):

        # Recent results?
        if not self.recent:

            # Assemble query string
            query_string = self.assembleQueryString()

            # Run the query
            self.query(query_string)

        # Return the number or results
        return len(self.results)

    # get query
    def getQuery(self):

        # Assemble query string
        query_string = self.assembleQueryString()

        # Run the query string
        return query_string

# eof