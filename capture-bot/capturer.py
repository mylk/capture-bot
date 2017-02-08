from PyQt4.QtCore import QUrl, QSize
from PyQt4.QtGui import QApplication, QImage, QPainter
from PyQt4.QtWebKit import QWebView
import time

class Capturer():
    def __init__(self):
        self.app = QApplication([])

    def capture(self, url, output_file):
        self.loaded = False

        web_view = QWebView()
        # get the page's main frame
        frame = web_view.page().mainFrame()
        # add event to happen when page finishes loading
        frame.loadFinished.connect(self.loadFinished)

        # load the url and wait till its loaded
        web_view.load(QUrl(url))
        self.wait_load(1)

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
            self.app.processEvents()
            time.sleep(delay)

    def loadFinished(self, result):
        self.loaded = True
