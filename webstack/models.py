from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=64, help_text='名称')
    # parent = models.IntegerField(default=0, help_text='主分类')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE, help_text='主分类')
    index = models.SmallIntegerField(default=0, help_text='排序，越大越靠前')
    icon = models.CharField(max_length=30, null=True, blank=True, help_text='图标')
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')

    def __str__(self):
        return f"{self.id}. {self.name}"


class Website(models.Model):
    name = models.CharField(max_length=64, help_text='名称')
    url = models.URLField(max_length=255, help_text='链接')
    logo = models.URLField(max_length=255, help_text='图标')
    desc = models.CharField(max_length=255, blank=True, help_text='简介')
    categorys = models.ManyToManyField(Category, related_name='websites', help_text='分类')
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')

    def __str__(self):
        return f"{self.id}. {self.name} ({self.url})"


class StaticFile(models.Model):
    name = models.CharField(max_length=40, help_text='名称')
    url = models.FileField(upload_to="static/%Y/%m/%d/", help_text='链接')
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')

    def __str__(self):
        return f"{self.id}. {self.name}: {self.url}"
