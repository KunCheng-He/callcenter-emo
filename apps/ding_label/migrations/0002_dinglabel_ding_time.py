# Generated by Django 4.2.8 on 2024-04-25 14:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ding_label', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dinglabel',
            name='ding_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='标注时间'),
            preserve_default=False,
        ),
    ]
