# Generated by Django 4.2.5 on 2023-12-11 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_purchaseorder_status_performancerecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(default='pending', max_length=50),
        ),
    ]
