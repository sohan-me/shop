# Generated by Django 4.0.6 on 2022-10-21 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_cartitem_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='quantity',
            new_name='quality',
        ),
    ]
