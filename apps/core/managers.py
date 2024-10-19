from django.db import models


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
        return super().get_queryset().filter(deleted=False)
