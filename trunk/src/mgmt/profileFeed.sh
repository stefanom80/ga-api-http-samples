#!/bin/bash
#
# Copyright 2010 Google Inc. All Rights Reserved
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Overview:
#   Accesses the Profile Feed of the Google Analytics Management API through
#   cURL. Users are prompted to input their Accounts and Web Property IDs to
#   narrow the response. The default for not specifiying an ID will return all
#   values the authorized user has access to.
#
# Usage:
#   You will need to run the getAuthToken.sh script to get the proper
#   authorization token to access your data.

authToken=`cat .testAuthToken`

read -p "Please enter an Account ID (default will use ~all): " account_id
if [ -z "$account_id" ] || [ "$account_id" == "~all" ]; then
  account_id="~all"
  web_property_id="~all"
else
  read -p "Please enter a Web Property ID (default will use ~all): " web_property_id
  if [ -z "$web_property_id" ] || [ "$web_property_id" == "~all" ]; then
    web_property_id="~all"
  fi
fi

feedUri="https://www.google.com\
/analytics/feeds/datasources/ga/accounts/$account_id/webproperties/$web_property_id/profiles\
?prettyprint=true"

echo "Using query: $feedUri"

curl $feedUri --silent \
  --header "Authorization: GoogleLogin auth=$authToken"

