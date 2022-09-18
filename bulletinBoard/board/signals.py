from django.db.models.signals import pre_save, post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from .models import Declaration, DeclarationResponse, UserActivation


@receiver(signal=post_save, sender=UserActivation)
def activate_user(sender, instance, created, **kwargs):
    if created:
        mail = instance.user.email
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


@receiver(signal=pre_save, sender=User)
def save_response(sender, instance, **kwargs):
    if instance.accepted:
        send_mail(
            subject=f'Ваш отклик принят',
            message=f'Ваш отклик "{instance.text}" \rна объявление "{instance.declaration.title}" - http://127.0.0.1/declaration/{instance.declaration.pk}/ \rбыл принят автором ',
            from_email=None,
            recipient_list=[instance.user.email],
        )
    else:
        send_mail(
            subject=f'Новый отклик на ваше объявление',
            message=f'На объявление "{instance.declaration.title}" - http://127.0.0.1/declaration/{instance.declaration.pk}/ \rбыл оставлен новый отклик {instance.text} от {instance.user.username}',
            from_email=None,
            recipient_list=[instance.declaration.user.email],
        )
