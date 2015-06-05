#!/usr/bin/env python

# author = Chuck King

# future imports must start at beginning of file
from __future__ import print_function
from datetime import datetime, date
import glob
import logging, logging.handlers
import sys
import optparse
import os
import re

class Person(object):
    """Data access object for post info"""
    def __init__(self, name):
        self.name = name
        self.posts_count = 0
        self.posts_in_window = 0

def main():

    LOG_FILENAME = 'log-teamwork-status-stats.log'

    global options, args
    (options, args) = process_options()

    global posters 
    posters = {}

    ########### 
    ##  Logger set up

    # Set up local stdin and file log destinations
    logger = logging.getLogger(LOG_FILENAME)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1000000, backupCount=10)
    # We'll leave the info logged to file at debug and alter the command line based upon cli options
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    if options.debug:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)
    # create formatters and add them to the handlers
    # you can use the same one but I didn't want the datetime on the console
    chformatter = logging.Formatter('%(levelname)-8s %(message)s')
    fhformatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(chformatter)
    fh.setFormatter(fhformatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    ##
    ##########

    logger.debug("=================================================================================")
    logger.debug("========================== STARTING NEW SCRIPT RUN ==============================")
    logger.debug("=================================================================================")


    logger.info("Check the log file at %s for debug-level logging info" % LOG_FILENAME)
    logger.info("Using start of %s and end of %s" % (options.start, options.end))

    if options.output:
        outfile = "output-status-stats-%s" % datetime.now().isoformat()
        o = open(outfile, 'w')
        logger.info("Writing results to %s" % outfile)
        o.write("# Using start of %s and end of %s\n" % (options.start, options.end))

    mystart = options.start.replace('-','.')
    myend = options.end.replace('-','.')

    processed_file_count = 0
    # grab the possible files to process
    for myfile in glob.iglob('*-posted-status-results*'):
        #print(myfile)
        # make sure the file is within the date ranges
        # grab the fist seven chars
        datepart = myfile[:7]
        # format as float so we can use simple math comparison later
        datepart = datepart.replace('-','.')

        # if not in range, skip it
        if mystart <= datepart <= myend:
            processed_file_count += 1
            load_status_file(myfile)

    # raw numbers
    logger.debug("Individual Raw Numbers")
    for myperson in sorted(posters):
        logger.debug("Name: %s, Posts: %s, Posts In Window: %s" % \
        (posters[myperson].name, \
        posters[myperson].posts_count, \
        posters[myperson].posts_in_window))

    # individual stats
    logger.info("Individual Posts-In-Window Percentages")
    if options.output:
        o.write("# Individual Posts-In-Window Percentages\n")
    for myperson in sorted(posters):
        (name,posts_count,posts_in_window) = \
        (posters[myperson].name, \
        posters[myperson].posts_count, \
        posters[myperson].posts_in_window)

        # coerce python to create percentages with floats
        percentage = float(posts_in_window) / float(posts_count) * 100

        logger.info("%s %2.2f" % (name, percentage))
        if options.output:
            o.write("%s %2.2f\n" % (name, percentage))

    # Aggregate stats
    agg_posts_count = 0
    agg_posts_in_window = 0
    for myperson in posters:
        (posts_count,posts_in_window) = (posters[myperson].posts_count, posters[myperson].posts_in_window)

        agg_posts_count += posts_count 
        agg_posts_in_window += posts_in_window

    # coerce python to create percentages with floats
    percentage = float(agg_posts_in_window) / float(agg_posts_count) * 100
    logger.info("Aggragate Posts-In-Window Percentage: %2.2f" % percentage)
    if options.output:
        o.write("# Aggragate Posts-In-Window Percentage: %2.2f" % percentage)

    logger.info("Processed %s status files matching your start/end criteria" % processed_file_count)

def load_status_file(filename):
    """load info from status file into python data objects"""

    global posters

    with open(filename, 'r') as f:
        for myline in f.readlines():

            if myline.startswith('#'):
                continue

            (year,week,name,posted,last_posted) = myline.split()

            if not name in posters:
                posters[name] = Person(name=name)

            posters[name].posts_count += 1

            if posted == 'Yes':
                posters[name].posts_in_window += 1


def process_options():
    """ process commandline options """
    usage = """usage: ./%prog [options]
    use -h for help / option descriptions 
    """

    parser = optparse.OptionParser(usage)
    parser.add_option("-s", "--start", dest="start", help="""Enter the starting year and two digit week-of-year number in YYYY-WW format. Examples: -s 2015-08 or --start=2015-08. Default is current year, week 00.""")
    parser.add_option("-e", "--end", dest="end", help="""Enter the ending year and two digit week-of-year number in YYYY-WW format. Examples: -e 2015-45 or --end=2015-45. Default is current year, week 52.""")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="""Optional.  Dump debug (vice info) output to the command line interface.  Debug-level output is automatically logged to rotating log files and is far easier to review there.""")
    parser.add_option("-o", "--output", action="store_true", dest="output", help="""Optional. This option will create a local file with the status results based on your parameters. This info will automatically be in the log file and pushed to the terminal, but this option allows you to get a clean (non-logging) output.""")

    (options, args) = parser.parse_args()

    if options.start:
        if not re.match('\d{4}-\d{2}', options.start):
            print('-s parameter :%s: does not match required format' % options.start)
            sys.exit(1)
    else:
        # Use current year and 00 week
        options.start = "%s-00" % date.today().year

    if options.end:
        if not re.match('\d{4}-\d{2}', options.end):
            print('-e parameter does not match required format')
            sys.exit(1)
    else:
        # Use current year and 52 week
        options.end = "%s-52" % date.today().year

    return (options, args)

if __name__ == "__main__":
    main()
