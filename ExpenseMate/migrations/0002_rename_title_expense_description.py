# Generated by Django 5.1.3 on 2024-12-03 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExpenseMate', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='title',
            new_name='description',
        ),
    ]
