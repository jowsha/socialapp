from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Count




# Create your models here.
class Posts(models.Model):
    post=models.CharField(max_length=150)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    decsription=models.CharField(max_length=200,null=True)
    user=models.ForeignKey(User,on_delete= models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    up_vote=models.ManyToManyField(User,related_name="up_vote")

    @property
    def fetch_comments(self): #comments
        ans=self.comments_set.all()
        return ans

    def __str__(self):
        return self.question

class Comments(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.CharField(max_length=150)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    up_vote=models.ManyToManyField(User,related_name="upvote")

    # def __str__(self):
    #     return self.comment
class UserDetails(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    use=models.CharField(max_length=200,null=True)
    contact_no=models.PositiveIntegerField(null=True)
    about=models.CharField(max_length=200,null=True)
    place=models.CharField(max_length=200,null=True)
    image=models.ImageField(upload_to="images/profile",null=True,blank=True)

    def __str__(self):
        return f'{self.user.username} UserDetails'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)