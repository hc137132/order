# Generated by Django 5.0.1 on 2024-05-09 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_projectdetail_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdetail',
            name='deadline',
            field=models.TimeField(max_length=50, verbose_name='期限'),
        ),
    ]
