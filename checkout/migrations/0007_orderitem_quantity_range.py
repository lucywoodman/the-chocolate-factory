# Generated by Django 3.2 on 2022-09-17 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='orderitem',
            constraint=models.CheckConstraint(check=models.Q(('quantity__gte', 0), ('quantity__lte', 99)), name='quantity_range'),
        ),
    ]
