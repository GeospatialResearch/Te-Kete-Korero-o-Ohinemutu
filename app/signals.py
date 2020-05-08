from .models import Comment, Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_email


@receiver(post_save, sender=Comment)
def notify_about_comment(sender, instance, **kwargs):

    emaildata = {
        'comment': instance,
        'mailing_list': [instance.story.owner.email],
        'subject': 'New comment in your narrative'
    }

    if instance.story.owner.email != 'admin@example.com':
        send_email(emaildata, 'comment_email')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
