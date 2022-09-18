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
        print(instance.secret_key)
        send_mail(
            subject='Подтверждение регистрации на портале',
            message=f'Код подтверждения: {instance.secret_key}\r Перейти на страницу активации: http://127.0.0.1:8000/account/activate',
            from_email=None,
            recipient_list=[instance.user.email],
        )
        return HttpResponseRedirect('/account/activate/')


@receiver(signal=post_save, sender=User)
def save_user(sender, instance, created, **kwargs):
    if created:
        user_activation = UserActivation.objects.create(user=instance)
        user_activation.save()


@receiver(signal=pre_save, sender=DeclarationResponse)
def save_response(sender, instance, **kwargs):
    if instance.accepted:
        send_mail(
            subject='Ваш отклик приняли',
            message=f'Ваш отклик {instance.text} на объявление {instance.declaration.title}, был принят автором '
                    f'\rhttp://127.0.0.1/declaration/{instance.declaration.pk}/',
            from_email=None,
            recipient_list=[instance.user.email],
        )
    else:
        send_mail(
            subject='Новый отклик на ваше объявление',
            message=f'На ваше объявление {instance.declaration.title} - http://127.0.0.1/declaration/{instance.declaration.pk}/ Был оставлен новый отклик {instance.text}',
            from_email=None,
            recipient_list=[instance.declaration.user.email],
        )
