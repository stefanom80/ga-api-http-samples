#!/bin/bash
#
# Copyright 2009 Google Inc. All Rights Reserved
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
# Access the Account Feed of the GA Data Export API through cURL

USER_EMAIL="" #Insert your Google Account email here
USER_PASS="" #Insert your password here

googleAuth="$(curl https://www.google.com/accounts/ClientLogin -s \
  -d Email=$USER_EMAIL \
  -d Passwd=$USER_PASS \
  -d accountType=GOOGLE \
  -d source=curl-accountFeed-v1 \
  -d service=analytics \
  | awk /Auth=.*/)"

feedUri="https://www.google.com/analytics/feeds/accounts/default\
?prettyprint=true"

curl $feedUri -s --header "Authorization: GoogleLogin $googleAuth"
