#!/bin/bash

# Get google account credentials. 
echo 'Please enter your google account credentials :'
echo -n 'Email: '
read username
echo -n 'Password:'
read -s password

# Export required environment variable.
export SLACK_WEBHOOK='https://hooks.slack.com/services/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'
export GOOGLE_USERNAME=$username
export GOOGLE_PASSWORD=$password

# Configure virtualenv.
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
