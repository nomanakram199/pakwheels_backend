from django.db import models


class SoftDeleteMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_active = False
        self.save(update_fields=['is_active'])
