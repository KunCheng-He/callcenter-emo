# Generated by Django 4.2.8 on 2024-04-20 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ser_model', '0001_initial'),
        ('upload_events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadevent',
            name='ser_model_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ser_model', to='ser_model.sermodel', verbose_name='语音情感识别模型'),
        ),
    ]
