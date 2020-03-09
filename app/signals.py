from .models import Comment
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_email

@receiver(post_save, sender=Comment)
def notify_about_comment(sender, instance, **kwargs):

    emaildata = {
        'comment': instance,
        'mailing_list': [instance.story.owner.email]
    }

    if instance.story.owner.email != 'admin@example.com':
        send_email(emaildata, 'comment_email')
