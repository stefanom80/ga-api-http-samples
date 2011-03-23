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


"""Demo on how to paginate through the Google Analytics Data Export API.

This application demonstrates how to paginate through more than 10,000 results.
All the results are outputted to a file as tab seperated text.

Usage: Set your table id parameter in the TABLE_ID variable. Configure which
    file to write to in the OUTPUT_FILE_NAME variable.

APP_NAME: The name of this application.
TABLE_ID: The Google Analytics Table ID from which to retrieve data.

  main(): The main logic of the application.
  GetAuthorizedClient(): Returns an authorized client object to make requests
      to the Google Analytics API.
  GetDataFeedQuery(): Returns a new data feed query object with a sample query.
  FeedPrinter: Converts the API response into a table.
  UnicodeWriter: Provides a way to write unicode tabbed seperated text.
"""

__author__ = 'api.nickm@google.com (Nick Mihailovski)'


import sys
import auth
import feed_printer
import gdata.analytics.client
import pagination


APP_NAME = 'AutoPaginator_Demo'
TABLE_ID = 'ga:xxxxx'  # Insert your Table Id here.
OUTPUT_FILE_NAME = 'my_output.tsv'


def main():
  """Main program."""
  my_auth_helper = auth.AuthRoutineUtil()
  my_client = GetAuthorizedClient(my_auth_helper, APP_NAME)

  paginator = pagination.AutoPaginator(my_client, my_auth_helper, verbose=True)

  my_query = GetDataFeedQuery(TABLE_ID)

  # Try to get all the pages avalaible in the query as one big feed object.
  try:
    feed = paginator.GetDataFeed(my_query, -1)

  except pagination.AutoPaginatorError, error:
    print error.msg
    sys.exit(1)

  # Output some stats.
  print '\nTotal results found: %d' % paginator.total_results
  print ('Total pages needed, with one page per API request: %d\n'
         % paginator.num_pages)

  # Output the results as a tsv file.
  printer = feed_printer.GetTsvFilePrinter(OUTPUT_FILE_NAME)
  printer.Output(feed)


def GetAuthorizedClient(my_auth_helper, app_name):
  """Returns an authorized Google Analytics API client object.

  If an error occurs with authorization, the error is printed and the
  program is terminated.

  Args:
    my_auth_helper: auth.AuthRoutine implementation. A class which simplifies
        getting the appropriate authorization token.
    app_name: string The name of this application.

  Returns:
    gdata.analytics.client.AnalyticsClient An object which can be used to make
    Google Analytics API requests.
  """
  my_client = gdata.analytics.client.AnalyticsClient(source=app_name)
  my_auth = auth.OAuthRoutine(my_client, my_auth_helper)

  try:
    my_client.auth_token = my_auth.GetAuthToken()
    return my_client

  except auth.AuthError, error:
    print error.msg
    sys.exit(1)


def GetDataFeedQuery(table_id):
  """Returns a Data Export API query object with a sample query.

  The query specifies the top sources of search traffic by visits
  to the site.

  Args:
    table_id: string The table id from which to retrieve data.
        Format is ga:xxxxxx, where xxxxxx is the profile ID.

  Returns:
    gdata.analytics.client.DataFeedQuery A data feed query object.
  """
  return gdata.analytics.client.DataFeedQuery({
      'ids': table_id,
      'start-date': '2010-10-01',
      'end-date': '2010-10-30',
      'dimensions': 'ga:source,ga:medium,ga:keyword',
      'metrics': 'ga:visits',
      'sort': '-ga:visits,ga:medium,ga:source'})


if __name__ == '__main__':
  main()
