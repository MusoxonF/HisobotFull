# Generated by Django 5.0.2 on 2024-03-20 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_remove_xodim_first_name_remove_xodim_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('Direktor', 'Direktor'), ('Admin', 'Admin'), ('Tekshiruvchi', 'Tekshiruvchi'), ('Bulim', 'Bulim'), ('Xodim', 'Xodim')], max_length=13),
        ),
    ]
