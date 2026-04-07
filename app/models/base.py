from typing import TYPE_CHECKING
from django.db import models
from django.utils import timezone

if TYPE_CHECKING:
    from django.contrib.auth.models import User


class __SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)
    
class SoftDeleteMixin(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        related_name='deleted_by',
        null=True,
        blank=True
    )
    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if not user or not isinstance(user, User):
            raise ValueError('User is required for soft delete purposes')
        self.deleted_at = timezone.now()
        self.deleted_by = user
        super().delete(*args, **kwargs)

    objects = __SoftDeleteManager()
    all_objects = models.Manager()

class AuditMixin(SoftDeleteMixin):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        related_name='created_by'
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        related_name='updated_by'
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if not user or not isinstance(user, User):
            raise ValueError('User is required for audit purposes')
        self.created_by = self.created_by or user
        self.updated_by = user
        super().save(*args, **kwargs)