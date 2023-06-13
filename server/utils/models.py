from django.db import models


class CreationModificationBase(models.Model):
    """Mixin for adding creation and modification datetime."""
    id = models.AutoField(primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, help_text="When this instance was created.")
    modified = models.DateTimeField(auto_now=True, help_text="When this instance was modified.")

    class Meta:
        abstract = True
