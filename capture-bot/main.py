#! /usr/bin/python2
# -*- coding: utf-8 -*-

from redditclient import RedditClient
from inspector import Inspector
from capturer import Capturer
from datetime import datetime
import re

reddit = RedditClient()
capturer = Capturer()
inspector = Inspector()

print datetime.now().strftime("Started at %Y-%m-%d %H:%M:%S.")

# fetch the latest reddit posts and comments of given subreddit
reddit.fetch_posts("greece")
posts = reddit.get_posts()

# loop through all results and check for links of the given domain
for post in posts:
    urls = inspector.find_domain_urls(post, "reddit.com")

    # capture all urls containing the domain name
    for url in urls:
        print "Capturing: %s" % (url)

        # sanitize the url, to use it as a filename
        filename = re.sub("[^0-9a-zA-Z]", "-", url)
        capturer.capture(url, "/tmp/%s.png" % (filename))

print datetime.now().strftime("Ended at %Y-%m-%d %H:%M:%S.")
