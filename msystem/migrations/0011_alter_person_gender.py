# Generated by Django 4.0.5 on 2022-06-20 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msystem', '0010_person_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
