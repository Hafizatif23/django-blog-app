from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):

    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    CATEGORY_CHOICES = [
        ('lifestyle', 'Lifestyle'),
        ('business', 'Business'), 
        ('tech', 'Tech'), 
        ('health', 'Health'), 
        ('other', 'Other')
        ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other' )
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    content = models.TextField()


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)