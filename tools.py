import logging
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

def get_data(partner_id, settings, logger=None):
    if not logger:
        logger = S2SFactory.get_logger()
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
        logger.debug("%s is a file: %s" % (file_name, os.path.isfile(file_name)))
        if os.path.isfile(file_name):
            fh = open(file_name, 'r')
            content = fh.read()
            fh.close()
            try:
                raw_data = json.loads(content)
                url = raw_data['url']
                tt  = raw_data['track_type']
                return rd2d(tt, url)
            except KeyValue as e:
                logger.error("Bad Format: %s" % file_name)
                return None
    logger.error('File NOT found for: %s:' % partner_id)
    return None

def rd2d(track_type, url):
    if track_type == 1:
        o = urlsplit(url)
        return S2SData(
            data   = o.query,
            url    = o.scheme + '://' + o.netloc + o.path,
            method = 'GET',
            content_type = '',
        )
