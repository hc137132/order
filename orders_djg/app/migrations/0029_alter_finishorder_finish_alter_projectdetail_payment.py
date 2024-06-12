# Generated by Django 5.0.1 on 2024-06-10 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_finishorder_commit_finishorder_finish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finishorder',
            name='finish',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='payment',
            field=models.BooleanField(max_length=5, null=True, verbose_name='付款情况'),
        ),
    ]
