# Generated by Django 4.0.6 on 2022-12-12 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('New', 'New'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='New', max_length=50),
        ),
    ]