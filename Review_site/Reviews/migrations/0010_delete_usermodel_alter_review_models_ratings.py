# Generated by Django 4.2.2 on 2023-06-27 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reviews', '0009_usermodel_alter_review_models_ratings'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserModel',
        ),
        migrations.AlterField(
            model_name='review_models',
            name='ratings',
            field=models.IntegerField(choices=[(5, '★★★★★'), (4, '★★★★'), (3, '★★★'), (2, '★★'), (1, '★')]),
        ),
    ]