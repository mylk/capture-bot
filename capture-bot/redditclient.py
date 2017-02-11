import urllib2
import json

class RedditClient:
    posts = []

    def fetch_posts(self, subreddit):
        self.request_posts(subreddit)

    def request_posts(self, subreddits):
        for subreddit in subreddits:
            try:
                # request posts and comments of subreddit
                posts_url = "https://www.reddit.com/r/%s/new/.json" % (subreddit)
                request = urllib2.Request(posts_url, headers={ "User-Agent": "Mozilla/5.0" })
                response = urllib2.urlopen(request).read()

                data = json.loads(response)
                # loop through all posts
                for post in data["data"]["children"]:
                    post = post["data"]

                    # keep post content for examination
                    self.add_post(self.ELEMENT_TYPE_POST, post)

                    # fetch post comments also, if any
                    if post["num_comments"]:
                        self.request_comments(post)
            except urllib2.HTTPError, e:
                print "Error code %s calling %s" % (e.code, "url")
                exit(1)

    def request_comments(self, post):
        try:
            comments_url = "https://www.reddit.com%s.json" % (post["permalink"])
            request = urllib2.Request(comments_url.encode("UTF-8"), headers={ "User-Agent": "Mozilla/5.0" })
            response = urllib2.urlopen(request).read()

            data = json.loads(response)
            # get comments and comments of comments
            self.parse_replies(data)
        except urllib2.HTTPError, e:
            print "Error code %s calling %s" % (e.code, "url")
            exit(1)

    def parse_replies(self, data):
        # loop through all comments
        for comment in data[1]["data"]["children"]:
            comment = comment["data"]

            if "body" in comment:
                self.add_post(2, comment["id"], comment["body"])

            # recurse for comments of comment
            if "replies" in comment:
                if comment["replies"]:
                    # format the input to make it look like post comments and simplify code
                    self.parse_replies([{}, comment["replies"]])

    def add_post(self, element_type, id, body):
        self.posts.append({ "type": element_type, "id": id, "body": body })

    def get_posts(self):
        return self.posts
