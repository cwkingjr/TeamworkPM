#!/usr/bin/env python

# author = Chuck King

import logging, logging.handlers
import sys
import optparse
import os

class Netblock(object):
    """Holds network address block, cidr mask, and pmap name/description info"""
    def __init__(self, startAddress, cidr, pmapName=None, pmapShortName=None):
        self.startAddress = startAddress
        self.cidr = cidr
        self.pmapName = pmapName
        self.pmapShortName = pmapShortName
        
    def getStartAddress(self):
        return self.startAddress

def main():

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

    global options, args
    (options, args) = processOptions()



def processOptions():
    """ process commandline options """
    usage = """usage: ./%prog [options]
    use -h for help / option descriptions 
    """

    parser = optparse.OptionParser(usage)
    parser.add_option("-c", "--pmap-concat", dest="pmapconcat", help="""Allows default pmap name concatenation string of ' - ' to be overridden.  A node's pmap name is derived from a reversed concatenation of the node's non-empty long name and each ancestor node's non-empty long name, separated by this concatenation string.  E.g., Grandparent - Parent - Child""")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="""Optional.  Dump debug (vice info) output to the command line interface.  Debug-level output is automatically logged to rotating log files and is far easier to review there.""")
    parser.add_option("-f", "--print-file-names", action="store_true", dest="printfilenames", help="""Optional.  Print the names of files that would be created (truncates if set-level option provided).  This is meant for use to check your setter-context file configuration.  When used, setter will terminate before creating the real files.""")
    parser.add_option("-i", "--in-file", dest="settxtfile", help="""Setter text file to process. Default is ~/setter-content.txt.""")

    (options, args) = parser.parse_args()

    if options.version:
        sys.stdout.write("Script version: %s\n" % (version))
        sys.exit(1)

    return (options, args)

if __name__ == "__main__":
    main()
