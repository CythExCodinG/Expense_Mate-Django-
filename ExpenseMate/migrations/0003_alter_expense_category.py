# Generated by Django 5.1.3 on 2024-12-03 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ExpenseMate', '0002_rename_title_expense_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(default='other', max_length=50),
        ),
    ]
