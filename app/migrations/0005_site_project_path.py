# Generated by Django 2.2 on 2019-10-12 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20190721_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='project_path',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='项目路径'),
        ),
    ]
