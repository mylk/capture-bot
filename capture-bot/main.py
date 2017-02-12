#! /usr/bin/python2
# -*- coding: utf-8 -*-

from redditclient import RedditClient
from inspector import Inspector
from capturer import Capturer
from database import Database
from datetime import datetime
import re

# read the domain names to be captured
domain_names_file = open("domain_names", "r")
domain_names = domain_names_file.read().split("\n")

# read the subreddits to be monitored
subreddits_file = open("subreddits", "r")
subreddits = subreddits_file.read().split("\n")

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
