# Generated by Django 5.0.1 on 2024-06-03 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_finishorder_alter_t_fdetail_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='finishorder',
            name='commit',
            field=models.IntegerField(null=True, verbose_name='commit number'),
        ),
        migrations.AddField(
            model_name='finishorder',
            name='finish',
            field=models.BooleanField(null=True),
        ),
    ]
