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
#   Accesses the Account Feed of the Google Analytics Management API through
#   cURL.
#
# Usage:
#   You will need to run the getAuthToken.sh script to get the proper
#   authorization token to access your data.

authToken=`cat .testAuthToken`

feedUri="https://www.google.com\
/analytics/feeds/datasources/ga/accounts\
?prettyprint=true"

echo "Using query: $feedUri"

curl $feedUri --silent \
  --header "Authorization: GoogleLogin auth=$authToken"

