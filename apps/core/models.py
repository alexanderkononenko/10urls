from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Url(BaseModel):
    owner = models.ForeignKey(User, null=False)
    url = models.CharField(max_length=255, null=False)
    hash = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return '%s (%s)' % (self.hash, self.url[:64],)