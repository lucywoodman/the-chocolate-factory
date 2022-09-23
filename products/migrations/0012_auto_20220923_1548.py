# Generated by Django 3.2 on 2022-09-23 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20220923_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allergy',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='flavour',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]