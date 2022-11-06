# Generated by Django 4.1.3 on 2022-11-06 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_paymentrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=256)),
                ('price_in_cents_cad', models.IntegerField(max_length=256)),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.AlterModelOptions(
            name='paymentrecord',
            options={'verbose_name': 'Payment Record', 'verbose_name_plural': 'Payment Records'},
        ),
    ]
