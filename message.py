class AbstractMessageHandler(object):
    def __init__(self, content):
        raise NotImplementedError

    def add_header(self, key, value):
        raise NotImplementedError

from email.MIMEBase import MIMEBase
from email import Encoders
class MIMEBase64(AbstractMessageHandler):
    def __init__(self, content):
        self.message = MIMEBase('text', 'plain')
        self.message.set_payload(content)
        Encoders.encode_base64(self.message)

    def add_header(self, key, value):
        self.message[key] = value

    def __str__(self):
        return self.message.as_string()

class DictMessage(AbstractMessageHandler):
    def __init__(self, content):
        self.message = { 
            'content' : content,
            'headers' : {},
        }

    def add_header(self, key, value):
        self.message['headers'][key] = value

    def __str__(self):
        string = "Content: %s\n" % self.message['content']
        for k,v in self.message['headers'].iteritems():
            string += "%s: %s\n" % (k,v)
        return string
        return "%s" % self.message
