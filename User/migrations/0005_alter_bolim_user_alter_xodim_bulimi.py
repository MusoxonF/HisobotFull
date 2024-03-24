# Generated by Django 5.0.2 on 2024-03-13 17:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_alter_bolim_name_alter_bolim_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bolim',
            name='user',
            field=models.OneToOneField(default="o'chirilgan user", null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='xodim',
            name='bulimi',
            field=models.ForeignKey(default="o'chirilgan user", on_delete=django.db.models.deletion.SET_DEFAULT, related_name='bolim', to='User.bolim'),
        ),
    ]