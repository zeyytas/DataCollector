# Generated by Django 3.2.25 on 2024-04-30 06:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.UUIDField(default=uuid.uuid4)),
                ('date_of_transaction', models.DateField()),
                ('status', models.IntegerField(choices=[(1, 'purchase'), (2, 'refund')])),
                ('store_id', models.CharField(max_length=16)),
            ],
        ),
    ]