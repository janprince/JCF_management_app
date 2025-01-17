# Generated by Django 4.0.5 on 2022-11-23 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('msystem', '0003_alter_person_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_info', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('solution', models.TextField(blank=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='msystem.person')),
            ],
        ),
    ]
