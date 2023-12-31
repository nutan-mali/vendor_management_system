# Generated by Django 4.2.5 on 2023-12-13 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_alter_purchaseorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_orders_for_vendor', to='app1.vendor'),
        ),
    ]
