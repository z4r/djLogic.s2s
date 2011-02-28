from celery.task import Task
from smtplib import SMTP
from email.MIMEBase import MIMEBase
from email import Encoders
from django.conf import settings

class PublishTask(Task):
    def run(self, user, s2s_data, click_id, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Running Publish for: %s" % user)
        s2s_data.data = s2s_data.data.replace('#UC#', click_id)
        try:
            logger.info("[SMTP] Connecting")
            logger.debug("[SMTP] Connecting @ %s:%s" % (settings.SMTP_HOST, settings.SMTP_PORT))
            server = SMTP(host = settings.SMTP_HOST, port = settings.SMTP_PORT)
            logger.info("[SMTP] Authenticating")
            logger.debug("[SMTP] Authenticating @ %s:%s" % (settings.SMTP_USER, settings.SMTP_PASS))
            server.login(user = settings.SMTP_USER, password = settings.SMTP_PASS)
            notify_from = "%s@%s" % (settings.SMTP_SENDER, settings.SMTP_DOMAIN)
            notify_rcpt = "%s@%s" % (user, settings.SMTP_DOMAIN)
            message = MIMEBase('text', 'plain')
            message.set_payload(s2s_data.data)
            Encoders.encode_base64(message)
            message['From']                      = notify_from
            message['To']                        = notify_rcpt
            message['Subject']                   = settings.SMTP_SUBJECT
            message['Message-ID']                = kwargs['task_id']
            message['X-Dada-MMS-GW-Servicecode'] = settings.SMTP_SERVICE_CODE
            message['X-DADA-S2S-REMOTE-METHOD']  = s2s_data.method
            message['X-DADA-S2S-REMOTE-URL']     = s2s_data.url
            message['X-DADA-S2S-REMOTE-CC']      = s2s_data.content_type
            logger.info("[SMTP] Sending Mail")
            for line in message.as_string().splitlines():
                logger.info("... %s" % line)
            server.sendmail(notify_from, notify_rcpt, message.as_string())
            logger.info("[SMTP] Quitting")
            server.quit()
            return 'OK'
        except Exception as e:
            logger.error("[SMTP] %s" % e)
            return 'KO'
            #retry
