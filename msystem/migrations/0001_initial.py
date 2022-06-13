# Generated by Django 4.0.5 on 2022-06-12 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('full_name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField(blank=True)),
                ('phone', models.IntegerField()),
                ('profession', models.CharField(blank=True, max_length=255)),
                ('telephone', models.IntegerField(blank=True)),
                ('religion', models.CharField(default='N/A', max_length=255)),
                ('residence', models.CharField(blank=True, max_length=255)),
                ('hometown', models.CharField(blank=True, max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('region', models.CharField(blank=True, max_length=255)),
                ('f_name', models.CharField(blank=True, max_length=255)),
                ('m_name', models.CharField(blank=True, max_length=255)),
                ('request_info', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('solution', models.TextField(blank=True)),
                ('is_client', models.BooleanField(blank=True, default=True)),
                ('is_student', models.BooleanField(blank=True)),
                ('is_employee', models.BooleanField(blank=True)),
                ('is_rep', models.BooleanField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, max_length=255)),
                ('region', models.CharField(blank=True, max_length=255)),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='msystem.person')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, max_length=255)),
                ('salary', models.IntegerField(blank=True)),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='msystem.person')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modes', models.CharField(choices=[('REMOTE', 'Remote'), ('ONSITE', 'Onsite')], max_length=255)),
                ('date', models.DateField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='msystem.person')),
            ],
        ),
    ]
