from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories', blank=True)
    posts = models.ManyToManyField('Post', through='PostCategory')

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type_choices = [
        ('news', 'Новость')
    ]
    post_type = models.CharField(max_length=10, choices=post_type_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.post_type == 'news' and not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'category')


@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group = Group.objects.get(name='common')
        instance.groups.add(common_group)


class LastWeeklyNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_notification_date = models.DateTimeField()

