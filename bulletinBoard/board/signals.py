from django.db.models.signals import post_save, post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from .models import Declaration, DeclarationResponse, UserActivation


@receiver(signal=post_save, sender=UserActivation)
def activate_user(sender, instance, created, **kwargs):
    if created:
        mail = instance.user.email
        print(instance.secret_key)
        send_mail(
            subject='Подтверждение регистрации на портале',
            message=f'Код подтверждения: {instance.secret_key} \r Перейти на страницу активации: http://127.0.0.1:8000/account/activate',
            from_email=None,
            recipient_list=[instance.user.email],
        )
        return HttpResponseRedirect('/account/activate/')


@receiver(signal=post_save, sender=User)
def save_user(sender, instance, created, **kwargs):
    if created:
        user_activation = UserActivation.objects.create(user=instance)
        user_activation.save()