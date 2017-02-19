#! /usr/bin/python2
# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
from optparse import OptionParser
from redditclient import RedditClient
from inspector import Inspector
from capturer import Capturer
from database import Database
from logger import Logger
from datetime import datetime
import json
import re

config = ConfigParser()
config.read("capture_bot.cfg")
options = {}
options.update({ "version": config.get("Generic", "version" )})
options.update({ "verbose": config.getboolean("Generic", "verbose") })
options.update({ "persist_parsed_threads": config.getboolean("Generic", "persist_parsed_threads") })
options.update({ "watched_subreddits": json.loads(config.get("Capture", "watched_subreddits")) })
options.update({ "captured_domain_names": json.loads(config.get("Capture", "captured_domain_names")) })
options.update({ "dump_directory": config.get("Capture", "dump_directory") })

arguments = OptionParser()
arguments.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Verbose mode")
arguments.add_option("-p", "--persist", action="store_true", dest="persist_parsed_threads", help="Persist parsed threads")
# merge with ConfigParser but let OptionParser win
arguments.set_defaults(**options)
options = arguments.parse_args()[0]

logger = Logger(options.verbose)
reddit = RedditClient()
capturer = Capturer()
inspector = Inspector(logger)
database = Database()

print datetime.now().strftime("Started at %Y-%m-%d %H:%M:%S.")

# fetch the latest reddit posts and comments of given subreddits
reddit.fetch_posts(options.watched_subreddits)
posts = reddit.get_posts()

# loop through all results and check for links of the given domains
for post in posts:
    if database.element_exists(post):
        logger.write_console("Element %s already parsed" % (post["id"]))
        continue
    else:
        logger.write_console("Element %s NOW parsed" % (post["id"]))
        if options.persist_parsed_threads:
            database.store_element(post)

    urls = inspector.find_domain_urls(post, options.captured_domain_names)

    # capture all urls containing the domain name
    for url in urls:
        # sanitize the url, to use it as a filename
        filename = re.sub("[^0-9a-zA-Z]", "-", url)
        capturer.capture(url, "%s/%s.png" % (options.dump_directory, filename))

print datetime.now().strftime("Ended at %Y-%m-%d %H:%M:%S.")
