# Generated by Django 3.2 on 2022-09-01 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_auto_20220820_0917"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="type",
            field=models.IntegerField(
                choices=[
                    (0, "milk"),
                    (1, "white"),
                    (2, "dark"),
                    (3, "black"),
                    (4, "vegan"),
                ],
                default=0,
            ),
        ),
    ]
