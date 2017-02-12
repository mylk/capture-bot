#! /usr/bin/python2
# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
from redditclient import RedditClient
from inspector import Inspector
from capturer import Capturer
from database import Database
from datetime import datetime
import json
import re


config = ConfigParser()
config.read("capture_bot.cfg")
subreddits = json.loads(config.get("Default", "subreddits"))
domain_names = json.loads(config.get("Default", "domain_names"))

reddit = RedditClient()
capturer = Capturer()
inspector = Inspector()
database = Database()

print datetime.now().strftime("Started at %Y-%m-%d %H:%M:%S.")

# fetch the latest reddit posts and comments of given subreddits
reddit.fetch_posts(subreddits)
posts = reddit.get_posts()

# loop through all results and check for links of the given domains
for post in posts:
    if database.element_exists(post):
        continue
    else:
        database.store_element(post)

    urls = inspector.find_domain_urls(post, domain_names)

    # capture all urls containing the domain name
    for url in urls:
        # sanitize the url, to use it as a filename
        filename = re.sub("[^0-9a-zA-Z]", "-", url)
        capturer.capture(url, "/tmp/%s.png" % (filename))

print datetime.now().strftime("Ended at %Y-%m-%d %H:%M:%S.")
