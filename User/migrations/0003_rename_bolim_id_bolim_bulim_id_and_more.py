# Generated by Django 5.0.2 on 2024-02-27 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_alter_user_gender_alter_user_image_alter_user_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bolim',
            old_name='bolim_id',
            new_name='bulim_id',
        ),
        migrations.RenameField(
            model_name='ish_turi',
            old_name='ish_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='image',
            new_name='photo',
        ),
        migrations.RenameField(
            model_name='xodim',
            old_name='bolimi',
            new_name='bulimi',
        ),
        migrations.RenameField(
            model_name='xodim',
            old_name='name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='xodim',
            old_name='xodim_id',
            new_name='id_raqam',
        ),
        migrations.RenameField(
            model_name='xodim',
            old_name='image',
            new_name='photo',
        ),
    ]