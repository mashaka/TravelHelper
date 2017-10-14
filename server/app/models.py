from django.contrib.auth import get_user_model
from django.db import models
from picklefield import PickledObjectField

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User)
    loaded = models.BooleanField(default=False)
    data = PickledObjectField(null=True)

    def __str__(self):
        return self.user.username
