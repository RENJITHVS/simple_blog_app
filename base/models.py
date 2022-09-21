
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User



# Blog model
class Blog(models.Model):
    user_data = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    tag_line = models.CharField(max_length=200, null=True, blank = True)
    description = models.TextField(null = True, blank = True)
    public = models.BooleanField(verbose_name="Make it Public", default = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated',]

    def __str__(self):
        return self.title


