import logging

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

    """
    partners = {
        partner_id : {
            data_instance : <S2SData instance>
            file_hash     : <last_hash>
        }
    }
    """
    partners = {}
    def get_data(cls, partner_id):
        """ 
        Initializes and returns a receiver instance.
        """
        try:
            last_hash = cls.partners[partner_id]['last_hash']
            #verifica hash
            #if update data_instance/file_hash
        except KeyError:
            #leggi file
            #update receiver/hash
            cls.partners[partner_id] = {
                'data_instance' : S2SData('us=#UC#', 'GET', 'www.partner.net', ''),
                'last_hash'     : '1234',
            }
        return cls.partners[partner_id]['data_instance'] 
    get_data = classmethod(get_data)
