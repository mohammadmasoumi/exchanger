# import logging
#
# from celery.signals import task_prerun, task_postrun
#
# logger = logging.getLogger(__name__)
#
#
# @task_prerun.connect
# def setup_db_connection(
#     sender=None, task_id=None, task=None, args=None, kwargs=None, **others
# ):
#     pass
#
#
# @task_postrun.connect
# def teardown_db_connection(
#     sender=None,
#     task_id=None,
#     task=None,
#     args=None,
#     kwargs=None,
#     retval=None,
#     state=None,
#     **others,
# ):
#     pass
