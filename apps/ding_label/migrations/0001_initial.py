# Generated by Django 4.2.8 on 2024-02-03 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('audio', '0003_audiopart'),
    ]

    operations = [
        migrations.CreateModel(
            name='DingLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_role', models.CharField(max_length=256, verbose_name='音频片段所属角色')),
                ('emotion_label', models.SmallIntegerField(verbose_name='情感标签')),
                ('text', models.CharField(max_length=256, verbose_name='音频文本内容')),
                ('pleasure', models.FloatField(verbose_name='愉悦维评分')),
                ('action', models.FloatField(verbose_name='激活维评分')),
                ('audio_part_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audio_part_id', to='audio.audiopart', verbose_name='音频片段ID')),
            ],
        ),
    ]
