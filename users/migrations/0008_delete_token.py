# Generated by Django 4.2.6 on 2023-10-09 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_token_creation_date_alter_token_delete_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Token',
        ),
    ]