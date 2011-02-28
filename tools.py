import logging
from django.conf import settings
import os.path
import json
from urlparse import urlsplit

class S2SData(object):
    def __init__(self, data, url, method, content_type):
        self.data         = data
        self.url          = url
        self.method       = method
        self.content_type = content_type

class S2SFactory(object):
    logger = None
    def get_logger(cls):
        if cls.logger is None:
            class NullHandler(logging.Handler):
                def emit(self, record):
                    pass

            cls.logger = logging.getLogger('s2s')
            cls.logger.addHandler(NullHandler())

        return cls.logger
    get_logger = classmethod(get_logger)

def get_data(partner_id):
    (country, campain, flight, creativity) = partner_id.split("_")
    input_data = {
        'country'    : country,
        'campain'    : campain,
        'flight'     : flight,
        'creativity' : creativity,
    }
    for template in ( settings.CAMPAIN_TEMPLATE_CRT,
                      settings.CAMPAIN_TEMPLATE_FLT,
                      settings.CAMPAIN_TEMPLATE_CMP, ):
        file_name = template % input_data
        if os.path.exists.(file_name) and os.path.isfile(file_name):
            fh = open(file_name, 'r')
            content = fh.read()
            try:
                raw_data = json.loads(content)
                url = raw_data['url']
                tt  = raw_data['track_type']
            except KeyValue:
                return None
    return None

def rd2d(track_type, url):
    if track_type = 1:
        o = urlsplit(url)
        return S2SData(
            data   = o.query,
            url    = o.scheme + '://' + o.netloc + o.path,
            method = 'GET',
            content_type = '',
        )
