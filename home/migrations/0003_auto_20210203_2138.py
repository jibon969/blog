# Generated by Django 2.0.10 on 2021-02-03 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210203_2059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogbanner',
            options={'ordering': ['-timestamp']},
        ),
    ]
