# Generated by Django 4.1 on 2022-08-31 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boke_apps', '0002_poetry'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_data',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=10)),
                ('user_pwd', models.CharField(max_length=15)),
            ],
        ),
    ]
