# Generated by Django 3.2.12 on 2022-04-23 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mod', '0008_rename_test_modinfo_tests'),
    ]

    operations = [
        migrations.AddField(
            model_name='modinfo',
            name='homepage',
            field=models.CharField(default='root', max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='modinfo',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
