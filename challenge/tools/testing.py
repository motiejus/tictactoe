from django.test import override_settings


def sync_celery(function=None):
    """Synchronous task execution by celery. Does not require redis"""
    actual_decorator = override_settings(
        CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
        CELERY_ALWAYS_EAGER=True,
        BROKER_BACKEND='memory'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
