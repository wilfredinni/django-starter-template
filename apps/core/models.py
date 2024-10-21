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
        """
        Meta options for the BaseModel.

        Attributes:
            abstract (bool): Indicates that this is an abstract base
            class and should not be used to create any database table.
            ordering (list): Sets the default ordering of records by
            the 'created_at' field in descending order.
        """

        abstract = True
        ordering = ["-created_at"]


class SoftDeleteBaseModel(BaseModel):
    """
    An abstract base model that provides soft delete functionality.
    """

    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Override the default manager with a custom one that filters
    # out soft deleted records. If the manager is overridden, the
    # objects property must be redefined.
    objects = SoftDeleteModelManager()

    class Meta:
        """
        Meta options for the SoftDeleteModel.

        Attributes:
            abstract (bool): Indicates that this is an abstract base
            class and should not be used to create any database table.
        """

        abstract = True

    def delete(self):
        """
        Marks the record as deleted by setting the 'deleted' flag to True.

        This method performs a soft delete by updating the 'deleted' attribute
        to True and then saving the instance. It does not remove the record
        from the database, allowing for potential recovery or auditing.
        """
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()
