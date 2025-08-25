from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_link = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"

        subject = 'Activate Your Account'
        message = f'Hi {instance.username},\n\nPlease click the link below to activate your account:\n{activation_link}\n\nThank you!'
        recipient_list = [instance.email]

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
        except Exception as e:
            print(f"Error sending email to {instance.email}: {e}")