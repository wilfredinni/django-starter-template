from django.db import models
from django.utils import timezone

from .managers import SoftDeleteModelManager


class BaseModel(models.Model):
    """
    An abstract base class that provides created_at and updated_at fields
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteBaseModel(BaseModel):
    """
    An abstract base model that provides soft delete functionality.
    """

    deleted_at = models.DateTimeField(null=True, blank=True)

    # Override the default manager with a custom one that filters
    # out soft deleted records. If the manager is overridden, the
    # objects property must be redefined.
    objects = SoftDeleteModelManager()

    class Meta:
        abstract = True

    def delete(self):
        """
        Mark this object as deleted by setting the deleted_at field.

        Note that the object will not be removed from the database. Instead,
        it will be excluded from the default queryset.
        """
        self.deleted_at = timezone.now()
        self.save()
