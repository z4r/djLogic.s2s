class settings(object):
    SMTP_HOST           = "localhost"
    SMTP_PORT           = 25
    SMTP_LOGIN_REQUIRED = False
    SMTP_DOMAIN         = 's2s.test.net'
    SMTP_SENDER         = 'djLogic'
    SMTP_SUBJECT        = 'S2SNotification'
    SMTP_SERVICE_CODE   = 's2s'
    
    CAMPAIN_TEMPLATE_CRT = '/home/z4r/Scrivania/pyTest/%(country)s/s2s/crt_%(creativity)s.json'
    CAMPAIN_TEMPLATE_FLT = '/home/z4r/Scrivania/pyTest/%(country)s/s2s/flt_%(flight)s.json'
    CAMPAIN_TEMPLATE_CMP = '/home/z4r/Scrivania/pyTest/%(country)s/s2s/cmp_%(campain)s.json'
    CAMPAIN_PLACE_HOLDER = '[UC]'

