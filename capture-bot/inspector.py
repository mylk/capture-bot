import re

class Inspector:
    def find_domain_urls(self, post, domains):
        results = []

        # find all urls in the post / comment body
        urls_body = re.findall("(?P<url>https?://[^\s\)]+)", post["body"])
        url_title = re.findall("(?P<url>https?://[^\s\)]+)", post["url"])
        urls = urls_body + url_title

        for domain in domains:
            # in the urls found, search for those that contain the domain name given
            for url in urls:
                if domain in url:
                    results.append(url)

        return results
