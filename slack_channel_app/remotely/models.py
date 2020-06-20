from django.db import models

# Create your models here.
class Users(models.Model): 
    uuid = models.UUIDField()
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    username = models.CharField(max_length=64)

    def __str__(self): 
        return (f"username: {self.username}")

class Message(models.Model): 
    uuid = models.UUIDField()
    message_date = models.DateField()
    image = models.ImageField(blank=True,null=True)
    message_content = models.CharField(max_length=512)

    def __str__(self): 
        return (f"username: {self.message_content}")

class Channel_Member(models.Model): 
    # Channel members table - is a relationship better? 
    uuid = models.UUIDField(blank=True,null=True)
    username = models.CharField(max_length=64,blank=True,null=True)
    date_joined = models.DateField(blank=True,null=True)

    def __str__(self): 
        return (f"username: {self.username}") 

class Channel(models.Model): 
    members =  models.ForeignKey(Channel_Member, on_delete=models.CASCADE, related_name="members")
    messages = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="messages")
    name = models.CharField(max_length=64)
    num_users =models.SmallIntegerField()

    def __str__(self): 
        return (f"name: {self.name} number of users: {self.num_users}")


