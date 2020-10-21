from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    post_input_text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT) 
    username = models.CharField(max_length=200)
    datetime = models.DateTimeField(default=timezone.now)   
    user_fullname = models.CharField(max_length=200)
    # ip_addr = models.GenericIPAddressField(default=request.META['REMOTE_ADDR'])
    # class Meta:
    #     ordering=['-id']
    # def __str__(self):
    #     return 'id=' + str(self.id) + ',text="' + self.text + '"'

class Profile(models.Model):
    bio_input_text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    # ip_addr = models.GenericIPAddressField(default=request.META['REMOTE_ADDR'])
    Profile_Picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    follower = models.ManyToManyField(User, related_name='follower')


    # def __str__(self):
    #     return 'id=' + str(self.id) + ',text="' + self.text + '"'

class Comment(models.Model):
    comment_input_text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None,on_delete=models.PROTECT)
    comment_profile = models.CharField(max_length=200)
    comment_date_time = models.DateTimeField(default=timezone.now)
    mypost = models.ForeignKey(Post, default=None, on_delete=models.PROTECT)
   
    # def __str__(self):
    #     return 'id=' + str(self.id) + ',text="' + self.text + '"'
