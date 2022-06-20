# from kombu import Queue

# from .factories import create_celery_app
# from . import app

# celery = create_celery_app(app)

# celery.conf.task_default_queue = "celery"
# celery.conf.task_queues = (
#     Queue("celery", routing_key="celery.#"),
# )

# from celery.schedules import crontab
# from .tasks.user_operations import auto_lock_user


# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(minute=0, hour=0),
#         auto_lock_user.s(),
#         name="Auto lock inactive user - execute at midnight (UTC) everyday",
#     )
