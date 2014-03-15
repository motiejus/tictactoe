from django.db import models


class OwnManager(models.Manager):
    def __init__(self, key):
        super(OwnManager, self).__init__()
        self._key = key

    def __call__(self, user, *args, **kwargs):
        self._user = user
        return self

    def get_queryset(self):
        assert hasattr(self, '_user'), "must call Manager with user instance"
        if self._user.is_superuser:
            return super(OwnManager, self).get_queryset()
        d = {self._key: self._user}
        return super(OwnManager, self).get_queryset().filter(**d)
