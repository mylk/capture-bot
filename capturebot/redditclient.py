import praw
import time

class RedditClient:
    options = {}
    posts = []
    ELEMENT_TYPE_POST = 1
    ELEMENT_TYPE_COMMENT = 2
    REPLY_WAIT_MINUTES_MAX = 10

    def __init__(self, options):
        self.options = options

    def fetch_posts(self, subreddit):
        self.request_posts(subreddit)

    def request_posts(self, subreddits):
        reddit = praw.Reddit(
            client_id=self.options.reddit_id,
            client_secret=self.options.reddit_secret,
            username=self.options.reddit_username,
            password=self.options.reddit_password,
            user_agent="ACaptureBot/%s by mylk" % (self.options.version)
        )

        for subreddit in subreddits:
            subreddit = reddit.subreddit(subreddit)

            posts = subreddit.new(limit=100)
            for post in posts:
                self.add_post(post)

                for comment in post.comments:
                    self.add_post(comment)

    def add_post(self, element):
        element_type = type(element).__name__

        if element_type == "Submission":
            element.element_type = self.ELEMENT_TYPE_POST
        elif element_type == "Comment":
            element.element_type = self.ELEMENT_TYPE_COMMENT
        elif element_type == "MoreComments":
            return

        if element.edited:
            element.created_utc = element.edited

        self.posts.append(element)

    def get_posts(self):
        return self.posts

    def post_comment(self, element, image_url):
        wait_minutes = 1
        while wait_minutes < self.REPLY_WAIT_MINUTES_MAX:
            try:
                element.reply(self.options.reddit_comment_text % (image_url))
                break
            except praw.exceptions.APIException:
                time.sleep(60 * wait_minutes)
                wait_minutes += 1
