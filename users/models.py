import uuid
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True, default='park')
    location = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    short_intro = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='profile_pics', default='profile_pics/mehdi.png')
    # ეს ორი რაღაცა (upload_to='profile_pics', default='profile_pics/mehdi.png') აკეთებს შემდეგ რამეს:
    # პირველი ეუბნება ჯანგოს თუ სად უნდა შეინახოს ატვირთული ფოტოები.
    # მეორე ეუბნება ჯანგოს თუ ფოტო არ ატვირტესო მიეცი ავტომატურად რამე სტანდარტული ფოტოო. (ვითომ კაცი)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    social_media = models.CharField(max_length=100, blank=True, null=True)
    wiki = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.username)



class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)



class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='messages')
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    file = models.FileField(blank=True, null=True, upload_to='message_files')
    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
