from django.http import HttpResponse
from tools import S2SFactory
from tasks import PublishTask


def publish(request, user, partner_id, click_id):
    logger = S2SFactory.get_logger()
    s2s_data = S2SFactory.get_data(partner_id)
    if not s2s_data:
        logger.info('[%s] PARTNER INFO NOT FOUND %s' % (user, partner_id))
        return HttpResponse('KO')
    else:
        task_id = PublishTask.delay(user, s2s_data, click_id)
        logger.info('[%s] NOTIFICATION QUEUED %s' % (user, task_id))
        return HttpResponse(task_id,status=202)
