# Generated by Django 3.2 on 2022-09-03 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderdetail',
            options={'verbose_name': 'Order'},
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='original_bag',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='stripe_pid',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='postcode',
            field=models.CharField(default='', max_length=20),
        ),
    ]
