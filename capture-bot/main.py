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

arguments = OptionParser()
arguments.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose mode")
options = arguments.parse_args()[0]

config = ConfigParser()
config.read("capture_bot.cfg")
subreddits = json.loads(config.get("Default", "subreddits"))
domain_names = json.loads(config.get("Default", "domain_names"))

logger = Logger(options.verbose)
reddit = RedditClient()
capturer = Capturer()
inspector = Inspector(logger)
database = Database()

print datetime.now().strftime("Started at %Y-%m-%d %H:%M:%S.")

# fetch the latest reddit posts and comments of given subreddits
reddit.fetch_posts(subreddits)
posts = reddit.get_posts()

# loop through all results and check for links of the given domains
for post in posts:
    if database.element_exists(post):
        logger.write_console("Element %s already parsed" % (post["id"]))
        continue
    else:
        logger.write_console("Element %s WASN't parsed" % (post["id"]))
        database.store_element(post)

    urls = inspector.find_domain_urls(post, domain_names)

    # capture all urls containing the domain name
    for url in urls:
        # sanitize the url, to use it as a filename
        filename = re.sub("[^0-9a-zA-Z]", "-", url)
        capturer.capture(url, "/tmp/%s.png" % (filename))

print datetime.now().strftime("Ended at %Y-%m-%d %H:%M:%S.")
