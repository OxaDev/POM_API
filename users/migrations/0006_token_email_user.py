# Generated by Django 4.2.6 on 2023-10-08 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_tokenvalue_token_token_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='email_user',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
