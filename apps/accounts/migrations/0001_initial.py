# Generated by Django 4.2.7 on 2023-11-29 20:54

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='角色名称')),
                ('describe', models.CharField(blank=True, max_length=256, null=True, verbose_name='角色描述')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(error_messages={'unique': '该邮箱地址已经存在'}, max_length=50, unique=True, verbose_name='用户邮箱')),
                ('username', models.CharField(max_length=50, verbose_name='用户名')),
                ('is_staff', models.BooleanField(default=False, help_text='指定用户是否可以登录到此管理网站', verbose_name='进入管理后台')),
                ('is_active', models.BooleanField(default=True, help_text='指定是否应将此用户视为活动用户。取消选择此项而不是删除帐户', verbose_name='活动用户')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='加入日期')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='accounts.userrole', verbose_name='用户角色')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
