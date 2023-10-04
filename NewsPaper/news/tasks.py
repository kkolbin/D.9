from .models import Post, LastWeeklyNotification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime
from django.utils import timezone
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_weekly_notification():
    last_week = timezone.now() - datetime.timedelta(days=7)
    new_news = Post.objects.filter(created_at__gte=last_week)

    users_news = {}
    for news in new_news:
        for category in news.categories.all():
            for user in category.subscribers.all():
                users_news.setdefault(user, []).append(news)

    for user, news in users_news.items():
        current_site = get_current_site(None)
        subject = 'Новые новости за неделю'
        from_email = 'projectnewspaper1@yandex.ru'
        to_email = user.email

        context = {
            'user': user,
            'news': news,
            'domain': current_site.domain
        }
        html_content = render_to_string('weekly_notification_email.html', context)
        text_content = strip_tags(html_content)

        send_mail(subject, text_content, from_email, [to_email], html_message=html_content)

        LastWeeklyNotification.objects.update_or_create(
            user=user,
            defaults={'last_notification_date': timezone.now()}
        )
