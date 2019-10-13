# Generated by Django 2.1.7 on 2019-06-10 03:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='站点名称')),
                ('href', models.CharField(max_length=200, verbose_name='网址')),
                ('coding', models.CharField(blank=True, max_length=200, null=True, verbose_name='coding 仓库')),
                ('need_verification', models.BooleanField(default=True, verbose_name='检查HTTPS')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='加入时间')),
                ('is_ignore', models.BooleanField(default=False, verbose_name='忽略检测')),
                ('restart', models.CharField(blank=True, max_length=100, null=True, verbose_name='重启文件')),
                ('deploy', models.CharField(blank=True, max_length=100, null=True, verbose_name='部署文件')),
                ('update_cert', models.CharField(blank=True, max_length=100, null=True, verbose_name='更新证书')),
            ],
            options={
                'verbose_name': '站点列表',
                'verbose_name_plural': '站点列表',
                'ordering': ['add_time', 'id'],
            },
        ),
        migrations.CreateModel(
            name='SiteHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verification_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='日期')),
                ('ping_time', models.FloatField(null=True, verbose_name='响应时间')),
                ('result', models.CharField(max_length=200, verbose_name='信息')),
                ('certificate', models.PositiveIntegerField(null=True, verbose_name='证书信息')),
                ('status_code', models.CharField(max_length=20, verbose_name='状态码')),
                ('site_type', models.CharField(choices=[('1', 'ok'), ('2', 'ssl_danger'), ('3', 'bad_response'), ('4', 'timeout'), ('5', 'refuced request')], default='1', max_length=20, verbose_name='站点状态')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Site')),
            ],
            options={
                'verbose_name': '站点检测历史记录',
                'verbose_name_plural': '站点检测历史记录',
                'ordering': ['-id'],
            },
        ),
    ]