from PyQt4.QtCore import QUrl, QSize
from PyQt4.QtGui import QApplication, QImage, QPainter
from PyQt4.QtWebKit import QWebView
import time

class Capturer():
    PAGE_LOAD_SECONDS_MAX = 20
    page_load_seconds_waited = 0

    def __init__(self):
        self.app = QApplication([])

    def capture(self, url, output_file):
        self.page_load_seconds_waited = 0
        self.loaded = False

        web_view = QWebView()
        # get the page's main frame
        frame = web_view.page().mainFrame()
        # add event to happen when page finishes loading
        frame.loadFinished.connect(self.loadFinished)

        # load the url and wait till its loaded
        web_view.load(QUrl(url))
        try:
            self.wait_load(1)
        except Exception as ex:
            print ex
            return

        # set viewport size
        web_view.page().setViewportSize(QSize(1280, frame.contentsSize().height()))

        # render image
        image = QImage(web_view.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        image.save(output_file)

    def wait_load(self, delay = 0):
        while not self.loaded:
            if self.page_load_seconds_waited > self.PAGE_LOAD_SECONDS_MAX:
                raise Exception("Page didn't load in a timely manner")

            self.app.processEvents()

            time.sleep(delay)
            self.page_load_seconds_waited += delay

    def loadFinished(self, result):
        self.loaded = True
