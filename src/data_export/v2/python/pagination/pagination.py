#!/usr/bin/python
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Provides a class to auto-paginate through the Data Export API.

The maximum number of results returned by the Data Export API is 10,000 per
page. In some cases a query can match more than that number of data points.
When this happens, one can paginate through the results to get all the data.

  AutoPaginator: handles pagination through the API.
  AutoPaginatorError: exception if the paginator encounters an API error.
"""

from __future__ import division

__author__ = 'api.nickm@google.com (Nick Mihailovski)'


import math
import gdata.client


class AutoPaginator(object):
  """Provides a class to get all the pages in a Data Export API query.

  Attributes:
    DEFAULT_START_INDEX: int The start index used by the API if not specified
        in the query start-index parameter.
    DEFAULT_MAX_RESULTS: int The number of max_results returned by the Data
        Export API if no max_results query paramater is specified.
  """

  DEFAULT_START_INDEX = 1
  DEFAULT_MAX_RESULTS = 10000

  def __init__(self, my_client, my_auth_helper, verbose=False):
    """initializes this class.

    Args:
      my_client: gdata.analytics.client.AnalyticsClient The main object to
          make requests to the API.
      my_auth_helper: auth.AuthRoutine implementation.
      verbose: boolean Whether to print the queries that are being executed.
    """
    self.my_client = my_client
    self.my_auth_helper = my_auth_helper
    self.verbose = verbose
    self.start_index = None
    self.total_results = None
    self.max_pages = None
    self.num_pages = None

  def GetDataFeed(self, query, num_pages):
    """Retrieves report data by paging through the Data Feed results.

    Args:
      query: gdata.analytics.client.DataQuery The query to pagniate.
          The start-index is respected. The max-results will be overwritten to
          the maximum number of results allowed by the API.
      num_pages: int The number of pages to retrieve from the API.
          if -1: return all pages in the result.
          if >0: return a specific number of pages in the result.

    Returns:
      gdata.analytics.data.DataFeed A DataFeed object with all the entries
      across all pages. The idea is to keep the interface of the result the
      same as if a single query was made.

    Raises:
      AutoPaginatorError if an error occurs with the API request.
    """
    # Issue the first query to see how many results the API returns.
    query.query['max-results'] = AutoPaginator.DEFAULT_MAX_RESULTS
    feed = self.GetData(query)

    # Determine the number of pages we need to retrieve.
    self.start_index = int(query.query.get('start-index') or
                           AutoPaginator.DEFAULT_START_INDEX)
    self.total_results = self.GetIndexedTotalResults(feed.total_results.text)
    self.max_pages = self.GetMaxPages()
    self.num_pages = self.DetermineNumPages(num_pages)

    # Retrieve the data for the remaining queries.
    start_indicies = self.GetStartIndicies()
    for start_index in start_indicies:
      query.query['start-index'] = str(start_index)
      page = self.GetData(query)
      feed.entry.extend(page.entry)

    return feed

  def GetIndexedTotalResults(self, total_results):
    """Returns the remaining results in the feed after the start-index.

    Args:
      total_results: str The total results the API found for the particular
          query. Usually found in the reponse of a query.

    Returns:
      int The remainin results in the feed.
    """
    return int(total_results) - self.start_index + 1

  def GetMaxPages(self):
    """Returns the number of pages in the feed.

    Returns:
      int The maximum number of pages that can be returned from the API for
      this query.
    """
    return int(math.ceil(self.total_results /
                         AutoPaginator.DEFAULT_MAX_RESULTS))

  def DetermineNumPages(self, num_pages):
    """Determines the number of pages to retrieve from the API.

    If num_pages == -1, this returns the maximum pages this query can return.
    Otherwise, it ensures the user does not specify more pages than exist for
    the query.

    Args:
      num_pages: int The number of pages to retrieve specified by the user.

    Returns:
      int The number of pages for which to retrieve data.

    Raises:
       AutoPaginatorError: if num_pages is invalid.
    """
    if num_pages == -1:
      num_pages = self.max_pages
    elif num_pages > 0:
      num_pages = min(self.max_pages, num_pages)
    else:
      raise AutoPaginatorError(msg=('num_pages must be either -1 or >0. '
                                    'Found %d' % num_pages))
    return num_pages

  def GetStartIndicies(self):
    """Returns a list of paginated start indicies.

    Returns:
      A list with each of the paginated start indicies.
    """
    start_indicies = []
    for page_number in range(self.num_pages)[1:]:  # Skip the first page.
      start_index = (page_number * AutoPaginator.DEFAULT_MAX_RESULTS +
                     self.start_index)
      start_indicies.append(start_index)

    return start_indicies

  def GetData(self, query):
    """Retrieves data from the API and does exception handling.

    If self.verbose is set to True, this will print out each query being
    executed. If the auth token is invalid, it will be deleted and an exception
    is raised.

    Args:
      query: gdata.analytics.client.DataFeedQuery The query to execute with the
          Google Analytics API.

    Returns:
      gdata.analytics.data.DataFeed The respose from the API.

    Raises:
      AutoPaginatorError if the token is either invalid or there was an issue
      with the API request.
    """
    if self.verbose:
      print 'Executing query: %s\n' % query

    try:
      return self.my_client.GetDataFeed(query)

    except gdata.client.Unauthorized, error:
      self.my_auth_helper.DeleteAuthToken()
      raise AutoPaginatorError(msg='%s\nDeleted token file.' % error)

    except gdata.client.RequestError, error:
      raise AutoPaginatorError(msg=('There was a error with this query: %s\n'
                                    'Error: \%s') % (query, error))


class AutoPaginatorError(Exception):
  """An application specific Error."""

  def __init__(self, msg=''):
    self.msg = msg
    Exception.__init__(self)

