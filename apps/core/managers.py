from django.db import models, transaction
from django.db.models.signals import post_delete, pre_delete
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """
    Custom QuerySet that overrides the delete method to perform a soft delete.
    """

    def delete(self):
        """
        Override the default delete method to perform a soft delete on each instance.
        """
        with transaction.atomic():
            # Send pre_delete signals for each instance
            for obj in self:
                pre_delete.send(sender=obj.__class__, instance=obj)

            result = self.update(deleted_at=timezone.now())

            # Send post_delete signals for each instance
            for obj in self:
                post_delete.send(sender=obj.__class__, instance=obj)

            return result


class SoftDeleteModelManager(models.Manager):
    """
    SoftDeleteModelManager is a custom manager for models that implement soft deletion.
    It overrides the default queryset to exclude objects marked as deleted.
    """

    def get_queryset(self):
        """
        Returns a queryset that filters out objects marked as deleted.
        Take note that this method will be overridden if a custom
        queryset is defined in the model.
        """
        return SoftDeleteQuerySet(self.model, using=self._db).filter(
            deleted_at__isnull=True
        )

    def deleted(self):
        """
        Returns only deleted objects
        """
        return SoftDeleteQuerySet(self.model, using=self._db).filter(
            deleted_at__isnull=False
        )

    def all_with_deleted(self):
        """
        Returns all objects, including deleted ones
        """
        return SoftDeleteQuerySet(self.model, using=self._db)
