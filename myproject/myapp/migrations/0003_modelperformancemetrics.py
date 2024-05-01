# Generated by Django 5.0.1 on 2024-05-01 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_modelconfig'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelPerformanceMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_count', models.IntegerField(default=0)),
                ('request_latency_sum', models.FloatField(default=0)),
                ('request_latency_count', models.IntegerField(default=0)),
                ('runtime_latency_sum', models.FloatField(default=0)),
                ('runtime_latency_count', models.IntegerField(default=0)),
                ('model_load_latency', models.FloatField(default=0)),
            ],
        ),
    ]
