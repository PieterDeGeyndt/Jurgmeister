# Generated by Django 4.0 on 2022-04-01 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails', '0015_alter_payment_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='link',
            field=models.TextField(blank=True, null=True),
        ),
    ]
