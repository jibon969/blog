# Generated by Django 2.0.10 on 2021-02-02 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='Banner title', max_length=120, null=True)),
                ('largeDevices', models.ImageField(blank=True, help_text='1400x400', null=True, upload_to='blog/')),
                ('mediumDevices', models.ImageField(blank=True, help_text='800X400', null=True, upload_to='blog/')),
                ('smallDevices', models.ImageField(blank=True, help_text='600x400', null=True, upload_to='blog/')),
                ('url_field', models.URLField(blank=True, max_length=120, null=True)),
                ('value', models.IntegerField(blank=True, null=True, verbose_name='Position')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
