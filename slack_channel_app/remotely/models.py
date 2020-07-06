from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin 

# Create your models here.
class Message(models.Model): 
    uuid = models.UUIDField()
    message_date = models.DateField()
    image = models.ImageField(blank=True,null=True)
    message_content = models.CharField(max_length=512)

    def __str__(self): 
        return (f"username: {self.message_content}")

class User(AbstractUser):
    uuid = models.UUIDField(blank=True,null=True)
    date_joined = models.DateField(blank=True,null=True)
    first_name = models.CharField(max_length=64, blank=True,null=True)
    last_name = models.CharField(max_length=64, blank=True,null=True)

    def __str__(self): 
        return (f"{self.first_name} {self.last_name}")

class Channel_Member(models.Model): 
    # Channel members table - is a relationship better? 
    #group_id = models.SmallIntegerField(default=0)
    channels = models.ManyToManyField("Channel", blank=True, related_name="members")
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self): 
        return (f"channel_group_id-") 

class Channel(models.Model): 
    
    #members =  models.ForeignKey(Channel_Member, on_delete=models.CASCADE, related_name="members")
    messages = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="messages", blank=True,null=True)
    name = models.CharField(max_length=64)
    num_users =models.SmallIntegerField()
    public = models.BooleanField(default=True)
    description = models.CharField(max_length=512,  blank=True,null=True)

    def __str__(self): 
        return (f"name: {self.name} number of users: {self.num_users}")


