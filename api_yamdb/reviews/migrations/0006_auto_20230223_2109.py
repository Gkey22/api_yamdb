# Generated by Django 3.2 on 2023-02-23 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_delete_genretitle'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-pub_date',)},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('name',)},
        ),
    ]
