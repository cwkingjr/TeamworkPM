#!/usr/bin/env python

# Author: Chuck King; based on script by Michelle Ward

# License GPLv2

# Pulls Teamwork PM statuses to see who posted this week.
# Expectation is that everyone updated their status between Mon-Thur.
# Run on Friday 
# Currently drops a year-weekofyear file of posting status in the 
# execution script folder. This is a design choice so folks can run 
# the script more than once per week if desired to see current status
# or rerun in case of some error without a single polluted master file.

import base64
from datetime import datetime, date, timedelta
import json
import os
import sys
import urllib2

if __name__ == "__main__":

    # Set to False normally
    # Setting to True allows the script to run when it's not Friday
    testing = False

    # set these in your .bashrc file and reload/source it after changes 
    # export TEAMWORKPM_SUBDOMAIN=mysubdomain
    # export TEAMWORKPM_API_KEY=myapikey
    # . ~/.bashrc
    subdomain = os.environ['TEAMWORKPM_SUBDOMAIN'] 
    key = os.environ['TEAMWORKPM_API_KEY'] 

    # Verify URL via browser
    status_url = "https://%s.teamworkpm.net/people/status.json" % subdomain

    # expects today to be Friday
    today = date.today()
    monday = today - timedelta(days=4)
    thursday = today - timedelta(days=1)

    # Determine year, week number, and day of week number
    # isocalendar tuple offsets for code readability
    YEAR, WEEK, DAY = (0,1,2)
    year = today.isocalendar()[YEAR] 
    week = today.isocalendar()[WEEK] 
    week = "%2s" % week # ensure two digit week
    day  = today.isocalendar()[DAY] 

    print "Using this info to make posting/filemane decisions"
    print "Last Monday (4 days ago): %s" % monday
    print "Last Thursday (1 day ago): %s" % thursday
    print "Current year: %s" % year
    print "Current week number (00-52): %2s" % week
    print "Current day of week number: %s (should be 5 for Friday)" % day

    if int(day) != 5:
        if testing:
            print "Warning: Today doesn't appear to be Friday so your readings will be wrong!"
        else:
            print "ERROR: Script must be run on Friday"
            sys.exit(1)

    posts = {} 

    request = urllib2.Request(status_url)
    request.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    response = urllib2.urlopen(request)
    statuses = json.loads(response.read())

    for person in statuses['userStatuses']:

        name = "%s.%s" % (person['first-name'], person['last-name'])

        # date string provided is in this format: 2015-05-08T15:15:55Z
        last_updated_str = person['last-changed-on']
        # convert date string to datetime object
        last_updated = datetime.strptime(last_updated_str, "%Y-%m-%dT%H:%M:%SZ")
        # get only date for comparison
        last_updated_day = last_updated.date()

        posts[name] = {}
        posts[name]['last_posted'] = last_updated_day.isoformat()
        if monday <= last_updated_day <= thursday:
            posts[name]['posted'] = 'Yes'
        else:
            posts[name]['posted'] = 'No'

    myfilename = "%s-%s-posted-status-results-%s.txt" % (year, week, today.isoformat())
    with open(myfilename, 'w') as f:
        f.write("#year week name posted_this_week last_posted\n")
        for name in sorted(posts):
            posted = posts[name]['posted']
            last_posted = posts[name]['last_posted']
            msg = "%4s %2s %s %s %s\n" % (year, week, name, posted, last_posted)
            f.write(msg)
