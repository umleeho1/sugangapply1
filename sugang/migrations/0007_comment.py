# Generated by Django 4.2.1 on 2023-06-07 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sugang', '0006_delete_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
