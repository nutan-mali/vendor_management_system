# Generated by Django 4.2.5 on 2023-12-12 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_alter_purchaseorder_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='purchase_orders',
            field=models.ManyToManyField(related_name='vendors', to='app1.purchaseorder'),
        ),
    ]
