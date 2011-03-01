from django.http import HttpResponse
from tools import S2SFactory,get_data
from tasks import PublishTask
from sender import SMTPSender, MockSender
from message import MIMEBase64, DictMessage 
from config import settings

def publish(request, partner_id, click_id, **kwargs):
    check = kwargs.get('check', False)
    logger = S2SFactory.get_logger()
    s2s_data = get_data(partner_id=partner_id,logger=logger,settings=settings)
    if not s2s_data:
        logger.info('PARTNER [%s] INFO NOT FOUND' % partner_id)
        return HttpResponse('KO')
    if check:
        task_id = PublishTask.delay(partner_id, s2s_data, click_id, MockSender, DictMessage, settings)
        logger.info('CHECK QUEUED [%s]' % task_id)
        task_id.wait(interval=0.1)
        logger.info('CHECK RESULT [%s]: %s' % (task_id, task_id.result))
        return HttpResponse(task_id.result)
    else:
        task_id = PublishTask.delay(partner_id, s2s_data, click_id, SMTPSender, MIMEBase64, settings)
        logger.info('NOTIFICATION QUEUED %s' % (task_id))
        return HttpResponse(task_id,status=202)
