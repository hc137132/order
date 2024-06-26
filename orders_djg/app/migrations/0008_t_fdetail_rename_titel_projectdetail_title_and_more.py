# Generated by Django 5.0.1 on 2024-04-11 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_projecttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='T_FDetail',
            fields=[
                ('nowdate', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=50)),
                ('uuidname', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=10)),
                ('content', models.TextField(null=True)),
                ('path', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='projectdetail',
            old_name='titel',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='projectdetail',
            name='filedetail',
        ),
        migrations.RemoveField(
            model_name='projectdetail',
            name='textdetail',
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='contentdetail',
            field=models.JSONField(null=True, verbose_name='包含了文本和文件的具体位置和内容'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='payment',
            field=models.CharField(default='0', max_length=5, null=True, verbose_name='付款情况'),
        ),
    ]
