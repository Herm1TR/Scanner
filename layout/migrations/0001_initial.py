# Generated by Django 5.1.7 on 2025-04-01 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField(default=0.0)),
                ('y', models.FloatField(default=0.0)),
                ('width', models.FloatField(default=100.0)),
                ('height', models.FloatField(default=100.0)),
            ],
        ),
    ]
