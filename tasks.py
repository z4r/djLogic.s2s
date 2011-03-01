from celery.task import Task

class PublishTask(Task):
    def run(self, partner_id, s2s_data, click_id, sender, message_builder, settings, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Running Publish for: %s" % partner_id)
        s2s_data.data = s2s_data.data.replace(settings.CAMPAIN_PLACE_HOLDER, click_id)
        sender = sender() 
        try:
            logger.info("[SMTP] Connecting")
            logger.debug("[SMTP] Connecting @ %s:%s" % (settings.SMTP_HOST, settings.SMTP_PORT))
            sender.connect(host = settings.SMTP_HOST, port = settings.SMTP_PORT)
            if settings.SMTP_LOGIN_REQUIRED:
                logger.info("[SMTP] Authenticating")
                logger.debug("[SMTP] Authenticating @ %s:%s" % (settings.SMTP_USER, settings.SMTP_PASS))
                sender.login(user = settings.SMTP_USER, password = settings.SMTP_PASS)
            notify_from = "%s@%s" % (settings.SMTP_SENDER, settings.SMTP_DOMAIN)
            notify_rcpt = "%s@%s" % (partner_id, settings.SMTP_DOMAIN)
            message = message_builder(s2s_data.data)
            message.add_header('From', notify_from)
            message.add_header('To', notify_rcpt)
            message.add_header('Subject', settings.SMTP_SUBJECT)
            message.add_header('Message-ID', kwargs['task_id'])
            message.add_header('X-Dada-MMS-GW-Servicecode', settings.SMTP_SERVICE_CODE)
            message.add_header('X-DADA-S2S-REMOTE-METHOD', s2s_data.method)
            message.add_header('X-DADA-S2S-REMOTE-URL', s2s_data.url)
            message.add_header('X-DADA-S2S-REMOTE-CC', s2s_data.content_type)
            logger.info("[SMTP] Sending Mail")
            for line in str(message).splitlines():
                logger.info("... %s" % line)
            sender.send(notify_from, notify_rcpt, str(message))
            logger.info("[SMTP] Quitting")
            sender.quit()
            return 'OK'
        except Exception as e:
            logger.error("[SMTP] %s" % e)
            return 'KO'
            #retry
