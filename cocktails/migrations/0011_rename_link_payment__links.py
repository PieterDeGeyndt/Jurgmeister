# Generated by Django 4.0 on 2022-04-01 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails', '0010_payment_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='link',
            new_name='_links',
        ),
    ]