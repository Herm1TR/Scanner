# Generated by Django 4.2 on 2025-04-05 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layout', '0003_box_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='color',
            field=models.CharField(default='#FF0000', max_length=7, verbose_name='方塊顏色'),
        ),
    ]
