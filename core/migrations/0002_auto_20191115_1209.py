# Generated by Django 2.2.6 on 2019-11-15 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='language',
            field=models.CharField(default='en-gb', max_length=5),
        ),
        migrations.AddField(
            model_name='question',
            name='ordinal_number',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(default='UK', max_length=2),
        ),
    ]