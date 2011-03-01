class AbstractSender(object):
    def __init__(self):
        raise NotImplementedError

    def connect(self, host, port):
        raise NotImplementedError

    def login(self, user, password):
        raise NotImplementedError

    def send(self, sender, rcpt, message):
        raise NotImplementedError

    def quit(self):
        raise NotImplementedError

from smtplib import SMTP
class SMTPSender(AbstractSender):
    def __init__(self):
        self.server = SMTP()

    def connect(self, host, port):
        self.server.connect(host = host, port = port)
 
    def login(self, user, password):
        self.server.login(user = user, password = password)

    def send(self, sender, rcpt, message):
        self.server.sendmail(sender, rcpt, message)

    def quit(self):
        self.server.quit()

class MockSender(AbstractSender):
    def __init__(self):
        pass

    def connect(self, host, port):
        pass

    def login(self, user, password):
        pass

    def send(self, sender, rcpt, message):
        pass

    def quit(self):
        pass
