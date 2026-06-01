from django.db import models


class ActiveQuerySet(models.QuerySet):

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class ActiveManager(models.Manager.from_queryset(ActiveQuerySet)):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def with_inactive(self):
        return super().get_queryset()

    def only_inactive(self):
        return super().get_queryset().filter(is_active=False)
