from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, blank = False, unique=True, primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    picture = models.ImageField(upload_to="profile_pictures/", default="blank-profile-picture.png")
    location = models.CharField(max_length=100, blank=True)



class Post(models.Model):
    created_by = models.ForeignKey(to=Profile, on_delete=models.CASCADE, blank=False)
    date = models.DateTimeField(blank=False, editable=False, auto_now_add=True)
    title = models.CharField(max_length=300, blank=False)
    body = models.TextField(blank = False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title


