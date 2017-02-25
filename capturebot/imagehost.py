from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

class ImageHost():
    options = {}

    def __init__(self, options):
        self.options = options

    def image_upload(self, image_path):
        client = ImgurClient(self.options.image_host_id, self.options.image_host_secret)

        try:
            return client.upload_from_path(image_path, config=None, anon=False)
        except IOError as e:
            print "ImageHost: I/O error - %s (%d)" % (e.strerror, e.errno)
        except ImgurClientError as e:
            print "ImageHost: Imgur error - %s (%d)" (e.error_message, e.status_code)
        except:
            print "ImageHost: Unknown error"
        else:
            return None