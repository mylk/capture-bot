from HTMLParser import HTMLParser
from selenium import webdriver

class Capturer():
    def capture(self, url, output_file):
        parser = HTMLParser()
        url = parser.unescape(url)

        print "Capturing: %s" % (url)

        driver = webdriver.PhantomJS()
        driver.set_window_size(1280, 1024)
        driver.get(url)
        driver.save_screenshot(output_file)
