# Generated by Django 2.2 on 2020-01-02 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_brstate_notifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brstate',
            name='notifier',
            field=models.BooleanField(default=False),
        ),
    ]
