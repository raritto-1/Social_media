from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.jpg', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def post_count(self):
        return self.user.posts.count()
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.user.following.count()

    def __str__(self):
        return self.user.username, self.user.password

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to='image/post_images')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Post by {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    related_post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='related_notifications')
    notification_type = models.CharField(max_length=20, choices=[
        ('like', 'Like'),
        ('follow', 'Follow'),
        ('comment', 'Comment'),
    ])

    def __str__(self):
        return f"{self.notification_type} notification for {self.user.username}"

    def get_message(self):
        if self.notification_type == 'like' and self.related_user and self.related_post:
            return f"{self.related_user.username} liked your post"
        elif self.notification_type == 'follow' and self.related_user:
            return f"{self.related_user.username} followed you"
        elif self.notification_type == 'comment' and self.related_user and self.related_post:
            return f"{self.related_user.username} commented on your post"
        return "You have a new notification"
