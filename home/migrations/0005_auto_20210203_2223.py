# Generated by Django 2.0.10 on 2021-02-03 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20210203_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.BlogSubCategory'),
        ),
    ]