from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db import models


class FbAuth(models.Model):
    """Stores Fb auth details for users who sign in via facebook"""
    user = models.OneToOneField(User)
    facebook_token = models.CharField(verbose_name="Facebook auth token", max_length=600, null=False, blank=False, unique=False)
    facebook_id = models.CharField(verbose_name="Facebook id", max_length=20, null=False, blank=False, unique=False)
    last_modified = models.DateTimeField(auto_now=True, null=False, blank=False)

    def __unicode__(self):
        return str(self.facebook_id)

    @staticmethod
    def create_or_update(user, facebook_id, facebook_token):
        try:
            entry = FbAuth.objects.create(user=user, facebook_id=facebook_id, facebook_token=facebook_token)
        except IntegrityError:
            entry = FbAuth.objects.get(user=user)

        return entry
