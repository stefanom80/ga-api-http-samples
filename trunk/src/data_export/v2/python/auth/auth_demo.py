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


"""Demo on how to authorize a client application for the Google Analytics API.

This file uses the auth module, also part of the sample code, to make
authorization to the Google Analytics API super easy. It supports both OAuth
For Installed Apps and Client Login routines.

Usage: Set your table id parameter in the TABLE_ID variable.

Generally you should use OAuth because the tokens are long-lived, it's
more secure and the tokens can be revoked through the Google Accounts
web interface.

ClientLogin is provided as a fall back option, but the tokens only last
for 14 days. Also there is no way to revoke a ClientLogin token if
the token is compromised.

APP_NAME: The name of this application.
TABLE_ID: The Google Analytics Table ID from which to retrieve data.

  GetClient(): Returns an object to make requests to the Google Analytics API.
  GetDataFeedQuery(): Returns a new data feed query object.
  PrintFeed(): Outputs the data from the API.
"""

__author__ = 'api.nickm@google.com (Nick Mihailovski)'


import sys
import auth
import gdata.analytics.client
import gdata.client


APP_NAME = 'GA_Auth_Helper_Demo'
TABLE_ID = 'ga:xxxx'  # Insert your Table Id here.
START_DATE = '2010-10-01'
END_DATE = '2010-10-30'


def main():
  """Main method of this application."""
  my_client = gdata.analytics.client.AnalyticsClient(source=APP_NAME)
  my_auth_helper = auth.AuthRoutineUtil()

  my_auth = auth.OAuthRoutine(my_client, my_auth_helper)

  # It's better to use OAuthHelper.
  # my_auth = auth.ClientLoginRoutine(my_client, my_auth_helper)

  try:
    my_client.auth_token = my_auth.GetAuthToken()

  except auth.AuthError, error:
    print error.msg
    sys.exit(1)

  data_query = GetDataFeedQuery(TABLE_ID, START_DATE, END_DATE)

  # If the token is invalid, a 401 status code is returned from the server and
  # a gdata.client.Unauthorized exception is raised by the client object.
  # For ClientLogin this happens after 14 days. For OAuth this happens if
  # the token is revoked through the Google Accounts admin web interface.
  # Either way, the token is invalid so we delete the token file on the
  # client. This allows the next iteration of the program to prompt the user
  # to acquire a new auth token.
  try:
    feed = my_client.GetDataFeed(data_query)

  except gdata.client.Unauthorized, error:
    print '%s\nDeleting token file.' % error
    my_auth_helper.DeleteAuthToken()
    sys.exit(1)

  PrintFeed(feed)


def GetDataFeedQuery(table_id, start_date, end_date):
  """Returns a Data Export API query object.

  The query specifies the top traffic sources by visits to the site.

  Args:
    table_id: string The table id from which to retrieve data.
        Format is ga:xxxxxx, where xxxxxx is the profile ID.
    start_date: string The beginning of the date range. Format YYYY-MM-DD.
    end_date: string The end og the date range. Format YYYY-MM-DD.

  Returns:
    A new gdata.analytics.client.DataFeedQuery object.
  """
  return gdata.analytics.client.DataFeedQuery({
      'ids': table_id,
      'start-date': start_date,
      'end-date': end_date,
      'dimensions': 'ga:source',
      'metrics': 'ga:visits',
      'sort': '-ga:visits',
      'max-results': '100'})


def PrintFeed(feed):
  """Outputs rows of data retrieved from the Data Export API.

  Args:
    feed: gdata.analytics.data.DataFeed The response from the Google Analytics
        Data Export API.
  """
  if feed.entry:
    row = []
    for dim in feed.entry[0].dimension:
      row.append(dim.name)
    for met in feed.entry[0].metric:
      row.append(met.name)
    print '\t'.join(row)

  for entry in feed.entry:
    row = []
    for dim in entry.dimension:
      row.append(dim.value)
    for met in entry.metric:
      row.append(met.value)
    print '\t'.join(row)


if __name__ == '__main__':
  main()

