# Generated by Django 4.0.4 on 2022-07-06 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('starting_bid', models.IntegerField()),
                ('category', models.CharField(max_length=64)),
                ('image_link', models.CharField(blank=True, default=None, max_length=200, null=True)),
            ],
        ),
    ]