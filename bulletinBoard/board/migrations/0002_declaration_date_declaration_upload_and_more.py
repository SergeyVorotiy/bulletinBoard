# Generated by Django 4.1.1 on 2022-09-17 09:29

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='declaration',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 9, 17, 9, 28, 54, 138159)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='declaration',
            name='upload',
            field=models.FileField(default=None, upload_to='media/'),
        ),
        migrations.AddField(
            model_name='declarationresponse',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 9, 17, 9, 29, 39, 186772)),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UserActivation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret_key', models.CharField(default='xv_!yb+t(t6w&!sz4%n-sm2yew!057&0-ln+$n((01v7-)7#%0', max_length=256)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
