# Generated by Django 4.1.1 on 2022-09-17 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0003_useractivation_user_activated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='declaration',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='declarationresponse',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='useractivation',
            name='secret_key',
            field=models.CharField(default='lzrn%v(wl8-s814j)6!6=ttgm9vfb!8r$*zqj8)*ps=pulg7y^', max_length=256),
        ),
    ]
