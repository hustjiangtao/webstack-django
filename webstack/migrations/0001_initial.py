# Generated by Django 2.2.8 on 2019-12-10 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='名称', max_length=64)),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='StaticFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='名称', max_length=40)),
                ('url', models.FileField(help_text='链接', upload_to='static/%Y/%m/%d/')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='名称', max_length=64)),
                ('url', models.URLField(help_text='链接', max_length=255)),
                ('logo', models.URLField(help_text='图标', max_length=255)),
                ('desc', models.CharField(blank=True, help_text='简介', max_length=255)),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间')),
                ('category', models.ManyToManyField(help_text='分类', to='webstack.Category')),
            ],
        ),
    ]
