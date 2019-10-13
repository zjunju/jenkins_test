from django.db import models
from django.utils import timezone


site_status = (
    ('1', 'ok',),
    ('2', 'ssl_danger',),
    ('3', 'bad_response',),
    ('4', 'timeout'),
    ('5', 'refuced request'),
)


class Site(models.Model):
    name = models.CharField(verbose_name="站点名称", max_length=50)
    href = models.CharField(verbose_name="网址", max_length=200)
    coding = models.CharField(verbose_name="coding 仓库", max_length=200, null=True, blank=True)
    need_verification = models.BooleanField(verbose_name="检查HTTPS", default=True)
    add_time = models.DateTimeField(default=timezone.now, verbose_name="加入时间")
    is_ignore = models.BooleanField(verbose_name='忽略检测', default=False)
    is_select = models.BooleanField(verbose_name='是否选择', default=True)
    overseas = models.BooleanField(verbose_name='长响应站点', default=False)

    restart = models.CharField(verbose_name="重启文件", max_length=100, null=True, blank=True)
    deploy = models.CharField(verbose_name="部署文件", max_length=100, null=True, blank=True)
    update_cert = models.CharField(verbose_name="更新证书", max_length=100, null=True, blank=True)
    copy = models.CharField(verbose_name="备份", max_length=100, null=True, blank=True)

    project_path = models.CharField(verbose_name="项目路径", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = '站点列表'
        ordering = ['add_time', 'id']

    def __str__(self):
        return self.name


class SiteHistory(models.Model):
    verification_date = models.DateTimeField(default=timezone.now, verbose_name="日期")
    site = models.ForeignKey(Site, on_delete = models.CASCADE)
    ping_time = models.FloatField(verbose_name="响应时间", null= True)
    result = models.CharField(verbose_name="信息", max_length=200)
    certificate = models.PositiveIntegerField(verbose_name="证书信息", null=True)
    status_code = models.CharField(verbose_name="状态码", max_length=20)
    site_type = models.CharField(verbose_name="站点状态", max_length=20,choices=site_status, default='1')

    class Meta:
        verbose_name = verbose_name_plural = '站点检测历史记录'
        ordering = ['-id']

    def __str__(self):
        return "%s: %s"%(self.site.name, self.site_type)
